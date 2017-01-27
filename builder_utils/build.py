#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=no-self-use
"""
Build libraries
"""
from __future__ import print_function
import os
import shutil
from multiprocessing import cpu_count

from .config import logger, command


class Builder(object):
    """Builder class"""
    def __init__(self, build_dir, install_dir):
        self.build_dir_ = build_dir
        self.install_dir_ = install_dir
        self.cpu_count_ = 4 if cpu_count() > 4 else cpu_count()
        logger.info("Using %d CPU(S) for building ffmpeg", self.cpu_count_)

    def build_lame(self):
        """build mp3lame library"""
        saved = os.getcwd()
        os.chdir(os.path.join(self.build_dir_, "lame-3.99.5"))
        command("./configure --prefix=%s --disable-shared --enable-static" % self.install_dir_)
        command(["make", "-j%d" % self.cpu_count_])
        command(["make", "install"])
        os.chdir(saved)

    def build_faac(self):
        """build faac library"""
        saved = os.getcwd()
        os.chdir(os.path.join(self.build_dir_, "faac-1.28"))
        command("./configure --prefix=%s --disable-shared --enable-static" % self.install_dir_)
        command(["make", "-j%d" % self.cpu_count_])
        command(["make", "install"])
        os.chdir(saved)

    def build_fdk_aac(self):
        """build fdk-faac library"""
        saved = os.getcwd()
        os.chdir(os.path.join(self.build_dir_, "fdk-aac"))
        command("autoreconf -fiv")
        command("./configure --prefix=%s --disable-shared --enable-static" % self.install_dir_)
        command(["make", "-j%d" % self.cpu_count_])
        command(["make", "install"])
        os.chdir(saved)

    def build_ass(self):
        """build ass library"""
        saved = os.getcwd()
        os.chdir(os.path.join(self.build_dir_, "libass"))
        command(["./autogen.sh"])
        command("./configure --prefix=%s --enable-shared=no --enable-static" % self.install_dir_)
        command(["make", "-j%d" % self.cpu_count_])
        command(["make", "install"])
        os.chdir(saved)

    def build_x264(self):
        """build x264 library"""
        saved = os.getcwd()
        os.chdir(os.path.join(self.build_dir_, "x264"))
        command(
            "./configure --prefix=%s --extra-cflags=\"-I%s/include\" --extra-ldflags=\"-L%s/lib\""
            " --enable-static --disable-lavf --disable-ffms --disable-opencl" % (
                self.install_dir_, self.install_dir_, self.install_dir_))
        command(["make", "-j%d" % self.cpu_count_])
        command(["make", "install"])
        os.chdir(saved)

    def build_sdl(self):
        """build sdl libraries"""
        saved = os.getcwd()
        os.chdir(os.path.join(self.build_dir_, "SDL-1.2.15"))
        command("./configure --prefix=%s --disable-shared" % self.install_dir_)
        command(["make", "-j%d" % self.cpu_count_])
        command(["make", "install"])
        os.chdir(saved)

    def build_ffmpeg(self, version, enable=[], disable=[]):  # pylint: disable=dangerous-default-value
        """build ffmpeg libraries"""
        saved = os.getcwd()
        os.chdir(os.path.join(self.build_dir_, "ffmpeg-%s" % version))
        command(
            "sed -i -e 's|SDL_CONFIG=\"${cross_prefix}sdl-config\"|"
            "SDL_CONFIG=\"%s/bin/sdl-config\"|' ./configure" % self.install_dir_)
        shutil.copy2("configure", "configure.orig")
        os.environ['PKG_CONFIG_PATH'] = "%s/lib/pkgconfig" % self.install_dir_
        cmd = ("./configure --prefix=%s --extra-cflags=\"-I%s/include\" "
               "--extra-ldflags=\"-L%s/lib\" --enable-libfdk-aac --enable-libmp3lame "
               "--enable-libx264 --enable-libzvbi --enable-libass --enable-gpl "
               "--enable-pthreads --enable-nonfree" % (
                   self.install_dir_, self.install_dir_, self.install_dir_))
        if enable:
            for opt in enable:
                cmd += ' --enable-' + opt
        if disable:
            for opt in disable:
                cmd += ' --disable-' + opt
        logger.info(cmd)
        command(cmd)
        shutil.move("configure.orig", "configure")
        command(["make", "-j%d" % self.cpu_count_])
        command(["make", "install"])
        os.chdir(saved)

    def patch_faac(self):
        """patch for faac library"""
        command("cp -v ../patches/faac-1.28-glibc_fixes-1.patch faac-1.28/")
        os.chdir("faac-1.28")
        command("patch -Np1 -i faac-1.28-glibc_fixes-1.patch")
        command("sed -i -e '/obj-type/d' -e '/Long Term/d' frontend/main.c")
        os.chdir("..")

    def patch_sdl(self):
        """patch for sdl library"""
        command("cp -v ../patches/libsdl-1.2.15-const-xdata32.patch SDL-1.2.15/")
        os.chdir("SDL-1.2.15")
        command("patch -Np1 -i libsdl-1.2.15-const-xdata32.patch")
        command("./autogen.sh")
        os.chdir("..")

    def patch_ffmpeg(self, version):
        """apply patches only to ffmpeg 2.6.4"""
        if version == '2.6.4':
            # command("cp -v ../patches/0000-patch6.patch ffmpeg-%s/" % version)
            command("cp -v ../patches/ffmpeg-2.6.4-scte_35-001.patch ffmpeg-%s/" % version)
            command("cp -v ../patches/ffmpeg-2.6.4-scte_35-002.patch ffmpeg-%s/" % version)
            command("cp -v ../patches/ffmpeg-2.6.4-scte_35-003.patch ffmpeg-%s/" % version)
            os.chdir("ffmpeg-%s" % version)
            # command("patch -Np1 -i 0000-patch6.patch")
            command("patch -Np0 -i ffmpeg-2.6.4-scte_35-001.patch")
            command("patch -Np0 -i ffmpeg-2.6.4-scte_35-002.patch")
            command("patch -Np0 -i ffmpeg-2.6.4-scte_35-003.patch")
            os.chdir("..")

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@script : build.py
@about  :
"""
import os
import shutil
from config import logger, command


def build_lame(install_dir):
  os.chdir("lame-3.99.5")
  command("./configure --prefix=%s --disable-shared --enable-static" % install_dir)
  command(["make"])
  command(["make", "install"])
  os.chdir("..")


def build_faac(install_dir):
  os.chdir("faac-1.28")
  command("./configure --prefix=%s --disable-shared --enable-static" % install_dir)
  command(["make"])
  command(["make", "install"])
  os.chdir("..")


def build_x264(install_dir):
  os.chdir("x264")
  command("./configure --prefix=%s --extra-cflags=\"-I%s/include\" --extra-ldflags=\"-L%s/lib\" --enable-static --disable-lavf --disable-ffms --disable-opencl" % (install_dir, install_dir, install_dir))
  command(["make"])
  command(["make", "install"])
  os.chdir("..")


def build_sdl(install_dir):
  os.chdir("SDL-1.2.15")
  command("./configure --prefix=%s --disable-shared" % install_dir)
  command(["make"])
  command(["make", "install"])
  os.chdir("..")


def build_ffmpeg(install_dir, version):
  os.chdir("ffmpeg-%s" % version)
  command("sed -i -e 's|SDL_CONFIG=\"${cross_prefix}sdl-config\"|SDL_CONFIG=\"%s/bin/sdl-config\"|' ./configure" % install_dir)
  shutil.copy2("configure", "configure.orig")
  cmd = "./configure --prefix=%s --extra-cflags=\"-I%s/include\" --extra-ldflags=\"-L%s/lib\" --enable-libfaac --enable-libmp3lame --enable-libx264 --enable-gpl --enable-pthreads --enable-nonfree" % (install_dir, install_dir, install_dir)
  command(cmd)
  shutil.move("configure.orig", "configure")
  command(["make"])
  command(["make", "install"])
  os.chdir("..")

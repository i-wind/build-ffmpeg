#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@script : patch.py
@about  :
"""
import os
import shlex
import shutil
from subprocess import call


def build_lame():
  user_dir = os.path.join(os.getcwd(), 'usr')
  os.chdir("lame-3.99.5")
  call(shlex.split("./configure --prefix=%s --disable-shared --enable-static" % user_dir))
  call(["make"])
  call(["make", "install"])
  os.chdir("..")


def build_faac():
  user_dir = os.path.join(os.getcwd(), 'usr')
  os.chdir("faac-1.28")
  call(shlex.split("./configure --prefix=%s --disable-shared --enable-static" % user_dir))
  call(["make"])
  call(["make", "install"])
  os.chdir("..")


def build_x264():
  user_dir = os.path.join(os.getcwd(), 'usr')
  os.chdir("x264")
  call(shlex.split("./configure --prefix=%s --extra-cflags=\"-I%s/include\" --extra-ldflags=\"-L%s/lib\" --enable-static --disable-lavf --disable-ffms --disable-opencl" % (user_dir, user_dir, user_dir)))
  call(["make"])
  call(["make", "install"])
  os.chdir("..")


def build_sdl():
  user_dir = os.path.join(os.getcwd(), 'usr')
  os.chdir("SDL-1.2.15")
  call(shlex.split("./configure --prefix=%s --disable-shared" % user_dir))
  call(["make"])
  call(["make", "install"])
  os.chdir("..")


def build_ffmpeg(version):
  user_dir = os.path.join(os.getcwd(), 'usr')
  os.chdir("ffmpeg-%s" % version)
  print os.getcwd()
  call(shlex.split("sed -i -e 's|SDL_CONFIG=\"${cross_prefix}sdl-config\"|SDL_CONFIG=\"%s/bin/sdl-config\"|' ./configure" % user_dir))
  shutil.copy2("configure", "configure.orig")
  command = shlex.split("./configure --prefix=%s --extra-cflags=\"-I%s/include\" --extra-ldflags=\"-L%s/lib\" --enable-libfaac --enable-libmp3lame --enable-libx264 --enable-gpl --enable-pthreads --enable-nonfree" % (user_dir, user_dir, user_dir))
  print " ==>", command
  call(command)
  shutil.move("configure.orig", "configure")
  call(["make"])
  call(["make", "install"])
  os.chdir("..")

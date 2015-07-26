#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@script : patch.py
@about  :
"""
import os
import shlex
from subprocess import call


def patch_faac():
  call(shlex.split("cp -v ../patches/faac-1.28-glibc_fixes-1.patch faac-1.28/"))
  os.chdir("faac-1.28")
  call(shlex.split("patch -Np1 -i faac-1.28-glibc_fixes-1.patch"))
  call(shlex.split("sed -i -e '/obj-type/d' -e '/Long Term/d' frontend/main.c"))
  os.chdir("..")


def patch_sdl():
  call(shlex.split("cp -v ../patches/libsdl-1.2.15-const-xdata32.patch SDL-1.2.15/"))
  os.chdir("SDL-1.2.15")
  call(shlex.split("patch -Np1 -i libsdl-1.2.15-const-xdata32.patch"))
  call(["./autogen.sh"])
  os.chdir("..")

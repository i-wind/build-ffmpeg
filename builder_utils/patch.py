#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@script : patch.py
@about  :
"""
import os
from config import logger, command


def patch_faac():
  command("cp -v ../patches/faac-1.28-glibc_fixes-1.patch faac-1.28/")
  os.chdir("faac-1.28")
  command("patch -Np1 -i faac-1.28-glibc_fixes-1.patch")
  command("sed -i -e '/obj-type/d' -e '/Long Term/d' frontend/main.c")
  os.chdir("..")


def patch_sdl():
  command("cp -v ../patches/libsdl-1.2.15-const-xdata32.patch SDL-1.2.15/")
  os.chdir("SDL-1.2.15")
  command("patch -Np1 -i libsdl-1.2.15-const-xdata32.patch")
  command("./autogen.sh")
  os.chdir("..")

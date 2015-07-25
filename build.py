#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
@script  : build.py
@about   :
"""
import os, sys
import urllib2
import shutil
import shlex
from subprocess import call


__version__ = "0.1.0"


def download(url):
  print "Opening url %s" % url
  file_name = url.split('/')[-1]
  u = urllib2.urlopen(url)
  meta = u.info()
  file_size = int(meta.getheaders("Content-Length")[0])
  print "Downloading: %s Bytes: %s" % (file_name, file_size)
  file_size_dl = 0
  block_sz = 8192
  with open(file_name, 'wb') as f:
    while True:
      buffer = u.read(block_sz)
      if not buffer: break
      file_size_dl += len(buffer)
      f.write(buffer)
      status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
      status = status + chr(8)*(len(status)+1)
      print status,
  print


def extract(name):
  if name.endswith('.tar.gz'):
    flag = 'xfz'
  elif name.endswith('.tar.bz2'):
    flag = 'xfj'
  else:
    raise Exception('Wrong archive name %s' % name)
  call(['tar', flag, name])


def patch_faac():
  call(shlex.split("cp -v patches/faac-1.28-glibc_fixes-1.patch faac-1.28/"))
  os.chdir("faac-1.28")
  call(shlex.split("patch -Np1 -i faac-1.28-glibc_fixes-1.patch"))
  call(shlex.split("sed -i -e '/obj-type/d' -e '/Long Term/d' frontend/main.c"))
  os.chdir("..")


def patch_sdl():
  call(shlex.split("cp -v patches/libsdl-1.2.15-const-xdata32.patch SDL-1.2.15/"))
  os.chdir("SDL-1.2.15")
  call(shlex.split("patch -Np1 -i libsdl-1.2.15-const-xdata32.patch"))
  call(["./autogen.sh"])
  os.chdir("..")


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


def build_ffmpeg():
  user_dir = os.path.join(os.getcwd(), 'usr')
  os.chdir("ffmpeg-2.6.3")
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


urls = [
    "http://sourceforge.net/projects/lame/files/lame/3.99/lame-3.99.5.tar.gz",
    "http://downloads.sourceforge.net/faac/faac-1.28.tar.bz2",
    "https://www.libsdl.org/release/SDL-1.2.15.tar.gz",
    "http://ffmpeg.org/releases/ffmpeg-2.6.3.tar.bz2"
  ]


if __name__ == '__main__':
  for url in urls:
    file_name = url.split('/')[-1]
    if not os.path.isfile(file_name):
      download(url)
      extract(file_name)
  if not os.path.isdir("x264"):
    call(shlex.split("git clone git://git.videolan.org/x264.git"))
    os.chdir("x264")
    call("git checkout stable".split())
    os.chdir("..")
  # apply patches
  patch_faac()
  patch_sdl()
  # build components
  build_lame()
  build_faac()
  build_x264()
  build_sdl()
  build_ffmpeg()

sys.exit(0)

# end of build.py

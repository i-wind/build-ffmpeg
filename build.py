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
from optparse import OptionParser, make_option


__version__ = "0.1.0"


def progress(count, total, suffix=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))
    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)
    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', suffix))
    sys.stdout.flush()


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
      progress(file_size_dl, file_size)
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


urls = {
    "lame"  : "http://sourceforge.net/projects/lame/files/lame/3.99/lame-3.99.5.tar.gz",
    "faac"  : "http://downloads.sourceforge.net/faac/faac-1.28.tar.bz2",
    "sdl"   : "https://www.libsdl.org/release/SDL-1.2.15.tar.gz",
    "ffmpeg": "http://ffmpeg.org/releases/ffmpeg-%s.tar.bz2"
  }


def parse_args():
  # parse command line arguments
  option_list = [
      make_option('-f', '--ffmpeg', action='store', default='2.6.3',
                  dest='ffmpeg', help='ffmpeg version to build (default 2.6.3)'),
  ]
  usage = """\
usage: %prog [options]

  Build ffmpeg from source in Linux..."""
  parser = OptionParser(option_list=option_list, usage=usage,
                        version='  %prog version ' + __version__,
                        epilog='Good luck...')
  return parser.parse_args()


if __name__ == '__main__':
  (options, _) = parse_args()
  urls["ffmpeg"] = urls["ffmpeg"] % options.ffmpeg

  # download components
  for lib, url in urls.items():
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
  build_ffmpeg(options.ffmpeg)

sys.exit(0)

# end of build.py

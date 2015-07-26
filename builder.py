#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
@script  : builder.py
@about   :
"""
import os, sys
import shlex
from subprocess import call
from optparse import OptionParser, make_option
from builder_utils import version, download, extract, patch_faac, patch_sdl, build_lame, \
                          build_faac, build_x264, build_sdl, build_ffmpeg


urls = {
    "lame"  : "http://sourceforge.net/projects/lame/files/lame/3.99/lame-3.99.5.tar.gz",
    "faac"  : "http://downloads.sourceforge.net/faac/faac-1.28.tar.bz2",
    "sdl"   : "https://www.libsdl.org/release/SDL-1.2.15.tar.gz",
    "ffmpeg": "http://ffmpeg.org/releases/ffmpeg-%s.tar.bz2"
  }


def parse_args():
  # parse command line arguments
  option_list = [
      make_option('-f', '--ffmpeg', action='store', default='2.6.4',
                  dest='ffmpeg', help='ffmpeg version to build (default 2.6.4)'),
  ]
  usage = """\
usage: %prog [options]

  Build ffmpeg from source in Linux..."""
  parser = OptionParser(option_list=option_list, usage=usage,
                        version='  %prog version ' + version(),
                        epilog='Good luck...')
  return parser.parse_args()


if __name__ == '__main__':
  (options, _) = parse_args()
  urls["ffmpeg"] = urls["ffmpeg"] % options.ffmpeg

  if not os.path.isdir('build'):
    os.mkdir('build')
  saved_dir = os.getcwd()
  os.chdir("build")

  # download components
  for lib, url in urls.items():
    file_name = url.split('/')[-1]
    if not os.path.isfile(file_name):
      download(url)
      if not os.path.isdir(file_name.split('.')[0]):
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
  user_dir = os.path.join(saved_dir, 'usr')
  build_lame(user_dir)
  build_faac(user_dir)
  build_x264(user_dir)
  build_sdl(user_dir)
  build_ffmpeg(user_dir, options.ffmpeg)

  sys.exit(0)

# end of builder.py

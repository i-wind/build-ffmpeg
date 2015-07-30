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
from builder_utils import *


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
  Cache.URLS["ffmpeg"] = Cache.URLS["ffmpeg"] % options.ffmpeg

  cache = Cache('.')
  cache.check()

  sys.exit(0)

  if not os.path.isdir('build'):
    logger.info('Create build directory')
    os.mkdir('build')
  saved_dir = os.getcwd()
  os.chdir("build")

  # apply patches
  logger.info('Patching faac')
  patch_faac()
  logger.info('Patching sdl')
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

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
      make_option('-p', '--prefix', action='store', default='./usr', dest='prefix', help='Installation directory prefix'), 
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

  cur_dir = os.getcwd()

  Cache.URLS["ffmpeg"] = Cache.URLS["ffmpeg"] % options.ffmpeg
  cache = Cache('.')
  cache.check()
  cache.extract('build')

  user_dir = os.path.join(cur_dir, options.prefix)
  builder = Builder('build', user_dir)

  if not os.path.isdir('build'):
    logger.info('Create build directory')
    os.mkdir('build')

  os.chdir("build")
  # apply patches
  logger.info('Patching faac')
  builder.patch_faac()
  logger.info('Patching sdl')
  builder.patch_sdl()
  os.chdir('..')

  # build components
  builder.build_lame()
  builder.build_faac()
  builder.build_x264()
  builder.build_sdl()
  builder.build_ffmpeg(options.ffmpeg)

  sys.exit(0)

# end of builder.py

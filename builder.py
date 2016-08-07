#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
@script : builder.py
@about  :
"""
import os
import sys
import logging
from time import time
from optparse import OptionParser, make_option
from builder_utils import *


def parse_args():
    # parse command line arguments
    option_list = [
        make_option('-f', '--ffmpeg', action='store', default='2.6.4',
                    dest='ffmpeg', help='ffmpeg version to build (default 2.6.4)'),
        make_option('-p', '--prefix', action='store', default='/usr/local',
                    dest='prefix', help='Installation directory prefix'),
        make_option('-l', '--log', action='store_true', default=False,
                    help='Use logging to file'),
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

    cur_dir = os.path.abspath(os.path.dirname(__file__))

    if options.log:
        logging.basicConfig(filename='ffmpeg_builder_%d.log' % int(time()),
                            level=logging.DEBUG, format='[%(asctime)s] %(message)s')
    else:
        logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] %(message)s')

    Cache.URLS['ffmpeg'] = Cache.URLS['ffmpeg'] % options.ffmpeg
    cache = Cache('.')
    cache.check()
    cache.extract('build')

    if options.prefix.startswith('/'):
        install_dir = options.prefix
    else:
        install_dir = os.path.join(cur_dir, options.prefix)
    build_dir = 'build'
    builder = Builder(build_dir, install_dir)

    if not os.path.isdir('build'):
        logger.info('Create build directory')
        os.mkdir(build_dir)

    os.chdir(build_dir)
    # apply patches
    logger.info('Patching faac')
    builder.patch_faac()
    logger.info('Patching sdl')
    builder.patch_sdl()
    logger.info('Patching ffmpeg')
    builder.patch_ffmpeg(options.ffmpeg)
    os.chdir('..')

    # build components
    builder.build_lame()
    builder.build_faac()
    builder.build_ass()
    builder.build_x264()
    builder.build_sdl()
    builder.build_ffmpeg(options.ffmpeg)
    logger.info('Done building ffmpeg ' + options.ffmpeg)

    sys.exit(0)

# end of builder.py

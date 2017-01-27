#!/usr/bin/env python
# -*- coding: utf8 -*-
# pylint: disable=invalid-name
"""
@script : builder.py
@about  :
@example:
  $ python builder.py --ffmpeg 3.1.3 --disable vaapi --prefix usr --log &
  $ python builder.py --ffmpeg 2.6.4 --enable openssl --prefix usr --log &
"""
import os
import sys
import logging
from time import time
from optparse import OptionParser, make_option
from builder_utils import Builder, Cache, logger, version


def parse_args():
    """parse command line arguments"""
    option_list = [
        make_option('-f', '--ffmpeg', action='store', default='2.6.4',
                    dest='ffmpeg', help='ffmpeg version to build (default 2.6.4)'),
        make_option('-p', '--prefix', action='store', default='/usr/local',
                    dest='prefix', help='Installation directory prefix'),
        make_option('-l', '--log', action='store_true', default=False,
                    help='Use logging to file'),
        make_option('-e', '--enable', action='store', dest='enable',
                    help='Enable ffmpeg components (separated by comma)'),
        make_option('-d', '--disable', action='store', dest='disable',
                    help='Disable ffmpeg components (separated by comma)'),
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

    Cache.URLS['ffmpeg'] = (Cache.URLS['ffmpeg'][0] % options.ffmpeg, Cache.URLS['ffmpeg'][1])
    cache = Cache('.')
    cache.check()
    build_dir = 'build'
    cache.extract(build_dir)

    if options.prefix.startswith('/'):
        install_dir = options.prefix
    else:
        install_dir = os.path.join(cur_dir, options.prefix)
    builder = Builder(build_dir, install_dir)

    os.chdir(build_dir)
    # apply patches
    # logger.info('Patching faac')
    # builder.patch_faac()
    logger.info('Patching sdl')
    builder.patch_sdl()
    logger.info('Patching ffmpeg')
    builder.patch_ffmpeg(options.ffmpeg)
    os.chdir('..')

    # build components
    builder.build_lame()
    # builder.build_faac()
    builder.build_fdk_aac()
    builder.build_ass()
    builder.build_x264()
    builder.build_sdl()

    enable = []
    if options.enable:
        for opt in options.enable.split(','):
            enable.append(opt.strip())
    disable = []
    if options.disable:
        for opt in options.disable.split(','):
            disable.append(opt.strip())

    builder.build_ffmpeg(options.ffmpeg, enable, disable)
    logger.info('Done building ffmpeg ' + options.ffmpeg)

    sys.exit(0)

# end of builder.py

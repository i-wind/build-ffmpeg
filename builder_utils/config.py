#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@script : config.py
@about  :
"""
import shlex
import logging
from time import time
from subprocess import Popen, PIPE, STDOUT


logging.basicConfig(filename='builder_%d.log' % int(time()),
                    level=logging.DEBUG, format='[%(asctime)s] %(message)s')
logger = logging.getLogger('FFMPEG.builder')


def command(cmd):
  if isinstance(cmd, basestring):
    cmd = shlex.split(cmd)
  proc = Popen(cmd, stdout=PIPE, stderr=STDOUT)
  for line in proc.stdout:
    logger.info(line.rstrip())
    #logger.handlers[0].flush()
  proc.wait()

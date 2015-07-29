#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@script : config.py
@about  :
"""
import shlex
import logging
from time import time
import contextlib
from subprocess import Popen, PIPE, STDOUT


logging.basicConfig(filename='ffmpeg_builder_%d.log' % int(time()),
                    level=logging.DEBUG, format='[%(asctime)s] %(message)s')
logger = logging.getLogger('FFMPEG.builder')

# Unix, Windows and old Macintosh end-of-line
newlines = ['\n', '\r\n', '\r']


def unbuffered(proc, stream='stdout'):
  stream = getattr(proc, stream)
  with contextlib.closing(stream):
    while True:
      out = []
      last = stream.read(1)
      # Don't loop forever
      if last == '' and proc.poll() is not None:
        break
      while last not in newlines:
        # Don't loop forever
        if last == '' and proc.poll() is not None:
          break
        out.append(last)
        last = stream.read(1)
      result = ''.join(out)
      yield result


def command(cmd):
  if isinstance(cmd, basestring):
    cmd = shlex.split(cmd)
  proc = Popen(cmd, stdout=PIPE, stderr=STDOUT,
               # Make all end-of-lines '\n'
               universal_newlines=True,
            )
  for line in unbuffered(proc):
    logger.info(line.rstrip())
    #logger.handlers[0].flush()
  proc.wait()

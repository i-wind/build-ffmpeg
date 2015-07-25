#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
@script  : download.py
@about   :
"""
import os, sys
import urllib2
from subprocess import Popen, call, PIPE


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
  call('tar %s %s' % (flag, name), shell=True)


urls = [
    "http://downloads.sourceforge.net/faac/faac-1.28.tar.bz2",
    "http://sourceforge.net/projects/lame/files/lame/3.99/lame-3.99.5.tar.gz",
    "https://www.libsdl.org/release/SDL-1.2.15.tar.gz",
    "http://ffmpeg.org/releases/ffmpeg-2.6.3.tar.bz2"
  ]


if __name__ == '__main__':
  for url in urls:
    download(url)
    extract(url.split('/')[-1])
  call('git clone git://git.videolan.org/x264.git', shell=True)
  call('cd x264 && git checkout stable && cd ..', shell=True)

sys.exit(0)

# end of download.py

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@script : cache.py
@about  :
"""
import os
import shlex
import shutil
import urllib2
from subprocess import call


class CacheError(Exception): pass


def progress(count, total, suffix=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))
    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)
    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', suffix))
    sys.stdout.flush()


class Cache:
  URLS = {
      "lame"  : "http://sourceforge.net/projects/lame/files/lame/3.99/lame-3.99.5.tar.gz",
      "faac"  : "http://downloads.sourceforge.net/faac/faac-1.28.tar.bz2",
      "sdl"   : "https://www.libsdl.org/release/SDL-1.2.15.tar.gz",
      "ffmpeg": "http://ffmpeg.org/releases/ffmpeg-%s.tar.bz2"
    }

  def __init__(self, root_dir):
    self.root_dir_ = os.path.abspath(root_dir)  # os.getcwd()
    self.arc_dir_ = os.path.join(self.root_dir_, 'cache', 'archive')
    self.git_dir_ = os.path.join(self.root_dir_, 'cache', 'github')
    self.check_dirs()

  def check_dirs(self):
    if not os.path.isdir(self.arc_dir_):
      os.makedirs(self.arc_dir_)
    if not os.path.isdir(self.git_dir_):
      os.mkdir(self.git_dir_)

  def download(self, url):
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

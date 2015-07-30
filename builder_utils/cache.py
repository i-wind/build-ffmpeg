#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@script : cache.py
@about  :
"""
import os, sys
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
      "ffmpeg": "http://ffmpeg.org/releases/ffmpeg-%s.tar.bz2",
      "x264"  : "git://git.videolan.org/x264.git",
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

  def download(self, url, dest=''):
    print "Opening url %s" % url
    if not dest: dest = self.arc_dir_
    file_name = url.split('/')[-1]
    u = urllib2.urlopen(url)
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    print "Downloading: %s Bytes: %s" % (file_name, file_size)
    file_size_dl = 0
    block_sz = 8192
    with open(os.path.join(dest, file_name), 'wb') as f:
      while True:
        buffer = u.read(block_sz)
        if not buffer: break
        file_size_dl += len(buffer)
        f.write(buffer)
        progress(file_size_dl, file_size)
    print

  def clone(self, url, dest=''):
    print "Cloning url %s" % url
    if not dest: dest = self.git_dir_
    call(shlex.split("git clone git://git.videolan.org/x264.git %s" % dest))
    saved = os.getcwd()
    os.chdir(dest)
    call("git checkout stable".split())
    os.chdir(saved)

  def has(self, name, source='arc'):
    result = False
    if source == 'arc':
      if os.path.isfile( os.path.join(self.arc_dir_, name) ):
        result = True
    elif source == 'git':
      if os.path.isdir( os.path.join(self.git_dir_, name) ):
        result = True
    return result

  def check(self):
    # download components
    for lib, url in Cache.URLS.items():
      file_name = url.split('/')[-1]
      name, ext = os.path.splitext(url)
      if ext in ['.gz', '.tgz', '.bz2']:
        source = 'arc'
      elif ext == '.git':
        source = 'git'
      else:
        raise CacheError('Wrong address %s' % url)
      if source == 'arc':
        if not self.has(file_name):
          self.download(url)
      else:
        if not self.has(file_name, 'git'):
          self.clone(url, os.path.join(self.git_dir_, lib))

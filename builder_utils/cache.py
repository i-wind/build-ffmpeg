#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=multiple-statements
"""
Cache for archives and repositories
"""
from __future__ import print_function
import os
import sys
import shlex
import shutil
import urllib2
from collections import namedtuple
from subprocess import call


class CacheError(Exception):
    """Class for Cache error"""
    pass


def progress(count, total, suffix=''):
    """prograss indicator"""
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))
    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)  # pylint: disable=blacklisted-name
    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', suffix))
    sys.stdout.flush()


Library = namedtuple('Library', 'url, type')


class Cache(object):
    """Cache class"""
    URLS = {
        "lame"   : ('http://sourceforge.net/projects/lame/files/lame/3.99/lame-3.99.5.tar.gz', 'gz'),
        "faac"   : ('http://downloads.sourceforge.net/faac/faac-1.28.tar.bz2', 'bz2'),
        "fdk-aac": ('https://github.com/mstorsjo/fdk-aac', 'git'),
        "sdl"    : ('https://www.libsdl.org/release/SDL-1.2.15.tar.gz', 'gz'),
        "ffmpeg" : ('http://ffmpeg.org/releases/ffmpeg-%s.tar.bz2', 'bz2'),
        "x264"   : ('git://git.videolan.org/x264.git', 'git'),
        "libass" : ('https://github.com/libass/libass.git', 'git'),
    }

    def __init__(self, root_dir):
        self.root_dir_ = os.path.abspath(root_dir)  # os.getcwd()
        self.arc_dir_ = os.path.join(self.root_dir_, 'cache', 'archive')
        self.git_dir_ = os.path.join(self.root_dir_, 'cache', 'github')
        self.check_dirs()

    def check_dirs(self):
        """check directories"""
        for path in [self.arc_dir_, self.git_dir_]:
            if not os.path.isdir(path):
                os.makedirs(path)

    def download(self, url, dest=''):
        """download archives"""
        print('Opening url ' + url)
        if not dest: dest = self.arc_dir_
        file_name = url.split('/')[-1]
        response = urllib2.urlopen(url)
        meta = response.info()
        file_size = int(meta.getheaders('Content-Length')[0])
        print('Downloading: {} Bytes: {}'.format(file_name, file_size))
        file_size_dl = 0
        block_sz = 8192
        with open(os.path.join(dest, file_name), 'wb') as fptr:
            while True:
                buffer = response.read(block_sz)  # pylint: disable=redefined-builtin
                if not buffer: break
                file_size_dl += len(buffer)
                fptr.write(buffer)
                progress(file_size_dl, file_size)
        print()

    def clone(self, url, branch='', dest=''):
        """clone repositories"""
        print('Cloning url ' + url)
        if not dest: dest = self.git_dir_
        cmd = 'git clone {} {}'.format(url, dest)
        print(cmd)
        call(shlex.split(cmd))
        saved = os.getcwd()
        if branch:
            os.chdir(dest)
            call(('git checkout ' + branch).split())
            os.chdir(saved)

    def has(self, name, source='arc'):
        """check existence"""
        result = False
        if source == 'arc':
            if os.path.isfile(os.path.join(self.arc_dir_, name)):
                result = True
        elif source == 'git':
            if os.path.isdir(os.path.join(self.git_dir_, name)):
                result = True
        return result

    def check(self):
        """check components"""
        for name, url in Cache.URLS.items():
            lib = Library(*url)
            file_name = lib.url.split('/')[-1]
            if lib.type in ['gz', 'bz2']:
                if not self.has(file_name):
                    self.download(lib.url)
            else:
                # Ubuntu 12.04:
                #   You could always build with the most recent libass commit that still
                #   supports your fontconfig (9a2b38e8f5957418362e86b525f72794565deedd).
                if not self.has(file_name, 'git'):
                    # branch = 'stable' if file_name == 'x264' else \
                    #     '9a2b38e8f5957418362e86b525f72794565deedd'
                    branch = 'stable' if file_name == 'x264' else 'master'
                    self.clone(lib.url, branch, os.path.join(self.git_dir_, name))

    def extract(self, dest):
        """extract items"""
        if not os.path.isdir(dest):
            os.makedirs(dest)
        for _, url in Cache.URLS.items():
            lib = Library(*url)
            file_name = lib.url.split('/')[-1]
            _, ext = os.path.splitext(lib.url)
            if ext in ['.gz', '.tgz', '.bz2']:
                full_name = os.path.join(self.arc_dir_, file_name)
                if ext == '.bz2':
                    cmd = 'tar xfj %s -C %s' % (full_name, dest)
                else:
                    cmd = 'tar xfz %s -C %s' % (full_name, dest)
                print(cmd)
                call(shlex.split(cmd))
            else:
                fname = file_name.split('.')[0]
                full_name = os.path.join(self.git_dir_, fname)
                if not os.path.isdir(os.path.join(dest, fname)):
                    shutil.copytree(full_name, os.path.join(dest, fname))

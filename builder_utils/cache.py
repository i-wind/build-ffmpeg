#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@script : cache.py
@about  :
"""
from __future__ import print_function
import os
import shlex
import shutil
import urllib2
from subprocess import call

from .download import progress


# pylint: disable=multiple-statements,missing-docstring
class CacheError(Exception): pass


class Cache(object):
    """Cache class"""
    URLS = {
        "lame"   : "http://sourceforge.net/projects/lame/files/lame/3.99/lame-3.99.5.tar.gz",
        "faac"   : "http://downloads.sourceforge.net/faac/faac-1.28.tar.bz2",
        "fdk-aac": "https://github.com/mstorsjo/fdk-aac/tarball/master",
        "sdl"    : "https://www.libsdl.org/release/SDL-1.2.15.tar.gz",
        "ffmpeg" : "http://ffmpeg.org/releases/ffmpeg-%s.tar.bz2",
        "x264"   : "git://git.videolan.org/x264.git",
        "libass" : "https://github.com/libass/libass.git",
    }

    def __init__(self, root_dir):
        self.root_dir_ = os.path.abspath(root_dir)  # os.getcwd()
        self.arc_dir_ = os.path.join(self.root_dir_, 'cache', 'archive')
        self.git_dir_ = os.path.join(self.root_dir_, 'cache', 'github')
        self.check_dirs()

    def check_dirs(self):
        """check directories"""
        if not os.path.isdir(self.arc_dir_):
            os.makedirs(self.arc_dir_)
        if not os.path.isdir(self.git_dir_):
            os.mkdir(self.git_dir_)

    def download(self, url, dest=''):
        """download archives"""
        print("Opening url %s" % url)
        if not dest: dest = self.arc_dir_
        file_name = url.split('/')[-1]
        if file_name == 'master':
            file_name = 'fdk-aac.tar.gz'
        response = urllib2.urlopen(url)
        meta = response.info()
        file_size = int(meta.getheaders("Content-Length")[0])
        print("Downloading: %s Bytes: %s" % (file_name, file_size))
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
        print("Cloning url %s" % url)
        if not dest: dest = self.git_dir_
        cmd = "git clone %s %s" % (url, dest)
        print(cmd)
        call(shlex.split(cmd))
        saved = os.getcwd()
        if branch:
            os.chdir(dest)
            call(("git checkout %s" % branch).split())
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
        for lib, url in Cache.URLS.items():
            file_name = url.split('/')[-1]
            if file_name == 'master':
                file_name = 'fdk-aac.tar.gz'
            _, ext = os.path.splitext(url)
            if ext in ['.gz', '.tgz', '.bz2'] or lib == 'fdk-aac':
                source = 'arc'
            elif ext == '.git':
                source = 'git'
            else:
                raise CacheError('Wrong address %s' % url)
            if source == 'arc':
                if not self.has(file_name):
                    self.download(url)
            else:
                # Ubuntu 12.04:
                #   You could always build with the most recent libass commit that still
                #   supports your fontconfig (9a2b38e8f5957418362e86b525f72794565deedd).
                if not self.has(file_name, 'git'):
                    branch = 'stable' if file_name == 'x264' else \
                        '9a2b38e8f5957418362e86b525f72794565deedd'
                    self.clone(url, branch, os.path.join(self.git_dir_, lib))

    def extract(self, dest):
        """extract items"""
        if not os.path.isdir(dest):
            os.makedirs(dest)
        for _, url in Cache.URLS.items():
            file_name = url.split('/')[-1]
            _, ext = os.path.splitext(url)
            if file_name == 'master':
                file_name = 'fdk-aac.tar.gz'
                ext = '.gz'
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
        for dname in os.listdir(dest):
            if 'fdk-aac' in dname and dname != 'fdk-aac': break
        # pylint: disable=undefined-loop-variable
        if not os.path.isdir(os.path.join(dest, 'fdk-aac')):
            cmd = 'rm -rf {}'.format(os.path.join(dest, 'fdk-aac'))
            call(shlex.split(cmd))
        cmd = 'mv -v {} {}'.format(
            os.path.join(dest, dname), os.path.join(dest, 'fdk-aac'))
        call(shlex.split(cmd))

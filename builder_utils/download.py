#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@script : download.py
@about  :
"""
from __future__ import print_function
import sys
import urllib2
from subprocess import call


def progress(count, total, suffix=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))
    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)
    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', suffix))
    sys.stdout.flush()


def download(url):
    print("Opening url %s" % url)
    file_name = url.split('/')[-1]
    u = urllib2.urlopen(url)
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    print("Downloading: %s Bytes: %s" % (file_name, file_size))
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


def extract(name):
    if name.endswith('.tar.gz'):
        flag = 'xfz'
    elif name.endswith('.tar.bz2'):
        flag = 'xfj'
    else:
        raise Exception('Wrong archive name %s' % name)
    call(['tar', flag, name])

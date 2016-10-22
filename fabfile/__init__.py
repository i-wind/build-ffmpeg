#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@script : __init__.py
@about  : fabric application tasks
"""
from fabric.api import task, local


@task
def pack():
    """pack git repository"""
    local('git gc')
    local('git fsck --full --unreachable')
    local('git prune')


@task
def squeeze():
    """compress git repository"""
    local('git fsck --unreachable --no-reflogs')
    local('git reflog expire --expire=now --all')
    local('git gc --aggressive --prune=now')


@task
def pyo():
    """compile python scripts to .pyo"""
    local('python -O -m compileall .')

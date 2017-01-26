#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@script : __init__.py
@about  : fabric application tasks
"""
from fabric.api import task, local


@task
def lint(arg):
    """Use pylint to check code"""
    local('pylint --rcfile=.pylintrc ' + arg)


@task
def pyo():
    """compile python scripts to .pyo"""
    local('python -O -m compileall .')

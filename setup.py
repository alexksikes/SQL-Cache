#!/usr/bin/env python

from distutils.core import setup

setup(name='SQLCache',
    version='0.3',
    description='A simple key-value MySQL store for small chunks of arbitrary data (strings, objects).',
    author='Alex Ksikes',
    author_email='alex.ksikes@gmail.com',
    py_modules=['sql_cache'],
    license='GPL'
)

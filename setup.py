#!/usr/bin/env python

from distutils.core import setup

setup(name='SQLCache',
    version='0.3',
    description='SQLCache is loosely similar to memcached but using MySQL.',
    author='Alex Ksikes',
    author_email='alex.ksikes@gmail.com',
    url='https://github.com/alexksikes/SQL-Cache',
    py_modules=['sql_cache'],
    long_description='A simple key-value MySQL store for small chunks of arbitrary data (strings, objects).',
    license='GPL'
)

#!/usr/bin/env python
"""
Bundle Python packages into a single script

A utility needed to build multiple files into a single script.
It can be useful for distribution or for easy writing of code
and bundle it (for example for www.codingame.com)
"""

import re

from distutils.core import setup

description, long_description = re.split('\n{2}', __doc__)

setup(
    name='pyndler',
    version='1.0.0',
    description=description,
    long_description=long_description,
    author='Dima Starkov',
    author_email='dvstark@yandex.ru',
    url='http://github.com/dimastark/pyndler',
    tests_require=['pytest'],
    scripts=["scripts/pyndler"],
    packages=['pyndler'],
)

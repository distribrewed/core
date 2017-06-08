#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import

from distutils.core import setup

from setuptools import find_packages

with open('requirements-core.txt') as f:
    content = f.readlines()

requires = [x.strip() for x in content]

setup(
    name='distribrewed_core',
    version='0.1.0',
    package_dir={'distribrewed.core': './core_dev/distribrewed/core'},
    packages=[p.split('core_dev.', 1)[1] for p in find_packages() if 'distribrewed.core' in p],
    install_requires=requires,
    description=__doc__,
    include_package_data=True,
    zip_safe=False,
)

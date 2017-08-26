#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='labor-api',
    version='0.0',
    description='',
    url='https://github.com/freieslabor/labor-api',
    author='Freies Labor',
    license='MPL-2.0',
    packages=find_packages(),
    scripts=[
        'bin/labor-api',
    ],
    install_requires=[
        'aiohttp-json-rpc==0.8.2',
    ],
)

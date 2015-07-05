#!/usr/bin/env python
"""
Install airconapp using setuptools
"""

import os

from setuptools import setup, find_packages
from setuptools.command.sdist import sdist

from airconapp import __version__
from airconapp.utils.setup import assets, add_subcommand, egg_info_datetime

with open('README.rst', 'r') as f:
    readme = f.read()

if os.getlogin() == 'vagrant':
    del os.link

setup(
    name='airconapp',
    version=__version__,
    description='airconapp',
    long_description=readme,
    author='Takeflight',
    author_email='admin@takeflight.com.au',
    url='https://bitbucket.org/takeflight/airconapp/',

    install_requires=[
        "Django==1.7.6",
        "psycopg2==2.5.2",
        "wagtail==1.0b1",
        "pytz>=0",
        "elasticsearch==1.2.0",
        "elasticutils==0.8.2",
    ],
    zip_safe=False,
    license='Proprietary License',

    packages=find_packages(),

    include_package_data=True,
    package_data={},

    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    cmdclass={
        'sdist': add_subcommand(sdist, [('assets', None)]),
        'egg_info': egg_info_datetime,
        'assets': assets,
    },
)

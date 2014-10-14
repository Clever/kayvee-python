#!/usr/bin/env python

import os
import sys
from setuptools import setup, find_packages
from pip.req import parse_requirements

import pkg_resources

version_file = pkg_resources.resource_stream(__name__, "kayvee/VERSION")
VERSION = version_file.readline().strip()

here = os.path.abspath(os.path.dirname(__file__))
try:
  with open(os.path.join(here, '../README.md')) as f:
    README = f.read()
  with open(os.path.join(here, '../CHANGES.md')) as f:
    CHANGES = f.read()
except:
  README = ''
  CHANGES = ''

reqs = './requirements.txt' if not sys.argv[1] in ['develop', 'test'] else './requirements-dev.txt'
install_reqs = parse_requirements(os.path.join(here, reqs))

setup(name='kayvee',
      version=VERSION,
      description='Write data to key=val pairs, for human and machine readability',
      author='Clever',
      author_email='tech-notify@getclever.com',
      url='https://github.com/Clever/kayvee-python/',
      long_description=README + '\n\n' + CHANGES,
      packages=find_packages(exclude=['*.tests']),
      install_requires=[str(ir.req) for ir in install_reqs],
      setup_requires=['nose>=1.0'],
      test_suite='test',
      )

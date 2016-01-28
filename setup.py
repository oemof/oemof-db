#! /usr/bin/env python

from distutils.core import setup

setup(name='oemof.db',
      version='0.0.1dev',
      description='The oemof database extension',
      namespace_package = ['oemof'],
      package_dir={'oemof': 'oemof'},
      install_requires=['sqlalchemy >= 1.0',
                        'keyring >= 4.0'])

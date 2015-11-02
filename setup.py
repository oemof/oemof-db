#! /usr/bin/env python

from distutils.core import setup

setup(name='oemof-pg',
      version='0.0.1dev',
      description='The oemof postgis extension',
      package_dir={'oemof_pg': 'oemof_pg'},
      install_requires=['sqlalchemy >= 1.0',
                        'keyring >= 4.0'])

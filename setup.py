#! /usr/bin/env python

from setuptools import find_packages, setup

setup(name='oemof.db',
      version='0.0.4',
      description='The oemof database extension',
      namespace_package = ['oemof'],
      packages=find_packages(),
      package_dir={'oemof': 'oemof'},
      install_requires=['sqlalchemy >= 1.0',
                        'keyring >= 4.0',
                        'shapely',
                        'psycopg2',
                        'keyrings.alt',
                        'pandas >=0.19.1, <=0.19.1'])

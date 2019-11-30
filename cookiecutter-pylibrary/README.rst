========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis|
        | |coveralls| |codecov|
        | |scrutinizer| |codacy| |codeclimate|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/oemof.db/badge/?style=flat
    :target: https://readthedocs.org/projects/oemofdb
    :alt: Documentation Status

.. |travis| image:: https://api.travis-ci.org/oemof/oemof.db.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/oemof/oemof.db

.. |coveralls| image:: https://coveralls.io/repos/oemof/oemof.db/badge.svg?branch=master&service=github
    :alt: Coverage Status
    :target: https://coveralls.io/r/oemof/oemof.db

.. |codecov| image:: https://codecov.io/github/oemof/oemof.db/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/oemof/oemof.db

.. |codacy| image:: https://img.shields.io/codacy/grade/[Get ID from https://app.codacy.com/app/oemof/oemof.db/settings].svg
    :target: https://www.codacy.com/app/oemof/oemof.db
    :alt: Codacy Code Quality Status

.. |codeclimate| image:: https://codeclimate.com/github/oemof/oemof.db/badges/gpa.svg
   :target: https://codeclimate.com/github/oemof/oemof.db
   :alt: CodeClimate Quality Status

.. |version| image:: https://img.shields.io/pypi/v/oemof.db.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/oemof.db

.. |wheel| image:: https://img.shields.io/pypi/wheel/oemof.db.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/oemof.db

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/oemof.db.svg
    :alt: Supported versions
    :target: https://pypi.org/project/oemof.db

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/oemof.db.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/oemof.db

.. |commits-since| image:: https://img.shields.io/github/commits-since/oemof/oemof.db/v0.0.6dev.svg
    :alt: Commits since latest release
    :target: https://github.com/oemof/oemof.db/compare/v0.0.6dev...master


.. |scrutinizer| image:: https://img.shields.io/scrutinizer/quality/g/oemof/oemof.db/master.svg
    :alt: Scrutinizer Status
    :target: https://scrutinizer-ci.com/g/oemof/oemof.db/


.. end-badges

Open Energy Modelling Framework - An extension for all database related things

* Free software: MIT license

Installation
============

::

    pip install oemof.db

You can also install the in-development version with::

    pip install https://github.com/oemof/oemof.db/archive/master.zip


Documentation
=============


https://oemof-db.readthedocs.io/


Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox

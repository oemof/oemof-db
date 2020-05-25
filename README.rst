========
Overview
========

.. start-badges

|version| |commits-since| |supported-versions| |license|

|travis| |wheel| |supported-implementations| |docs|

|coveralls| |codecov| |scrutinizer| |codacy| |codeclimate|

.. |docs| image:: https://readthedocs.org/projects/oemofdb/badge/?style=flat
    :target: https://readthedocs.org/projects/oemofdb
    :alt: Documentation Status

.. |travis| image:: https://api.travis-ci.org/oemof/oemof.db.svg?branch=dev
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/oemof/oemof.db

.. |coveralls| image:: https://coveralls.io/repos/github/oemof/oemof-db/badge.svg?branch=dev
    :alt: coveralls status
    :target: https://coveralls.io/github/oemof/oemof-db?branch=dev


.. |codecov| image:: https://codecov.io/github/oemof/oemof-db/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/oemof/oemof-db

.. |codacy| image:: https://img.shields.io/codacy/grade/7088c02f36304a21b61995dcf6f071c7.svg
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

.. |commits-since| image:: https://img.shields.io/badge/dynamic/json.svg?label=%2B&url=https%3A%2F%2Fapi.github.com%2Frepos%2Foemof%2Foemof-db%2Fcompare%2Fv0.0.6...dev&query=%24.total_commits&colorB=blue
    :alt: Commits since latest release
    :target: https://github.com/oemof/oemof-db/compare/v0.0.6...dev


.. |scrutinizer| image:: https://img.shields.io/scrutinizer/quality/g/oemof/oemof.db/dev.svg
    :alt: Scrutinizer Status
    :target: https://scrutinizer-ci.com/g/oemof/oemof.db/


.. |license| image:: https://img.shields.io/pypi/l/oemof.db.svg?colorB=blue
    :alt: PyPI - License
    :target: https://github.com/oemof/oemof-db/blob/master/LICENSE

.. end-badges

Open Energy Modelling Framework - An extension for all database related things

See `the documentation`_ for more information!

.. _`the documentation`: https://oemofdb.readthedocs.io



Installation
++++++++++++

  ..

    ::

        pip install oemof.db

    You can also install the in-development version with::

        pip install https://github.com/oemof/oemof.db/archive/master.zip

Unfortunately installing the PyPi package doesn't work until #28 is fixed.
Instead, you have to install via:

  .. code:: bash

    pip install -e git://github.com/oemof/oemof.db.git@master#egg=oemof.db

Note that you have to have `git` installed for this to work.

If you want to have the developer version clone the repository by

  .. code:: bash

    git clone git@github.com:oemof/oemof.db.git

and you can install it using pip3 with the -e flag.

  .. code:: bash

    sudo pip3 install -e <path/to/the/oemof.db/repository/root/directory>

.. _readme#configuration:

Keep `virtualenvs`_ in mind!

.. _virtualenvs: https://virtualenv.pypa.io

Configuration and usage
+++++++++++++++++++++++

As the purpose of this package is to facilitate usage of the ``oemof``
database, it needs to know how to connect to this database. Being part of
``oemof``, as fallback ``oemof.db`` always looks for this configuration in the
file ``config.ini`` in a directory called ``.oemof`` in your home directory.

A particular config-file can either specified and accessed via


.. code-block:: python

    from oemof.db import cfg

    # only load config file
    cfg.load_config(config_file=<you-config-file>)

    # access config parameters
    cfg.get(<section>, <parameter>)

If you're interested in establishing a database connection and specify config
file connection parameters are stored in use

.. code-block:: python

    from oemof.db import cfg

    # establish database connection with specified section and config_file
    db.connection(section=<section>, config_file=<you-config-file>)

To configure database access this file has to have at least one dedicated
section containing the necessary options, like this:

  .. code:: INI
    :name: config.ini

    [postGIS]
    username = username under which to connect to the database
    database = name of the database from which to read
    host     = host to connect to
    port     = port to connect to
    pw       = password used to connect with the given username (OPTIONAL)

The section is assumed to be named ``postGIS`` by default, but you can name it
differently and have multiple sections for different databases if the need
arises.

The password is optional. If you don't want to store the password in the
``config.ini``, you may store it using the `keyring package`_, which is a
dependency of ``oemof.db``, like this:

  .. code:: python

    >>> import keyring
    >>> keyring.set_password("database", "username")

where ``"database"`` and ``"username"`` have the same values as the
corresponding options in ``config.ini``.

.. _`keyring package`: https://pypi.python.org/pypi/keyring


Development
+++++++++++

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

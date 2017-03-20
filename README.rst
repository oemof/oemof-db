An oemof extension to use the oemof related postgis database.

See `the documentation`_ for more information!

.. _`the documentation`: https://oemofdb.readthedocs.io



Installation
++++++++++++

Use pypi to install the latest oemof version.

.. code:: bash

  pip3 install oemof.db

If you want to have the developer version clone the repository by

  .. code:: bash

    git clone git@github.com:oemof/oemof.db.git

and can install it using pip3 with the -e flag.

  .. code:: bash

    sudo pip3 install -e <path/to/the/oemof.db/repository/root/directory>

.. _readme#configuration:

Keep `virtualenvs`_ in mind!

.. _`keyring package`: https://virtualenv.pypa.io

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

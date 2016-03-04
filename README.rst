An oemof extension to use the oemof related postgis database.

To use this extension you have to have access to the oemof postgis database.

The oemof code will be released in early 2016 but you can try this extension
already with the feedinlib. If you are interested to join the oemof database
project please contact us.

Installation
++++++++++++

Clone the repository to your local system.

  .. code:: bash

    git clone git@github.com:oemof/oemof.db.git

Then you can install it using pip3 with the -e flag.

  .. code:: bash

    sudo pip3 install -e <path/to/the/oemof.db/root/dir>


.. _readme#configuration:

Configuration
+++++++++++++

As the purpose of this package is to facilitate usage of the ``oemof``
database, it needs to know how to connect to this database. Being part of
``oemof``, ``oemof.db`` looks for this configuration in the file ``config.ini``
in a directory called ``.oemof`` in your home directory.

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

Required packages
+++++++++++++++++

* python3-sqlalchemy
* python3-keyring

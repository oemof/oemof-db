from configparser import NoOptionError as option, NoSectionError
from sqlalchemy import create_engine
import keyring
from . import config as cfg
from oemof.db.tools import db_table2pandas
import getpass


__version__ = '0.0.5'

def url(section="postGIS", config_file=None):
    """ Retrieve the URL used to connect to the database.

    Use this if you have your own means of accessing the database and do not
    want to use :func:`engine` or :func:`connection`.

    Parameters
    ----------
    section : str, optional
        The `config.ini` section corresponding to the targeted database.
        It should contain all the details that needed to set up a connection.

    Returns
    -------
    database URL : str
        The URL with which one can connect to the database. Be careful as this
        will probably contain sensitive data like the username/password
        combination.
    config_file : str, optional
        Relative of absolute of config.ini. If not specified, it tries to read
        from .oemof/config.ini in your HOME dir

    Notes
    -----

    For documentation on config.ini see the README section on
    :ref:`configuring <readme#configuration>` :mod:`oemof.db`.
    """

    cfg.load_config(config_file)

    try:
        pw = keyring.get_password(cfg.get(section, "database"),
                                  cfg.get(section, "username"))
    except NoSectionError as e:
        print("There is no section {section} in your config file. Please "
              "choose one available section from your config file or "
              "specify a new one!".format(
            section=section))
        exit(-1)


    if pw is None:
        try:
            pw = cfg.get(section, "pw")
        except option:
            pw = getpass.getpass(prompt="No password available in your "\
                                        "keyring for database {database}. "
                                        "\n\nEnter your password to " \
                                        "store it in "
                                        "keyring:".format(database=section))
            keyring.set_password(section, cfg.get(section, "username"), pw)
        except NoSectionError:
            print("Unable to find the 'postGIS' section in oemof's config." +
                  "\nExiting.")
            exit(-1)

    return "postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{db}".format(
            user=cfg.get(section, "username"),
            passwd=pw,
            host=cfg.get(section, "host"),
            db=cfg.get(section, "database"),
            port=int(cfg.get(section, "port")))


def engine(section="postGIS", config_file=None):
    """Creates engine object for database access

    If keyword argument `section` is used it requires an existing config.ini
    file at the right location.

    Parameters
    ----------
    section : str, optional
        Section (in config.ini) of targeted database containing connection
        details that are used to set up connection
    config_file : str, optional
        Relative of absolute of config.ini. If not specified, it tries to read
        from .oemof/config.ini in your HOME dir

    Returns
    -------
    engine : :class:`sqlalchemy.engine.Engine`
        Engine for sqlalchemy

    Notes
    -----

    For documentation on config.ini see the README section on
    :ref:`configuring <readme#configuration>` :mod:`oemof.db`.
    """

    return create_engine(url(section, config_file=config_file))


def connection(section="postGIS", config_file=None):
    """Database connection method of sqlalchemy engine object

    This function purely calls the `connect()` method of the engine object
    returned by :py:func:`engine`.

    For description of parameters see :py:func:`engine`.
    """

    return engine(section=section, config_file=config_file).connect()
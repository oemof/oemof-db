from configparser import NoOptionError as option, NoSectionError as section
from sqlalchemy import create_engine
import keyring
from . import config as cfg


def engine(section="postGIS"):
    """Creates engine object for database access

    If keyword argument `section` is used it requires an existing config.ini
    file at the right location.

    Parameters
    ----------
    section : str, optional
        Section (in config.ini) of targeted database containing connection
        details that are used to set up connection

    Returns
    -------
    engine : :class:`sqlalchemy.engine.Engine`
        Engine for sqlalchemy

    Notes
    -----

    For documentation on config.ini see the README section on
    :ref:`configuring <readme#configuration>` :mod:`oemof.db`.
    """

    pw = keyring.get_password(cfg.get(section, "database"),
                              cfg.get(section, "username"))

    if pw is None:
        try:
            pw = cfg.get(section, "pw")
        except option:
            print("Unable to find the database password in " +
                  "the oemof config or keyring." +
                  "\nExiting.")
            exit(-1)
        except section:
            print("Unable to find the 'postGIS' section in oemof's config." +
                  "\nExiting.")
            exit(-1)

    return create_engine(
        "postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{db}".format(
            user=cfg.get(section, "username"),
            passwd=pw,
            host=cfg.get(section, "host"),
            db=cfg.get(section, "database"),
            port=int(cfg.get(section, "port"))))


def connection(section="postGIS"):
    """Database connection method of sqlalchemy engine object

    This function purely calls the `connect()` method of the engine object
    returned by :py:func:`engine`.

    For description of parameters see :py:func:`engine`.
    """
    return engine(section=section).connect()

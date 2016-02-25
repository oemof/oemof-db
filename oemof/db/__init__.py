from configparser import NoOptionError as option, NoSectionError as section
from sqlalchemy import create_engine
import keyring
from . import config as cfg


def engine(db_section="postGIS"):
    """Creates engine for database access

    If keyword argument 'db_section' is used it requires an existing config.ini
    file at the right location.

    Keyword arguments:
    db_section -- name of section in config.ini (default 'postGIS')
    """
    pw = keyring.get_password(cfg.get(db_section, "database"),
                              cfg.get(db_section, "username"))

    if pw is None:
      try: pw = cfg.get(db_section, "pw")
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
            user=cfg.get(db_section, "username"),
            passwd=pw,
            host=cfg.get(db_section, "host"),
            db=cfg.get(db_section, "database"),
            port=int(cfg.get(db_section, "port"))))

def connection(db_section="postGIS"):
    return engine(db_section=db_section).connect()
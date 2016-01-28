from configparser import NoOptionError as option, NoSectionError as section
from sqlalchemy import create_engine
import keyring
from . import config as cfg


def engine():
    pw = keyring.get_password(cfg.get("postGIS", "database"),
                              cfg.get("postGIS", "username"))

    if pw is None:
      try: pw = cfg.get("postGIS", "pw")
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
            user=cfg.get("postGIS", "username"),
            passwd=pw,
            host=cfg.get("postGIS", "host"),
            db=cfg.get("postGIS", "database"),
            port=int(cfg.get("postGIS", "port"))))

def connection():
    return engine().connect()

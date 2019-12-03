# -*- coding: utf-8 -*-
"""
Created on Fri Sep  5 12:26:40 2014

:module-author: steffen
:filename: config.py


This module provides a highlevel layer for reading and writing config files.
There must be a file called "config.ini" in the root-folder of the project.
The file has to be of the following structure to be imported correctly.

# this is a comment \n
# the filestructure is like: \n
 \n
[netCDF] \n
RootFolder = c://netCDF \n
FilePrefix = cd2_ \n
 \n
[mySQL] \n
host = localhost \n
user = guest \n
password = root \n
database = znes \n
 \n
[SectionName] \n
OptionName = value \n
Option2 = value2 \n


"""
import os
import logging

try:
    import configparser as cp
except:
    # to be compatible with Python2.7
    import ConfigParser as cp

FILENAME = 'config.ini'
FILE = os.path.join(os.path.expanduser("~"), '.oemof', FILENAME)

cfg = cp.RawConfigParser()
_loaded = False


def load_config(filename):
    """
    Load data from config file to `cfg` that can be accessed by get, set
    afterwards.

    Specify absolute or relative path to your config file.

    :param filename: Relative or absolute path
    :type filename: str
    """

    if filename is None:
        filename = ''

    abs_filename = os.path.join(os.getcwd(), filename)

    global FILE

    # find the config file
    if os.path.isfile(filename):
        FILE = filename
    elif os.path.isfile(abs_filename):
        FILE = abs_filename
    elif os.path.isfile(FILE):
        pass
    else:
        if os.path.dirname(filename):
            file_not_found = filename
        else:
            file_not_found = abs_filename
        file_not_found_message(file_not_found)

    # load config
    init(FILE)


def file_not_found_message(file_not_found):
    """
    Show error message incl. help if file not found

    :param filename:
    :type filename: str
    """

    logging.error(
        """
        Config file {file} cannot be found.  Make sure this file exists!

        An exemplary section in the config file looks as follows

        [database]
        username = username under which to connect to the database
        database = name of the database from which to read
        host     = host to connect to
        port     = port to connect to

        For further advice, see in the docs (https://oemofdb.readthedocs.io)
        how to format the config.
        """.format(file=file_not_found))


def main():
    pass


def init(FILE):
    """
    Read config file

    :param FILE: Absolute path to config file (incl. filename)
    :type FILE: str
    """
    try:
        cfg.read(FILE)
        global _loaded
        _loaded = True
    except:
        file_not_found_message(FILE)


def get(section, key):
    """
    returns the value of a given key of a given section of the main
    config file.

    :param section: the section.
    :type section: str.
    :param key: the key.
    :type key: str.

    :returns: the value which will be casted to float, int or boolean.
    if no cast is successfull, the raw string will be returned.

    """
    # FILE = 'config_misc'
    if not _loaded:
        init(FILE)
    try:
        return cfg.getfloat(section, key)
    except Exception:
        try:
            return cfg.getint(section, key)
        except:
            try:
                return cfg.getboolean(section, key)
            except:
                return cfg.get(section, key)


def set(section, key, value):
    """
    sets a value to a [section] key - pair.
    if the section doesn't exist yet, it will be created.

    :param section: the section.
    :type section: str.
    :param key: the key.
    :type key: str.
    :param value: the value.
    :type value: float, int, str.
    """

    if not _loaded:
        init()

    if not cfg.has_section(section):
        cfg.add_section(section)

    cfg.set(section, key, value)

    with open(FILE, 'w') as configfile:
        cfg.write(configfile)

if __name__ == "__main__":
    main()

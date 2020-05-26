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
FilePrefix = cd2 \n
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

import configparser as cp
import logging
import os

FILENAME = 'config.ini'
FILE = os.path.join(os.path.expanduser("~"), '.oemof', FILENAME)

cfg = cp.RawConfigParser()
_loaded = False


def load_config(filename):
    """
    Load data from config file to `cfg` that can be accessed by get, set
    afterwards.

    Specify absolute or relative path to your config file.

    Parameters
    ----------
    filename : str
        Relative or absolute path
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

    Parameters
    ----------
    file_not_found : str
        Relative or absolute path
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

    Parameters
    ----------
    FILE : str
        Absolute path to config file (incl. filename)

    """
    cfg.read(FILE)
    global _loaded
    _loaded = True


def get(section, key):
    """
    returns the value of a given key of a given section of the main
    config file.

    Parameters
    ----------
    section : str
        the section.
    key : str
        the key.

    Returns
    -------
    float, int, bool, str
        The value which will be casted to float, int or boolean. If no cast is
        successful, the raw string will be returned.

    """
    # FILE = 'config_misc'
    if not _loaded:
        init(FILE)
    try:
        return cfg.getint(section, key)
    except ValueError:
        try:
            return cfg.getfloat(section, key)
        except ValueError:
            try:
                return cfg.getboolean(section, key)
            except ValueError:
                value = cfg.get(section, key)
                if value == "None":
                    value = None
                return value


def set(section, key, value):
    """
    sets a value to a [section] key - pair.
    if the section doesn't exist yet, it will be created.

    Parameters
    ----------
    section : str
        the section.
    key : str
        the key.
    value : float, int, str
        the value.
    """

    if not _loaded:
        init(FILE)

    if not cfg.has_section(section):
        cfg.add_section(section)

    cfg.set(section, key, value)

    with open(FILE, 'w') as configfile:
        cfg.write(configfile)

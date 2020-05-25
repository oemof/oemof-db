# -*- coding: utf-8 -

"""Tests of the component module.

SPDX-License-Identifier: MIT
"""

from configparser import NoSectionError
from unittest.mock import MagicMock
import getpass
import os

import keyring
import pytest

from oemof.db import connect


def test_url_with_keyring():
    os.chdir(os.path.dirname(__file__))
    config_fn = "connect1.ini"
    keyring.get_password = MagicMock(return_value="super_secure_pw")
    keyring.set_password = MagicMock()
    es = "postgresql+psycopg2://my_name:super_secure_pw@00.00.00.00:815/my_db"
    assert es == connect.url(section="db", config_file=config_fn)


def test_url_without_keyring_pw_typed_in():
    config_fn = "connect1.ini"
    keyring.get_password = MagicMock(return_value=None)
    getpass.getpass = MagicMock(return_value="type_in_pw")
    es = "postgresql+psycopg2://my_name:type_in_pw@00.00.00.00:815/my_db"
    assert es == connect.url(section="db", config_file=config_fn)


def test_url_without_keyring_pw_from_ini():
    config_fn = os.path.join(os.getcwd(), "connect2.ini")
    keyring.get_password = MagicMock(return_value=None)
    es = "postgresql+psycopg2://my_name:pw_from_ini@00.00.00.00:815/my_db"
    assert es == connect.url(section="db", config_file=config_fn)


def test_url_missing_section_in_ini():
    keyring.get_password = MagicMock(
        side_effect=NoSectionError(section="dsfa"))
    msg = "No section: 'There is no section db in your config file."
    with pytest.raises(NoSectionError, match=msg):
        connect.url(section="db")

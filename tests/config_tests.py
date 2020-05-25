# -*- coding: utf-8 -

"""Tests of the component module.

SPDX-License-Identifier: MIT
"""


from nose.tools import eq_, ok_, assert_raises_regexp
from configparser import NoOptionError, NoSectionError
import os
from oemof.db import config


def test_main_basic():
    config.main()


def test_correct_filename():
    fn = "dahfausf.ini"
    f = open(fn, "w+")
    f.write("[type_tester]\n")
    f.write("asd = hello blubb")
    f.close()
    config.load_config(fn)
    assert config.get("type_tester", "asd") == "hello blubb"
    os.remove(fn)
    config.FILE = ""


def test_init_wrong_filename(caplog):
    config.load_config("wrong_filename")
    assert "For further advice, see in the docs" in caplog.text


def test_get_function():
    """Read config file."""
    config.init("config_test.ini")
    assert config.get("type_tester", "my_bool") is True
    assert isinstance(config.get("type_tester", "my_int"), int)
    assert config.get("type_tester", "my_int") == 5
    assert isinstance(config.get("type_tester", "my_float"), float)
    assert config.get("type_tester", "my_float") == 4.5
    assert isinstance(config.get("type_tester", "my_string"), str)
    assert config.get("type_tester", "my_string") == "hallo"
    assert isinstance(config.get("type_tester", "my_None"), type(None))
    assert config.get("type_tester", "my_none") is None
    assert isinstance(config.get("type_tester", "my_list"), str)
    assert config.get("type_tester", "my_list") == "4,6,7,9"


def test_missing_value():
    config.FILE = "config_test.ini"
    with assert_raises_regexp(
        NoOptionError, "No option 'blubb' in section: 'type_tester'"
    ):
        config.get("type_tester", "blubb")
    with assert_raises_regexp(NoSectionError, "No section: 'typetester'"):
        config.get("typetester", "my_bool")


def test_set_temp_value():

    config.FILE = "config_test.ini"
    with assert_raises_regexp(
        NoOptionError, "No option 'blubb' in section: 'type_tester'"
    ):
        config.get("type_tester", "blubb")
    config.set("type_tester", "blubb", "None")
    eq_(config.get("type_tester", "blubb"), None)
    config.set("type_tester", "blubb", "5.5")
    eq_(config.get("type_tester", "blubb"), 5.5)
    remove_line()


def test_set_temp_without_init():
    config.set("type_tester", "blubb", "None")
    remove_line()


def remove_line():
    with open("config_test.ini", "r") as f:
        lines = f.readlines()
    with open("config_test.ini", "w") as f:
        for line in lines:
            print(line)
            if "blubb" not in line:
                f.write(line)

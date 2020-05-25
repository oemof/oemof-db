# -*- coding: utf-8 -

"""Tests of the component module.

SPDX-License-Identifier: MIT
"""

import oemof

import oemof.db.connect as oemofdb


def test_that_oemof_is_importable():
    assert oemof.db.__version__


def test_oemofdb_imports():
    assert oemofdb.connection
    assert oemofdb.engine
    assert oemofdb.url

# -*- coding: utf-8 -

"""Tests of the component module.

SPDX-License-Identifier: MIT
"""

from nose.tools import ok_

import oemof
import oemof.db.connect as oemofdb


def test_that_oemof_is_importable():
    ok_(oemof.db.__version__)


def test_oemofdb_imports():
    ok_(oemofdb.connection)
    ok_(oemofdb.engine)
    ok_(oemofdb.url)

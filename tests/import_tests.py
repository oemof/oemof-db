from nose.tools import ok_

import oemof
import oemof.db as oemofdb


def test_that_oemof_is_importable():
    ok_(oemof.__version__)


def test_oemofdb_imports():
    ok_(oemofdb.connection)
    ok_(oemofdb.engine)
    ok_(oemofdb.url)

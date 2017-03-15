from nose.tools import ok_

import oemof.db as oemofdb

def test_oemofdb_imports():
    ok_(oemofdb.connection)
    ok_(oemofdb.engine)
    ok_(oemofdb.url)


#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from datetime import datetime

from tinydb_jsonorm import Database
from tinydb_jsonorm import TinyJsonModel
from tinydb_jsonorm import fields

#import tinydb_jsonorm


def test_main():
    #assert tinydb_jsonorm  # use your library here
    assert Database
    assert TinyJsonModel
    assert fields

    # Our database
    dbpath = 'tinyjdb-%s.json' % datetime.now().strftime("%y%m%d_%H%M%S")
    table1 = 'config'

    print(dbpath)

    # Usando TinyJ
    dbj = Database(dbpath)
    assert isinstance(dbj, Database), "Missing instance"

    # Purge database tables
    assert dbj._conn.purge_table(table1) == None



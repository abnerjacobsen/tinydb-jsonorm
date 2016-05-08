#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import time
from datetime import datetime
from pprint import pprint

from tinydb_jsonorm import Database
from tinydb_jsonorm import TinyJsonModel
from tinydb_jsonorm import fields

def main():
    # Our database
    dbpath = 't1.json'

    # Usando TinyJ
    dbj = Database(dbpath)

    class ConfigModel(TinyJsonModel):
        __tablename__ = "config"

        name = fields.StringField()
        key = fields.StringField()
        last_update = fields.DateTimeField(required=True)
        created_at = fields.DateTimeField(required=True)

        def __init__(self, *args, **kwargs):
            self.last_update = datetime.utcnow()
            self.created_at = self.last_update
            super(ConfigModel, self).__init__(*args, **kwargs)
            
        # this attribute wont be saved because it's not a field
        address = "this attribute will not be saved"

        # Example model custom method
        def created_at_datetime(self):
            return self.created_at

        @property
        def location(self):
            return "Earth"

        class Meta:
            database = dbj

    
    # Create new record
    model = ConfigModel()
    model.name = "original"
    model.key = "test"
    model.created_at = datetime.utcnow()

    # Insert/save the new record
    newrecid = model.insert()

    # Set table object where perform query, if no set the record is saved in default table of Tinydb
    table = dbj.table(model.__tablename__, cache_size=None)

    # Query all records in table
    allrec = table.all()
    qList = []
    qlist = [ConfigModel(eid=row.eid, **row) for row in allrec]
    print("\nRecords in database: %d" % len(qlist))
    #for rec in qlist:
    #    print("Rec: ", rec.id, rec.key, rec.name)

    # tinydbj - create model from table's record
    row = table.get(dbj.where("key") == "test")
    new_model = ConfigModel(eid=row.eid, **row)

    print("\nLast inserted record")
    print(new_model.id)
    print(new_model.name)
    print(new_model.key)
    print(new_model.created_at)
    print(new_model.address)
    print(new_model.location)
    print(new_model.created_at_datetime())

    # Change/update record
    print("\nChanging last insert record key field")
    new_model.key = 'dev'
    new_model.save()
    print(new_model.id)
    print(new_model.name)
    print(new_model.key)
    print(new_model.created_at)
    print(new_model.address)
    print(new_model.location)
    print(new_model.created_at_datetime())

    # Create record to be deleted
    delrec = ConfigModel(name="nooriginal", key="tobedeleted", created_at=datetime.utcnow())
    delrecid = delrec.insert()


    # Delete record using table object using id
    print("\nDeleting record: %d" % delrecid)
    rectodel = ConfigModel.get(eid=delrecid)
    #rectodel = ConfigModel.get(dbj.where("key") == "tobedeleted")
    print("Created rec: ", model.id, model.key, model.name)
    print("To Delete: ", rectodel.id, rectodel.key, rectodel.name)
    rectodel.delete()

    #drec = ConfigModel(eid=row.eid, **row)
    #print("Rec: ", drec.id, drec.key, drec.name)

if __name__ == "__main__":
    main()


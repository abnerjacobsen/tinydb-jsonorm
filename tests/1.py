#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from datetime import datetime

from tinydb import TinyDB
from tinydb.storages import JSONStorage
from tinydb_smartcache import SmartCacheTable
from tinydb_serialization import Serializer, SerializationMiddleware

from jsonmodels import fields
from tinydb_orm import Database
from tinydb_orm import Model

# To solve json problems with python datetime type
class DateTimeSerializer(Serializer):
    OBJ_CLASS = datetime
    FORMAT = '%Y-%m-%dT%H:%M:%S'

    def encode(self, obj):
        return obj.strftime(self.FORMAT)

    def decode(self, s):
        return datetime.strptime(s, self.FORMAT)

class BaseModel(Model):
    __tablename__ = "BaseModel"

    last_update = fields.DateTimeField(required=True)
    created_at = fields.DateTimeField(required=True)

    def __init__(self, eid=0, *args, **kwargs):
        self.eid = eid
        self.last_update = datetime.utcnow()
        self.created_at = datetime.utcnow()
        super(BaseModel, self).__init__(*args, **kwargs)

    @property
    def location(self):
        return "Earth"

    @property
    def id(self):
        return self.eid

    def created_at_datetime(self):
        return self.created_at

    def save(self):
        table = self.Meta.database.table(self.__tablename__)
        print("UPDATE: ", table.update(self.to_struct(), eids=[self.eid]))

    def insert(self):
        table = self.Meta.database.table(self.__tablename__)
        newid = table.insert(self.to_struct())
        if newid > 0:
            print("EID: ", newid)
            self.eid = newid
        else:
            print("Failed to get eid for the new insert record")


def main():
    # Our database
    dbpath = 't1.json'
    serializer = SerializationMiddleware(JSONStorage)
    serializer.register_serializer(DateTimeSerializer(), 'TinyDate')

    # Usando tinykit
    #dbk = Database(dbpath, storage=serializer)
    #dbk.table_class = SmartCacheTable
    dbk = Database(dbpath)

    # Usando tinyDb puro
    db = TinyDB(dbpath, storage=serializer)
    db.table_class = SmartCacheTable

    class ConfigModel(BaseModel):
        __tablename__ = "config"

        name = fields.StringField()
        key = fields.StringField()

        # this attribute wont be saved because it's not a field
        address = "this attribute will not be saved"

        class Meta:
            database = dbk


    model = ConfigModel()
    model.name = "original"
    model.key = "test"
    model.created_at = datetime.utcnow()

    # TinyDb puro
    #table = db.table(model.__tablename__)
    #model.tinsert()

    # Tinydb com tinykit
    table = dbk.table(model.__tablename__)
    model.insert()

    allrec = table.all()
    qlist = []
    qlist = [ConfigModel(eid=row.eid, **row) for row in allrec]
    for rec in qlist:
        print("Rec: ", rec.id, rec.key, rec.name)

    # tinydbk - create model from table's data
    row = table.get(dbk.where("key") == "test")
    new_model = ConfigModel(eid=row.eid, **row)

    print(new_model.id)
    print(new_model.name)
    print(new_model.key)
    print(new_model.created_at)
    print(new_model.address)
    print(new_model.location)
    print(new_model.created_at_datetime())

    new_model.key = 'dev'
    new_model.save()
    print(new_model.id)
    print(new_model.name)
    print(new_model.key)
    print(new_model.created_at)
    print(new_model.address)
    print(new_model.location)
    print(new_model.created_at_datetime())



if __name__ == "__main__":
    main()


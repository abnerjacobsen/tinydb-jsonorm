from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from datetime import datetime

import tinydb
from tinydb_smartcache import SmartCacheTable
from tinydb_serialization import Serializer, SerializationMiddleware

# To solve json problems with python datetime type
class DateTimeSerializer(Serializer):
    OBJ_CLASS = datetime
    FORMAT = '%Y-%m-%dT%H:%M:%S'

    def encode(self, obj):
        return obj.strftime(self.FORMAT)

    def decode(self, s):
        return datetime.strptime(s, self.FORMAT)


class Database(object):
    """A class acts as a wrapper of ``tinydb.TinyDB`` with
    additional features.

    Typical usage::

        db = Database("/path/to/db.json")
        table = db.table("testing")

        with db.transaction(table) as tr:
            tr.insert({"label": "database"})

        table.get(db.where("label") == "database")

    When using a subclass of ``tinykit.models.Model``::

        from jsonmodels.fields import StringField


        class TestingModel(Model):
            __tablename__ = "testing"
            label = StringField()

        model = TestingModel()
        model.label = "database"

        db = Database("/path/to/db.json")
        table = db.table(model.__tablename__)

        with db.transaction(table) as tr:
            tr.insert(model.to_struct())

        table.get(db.where("label") == model.label)

    :param args: Positional arguments passed to the underlying
                 ``tinydb.TinyDB`` object.
    :param kwargs: Keyword arguments passed to the underlying
                   ``tinydb.TinyDB`` object.
    """

    #def __init__(self, *args, **kwargs):
    def __init__(self, db='nonedb.json'):

        # Storage and serialization
        serializer = SerializationMiddleware(tinydb.storages.JSONStorage)
        serializer.register_serializer(DateTimeSerializer(), 'TinyDateTime')

        # A reference to the actual database object.
        self._conn = tinydb.TinyDB(db, storage=serializer)

        # Activat SmartCache
        self._conn.table_class = SmartCacheTable

        # A shortcut to ``tinydb.TinyDB.table`` method.
        # See http://tinydb.readthedocs.org/en/latest/usage.html#tables
        # for reference.
        self.table = self._conn.table

        # A shortcut to ``tinydb.where`` object.
        # See http://tinydb.readthedocs.org/en/latest/usage.html#queries
        # for reference.
        self.where = tinydb.where

    def __repr__(self):
        return "<{}: storage={}>".format(
            self.__class__.__name__,
            self._conn._storage.__class__.__name__,
        )




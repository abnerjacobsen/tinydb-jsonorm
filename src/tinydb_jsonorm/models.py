from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import jsonmodels.models
from six import add_metaclass


class TablenameMeta(type):
    """Adds ``__tablename__`` attribute to a class.
    """

    def __new__(cls, name, parents, attrs):
        # sets __tablename__ attribute in class;
        # default to class' lowercased name
        attrs.setdefault("__tablename__", name.lower())
        return type.__new__(cls, name, parents, attrs)


@add_metaclass(TablenameMeta)
class Model(jsonmodels.models.Base):
    """A base class for declared model class.

    This class should not be instantiated directly.
    """

    def __repr__(self):
        return "<{}: __tablename__={}>".format(
            self.__class__.__name__,
            self.__tablename__,
        )


class TinyJsonModel(Model):
    __tablename__ = "TinyjModel"

    def __init__(self, eid=0, *args, **kwargs):
        self.eid = eid
        super(TinyJsonModel, self).__init__(*args, **kwargs)

    @property
    def id(self):
        return self.eid

    def save(self):
        table = self.Meta.database.table(self.__tablename__)
        table.update(self.to_struct(), eids=[self.eid])

    def insert(self):
        table = self.Meta.database.table(self.__tablename__)
        newid = table.insert(self.to_struct())
        if newid > 0:
            self.eid = newid
            return self.eid
        else:
            raise ValueError('Failed to get eid for the new insert record')
            




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

    def __init__(self, eid=None, *args, **kwargs):
        if eid is not None:
            self.eid = eid
        super(TinyJsonModel, self).__init__(*args, **kwargs)

    @property
    def id(self):
        return self.eid

    @classmethod
    def get(cls, cond=None, eid=None):
        table = cls.Meta.database.table(cls.__tablename__)
        if eid is not None:
            row = table.get(eid=eid)
        else:
            row = table.get(cond=cond)

        if row is not None:
            return cls(eid=row.eid, **row)
        else:
            raise ValueError('Record not exist')


    def delete(self):
        deletedeid = None
        if self.eid > 0:
            table = self.Meta.database.table(self.__tablename__)
            deletedeid = table.remove(eids=[self.eid])
        else:
            raise ValueError('Record without eid set')
        return deletedeid

    def save(self):
        savedeid = None
        if self.eid > 0:
            table = self.Meta.database.table(self.__tablename__)
            savedeid = table.update(self.to_struct(), eids=[self.eid])
        else:
            raise ValueError('Record without eid set')
        return savedeid

    def insert(self):
        table = self.Meta.database.table(self.__tablename__)
        newid = table.insert(self.to_struct())
        if newid > 0:
            self.eid = newid
            return self.eid
        else:
            raise ValueError('Failed to get eid for the new insert record')
            




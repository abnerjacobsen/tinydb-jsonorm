#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
from datetime import datetime

from tinydb_jsonorm import Database
from tinydb_jsonorm import TinyJsonModel
from tinydb_jsonorm import fields

from jsonmodels import models, validators

from flask import Flask
from flask_debug import Debug

# Hard coded jsonmodels datastores
class CacheType(models.Base):
    __tablename__ = "cachetypes"
    engine = fields.StringField(required=True)
    host =  fields.StringField(required=True, validators=[validators.Length(1, 256)])
    port = fields.IntField(validators=[validators.Min(0), validators.Max(65535)])
    username = fields.StringField()
    password = fields.StringField()

class AuthType(models.Base):
    __tablename__ = "authtypes"
    provider =  fields.StringField(required=True, validators=[validators.Length(1, 256)])


# Initialize some default list options


def main():
    # Our database
    dbpath = 'dbflask-config.json'

    # Usando TinyJ
    dbj = Database(dbpath)

    class ConfigModel(TinyJsonModel):
        __tablename__ = "config"

        ENV =  fields.StringField(required=True, validators=[validators.Length(3, 25)])
        SECRET_KEY = fields.StringField(required=True, validators=[validators.Length(50, 64)])
        APP_DIR = fields.StringField(required=True, validators=[validators.Length(1, 253)])
        PROJECT_ROOT = fields.StringField(required=True, validators=[validators.Length(1, 256)])
        BCRYPT_LOG_ROUNDS = fields.IntField(required=True, validators=[validators.Min(4), validators.Max(10000)]) # needs at least 4 to avoid "ValueError: Invalid rounds"
        DEBUG = fields.BoolField(required=True)
        ASSETS_DEBUG = fields.BoolField(required=True)
        DEBUG_TB_ENABLED = fields.BoolField(required=True)
        DEBUG_TB_INTERCEPT_REDIRECTS = fields.BoolField(required=True)
        CACHE_TYPE = fields.EmbeddedField(CacheType)
        SQLALCHEMY_TRACK_MODIFICATIONS = fields.BoolField(required=True)
        APP_NAME = fields.StringField(required=True, validators=[validators.Length(1, 32)])
        APP_TMPL = fields.StringField(required=True, validators=[validators.Length(1, 32)])
        DB_NAME = fields.StringField(required=True, validators=[validators.Length(1, 32)])
        DB_PATH = fields.StringField(required=True, validators=[validators.Length(1, 256)])
        SQLALCHEMY_DATABASE_URI = fields.StringField(required=True, validators=[validators.Length(1, 256)])
        WTF_CSRF_ENABLED = fields.BoolField(required=True)
        TESTING = fields.BoolField(required=True)
        AUTH_ENGINES = fields.ListField([AuthType])
        FLASK_DEBUG_DISABLE_STRICT = fields.BoolField(required=True)
        _last_update = fields.DateTimeField(required=True)
        _created_at = fields.DateTimeField(required=True)

        def __init__(self, *args, **kwargs):
            super(ConfigModel, self).__init__(*args, **kwargs)
            self._last_update = datetime.utcnow()
            self._created_at = self._last_update

        # Example model custom method
        def created_at_datetime(self):
            return self._created_at

        @property
        def getauthbackends(self):
            return self.AUTH_ENGINES

        class Meta:
            database = dbj


    # Create new record for dev config
    devcfg = ConfigModel(
        ENV = 'dev',
        SECRET_KEY = os.urandom(25).encode('hex'),
        APP_DIR = os.path.abspath(os.path.dirname(__file__)),  # This directory
        #PROJECT_ROOT = os.path.abspath(os.path.join(config.APP_DIR, os.pardir)),
        PROJECT_ROOT = os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir)),
        # For faster tests use 4, see http://security.stackexchange.com/questions/3959/recommended-of-iterations-when-using-pkbdf2-sha256/3993#3993
        BCRYPT_LOG_ROUNDS = 100,
        DEBUG = True,
        ASSETS_DEBUG = True,
        DEBUG_TB_ENABLED = True,
        DEBUG_TB_INTERCEPT_REDIRECTS = False,
        CACHE_TYPE = CacheType(engine='Memcached', host='localhost', port=11211),
        SQLALCHEMY_TRACK_MODIFICATIONS = False,
        APP_NAME = 'Daspanel - Panel GUI',
        APP_TMPL = 'sb-admin',
        DB_NAME = 'dev.db',
        #DB_PATH = os.path.join('/opt/daspanel/data/db', config.DB_NAME),
        DB_PATH = '/opt/daspanel/data/db/dev.db',
        #SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(config.DB_PATH),
        SQLALCHEMY_DATABASE_URI = 'sqlite:////opt/daspanel/data/db/dev.db',
        WTF_CSRF_ENABLED = False,
        TESTING = False,
        AUTH_ENGINES = [
            AuthType(provider='Local'),
            AuthType(provider='Daspanel')
        ],
        FLASK_DEBUG_DISABLE_STRICT = True,
    )
    # ListField can have valued appended
    devcfg.AUTH_ENGINES.append(AuthType(provider='Getuuid'))

    # Validate before save
    devcfg.validate()

    # Insert/save the new record
    devcfgid = devcfg.insert()
    devcfgcuid = devcfg._cuid
    print("\nDevcfg: ", devcfgid, devcfg.id, devcfgcuid, devcfg._cuid, devcfg.ENV, devcfg.AUTH_ENGINES)


    # Create new record for staging config
    stgcfg = ConfigModel()
    stgcfg.ENV = 'staging'
    stgcfg.SECRET_KEY = os.urandom(25).encode('hex')
    stgcfg.APP_DIR = os.path.abspath(os.path.dirname(__file__))
    stgcfg.PROJECT_ROOT = os.path.abspath(os.path.join(stgcfg.APP_DIR, os.pardir))
    stgcfg.BCRYPT_LOG_ROUNDS = 100
    stgcfg.DEBUG = True
    stgcfg.ASSETS_DEBUG = True
    stgcfg.DEBUG_TB_ENABLED = True
    stgcfg.DEBUG_TB_INTERCEPT_REDIRECTS = False
    stgcfg.CACHE_TYPE = CacheType(engine='Memcached', host='localhost', port=11211)
    stgcfg.SQLALCHEMY_TRACK_MODIFICATIONS = False
    stgcfg.APP_NAME = 'Daspanel - Panel GUI'
    stgcfg.APP_TMPL = 'sb-admin'
    stgcfg.DB_NAME = 'dev.db'
    stgcfg.DB_PATH = os.path.join('/opt/daspanel/data/db', stgcfg.DB_NAME)
    stgcfg.SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(stgcfg.DB_PATH)
    stgcfg.WTF_CSRF_ENABLED = False
    stgcfg.TESTING = False
    stgcfg.AUTH_ENGINES = [AuthType(provider='Getuuid'), AuthType(provider='Local')]
    stgcfg.FLASK_DEBUG_DISABLE_STRICT = True

    stgcfg.validate()
    stgcfgid = stgcfg.insert()
    print("Stgcfg: ", stgcfgid, stgcfg.id, stgcfg._cuid, stgcfg.ENV, stgcfg.AUTH_ENGINES)

    # Create new record for production config
    prodcfg = ConfigModel()
    prodcfg.ENV = 'prod'
    prodcfg.SECRET_KEY = os.urandom(25).encode('hex')
    prodcfg.APP_DIR = os.path.abspath(os.path.dirname(__file__))
    prodcfg.PROJECT_ROOT = os.path.abspath(os.path.join(prodcfg.APP_DIR, os.pardir))
    prodcfg.BCRYPT_LOG_ROUNDS = 100
    prodcfg.DEBUG = True
    prodcfg.ASSETS_DEBUG = True
    prodcfg.DEBUG_TB_ENABLED = True
    prodcfg.DEBUG_TB_INTERCEPT_REDIRECTS = False
    prodcfg.CACHE_TYPE = CacheType(engine='Memcached', host='localhost', port=11211)
    prodcfg.SQLALCHEMY_TRACK_MODIFICATIONS = False
    prodcfg.APP_NAME = 'Daspanel - Panel GUI'
    prodcfg.APP_TMPL = 'sb-admin'
    prodcfg.DB_NAME = 'dev.db'
    prodcfg.DB_PATH = os.path.join('/opt/daspanel/data/db', prodcfg.DB_NAME)
    prodcfg.SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(prodcfg.DB_PATH)
    prodcfg.WTF_CSRF_ENABLED = False
    prodcfg.TESTING = False
    prodcfg.AUTH_ENGINES = [AuthType(provider='Getuuid'), AuthType(provider='Daspanel')]
    prodcfg.FLASK_DEBUG_DISABLE_STRICT = True

    prodcfg.validate()
    prodcfgid = prodcfg.insert()
    prodcfgcuid = prodcfg._cuid
    print("Prodcfg: ", prodcfgid, prodcfg.id, prodcfgcuid, prodcfg._cuid, prodcfg.ENV, prodcfg.AUTH_ENGINES, "\n")

    # Get Config record
    myconfig = ConfigModel.get(dbj.where("ENV") == "prod").to_struct()
    app = Flask(__name__)
    app.config.update(myconfig)

    Debug(app)
    app.run(debug=True, port=8000, host='0.0.0.0')



if __name__ == "__main__":
    main()


#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of <%= package.name %>.
# <%= package.url %>

# Licensed under the <%= package.license %> license:
# http://www.opensource.org/licenses/<%= package.license%>-license
# Copyright (c) <%= package.created.year %>, <%= package.author.name %> <<%= package.author.email %>>

import logging
<% if (package.services.mongodb && package.flask.mongoengine) { %>
import sys
<% } %>

from flask import Blueprint
<% if (package.services.mongodb && package.flask.mongoengine) { %>
from flask.ext.mongoengine import MongoEngine, MongoEngineSessionInterface
#from flask.ext.mongoengine import MongoEngineSessionInterface
from pymongo.errors import AutoReconnect
<% } %>
<% if (package.flask.sqlalchemy) { %>
from flask.ext.sqlalchemy import SQLAlchemy
from flask import got_request_exception, current_app

db = SQLAlchemy()

def got_request_exception_handler(sender, exception, **extras):
    db.session.rollback()  # pragma: no cover
<% } %>


<% if (package.services.mongodb && package.flask.mongoengine) { %>
mongo = MongoEngine()

def do_mongoengine_healthcheck():
    conn = mongo.connection.connection
    try:
        return conn.command('ping').get('ok', 0) == 1.0
    except AutoReconnect:
        logging.exception(sys.exc_info()[1])
        return False
<% } %>


mod = Blueprint('db', __name__)


def init_app(app):
    app.register_blueprint(mod)
    logging.info('initializing db')
<% if (package.flask.sqlalchemy) { %>
    db.init_app(app)
    app.db = db
    got_request_exception.connect_via(app)(got_request_exception_handler)

    if app.debug:
        app.config['DEBUG_TB_PANELS'].append('flask_debugtoolbar.panels.sqlalchemy.SQLAlchemyDebugPanel')
<% } %>
<% if (package.services.mongodb && package.flask.mongoengine) { %>
    mongo.init_app(app)

    if app.debug:
        app.config['DEBUG_TB_PANELS'].append('flask.ext.mongoengine.panels.MongoDebugPanel')

    # uncomment this line and the related import to use mongo as your session store
    #app.session_interface = MongoEngineSessionInterface(mongo)
<% } %>

<% if (package.flask.sqlalchemy) { %>
@mod.after_app_request
def after_app_request(f):
    if current_app.config.get('COMMIT_ON_AFTER_REQUEST', True):  # pragma: no cover
        db.session.commit()
    return f
<% } %>

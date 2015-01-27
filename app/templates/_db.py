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

<% if (package.services.mongodb && package.flask.mongoengine) { %>
from flask.ext.mongoengine import MongoEngine, MongoEngineSessionInterface
#from flask.ext.mongoengine import MongoEngineSessionInterface
from pymongo.errors import AutoReconnect
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

def init_app(app):
    logging.info('initializing db')
<% if (package.services.mongodb && package.flask.mongoengine) { %>
    mongo.init_app(app)

    if app.debug:
        app.config['DEBUG_TB_PANELS'].append('flask.ext.mongoengine.panels.MongoDebugPanel')

    # uncomment this line and the related import to use mongo as your session store
    #app.session_interface = MongoEngineSessionInterface(mongo)
<% } %>

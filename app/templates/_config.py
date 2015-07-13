#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of <%= package.name %>.
# <%= package.url %>

# Licensed under the <%= package.license %> license:
# http://www.opensource.org/licenses/<%= package.license%>-license
# Copyright (c) <%= package.created.year %>, <%= package.author.name %> <<%= package.author.email %>>

import os
from derpconf.config import Config, generate_config

STATIC_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static'))

Config.define('APP_SECRET_KEY', None, 'SECRET KEY TO CONFIGURE <%= package.name %>', 'Security')

Config.define('WEBASSETS_DIRECTORY', STATIC_PATH, 'Folder to be root directory for webassets', 'Web')
Config.define('WEBASSETS_AUTO_BUILD', True, 'Auto build static files', 'Web')
Config.define('WEBASSETS_CACHE_PATH', '/tmp/<%= package.pythonName %>/.webassets_cache', 'WebAssets cache path', 'Web')

<% if (package.services.mongodb && package.flask.mongoengine) { %>
Config.define('MONGODB_HOST', 'localhost', 'Host for the MongoDB database', 'MongoDB')
Config.define('MONGODB_DB', '<%= package.pythonName %>', 'Database name for the MongoDB database', 'MongoDB')
Config.define('MONGODB_PORT', 3333, 'Port for the MongoDB database', 'MongoDB')
Config.define('MONGODB_USERNAME', None, 'Username for the MongoDB database', 'MongoDB')
Config.define('MONGODB_PASSWORD', None, 'Password for the MongoDB database', 'MongoDB')
<% } %>
<% if (package.flask.sqlalchemy) { %>
Config.define(
    'SQLALCHEMY_DATABASE_URI',
    'mysql+mysqldb://root@localhost:3306/<%= package.pythonName %>',
    'SQLAlchemy Connection String',
    'SQLAlchemy'
)
<% } %>
<% if (package.flask.useAuth) { %>
Config.define('AUTH_PROVIDERS', None, 'Configuration for authentication providers', 'Auth')
Config.define('AVATAR_SIZE', 320, 'Default user picture size to store in DB', 'Auth')
Config.define('AUTHORIZED_ADMINS', [], 'List of authorized admin e-mail addresses', 'Admin')
<% } %>
<% if (package.services.redis) { %>
Config.define('REDIS_HOST', '127.0.0.1', 'Redis Host IP', 'Redis')
Config.define('REDIS_PORT', 4444, 'Redis port', 'Redis')
Config.define('REDIS_PASS', None, 'Redis Password', 'Redis')
<% } %>
<% if (package.flask.pyres) { %>
Config.define('RESWEB_USER', 'admin', 'PyRes Admin username', 'Redis')
Config.define('RESWEB_PASS', '123', 'PyRes Admin password', 'Redis')
# TODO: PLEASE CHANGE THIS TO VALUES THAT MAKE SENSE TO YOUR APP
Config.define('DEFAULT_QUEUES', ['sample'], 'PyRes Default Queues per Worker', 'Redis')
<% } %>


def init_app(app, path=None):
    conf = Config.load(path)
    for conf_option, _ in conf.items.items():
        app.config[conf_option] = conf[conf_option]

    app.secret_key = app.config['APP_SECRET_KEY']

if __name__ == '__main__':
    generate_config()

#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of <%= package.name %>.
# <%= package.url %>

# Licensed under the <%= package.license %> license:
# http://www.opensource.org/licenses/<%= package.license%>-license
# Copyright (c) <%= package.created.year %>, <%= package.author.name %> <<%= package.author.email %>>

from flask import Blueprint
<% if (package.flask.pyres) { %>
from pyres import ResQ
<% } %>

mod = Blueprint('queue', __name__)


def init_app(app):
    app.register_blueprint(mod)
<% if (package.flask.pyres) { %>
    app.pyres = ResQ(server="%s:%s" % (app.config['REDIS_HOST'], app.config['REDIS_PORT']), password=app.config['REDIS_PASS'])
<% } %>

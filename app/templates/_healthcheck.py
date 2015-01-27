#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of <%= package.name %>.
# <%= package.url %>

# Licensed under the <%= package.license %> license:
# http://www.opensource.org/licenses/<%= package.license%>-license
# Copyright (c) <%= package.created.year %>, <%= package.author.name %> <<%= package.author.email %>>


from flask import Blueprint

<% if (package.services.mongodb && package.flask.mongoengine) { %>
from <%= package.pythonName %>.db import do_mongoengine_healthcheck
<% } %>

mod = Blueprint('healthcheck', __name__)


@mod.route("/healthcheck/")
def healthcheck():
    <% if (package.services.mongodb && package.flask.mongoengine) { %>
    if not do_mongoengine_healthcheck():
        return 'MONGODB is DOWN'
    <% } %>

    return 'WORKING'

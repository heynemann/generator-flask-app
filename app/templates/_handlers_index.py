#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of <%= package.name %>.
# <%= package.url %>

# Licensed under the <%= package.license %> license:
# http://www.opensource.org/licenses/<%= package.license%>-license
# Copyright (c) <%= package.created.year %>, <%= package.author.name %> <<%= package.author.email %>>

from datetime import datetime

from flask import Blueprint, render_template, current_app

<% if ((package.services.mongodb && package.flask.mongoengine) || package.flask.sqlalchemy) { %>
from <%= package.pythonName %>.models.user import User
<% } %>


mod = Blueprint('index', __name__)


@mod.route("/")
def index():
    <% if (package.services.mongodb && package.flask.mongoengine) { %>
    users = list(User.objects.all())
    <% } else if (package.flask.sqlalchemy) { %>
    users = list(current_app.db.session.query(User).all())
    <% } else { %>
    users = []
    <% } %>
    return render_template('index.html', dt=datetime.now().strftime("%d %M %Y - %H %m %s"), users=users)

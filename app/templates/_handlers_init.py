#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of <%= package.name %>.
# <%= package.url %>

# Licensed under the <%= package.license %> license:
# http://www.opensource.org/licenses/<%= package.license%>-license
# Copyright (c) <%= package.created.year %>, <%= package.author.name %> <<%= package.author.email %>>


from <%= package.pythonName %>.handlers import (
    healthcheck,
    # add your own handlers here
)


def init_app(app):
    app.register_blueprint(healthcheck.mod)

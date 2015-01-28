#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of <%= package.name %>.
# <%= package.url %>

# Licensed under the <%= package.license %> license:
# http://www.opensource.org/licenses/<%= package.license%>-license
# Copyright (c) <%= package.created.year %>, <%= package.author.name %> <<%= package.author.email %>>

from <%= package.pythonName %>.db import mongo


class User(mongo.Document):
    email = mongo.StringField(required=True)
    first_name = mongo.StringField(max_length=50)
    last_name = mongo.StringField(max_length=50)

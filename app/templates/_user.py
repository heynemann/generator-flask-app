#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of <%= package.name %>.
# <%= package.url %>

# Licensed under the <%= package.license %> license:
# http://www.opensource.org/licenses/<%= package.license%>-license
# Copyright (c) <%= package.created.year %>, <%= package.author.name %> <<%= package.author.email %>>

from <%= package.pythonName %>.db import mongo


class User(mongo.Document):
    email = mongo.StringField(max_length=2000)
    picture = mongo.StringField(max_length=2000)
    username = mongo.StringField(max_length=255)
    name = mongo.StringField(max_length=255)
    user_id = mongo.StringField(required=True)
    provider = mongo.StringField(required=True)

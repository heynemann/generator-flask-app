#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of <%= package.name %>.
# <%= package.url %>

# Licensed under the <%= package.license %> license:
# http://www.opensource.org/licenses/<%= package.license%>-license
# Copyright (c) <%= package.created.year %>, <%= package.author.name %> <<%= package.author.email %>>
<% if (package.services.mongodb && package.flask.mongoengine) { %>
from <%= package.pythonName %>.db import mongo


class User(mongo.Document):
    email = mongo.StringField(max_length=2000)
    picture = mongo.StringField(max_length=2000)
    username = mongo.StringField(max_length=255)
    name = mongo.StringField(max_length=255)
    user_id = mongo.StringField(required=True)
    provider = mongo.StringField(required=True)
<% } %>
<% if (package.flask.sqlalchemy) { %>
from <%= package.pythonName %>.db import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    username = db.Column(db.String(200))
    email = db.Column(db.String(200), unique=True)
    user_id = db.Column(db.String(255), unique=True)
    provider = db.Column(db.String(255), unique=True)
    picture = db.Column(db.String(255))

    @classmethod
    def by_email(cls, email):
        return cls.query.filter(cls.email == email).first()

    @classmethod
    def by_id(cls, user_id):
        return cls.query.filter(cls.user_id == user_id).first()

    def __unicode__(self):
        return self.username
<% } %>

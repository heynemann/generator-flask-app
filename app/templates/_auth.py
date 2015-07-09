#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of <%= package.name %>.
# <%= package.url %>

# Licensed under the <%= package.license %> license:
# http://www.opensource.org/licenses/<%= package.license%>-license
# Copyright (c) <%= package.created.year %>, <%= package.author.name %> <<%= package.author.email %>>

from urlparse import urljoin
from functools import wraps

from flask import (
    Blueprint, render_template, request, make_response, current_app, session,
    redirect, g, url_for
)

from authomatic.adapters import WerkzeugAdapter
from authomatic import Authomatic, provider_id
from authomatic.providers import oauth2, oauth1

from <%= package.pythonName %>.models.user import User


mod = Blueprint('auth', __name__, url_prefix='/auth')


def init_app(app):
    if app.config['AUTH_PROVIDERS'] is None:
        raise RuntimeError('You must configure the authentication providers. For more info look at the local.conf file')

    app.authomatic = Authomatic(
        app.config['AUTH_PROVIDERS'],
        app.config['APP_SECRET_KEY'],
        report_errors=False
    )

    app.register_blueprint(mod)


def authenticated(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not g.user:
            return redirect(url_for('auth.login_page', next=request.path))
        return f(*args, **kwargs)
    return decorated


@mod.before_app_request
def before_app_request():
    g.user = None
    if 'user_id' in session:
        <% if (package.services.mongodb && package.flask.mongoengine) { %>
        g.user = User.objects(user_id=session['user_id']).first()
        <% } %>
        <% if (package.flask.sqlalchemy) { %>
        g.user = User.by_id(session['user_id'])
        <% } %>


@mod.route('/login/')
def login_page():
    if g.user:
        return redirect_next()
    next_url = request.args.get('next', '')
    if next_url:
        session['next'] = next_url
    return render_template('login.html')


@mod.route('/logout/')
def logout():
    if 'user_id' in session:
        del session['user_id']
    if 'next' in session:
        del session['next']
    return redirect(url_for('index.index'))


@mod.route('/login/<provider_name>/', methods=['GET', 'POST'])
def login(provider_name):
    response = make_response()
    result = current_app.authomatic.login(
        CustomWerkzeugAdapter(request, response), provider_name
    )

    if result:
        if result.user:
            result.user.update()

            <% if (package.services.mongodb && package.flask.mongoengine) { %>
            user = User.objects.filter(provider=provider_name, user_id=result.user.id).first()
            <% } %>
            <% if (package.flask.sqlalchemy) { %>
            user = User.by_email(result.user.email)
            <% } %>

            picture = ''
            if provider_name == "facebook":
                picture = "http://graph.facebook.com/%s/picture?type=large" % result.user.id
            elif result.user.picture:
                picture = result.user.picture.replace('sz=50', 'sz=%d' % current_app.config['AVATAR_SIZE'])
            else:
                picture = result.user.picture

            if user is None:
                user = User(
                    username=result.user.username,
                    email=result.user.email,
                    name=result.user.name,
                    user_id=result.user.id,
                    provider=provider_name,
                    picture=picture
                )
                <% if (package.services.mongodb && package.flask.mongoengine) { %>
                user.save()
                <% } %>
                <% if (package.flask.sqlalchemy) { %>
                current_app.db.session.add(user)
                <% } %>
            else:
                user.name = result.user.name
                user.email = result.user.email
                user.picture = picture
                <% if (package.services.mongodb && package.flask.mongoengine) { %>
                user.save()
                <% } %>

            session['user_id'] = user.user_id
            return redirect_next()

        flash_error('Authentication failed')
        return redirect(url_for('auth.login_page', next=request.path))

    return response


def redirect_next():
    next_url = session.pop('next', None)

    if next_url is None:
        endpoint = current_app.config.get('LOGIN_REDIRECT_ENDPOINT', None)
        if endpoint is None:
            next_url = '/'
        else:
            next_url = url_for(endpoint)

    return redirect(next_url)
<% if (package.flask.authProviders.google) { %>


class CustomGoogle(oauth2.Google):
    def _fetch(self, *args, **kw):
        return custom_fetch(self, *args, **kw)
<% } %>
<% if (package.flask.authProviders.facebook) { %>


class CustomFacebook(oauth2.Facebook):
    def _fetch(self, *args, **kw):
        return custom_fetch(self, *args, **kw)
<% } %>


class CustomWerkzeugAdapter(WerkzeugAdapter):
    @property
    def url(self):
        url = current_app.config.get('BASE_URL', None)
        if not url:
            url = self.request.base_url  # even if url is empty (not None)
        else:
            url = url % (self.request.path.replace('/auth/login/', '').rstrip('/'))
        return url

PROVIDER_ID_MAP = [
    <% if (package.flask.authProviders.google) { %>
    CustomGoogle,
    <% } %>
    <% if (package.flask.authProviders.facebook) { %>
    CustomFacebook,
    <% } %>
    <% if (package.flask.authProviders.twitter) { %>
    oauth1.Twitter,
    <% } %>
]

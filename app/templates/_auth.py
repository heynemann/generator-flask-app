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
from authomatic.providers import oauth2
from authomatic.providers import oauth1

from <%= package.pythonName %>.db import mongo
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
        g.user = User.query.filter_by(user_id=session['user_id']).first()


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
    return redirect(url_for('auth.login_page', next=request.path))


@mod.route('/login/<provider_name>/', methods=['GET', 'POST'])
def login(provider_name):
    response = make_response()
    result = current_app.authomatic.login(
        WerkzeugAdapter(request, response), provider_name
    )

    if result:
        if result.user:
            first_login = False
            result.user.update()
            user = User.query.filter_by(provider=provider_name, user_id=result.user.id).first()
            if user is None:
                user = User(
                    username=result.user.username,
                    email=result.user.email,
                    name=result.user.name,
                    user_id=result.user.id,
                    provider=provider_name
                )
                mongo.session.add(user)
                mongo.session.flush()
                first_login = True
            else:
                user.name = result.user.name
                user.email = result.user.email

            session['user_id'] = user.user_id
            return redirect_next()

        flash_error('Authentication failed')
        return redirect(url_for('auth.login_page', next=request.path))

    return response


def redirect_next():
    next_url = session.pop('next', None)
    return redirect(
        next_url if next_url else url_for(
            current_app.config.get('LOGIN_REDIRECT_ENDPOINT', '/')
        )
    )

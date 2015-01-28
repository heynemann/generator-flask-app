#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of <%= package.name %>.
# <%= package.url %>

# Licensed under the <%= package.license %> license:
# http://www.opensource.org/licenses/<%= package.license%>-license
# Copyright (c) <%= package.created.year %>, <%= package.author.name %> <<%= package.author.email %>>

import os
import os.path
import logging
import sys
import argparse
from urlparse import urlparse, urlunparse

from flask import Flask, request, redirect, current_app
from flask_debugtoolbar import DebugToolbarExtension

from <%= package.pythonName %> import config as config_module
from <%= package.pythonName %>.static import assets
from <%= package.pythonName %> import (
    handlers,
    db,
<% if (package.flask.useAuth) { %>
    auth,
<% } %>
)

blueprints = (
    handlers,
    assets,
<% if (package.services.mongodb && package.flask.mongoengine) { %>
    db,
<% } %>
<% if (package.flask.useAuth) { %>
    auth,
<% } %>
)


def run_bower_list():
    bower_list_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
    bower_list = 'bower_list.js'
    try:
        os.system('cd %s && node %s' % (bower_list_path, bower_list))
    except Exception:
        err = sys.exc_info()[1]
        print "Could not update bower list of assets (%s). Shutting down." % err
        sys.exit(1)


def create_app(config, debug=False):
    if config is None:
        config = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'config', 'local.conf'))

    app = Flask(__name__)
    app.debug = debug
    config_module.init_app(app, config)


    logging.basicConfig(level=logging.DEBUG)

    if app.debug:
        app.config['DEBUG_TB_PROFILER_ENABLED'] = True
        app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
        app.config['DEBUG_TB_PANELS'] = app.config.get('DEBUG_TB_PANELS', [
            'flask_debugtoolbar.panels.versions.VersionDebugPanel',
            'flask_debugtoolbar.panels.timer.TimerDebugPanel',
            'flask_debugtoolbar.panels.headers.HeaderDebugPanel',
            'flask_debugtoolbar.panels.request_vars.RequestVarsDebugPanel',
            'flask_debugtoolbar.panels.config_vars.ConfigVarsDebugPanel',
            'flask_debugtoolbar.panels.template.TemplateDebugPanel',
            'flask_debugtoolbar.panels.logger.LoggingPanel',
            'flask_debugtoolbar.panels.profiler.ProfilerDebugPanel',
        ])
        app.toolbar = DebugToolbarExtension(app)

    for blueprint in blueprints:
        blueprint.init_app(app)

    if app.debug:
        run_bower_list()

    return app


def main():
    args = parse_arguments()
    app = create_app(args.conf, debug=args.debug)
    app.run(debug=args.debug, host=args.bind, port=args.port, threaded=True)


def parse_arguments(args=None):
    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser()
    parser.add_argument('--port', '-p', type=int, default="3000", help="Port to start the server with.")
    parser.add_argument('--bind', '-b', default="0.0.0.0", help="IP to bind the server to.")
    parser.add_argument('--conf', '-c', default='<%= package.pythonName %>/config/local.conf', help="Path to configuration file.")
    parser.add_argument('--debug', '-d', action='store_true', default=False, help='Indicates whether to run in debug mode.')

    options = parser.parse_args(args)
    return options

#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of <%= package.name %>.
# <%= package.url %>

# Licensed under the <%= package.license %> license:
# http://www.opensource.org/licenses/<%= package.license%>-license
# Copyright (c) <%= package.created.year %>, <%= package.author.name %> <<%= package.author.email %>>

import logging
import os
import sys
import argparse
import tempfile

<% if (package.flask.pyres) { %>
from pyres import ResQ

from <%= package.pythonName %>.app import create_app
<% } %>
<% if (package.flask.pyres) { %>


def main():
    args = parse_arguments()
    app = create_app(args.conf, debug=args.debug)

    try:
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write('RESWEB_HOST = "%s:%s"\n' % (app.config['REDIS_HOST'], app.config['REDIS_PORT']))
            if app.config['REDIS_PASS']:
                f.write('RESWEB_PASSWORD = "%s"\n' % app.config['REDIS_PASS'])
            f.write('SERVER_HOST = "%s"\n' % args.bind)
            f.write('SERVER_PORT = %d\n' % args.port)

            f.write('BASIC_AUTH = True\n')
            f.write('AUTH_USERNAME = "%s"\n' % app.config['RESWEB_USER'])
            f.write('AUTH_PASSWORD = "%s"\n' % app.config['RESWEB_PASS'])

            os.environ['RESWEB_SETTINGS'] = f.name

        from resweb.core import main as resweb_main  # IMPORT HERE TO LOAD ENV
        resweb_main()
    finally:
        os.unlink(f.name)


def parse_arguments(args=None):
    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser()
    parser.add_argument('--port', '-p', type=int, default="3001", help="Port to start the server with.")
    parser.add_argument('--bind', '-b', default="0.0.0.0", help="IP to bind the server to.")
    parser.add_argument('--conf', '-c', default='<%= package.pythonName %>/config/local.conf', help="Path to configuration file.")
    parser.add_argument('--debug', '-d', action='store_true', default=False, help='Indicates whether to run in debug mode.')

    options = parser.parse_args(args)
    return options
<% } %>

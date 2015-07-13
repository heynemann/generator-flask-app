#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of <%= package.name %>.
# <%= package.url %>

# Licensed under the <%= package.license %> license:
# http://www.opensource.org/licenses/<%= package.license%>-license
# Copyright (c) <%= package.created.year %>, <%= package.author.name %> <<%= package.author.email %>>


import sys
import argparse

from pyres.worker import Worker

from <%= package.pythonName %>.app import create_app


def main():
    args = parse_arguments()
    app = create_app(args.conf, debug=args.debug)

    if args.queue:
        queue = args.queue.split(',')
    else:
        queue = app.config['DEFAULT_QUEUES']

    with app.app_context():
        Worker.run(queue, server="%s:%s" % (app.config['REDIS_HOST'], app.config['REDIS_PORT']), password=app.config['REDIS_PASS'])


def parse_arguments(args=None):
    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser()
    parser.add_argument('--conf', '-c', default='<%= package.pythonName %>/config/local.conf', help="Path to configuration file.")
    parser.add_argument('--queue', '-q', default='', help="CSV with names of queues that this worker should listen to.")
    parser.add_argument('--debug', '-d', action='store_true', default=False, help='Indicates whether to run in debug mode.')

    options = parser.parse_args(args)
    return options

#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of <%= package.name %>.
# <%= package.url %>

# Licensed under the <%= package.license %> license:
# http://www.opensource.org/licenses/<%= package.license%>-license
# Copyright (c) <%= package.created.year %>, <%= package.author.name %> <<%= package.author.email %>>

import os
import re

from flask import json
from flask.ext import assets

from webassets.updater import TimestampUpdater


STATIC_PATH = os.path.join(os.path.dirname(__file__))
VENDOR_PATH = os.path.join(STATIC_PATH, 'vendor')
PACKAGE_REGEX = re.compile(r'(?:(?:[├│└──┬]+)\s*)+\s([^#]+(?!.+extraneous))')

assets_env = assets.Environment()


def init_app(app):
    assets_env.app = app
    assets_env.init_app(app)

    assets_env.manifest = "file:%s" % (os.path.join(STATIC_PATH, '.webassets-manifest'))
    cache_path = app.config['WEBASSETS_CACHE_PATH']
    if not app.debug and not os.path.exists(cache_path):
        os.makedirs(cache_path)
    assets_env.cache = cache_path

    assets_env.load_path = STATIC_PATH
    assets_env.versions = 'hash:32'
    assets_env.auto_build = app.config['WEBASSETS_AUTO_BUILD']
    assets_env.url_expire = False

    # Tell flask-assets where to look for our coffeescript and scss files.
    assets_env.load_path = [
        os.path.join(os.path.dirname(__file__), 'scss'),
        os.path.join(os.path.dirname(__file__), 'coffee'),
        VENDOR_PATH
    ]

    bower_dependencies = read_bower_json()
    js_files = bower_dependencies.get('.js', [])

    js_out = 'js/js_app.%(version)s.js'
    if app.debug:
        js_out = 'js/js_app.js'

    js_files.append(
        assets.Bundle(
            *get_coffee_files(),
            depends=('*.coffee'),
            # OTHER CONFIGS
            filters=['coffeescript'], output=js_out
        )
    )

    app.config['COMPASS_CONFIG'] = dict(
        encoding="utf-8",
        css_dir="css",
        fonts_dir="fonts",
        sass_dir="scss",
        images_dir="images",
        javascripts_dir="js",
        relative_assets=True,
    )

    js_out = 'js/js_all.%(version)s.js'
    if app.debug:
        js_out = 'js/js_all.js'

    js_all_bundle = assets.Bundle(
        *js_files,
        output=js_out
    )
    assets_env.register('js_all', js_all_bundle)

    css_out = 'css/css_all.%(version)s.css'
    if app.debug:
        css_out = 'css/css_all.css'

    css_all_bundle = assets.Bundle(
        'all.scss',
        depends=('_*.scss'),
        filters=['compass', 'cssmin'],
        output=css_out
    )
    assets_env.register('css_all', css_all_bundle)

    css_out = 'css/base.%(version)s.css'
    if app.debug:
        css_out = 'css/base.css'

    css_files = bower_dependencies.get('.css', [])
    css_base_bundle = assets.Bundle(
        *css_files,
        filters=['cssmin'],
        output=css_out
    )
    assets_env.register('css_base', css_base_bundle)

    if app.debug:
        assets_env.set_updater(TimestampUpdater())
        assets_env.cache = False
        assets_env.auto_build = True
        assets_env.debug = True


def read_bower_json():
    result = {}
    bower_dependencies = os.path.join(
        os.path.dirname(__file__), 'bower_dependencies.json'
    )

    if not os.path.exists(bower_dependencies):
        return result

    with open(bower_dependencies, 'r') as f:
        result = json.loads(f.read())
    for k, v in result.items():
        result[k] = [depFile.replace('static/vendor/', '') for depFile in v]
    return result


def get_coffee_files():
    coffee_files = []

    coffee_root = os.path.join(
        os.path.dirname(__file__), 'coffee'
    )

    for filename in os.listdir(coffee_root):
        if os.path.splitext(filename)[1] == '.coffee':
            coffee_files.append(filename)

    return list(sorted(coffee_files))

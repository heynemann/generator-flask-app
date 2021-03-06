#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of <%= package.name %>.
# <%= package.url %>

# Licensed under the <%= package.license %> license:
# http://www.opensource.org/licenses/<%= package.license%>-license
# Copyright (c) <%= package.created.year %>, <%= package.author.name %> <<%= package.author.email %>>

from setuptools import setup, find_packages
from <%= package.pythonName %> import __version__

tests_require = [
    'mock',
    'nose',
    'coverage',
    'yanc',
    'preggy',
    'tox',
    'ipdb',
    'coveralls',
    'sphinx',
]

setup(
    name='<%= package.name %>',
    version=__version__,
    description='<%= package.description %>',
    long_description='''
<%= package.description %>
''',
    keywords='<%= package.keywords %>',
    author='<%= package.author.name %>',
    author_email='<%= package.author.email %>',
    url='<%= package.url %>',
    license='<%= package.license %>',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: <%= package.license %> License',
        'Natural Language :: English',
        'Operating System :: Unix',
        <% for (var i=0; i< package.troves.length; i++) { %>'<%= package.troves[i] %>',
        <% } %>'Operating System :: OS Independent',
    ],
    packages=find_packages(),
    include_package_data=<%= package.includePackageData ? "True" : "False" %>,
    install_requires=[
        'Flask>=0.10.0,<0.11.0',
        'derpconf>=0.7.0,<0.8.0',
        'flask-debugtoolbar>=0.9.0,<0.10.0',
        'flask-assets>=0.10',
        'cssmin>=0.2.0,<0.3.0',
        'Flask-Script>=2.0.0,<2.1.0',
<% if (package.services.mongodb && package.flask.mongoengine) { %>
        'pymongo>=2.8,<2.9',
        'flask-mongoengine>=0.7.0,<0.8.0',
<% } %>
<% if (package.flask.sqlalchemy) { %>
        'flask-sqlalchemy>=2.0,<2.1',
        'alembic>=0.7.6,<0.8.0',
        'mysql-python>=1.2.5,<1.3.0',
<% } %>
<% if (package.flask.admin) { %>
        'Flask-Admin>=1.2.0,<1.3.0',
<% } %>
<% if (package.flask.useAuth) { %>
        'Authomatic>=0.1.0,<0.2.0',
<% } %>
<% if (package.flask.pyres) { %>
        'pyres>=1.5,<1.6',
        'resweb>=0.1.7,<0.2.0',
<% } %>
    ],
    extras_require={
        'tests': tests_require,
    },
    entry_points={
        'console_scripts': [
            '<%= package.commandName %>=<%= package.pythonName %>.app:main',
            '<%= package.commandName %>-manage=<%= package.pythonName %>.manage:main',
<% if (package.flask.pyres) { %>
            '<%= package.commandName %>-resweb=<%= package.pythonName %>.resweb_ext:main',
            '<%= package.commandName %>-worker=<%= package.pythonName %>.pyres_worker:main',
<% } %>
        ],
    },
)

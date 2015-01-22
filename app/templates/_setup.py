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
        # add your dependencies here
        # remember to use 'package-name>=x.y.z,<x.y+1.0' notation (this way you get bugfixes)
    ],
    extras_require={
        'tests': tests_require,
    },
    entry_points={
        'console_scripts': [
            # add cli scripts here in this form:
            '<%= package.pythonName %>=<%= package.pythonName %>.app:main',
        ],
    },
)

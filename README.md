# generator-flask-app

Yeoman Generator for modern web applications using flask.

## Features

* Flask Application infrastructure;
* [Flask Script](http://flask-script.readthedocs.org/en/latest/) support;
* Templates with Layout pre-configured;
* [Flask Debug Toolbar](https://flask-debugtoolbar.readthedocs.org/en/latest/) support;
* [OAuth Authentication](http://peterhudec.github.io/authomatic/) with Google, Facebook, Github and Twitter support;
* [MongoEngine](http://mongoengine.org/) models with User example;
* [SQLAlchemy](http://www.sqlalchemy.org/) models with User example;
* [Coffeescript](http://coffeescript.org/) and [Compass](http://compass-style.org/)/[scss](http://sass-lang.com/) static support with auto-reload;
* [Bower](http://bower.io/) support;
* Automatic spriting via compass;
* [Alembic](https://alembic.readthedocs.org/en/rel_0_7/) Migrations;
* [Flask Admin](https://flask-admin.readthedocs.org/en/latest/) with automatic panels for mongoengine and sqlalchemy;
* Resque([PyRes](https://github.com/binarydud/pyres)) queueing support;
* [Celery](http://www.celeryproject.org/) queueing support (still not implemented);
* [Travis](https://travis-ci.org/) continuous integration support (still not implemented);
* [Heroku](https://www.heroku.com/) application deployment support (still not implemented).

## Installing

To install flask-app generator, run:

    $ npm install generator-flask-app



## Usage

Creating your app is as easy as:

    $ yo flask-app

Just make sure you are already inside the directory for your new application. Just follow the questions and you'll have an application running in a moment;

## Running My App

Before starting, make sure you have:

* A VirtualEnv (or similar) set-up for the new environment;
* A ruby environment with an interpreter version compatible with Sass/Compass;
* Node.js correctly installed.

To setup all the dependencies for your project, run `make setup`.

After all the dependencies have been installed, you should be able to run your application with `make run`.

If you have selected sqlalchemy support, you probable need to create the database before running with `make db`.

## Running tests

To run your application tests, just run `make test`.

## Application usage

### General commands
* "make list" to list all available targets;
* "make setup" to install all dependencies (do not forget to create a virtualenv first);
* "make test" to test your application (tests in the tests/ directory);

### Redis commands
* "make redis" to get a redis instance up (localhost:4444);
* "make kill-redis" to kill this redis instance (localhost:4444);
* "make redis-test" to get a redis instance up for your unit tests (localhost:4448);
* "make kill-redis-test" to kill the test redis instance (localhost:4448);
* "make tox" to run tests against all supported python versions.

### Running my App
* "make run" to run your application with local.conf (http://local.generator.com:3000/);

**IMPORTANT**: In order for the authentication to work properly, you must run in http://local.generator.com:3000. This will use the sample oauth apps. In order to run your own app you must change the AUTH_PROVIDERS configuration. Refer to local.conf in order to change that.

### Using Flask Admin
* Just access http://local.generator.com:3000/admin/;
* In order to access the admin you must change your local.conf file to change the AUTHORIZED_ADMINS configuration to include the e-mail you are logging with;

### SQL Alchemy commands
* "make migration DESC="<description of the migration>"" to create a new database migration;
* "make auto_migration DESC="<description of the migration>"" to create a new database migration automatically from changes in the model;
* "make db" to create the database and run migrations;
* "make data" to run migrations;
**IMPORTANT**: Do not forget to update configuration (local.conf and other environments) with your MySQL (or other database) connection string;

### PyRes commands
  * "make worker" to run a PyRes Worker;
  * "make resweb" to run a web dashboard for PyRes (available at http://127.0.0.1:3001 - user: admin, pass: 123);

In order to use pyres, you must specify the queues to listen on. This can be done by setting the DEFAULT_QUEUES configuration or by running workers with "-q queue1,queue2";

**IMPORTANT**: Do not forget to update configuration (local.conf and other environments) with your redis connection string and change the resweb user and password;

## Contributing

Please fork, update what you need and pull request.

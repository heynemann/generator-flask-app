'use strict';
var util = require('util');
var path = require('path');
var yeoman = require('yeoman-generator');
var yosay = require('yosay');
var chalk = require('chalk');
var sys = require('sys')
var exec = require('child_process').exec;
var PythonPackageGenerator = require('generator-python-package');

var currentPath = path.basename(process.cwd());

var validateOptions = function(app, pkg) {
  if (pkg.flask.mongoengine && pkg.flask.sqlalchemy) {
    app.log.error("You need to select either MongoEngine or SQLAlchemy. The generator won't work with both.");
    return false;
  }
  return true;
};


var FlaskAppGenerator = yeoman.generators.Base.extend({
  init: function () {
    PythonPackageGenerator.prototype.init.apply(this, arguments);
  },

  askFor: function () {
    var done = this.async();
    var self = this;

    this.log(yosay('Welcome to the flask application generator\nRun this generator in the folder where your app will be created'));

    PythonPackageGenerator.prototype.askFor.apply(this, [true, function(pythonPackage) {
      var prompts = [];

      var orms = [
        { name: "None", value: "none", selected: true },
        { name: "MongoEngine", value: "mongoengine", selected: false },
        { name: "SQL Alchemy", value: "sqlalchemy", selected: false }
      ];

      prompts.push({
        type: 'list',
        name: 'orm',
        message: 'ORM you want to use',
        choices: orms
      });

      var authProviders = [
        { name: "Google", value: "google", checked: false },
        { name: "Facebook", value: "facebook", checked: false },
        { name: "Twitter", value: "twitter", checked: false },
        { name: "Github", value: "github", checked: false }
      ];

      prompts.push({
        type: 'checkbox',
        name: 'authProviders',
        message: 'Services you want to allow your users to authenticate with',
        choices: authProviders
      });

      prompts.push({
        type: 'confirm',
        name: 'admin',
        message: 'Use Flask Admin?',
        default: true
      });

      var queues = [
        { name: "None", value: "none", selected: true },
        { name: "Pyres", value: "pyres", selected: false },
        { name: "Celery", value: "celery", selected: false }
      ];

      prompts.push({
        type: 'list',
        name: 'queue',
        message: 'Queueing service you want to use',
        choices: queues
      });

      self.prompt(prompts, function (props) {
        pythonPackage['flask'] = {
          mongoengine: props.orm == "mongoengine",
          sqlalchemy: props.orm == "sqlalchemy",
          admin: props.admin,
          pyres: props.queue == 'pyres',
          celery: props.queue == 'celery'
        };

        if (pythonPackage.flask.mongoengine) {
          pythonPackage.services.mongodb = true;
        }

        if (pythonPackage.flask.pyres) {
          pythonPackage.services.redis = true;
        }

        var pkgAuthProviders = {
          google: false,
          facebook: false,
          twitter: false,
          github: false
        };

        var useAuth = false;
        for (var i=0; i < props.authProviders.length; i++) {
          useAuth = true;
          pkgAuthProviders[props.authProviders[i]] = true;
        }
        pythonPackage['flask']['authProviders'] = pkgAuthProviders;
        pythonPackage['flask']['useAuth'] = useAuth;

        self.pythonPackage = pythonPackage;
        done();
      });
    }]);

  },

  app: function () {
    var pkg = this.pythonPackage;

    if (!validateOptions(this, pkg)) {
      return;
    }

    pkg.commandName = pkg.pythonName.replace(/[_]/g, '-');

    PythonPackageGenerator.prototype.app.apply(this, [pkg]);

    this.template('_app.py', pkg.pythonName + '/app.py');
    this.template('_manage.py', pkg.pythonName + '/manage.py');

    // app config
    this.mkdir(pkg.pythonName + '/config');
    this.template('_config.py', pkg.pythonName + '/config/__init__.py');
    this.template('_local.conf', pkg.pythonName + '/config/local.conf');

    // mongoengine
    if (pkg.services.mongodb && pkg.flask.mongoengine) {
        this.template('_db.py', pkg.pythonName + '/db.py');
        this.mkdir(pkg.pythonName + "/models");
        this.template('_models.py', pkg.pythonName + '/models/__init__.py');
        this.template('_user.py', pkg.pythonName + '/models/user.py');
    }

    // sqlalchemy
    if (pkg.flask.sqlalchemy) {
        this.template('_db.py', pkg.pythonName + '/db.py');
        this.template('_alembic.ini', pkg.pythonName + '/alembic.ini');
        this.mkdir(pkg.pythonName + "/migrations");
        this.template('_env.py', pkg.pythonName + '/migrations/env.py');
        this.template('_script.py.mako', pkg.pythonName + '/migrations/script.py.mako');
        this.mkdir(pkg.pythonName + "/migrations/versions");
        this.template('_init.py', pkg.pythonName + '/migrations/versions/__init__.py');
        this.template(
          '_300eb7b9958_create_user_table.py',
          pkg.pythonName + '/migrations/versions/300eb7b9958_create_user_table.py'
        );
        this.mkdir(pkg.pythonName + "/models");
        this.template('_models.py', pkg.pythonName + '/models/__init__.py');
        this.template('_user.py', pkg.pythonName + '/models/user.py');
    }

    // Flask Admin
    if (pkg.flask.admin) {
        this.template('_admin.py', pkg.pythonName + '/admin.py');
    }

    // PyRes
    if (pkg.flask.pyres) {
        this.template('_queue.py', pkg.pythonName + '/queue.py');
        this.template('_resweb_ext.py', pkg.pythonName + '/resweb_ext.py');
        this.template('_pyres_worker.py', pkg.pythonName + '/pyres_worker.py');
    }

    // static assets
    this.mkdir(pkg.pythonName + '/static');
    this.mkdir(pkg.pythonName + '/static/coffee');
    this.mkdir(pkg.pythonName + '/static/scss');
    this.mkdir(pkg.pythonName + '/static/fonts');
    this.mkdir(pkg.pythonName + '/static/images');
    this.mkdir(pkg.pythonName + '/static/vendor');
    this.template('_bower_list.js', 'bower_list.js');
    this.template('_init.py', pkg.pythonName + '/static/__init__.py');
    this.template('_assets.py', pkg.pythonName + '/static/assets.py');
    this.template('_base.coffee', pkg.pythonName + '/static/coffee/000-base.coffee');
    this.template('_all.scss', pkg.pythonName + '/static/scss/all.scss');
    this.template('_base.scss', pkg.pythonName + '/static/scss/_base.scss');

    // sprites
    this.mkdir(pkg.pythonName + '/static/images/common');
    this.template('_sprite.scss', pkg.pythonName + '/static/scss/_sprite.scss');
    this.copy('_check.png', pkg.pythonName + '/static/images/common/' + 'check.png');

    // ruby for compass
    this.template('_ruby-gemset', '.ruby-gemset');
    this.template('_ruby-version', '.ruby-version');
    this.template('_Gemfile', 'Gemfile');

    // bower
    this.template('_package.json', 'package.json');
    this.template('_bowerrc', '.bowerrc');
    this.template('_bower.json', 'bower.json');

    // handlers
    this.mkdir(pkg.pythonName + '/handlers');
    this.template('_handlers_init.py', pkg.pythonName + '/handlers/__init__.py');
    this.template('_healthcheck.py', pkg.pythonName + '/handlers/healthcheck.py');
    this.template('_handlers_index.py', pkg.pythonName + '/handlers/index.py');
    this.template('_authomatic_ext.py', pkg.pythonName + '/authomatic_ext.py');

    // templates
    this.mkdir(pkg.pythonName + '/templates');
    this.template('_layout.html', pkg.pythonName + '/templates/layout.html');
    this.template('_index.html', pkg.pythonName + '/templates/index.html');

    if (pkg.flask.useAuth) {
        // authentication
        this.template('_auth.py', pkg.pythonName + '/auth.py');
        this.template('_login.html', pkg.pythonName + '/templates/login.html');
    }

    if (pkg.flask.admin) {
      this.template('_admin_index.html', pkg.pythonName + '/templates/admin_index.html');
    }
  },

  getUsageMessage: function() {
    var pkg = this.pythonPackage;

    PythonPackageGenerator.prototype.getUsageMessage.apply(this);

    this.log('\nRunning my App:');
    this.log('  * "make run" to run your application with local.conf (http://local.generator.com:3000/);');

    if (pkg.flask.useAuth) {
      this.log('  **IMPORTANT**: In order for the authentication to work properly, you must run in http://local.generator.com:3000.');
      this.log('  This will use the sample oauth apps. In order to run your own app you must change the AUTH_PROVIDERS configuration.');
      this.log('  Refer to local.conf in order to change that.');
    }

    if (pkg.flask.admin) {
      this.log('\nUsing Flask Admin:');
      this.log('  * Just access http://local.generator.com:3000/admin/;');
      this.log('  * In order to access the admin you must change your local.conf file to change the AUTHORIZED_ADMINS configuration to include the e-mail you are logging with;');
    }

    if (pkg.flask.sqlalchemy) {
      this.log("\nSQL Alchemy commands:");
      this.log('  * "make migration DESC=\"<description of the migration>\"" to create a new database migration;');
      this.log('  * "make auto_migration DESC=\"<description of the migration>\"" to create a new database migration automatically from changes in the model;');
      this.log('  * "make db" to create the database and run migrations;');
      this.log('  * "make data" to run migrations;');
      this.log('  **IMPORTANT**: Do not forget to update configuration (local.conf and other environments) with your MySQL (or other database) connection string;');
    }

    if (pkg.flask.pyres) {
      this.log("\nPyRes commands:");
      this.log('  * "make worker" to run a PyRes Worker;');
      this.log('  * "make resweb" to run a web dashboard for PyRes (available at http://127.0.0.1:3001 - user: admin, pass: 123);');
      this.log('');
      this.log('  In order to use pyres, you must specify the queues to listen on. This can be done by setting the DEFAULT_QUEUES configuration or by running workers with "-q queue1,queue2";');
      this.log('');
      this.log('  **IMPORTANT**: Do not forget to update configuration (local.conf and other environments) with your redis connection string and change the resweb user and password;');
    }

  },

});

module.exports = FlaskAppGenerator;

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

      if (pythonPackage.services.mongodb) {
        prompts.push({
          type: 'confirm',
          name: 'mongoengine',
          message: 'Use MongoEngine for the models?',
          default: true
        });
      }

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

      self.prompt(prompts, function (props) {
        pythonPackage['flask'] = {
          mongoengine: props.mongoengine
        };

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

    // static assets
    this.mkdir(pkg.pythonName + '/static');
    this.mkdir(pkg.pythonName + '/static/coffee');
    this.mkdir(pkg.pythonName + '/static/scss');
    this.mkdir(pkg.pythonName + '/static/fonts');
    this.mkdir(pkg.pythonName + '/static/images');
    this.mkdir(pkg.pythonName + '/static/vendor');
    this.template('_bower_list.js', pkg.pythonName + '/bower_list.js');
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
    this.template('_bowerrc', pkg.pythonName + '/.bowerrc');
    this.template('_bower.json', pkg.pythonName + '/bower.json');

    // handlers
    this.mkdir(pkg.pythonName + '/handlers');
    this.template('_handlers_init.py', pkg.pythonName + '/handlers/__init__.py');
    this.template('_healthcheck.py', pkg.pythonName + '/handlers/healthcheck.py');
    this.template('_handlers_index.py', pkg.pythonName + '/handlers/index.py');

    // templates
    this.mkdir(pkg.pythonName + '/templates');
    this.template('_layout.html', pkg.pythonName + '/templates/layout.html');
    this.template('_index.html', pkg.pythonName + '/templates/index.html');

    if (pkg.flask.useAuth) {
        // authentication
        this.template('_auth.py', pkg.pythonName + '/auth.py');
        this.template('_login.html', pkg.pythonName + '/templates/login.html');
    }
  },

  getUsageMessage: function() {
    var pkg = this.pkg;
    //this.log("\n\nNow that your project is all created, here is what the make commands can do for you!\n");
    //this.log("General commands:");
    //this.log('* "make list" to list all available targets;');

    //this.log('* "make setup" to install all dependencies (do not forget to create a virtualenv first);');
    //this.log('* "make test" to test your application (tests in the tests/ directory);');

    //if (pkg.services.redis) {
      //this.log("\nRedis commands:");
      //this.log('* "make redis" to get a redis instance up (localhost:4444);');
      //this.log('* "make kill-redis" to kill this redis instance (localhost:4444);');
      //this.log('* "make redis-test" to get a redis instance up for your unit tests (localhost:4448);');
      //this.log('* "make kill-redis-test" to kill the test redis instance (localhost:4448);');
    //}

    //if (pkg.services.mongodb) {
      //this.log("\nMongoDB commands:");
      //this.log('* "make mongo" to get a mongodb instance up (localhost:3333);');
      //this.log('* "make kill-mongo" to kill this mongodb instance (localhost:3333);');
      //this.log('* "make clear-mongo" to clear all data in this mongodb instance (localhost: 3333);');
      //this.log('* "make mongo-test" to get a mongodb instance up for your unit tests (localhost:3334);');
      //this.log('* "make kill-mongo-test" to kill the test mongodb instance (localhost: 3334);');
    //}

    //this.log('* "make tox" to run tests against all supported python versions.');
  },

});

module.exports = FlaskAppGenerator;

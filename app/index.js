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
      var prompts = [{
        type: 'confirm',
        name: 'coffee',
        message: 'Use CoffeeScript?',
        default: true
      }, {
        type: 'confirm',
        name: 'compass',
        message: 'Use Compass?',
        default: true
      }];

      self.prompt(prompts, function (props) {
        pythonPackage['flask'] = {
          coffee: props.coffee,
          compass: props.compass
        };

        self.pythonPackage = pythonPackage;
        done();
      });
    }]);

  },

  app: function () {
    var pkg = this.pythonPackage;

    PythonPackageGenerator.prototype.app.apply(this, [pkg]);

    this.template('_app.py', pkg.pythonName + '/app.py');

    // app config
    this.mkdir(pkg.pythonName + '/config');
    this.template('_config.py', pkg.pythonName + '/config/__init__.py');
    this.template('_local.conf', pkg.pythonName + '/config/local.conf');

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
    this.template('_base.coffee', pkg.pythonName + '/static/coffee/base.coffee');
    this.template('_all.scss', pkg.pythonName + '/static/scss/all.scss');

    // handlers
    this.mkdir(pkg.pythonName + '/handlers');
    this.template('_handlers_init.py', pkg.pythonName + '/handlers/__init__.py');
    this.template('_healthcheck.py', pkg.pythonName + '/handlers/healthcheck.py');
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
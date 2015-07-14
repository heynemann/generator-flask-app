// This file is part of <%= package.name %>.
// <%= package.url %>

// Licensed under the <%= package.license %> license:
// http://www.opensource.org/licenses/<%= package.license%>-license
// Copyright (c) <%= package.created.year %>, <%= package.author.name %> <<%= package.author.email %>>

var bower = require('./node_modules/bower');
var organizeSources = require('./node_modules/organize-bower-sources');
var fs = require('fs');

var writeDependenciesFile = function(file, content) {
    fs.writeFile(file, content, function(err) {
        if (err) {
            console.log('Could not create ' + file + '. ' + err);
        } else {
            console.log('File ' + file + ' created successfully!');
        }
    })
};

bower.commands.list({json: true})
.on('end', function(list){
    var bowerSources = organizeSources( list );
    writeDependenciesFile('./<%= package.pythonName %>/static/bower_dependencies.json', JSON.stringify(bowerSources));
})

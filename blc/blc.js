#!/usr/bin/env node

/* jshint esversion: 6 */

'use strict';

var chalk = require('chalk');
var fs = require('fs');
var markdownLinkCheck = require('markdown-link-check');
var program = require('commander');
var path = require('path');

var statusLabels = {
    alive: chalk.green('GOOD'),
    dead: chalk.red('BAD')
};

const getArgs = () => {
    var opts = {};
    var stream = process.stdin; // read from stdin unless a filename is given
    program
        .version('0.1.0')
        .option('-p, --progress', 'show progress bar')
        .option('-b, --badonly', 'only show failed links')
        .option('-v, --verbose', 'Verbose output')
        .arguments('[filename]').action(filename => {
            opts.baseUrl = 'file://' + path.dirname(path.resolve(filename));
            opts.filename = filename;
            stream = fs.createReadStream(filename);
        })
        .parse(process.argv);
    opts.showProgressBar = (program.progress === true); // force true or undefined to be true or false.
    opts.badOnly = (program.badonly === true);  // Only show failed links
    opts.verbose = (program.verbose === true);
    opts.stream = stream;
    return opts;
};

let opts = getArgs();

const display = (filename, status, link, badOnly) => {
    if(status === 'dead'){
        console.log('%s: %s', chalk.red(filename), link);
    } else if (status === 'alive' && !badOnly) {
        console.log('%s: %s', chalk.green(filename), link);
    }
};

var error = false;
var markdown = ''; // collect the markdown data, then process it
opts.stream.on('data', (chunk) => {
    markdown += chunk.toString();
}).on('end', () =>     
    markdownLinkCheck(markdown, opts, (err, results) =>         
        results.forEach(result => 
            display(opts.filename, result.status, result.link, opts.badOnly))
));



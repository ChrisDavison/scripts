#!/usr/bin/env node

/*jshint esversion: 6 */

'use strict';

var chalk = require('chalk');
var fs = require('fs');
var markdownLinkCheck = require('markdown-link-check');
var program = require('commander');
var request = require('request');
var url = require('url');
var path = require('path');

var statusLabels = {
    alive: chalk.green('GOOD'),
    dead: chalk.red('BAD')
};

var error = false;
var opts = {};
var stream = process.stdin; // read from stdin unless a filename is given
program
    .version('0.1.0')
    .option('-p, --progress', 'show progress bar')
    .option('-b, --badonly', 'only show failed links')
    .option('-v, --verbose', 'Verbose output')
    .arguments('[filenameOrUrl]').action(function (filenameOrUrl) {
        if (/https?:/.test(filenameOrUrl)) {
            stream = request.get(filenameOrUrl);
            try { // extract baseUrl from supplied URL
                var parsed = url.parse(filenameOrUrl);
                delete parsed.search;
                delete parsed.hash;
                if (parsed.pathname.lastIndexOf('/') !== -1) {
                    parsed.pathname = parsed.pathname.substr(0, parsed.pathname.lastIndexOf('/') + 1);
                }
                opts.baseUrl = url.format(parsed);
            } catch (err) { /* ignore error */ }
        } else {
            opts.baseUrl = 'file://' + path.dirname(path.resolve(filenameOrUrl));
            stream = fs.createReadStream(filenameOrUrl);
        }})
    .parse(process.argv);

opts.showProgressBar = (program.progress === true); // force true or undefined to be true or false.
opts.badOnly = (program.badonly === true);  // Only show failed links
opts.verbose = (program.verbose === true);

var markdown = ''; // collect the markdown data, then process it
stream.on('data', (chunk) => {
    markdown += chunk.toString();
}).on('end', () => {
    markdownLinkCheck(markdown, opts, (err, results) => {
        if(opts.verbose && results.length === 0){
            console.log(chalk.yellow('No hyperlinks found!'));
        }
        results.forEach(result => {
            if(result.status === 'dead'){
                console.log('%s: %s', chalk.red('BAD'), result.link);
                error = true;
            } else if (result.status === 'alive' && !opts.badOnly){
                console.log('%s: %s', chalk.green('GG'), result.link);
            }
        });
    });
});

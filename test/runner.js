(function () {
	'use strict';

	var fs = require('fs'),
		gzip = require('../index.js'),
		data,
		out;

	data = fs.readFileSync('test.txt', 'utf8');
	out = new Buffer(gzip.zip(data, 6, fs.lstatSync('test.txt'), 'test.txt'));

	fs.writeFile('out.gz', out);
}());

(function () {
	'use strict';

	var fs = require('fs'),
		gzip = require('../index.js'),
		data,
		out,
		file = 'test.txt',
		options = {
			name: file,
			timestamp: parseInt(fs.lstatSync(file).mtime.getTime() / 1000)
		};

	data = fs.readFileSync(file, 'utf8');
	out = new Buffer(gzip.zip(data, options));

	fs.writeFile('out.gz', out);
}());

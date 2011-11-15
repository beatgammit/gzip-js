Intro
=====

*gzip-js* is a pure JavaScript implementation of the GZIP file format. It uses the DEFLATE algorithm for compressing data.

Since this module is just the GZIP file format, this does not rely on any compression algorithm in particular (or any module), but deflate is used by default.

Please note that since this is a pure JavaScript implementation, it should NOT be used on the server for production code. It also does not comply 100% with the standard.

The main goal of this project is to bring GZIP compression to the browser.

API
===

There is only one function so far, zip:

> function zip(data, level, fileData[, name])
> * data- String of text to compress
> * level- compression level (1-9)
> * fileData- stat object, with at least mtime as a JavaScript Date object
> * name- optional; original name of the file

Sample usage:

    var gzip = require('gzip-js'),
		stat = {
			mtime: new Date()
		};

	// out will be a JavaScript Array of bytes
	var out = gzip.zip('Hello world', 3, stat, 'hello-world.txt');

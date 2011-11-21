(function () {
	'use strict';

	var ender = require('ender'),
		gzip = require('../lib/gzip'),
		toDataURL = require('toDataURL');

	ender.domReady(function () {
		ender('#example button').click(function () {
			var out,
				arr,
				data;

			data = ender('#example textarea').val();
			arr = Array.prototype.map.call(data, function (char) {
				return char.charCodeAt(0);
			});

			out = gzip.zip(arr, {
				name: 'hello-world.txt',
				timestamp: 1321903458,
				level: 6
			});

			toDataURL.toDataURL(out, 'application/x-gzip', true);

			out = out.map(function (byte) {
				return byte.toString(16);
			});

			console.log(out);
		});
	});
}());

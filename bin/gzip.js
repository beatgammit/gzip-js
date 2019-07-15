#!/usr/bin/env node

(function () {
    "use strict";

    var fs = require("fs");
    var optimist = require("optimist");
    var gzip = require("../lib/gzip.js");
    var argv;
    var stat;
    var out;

    argv = optimist.usage("Usage: $0 --file [filename] --output [filename]")
        .alias({
            "f": "file",
            "o": "output"
        })
        .demand(["file"]).argv;

    stat = fs.statSync(argv.file);
    out = gzip.unzip(fs.readFileSync(argv.file), {
        name: argv.file,
        timestamp: parseInt(Math.round(stat.mtime.getTime() / 1000))
    });

    fs.writeFileSync(argv.output || argv.file.replace(/\.gz$/, ""), new Buffer(out));
}());

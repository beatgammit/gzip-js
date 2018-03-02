var path = require('path');
var commonjs = require('rollup-plugin-commonjs');
var nodeResolve = require('rollup-plugin-node-resolve');

module.exports = {
    name: 'gzip',
    input: path.resolve(__dirname, '../lib/gzip.js'),
    output: {
        file: path.resolve(__dirname, '../dist/index.js'),
        format: 'umd'
    },
    plugins: [
        nodeResolve(),
        commonjs()
    ],
    exports: 'named'
};


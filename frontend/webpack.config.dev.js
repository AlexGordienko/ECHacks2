var webpackMerge = require('webpack-merge');
var commonConfig = require('./webpack.config.common.js');

module.exports = webpackMerge(commonConfig, {
    devtool: 'cheap-module-eval-source-map',

    output: {
        path: './public/js/app',
        filename: 'bundle.js',
        publicPath: '/js/app/',
        chunkFilename: '[id].chunk.js'
    }
});
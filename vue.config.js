const path = require('path');
const CopyWebpackPlugin = require('copy-webpack-plugin');

module.exports = {
    pages: {
        index: {
            entry: 'api/src/main.js',
            template: 'api/public/index.html'
        }
    },
    configureWebpack: {
        plugins: [
            new CopyWebpackPlugin([{
                from: path.join(__dirname, 'api/public/'),
                to: path.join(__dirname, 'dist'),
                toType: 'dir',
            }])
        ]
    },
    devServer: {
        proxy: 'http://localhost:8000'
    }
}

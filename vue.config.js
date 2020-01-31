module.exports = {
    pages: {
        index: {
            entry: 'api/src/main.js',
            template: 'api/public/index.html'
        }
    },
    devServer: {
        proxy: 'http://localhost:8000'
    }
}

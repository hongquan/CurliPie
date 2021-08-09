import ky from 'https://unpkg.com/ky'
import 'https://unpkg.com/@highlightjs/cdn-assets@11.2.0/highlight.min.js'
import 'https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.2.0/build/languages/shell.min.js'

window.app = function() {
  return {
    curl: '',
    httpie: '',
    errors: [],
    async onSubmit() {
      const { httpie, errors } = await ky.post('/api/', { json: { curl: this.curl } }).json()
      this.httpie = '$ ' + httpie
      this.errors = errors
    },
    colorizeHttpie() {
      return hljs.highlight(this.httpie, { language: 'shell' }).value
    }
  }
}

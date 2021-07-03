import ky from 'https://unpkg.com/ky';
import 'https://unpkg.com/@highlightjs/cdn-assets@11.0.1/highlight.min.js';

window.app = function() {
  return {
    curl: '',
    httpie: '',
    errors: [],
    async onSubmit() {
      const { httpie } = await ky.post('/api/', { json: { curl: this.curl } }).json();
      this.httpie = httpie;
    },
    colorizeHttpie() {
      return hljs.highlight(this.httpie, { language: 'bash' }).value
    }
  }
}

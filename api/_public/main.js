import ky from './ky.min.js';
import './highlight/highlight.js';

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

import ky from 'https://unpkg.com/ky'
import Alpine from 'https://esm.sh/alpinejs@3.14.0'
import { getHighlighter } from 'https://esm.sh/shiki'


const highlighter = await getHighlighter({
  themes: ['andromeeda'],
  langs: ['shellsession', 'shell'],
})

console.log('highlighter', highlighter)


document.addEventListener('alpine:init', () => {
  Alpine.data('app', () => ({
    curl: '',
    httpie: '',
    errors: [],
    async onSubmit() {
      const { httpie, errors } = await ky.post('/api/', { json: { curl: this.curl } }).json()
      this.httpie = '$ ' + httpie
      this.errors = errors
    },
    colorizeHttpie() {
      if (!this.httpie) return ''
      return highlighter.codeToHtml(this.httpie, { lang: 'shellsession', theme: 'andromeeda' })
    }
  }))
})

window.Alpine = Alpine
Alpine.start()

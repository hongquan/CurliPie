import ky from 'https://unpkg.com/ky'
import Alpine from 'https://esm.sh/alpinejs@3.14.0'
import { createHighlighter } from 'https://esm.sh/shiki'


const highlighter = await createHighlighter({
  themes: ['andromeeda'],
  langs: ['shellsession', 'shell'],
})

document.getElementById('hl-loading')?.remove()
console.log('highlighter', highlighter)


document.addEventListener('alpine:init', () => {
  Alpine.data('app', () => ({
    curl: '',
    httpie: '',
    errors: [],
    loading: false,
    highlighting: false,
    highlightedHtml: '',
    async onSubmit() {
      this.loading = true
      const { httpie, errors } = await ky.post('/api/', { json: { curl: this.curl } }).json()
      this.httpie = '$ ' + httpie
      this.errors = errors
      this.loading = false
      this.highlighting = true
      setTimeout(() => {
        this.highlightedHtml = highlighter.codeToHtml(this.httpie, { lang: 'shellsession', theme: 'andromeeda' })
        this.highlighting = false
      }, 0)
    },
    colorizeHttpie() {
      if (!this.httpie) return ''
      return highlighter.codeToHtml(this.httpie, { lang: 'shellsession', theme: 'andromeeda' })
    },
    copyHttpie() {
      const cmd = (this.httpie || '').replace(/^\$ /, '')
      if (!cmd) return
      navigator.clipboard?.writeText(cmd)
    }
  }))
})

window.Alpine = Alpine
Alpine.start()

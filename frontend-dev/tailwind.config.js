module.exports = {
  purge: [
    '../api/**/*.jinja',
  ],
  darkMode: false, // or 'media' or 'class'
  theme: {
    minHeight: {
      0: '0px',
      24: '6rem',
      full: '100%',
      screen: '100vh',
    },
    extend: {
      typography: (theme) => ({
        DEFAULT: {
          css: {
            p: {
              marginTop: '0.75em',
              marginBottom: '0.75em',
            },
            pre: {
              marginTop: '1em',
              marginBottom: '1em',
              lineHeight: 1.5,
              backgroundColor: theme('colors.gray.900'),
            },
            img: {
              marginTop: '1em',
              marginBottom: '1em',
            },
          }
        }
      })
    },
  },
  variants: {
    extend: {},
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/aspect-ratio'),
    require('@tailwindcss/typography'),
  ],
}

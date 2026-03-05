/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './events/templates/**/*.html',
    './events/static/events/js/**/*.js'
  ],
  theme: {
    extend: {
      colors: {
        primary: '#359EFF',
        'background-dark': '#0f1923',
        'text-main': '#0c101d',
        'text-muted': '#64748b'
      },
      fontFamily: {
        display: ['Space Grotesk', 'sans-serif'],
        body: ['Noto Sans', 'sans-serif']
      },
      boxShadow: {
        card: '0 10px 30px -10px rgba(0, 0, 0, 0.1)'
      }
    }
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/container-queries')
  ]
};

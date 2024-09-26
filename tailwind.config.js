/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './budgetbuddy/authen/templates/**/*.html', 
    './budgetbuddy/account/templates/**/*.html'
  ],
  theme: {
    extend: {
      colors: {
        'custom-green': '#55c172'
      }
    },
  },
  plugins: [],
}


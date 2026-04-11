/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#2ECC71',
        'primary-dark': '#1A8A4A',
        'primary-light': '#E8F5EE',
        navy: '#0D1B2A',
        'navy-light': '#162840',
        'amber-custom': '#F39C12',
        'red-custom': '#E74C3C',
        'gray-soft': '#F8FAF9',
      },
      fontFamily: {
        poppins: ['Poppins', 'sans-serif'],
        inter: ['Inter', 'sans-serif'],
      },
    },
  },
  plugins: [],
}

/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#138808',
        'primary-dark': '#0A5A05',
        'primary-light': '#E8F5E9',
        orange: '#FF9933',
        'orange-dark': '#E67E22',
        'orange-light': '#FFF3E0',
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

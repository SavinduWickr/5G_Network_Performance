/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './src/**/*.{html,js,jsx,ts,tsx}',
    './public/index.html'
  ],
  theme: {
    extend: {
      colors: {
        black: "#000000",
        grape: "#430c28",
        eggplant: "#6d4c74",
        violet: "#997788",
        copper: "#b04a29",
        terracotta: "#8b2d2c",
      },
    },
  },  
  plugins: [],
}


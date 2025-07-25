/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        exBlue: "#003366",
        exTeal: "#0077b6",
        exGray: "#f5f7fa",
      },
    },
  },
  plugins: [],
}

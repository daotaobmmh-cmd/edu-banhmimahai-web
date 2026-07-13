module.exports = {
  content: [
    "./hoinhap/index.src.html",
    "./hoinhap/app.js"
  ],
  theme: {
    extend: {
      colors: {
        primary: "#39B54A",
        error: "#EC1C24",
        secondary: "#00ADEF",
        warning: "#F4CC34",
        background: "#FAF7F2",
        "surface-variant": "#e4e2e2",
        "on-surface-variant": "#3e4a3c"
      },
      borderRadius: {
        xl: "0.75rem",
        "2xl": "1.25rem"
      }
    }
  },
  plugins: []
}

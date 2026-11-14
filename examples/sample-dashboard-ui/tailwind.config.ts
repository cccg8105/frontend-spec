import type { Config } from "tailwindcss";

export default {
  darkMode: ["class"],
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        bgBase: "var(--color-bg-base)",
        surface: "var(--color-surface)",
        primary: "var(--color-primary)",
        textMain: "var(--color-text-main)",
        border: "var(--color-border)",
        danger: "var(--color-danger)",
      },
    },
  },
  plugins: [],
} satisfies Config;

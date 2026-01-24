/** @type {import('tailwindcss').Config} */
export default {
    content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
    theme: {
        extend: {
            colors: {
                primary: '#4A6C6F', // Deep Sage
                secondary: '#F5F0E6', // Sand Beige
                accent: '#C88D7D', // Terracotta
                'text-main': '#2C3E50', // Charcoal
            },
            fontFamily: {
                serif: ['"Playfair Display"', 'serif'],
                sans: ['"Lato"', 'sans-serif'],
            },
        },
    },
    plugins: [],
}

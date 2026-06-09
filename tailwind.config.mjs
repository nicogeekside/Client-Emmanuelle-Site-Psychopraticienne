/** @type {import('tailwindcss').Config} */
export default {
    content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
    theme: {
        extend: {
            colors: {
                // 🌿 LA TOUCHE "SAUGE" DEMANDÉE PAR EMMA
                primary: '#5C7A62',         // Sauge Clair (plus aéré et lumineux)
                'primary-light': '#829A86', // Sauge Doux (Idéal pour les icônes, traits ou fonds secondaires)
                
                // 🎨 L'IDENTITÉ VISUELLE DU LOGO / CARTE DE VISITE
                secondary: '#EBDCCC',       // Beige Sable du logo (Pour les cartes ou sections douces)
                'text-muted': '#85827D',    // Gris Taupe du texte "Psychopraticienne" du logo
                
                // 🎯 LES FONDS ET L'ACTION
                background: '#FAF7F3',      // Blanc cassé très léger pour le fond global
                accent: '#C88D7D',          // Terracotta (Pour le bouton Prendre RDV)
                'text-main': '#2C3E50',     // Gris Anthracite (Pour les longs paragraphes)
            },
            fontFamily: {
                serif: ['"Playfair Display"', 'serif'],
                sans: ['"Lato"', 'sans-serif'],
            },
        },
    },
    plugins: [],
}

// Forcer la purge du cache Vercel

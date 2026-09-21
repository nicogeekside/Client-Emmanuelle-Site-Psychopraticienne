/** @type {import('tailwindcss').Config} */
export default {
    content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
    theme: {
        extend: {
            colors: {
                // 🌿 LA TOUCHE "SAUGE" DEMANDÉE PAR EMMA
                primary: '#5C7A62',         // Sauge Clair (plus aéré et lumineux)
                'primary-light': '#829A86', // Sauge Doux (Idéal pour les icônes, traits ou fonds secondaires)
                'primary-dark': '#3D5A4E',  // Sauge Profond — pour le pied de page et le texte sauge sur fond clair (7,1:1 sur crème)
                
                // 🎨 L'IDENTITÉ VISUELLE DU LOGO / CARTE DE VISITE
                secondary: '#EBDCCC',       // Beige Sable du logo (Pour les cartes ou sections douces)
                'text-muted': '#85827D',    // Gris Taupe du texte "Psychopraticienne" du logo
                
                // 🎯 LES FONDS ET L'ACTION
                background: '#FAF7F3',      // Blanc cassé très léger pour le fond global
                // Terracotta de la carte de visite. Il ne porte PAS de texte blanc
                // (2,78:1) : réservé aux aplats, filets et pastilles décoratives.
                accent: '#C88D7D',
                'accent-dark': '#9A5849',   // Terracotta Profond — fond des boutons et texte terracotta sur fond clair (5,4:1 sur blanc)
                'accent-light': '#E8C4B8',  // Terracotta Clair — texte terracotta sur le sauge profond du pied de page (4,7:1)
                'text-main': '#2C3E50',     // Gris Anthracite (Pour les longs paragraphes)
            },
            fontFamily: {
                serif: ['"Playfair Display"', 'serif'],
                sans: ['"Lato"', 'sans-serif'],
            },
        },
    },
    plugins: [
        require('@tailwindcss/typography'),
    ],
}

// Forcer la purge du cache Vercel

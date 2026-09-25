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
                // Terracotta de titraille, au plus près de la carte de visite.
                // USAGE UNIQUE : grand texte (>=24px, ou >=18,66px gras) sur fond
                // clair. 3,10:1 sur le beige — conforme au seuil du grand texte.
                // Il ne peut PAS porter de texte blanc (4,17) ni servir en texte
                // courant (4,17 sur blanc) : aucune couleur de texte ne passe dessus.
                'accent-display': '#A07164',
                'accent-dark': '#9A5849',   // Terracotta Profond — fond des boutons et texte courant terracotta (5,4:1 sur blanc)
                'accent-light': '#E8C4B8',  // Terracotta Clair — texte terracotta sur le sauge profond du pied de page (4,7:1)
                'text-main': '#2C3E50',     // Gris Anthracite (Pour les longs paragraphes)
            },
            // ÉCHELLE D'OPACITÉ — 5 paliers : /10 /30 /50 /70 /90
            // Elle s'applique aux FONDS, BORDURES et remplissages décoratifs.
            // Les couleurs de TEXTE en sont exemptées : l'opacité y est un
            // levier de contraste, pas un choix de style. Les arrondir vers le
            // bas fait passer du texte sous le seuil AA — c'est arrivé une fois.
            fontFamily: {
                serif: ['"Playfair Display"', 'serif'],
                sans: ['"Lato"', 'sans-serif'],
            },
            // LE TEXTE LONG — blog, charte deontologique, page post-partum.
            // Sans cette cle, @tailwindcss/typography habille TOUT le contenu
            // .prose dans son gris par defaut (corps #374151, gras #111827,
            // puces #d1d5db, filets #e5e7eb) : une palette etrangere de plus,
            // invisible dans la source puisque c'est le plugin qui la genere.
            // C'est la surface la plus lue du site : les 20 articles.
            typography: ({ theme }) => ({
                DEFAULT: {
                    css: {
                        '--tw-prose-body': theme('colors.text-main'),
                        '--tw-prose-headings': theme('colors.primary-dark'),
                        '--tw-prose-lead': theme('colors.text-main'),
                        '--tw-prose-links': theme('colors.accent-dark'),
                        '--tw-prose-bold': theme('colors.text-main'),
                        // Puces et numeros : terracotta profond, 5,4:1 sur blanc.
                        '--tw-prose-counters': theme('colors.accent-dark'),
                        '--tw-prose-bullets': theme('colors.accent-dark'),
                        '--tw-prose-hr': theme('colors.secondary'),
                        '--tw-prose-quotes': theme('colors.primary-dark'),
                        '--tw-prose-quote-borders': theme('colors.accent'),
                        '--tw-prose-captions': theme('colors.text-main'),
                        '--tw-prose-kbd': theme('colors.text-main'),
                        '--tw-prose-code': theme('colors.text-main'),
                        '--tw-prose-pre-code': theme('colors.secondary'),
                        '--tw-prose-pre-bg': theme('colors.primary-dark'),
                        '--tw-prose-th-borders': theme('colors.secondary'),
                        '--tw-prose-td-borders': theme('colors.secondary'),
                    },
                },
            }),
        },
    },
    plugins: [
        require('@tailwindcss/typography'),
    ],
}


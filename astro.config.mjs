import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';
import sitemap from '@astrojs/sitemap';

// https://astro.build/config
export default defineConfig({
  site: 'https://www.emma-psychopraticienne.fr', // Remplace par le vrai domaine final si besoin
  integrations: [
    tailwind({ applyBaseStyles: false }),
    sitemap()
  ],
});

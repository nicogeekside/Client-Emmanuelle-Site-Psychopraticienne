import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';
import sitemap from '@astrojs/sitemap';
import fs from 'node:fs';
import optimiserImagesUploadees from './scripts/optimiser-images-uploadees.mjs';
import rehypeWebpUploads from './scripts/rehype-webp-uploads.mjs';

// Le serveur de production force le domaine sans www (www -> 301 -> non-www).
// Tout doit s'aligner dessus : sitemap, canonical, og:url, robots.txt.
const SITE = 'https://emma-psychopraticienne.fr';

const DOSSIER_BLOG = new URL('./src/content/blog/', import.meta.url);

// slug -> date de publication, pour renseigner le <lastmod> des articles.
// On lit le frontmatter directement : getCollection() n'est pas disponible ici.
function datesDesArticles() {
  const dates = new Map();
  for (const fichier of fs.readdirSync(DOSSIER_BLOG)) {
    if (!fichier.endsWith('.md')) continue;
    const contenu = fs.readFileSync(new URL(fichier, DOSSIER_BLOG), 'utf8');
    const slug = contenu.match(/^slug:\s*["']?(.+?)["']?\s*$/m)?.[1]?.trim()
      ?? fichier.replace(/\.md$/, '');
    const publie = contenu.match(/^pubDate:\s*["']?(.+?)["']?\s*$/m)?.[1]?.trim();
    if (publie && !Number.isNaN(Date.parse(publie))) {
      dates.set(slug, new Date(publie));
    }
  }
  return dates;
}

const datesArticles = datesDesArticles();

export default defineConfig({
  site: SITE,
  markdown: {
    // Bascule les images du corps des articles sur un jumeau WebP —
    // voir scripts/rehype-webp-uploads.mjs.
    rehypePlugins: [rehypeWebpUploads],
  },
  integrations: [
    tailwind({ applyBaseStyles: false }),
    // Compresse les uploads Decap à chaque build — voir le fichier pour
    // le diagnostic complet et pourquoi rien ne touche à public/.
    optimiserImagesUploadees(),
    sitemap({
      // /merci/ est une confirmation, /admin/ est le back-office : ni l'une ni
      // l'autre n'a vocation a etre indexee ou proposee dans Google.
      filter: (page) => !page.includes('/merci/') && !page.includes('/admin/'),
      serialize(entree) {
        const article = entree.url.match(/\/blog\/([^/]+)\/$/);
        if (article) {
          const date = datesArticles.get(decodeURIComponent(article[1]));
          if (date) entree.lastmod = date.toISOString();
        }
        return entree;
      },
    }),
  ],
});

// Bascule les images du CORPS des articles de blog (les ![]() du markdown,
// donc hors couverture et vignette — elles passent par UploadImage.astro)
// sur un <picture> avec repli WebP. Même logique que UploadImage.astro,
// mais appliquée par le pipeline markdown d'Astro (remark/rehype) puisque
// Decap n'écrit que du Markdown brut : on ne peut pas y glisser un composant.
//
// Câblé dans astro.config.mjs (markdown.rehypePlugins). S'applique à
// chaque build — rien à faire dans les articles existants ni futurs.
import { visit } from 'unist-util-visit';

const EXTENSION_IMAGE_UPLOADEE = /^\/images\/uploads\/.+\.(png|jpe?g)$/i;

export default function rehypeWebpUploads() {
  return (arbre) => {
    visit(arbre, 'element', (noeud, index, parent) => {
      if (noeud.tagName !== 'img' || parent == null || index == null) return;
      const src = noeud.properties?.src;
      if (typeof src !== 'string' || !EXTENSION_IMAGE_UPLOADEE.test(src)) return;

      // Deja en .webp : rien a doubler.
      if (/\.webp$/i.test(src)) return;

      const webp = src.replace(/\.(png|jpe?g)$/i, '.webp');
      parent.children[index] = {
        type: 'element',
        tagName: 'picture',
        properties: {},
        children: [
          { type: 'element', tagName: 'source', properties: { srcset: webp, type: 'image/webp' }, children: [] },
          noeud,
        ],
      };
    });
  };
}

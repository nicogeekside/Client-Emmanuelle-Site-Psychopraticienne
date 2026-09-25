// Piege n°1 du projet : une classe Tailwind ecrite dans la source mais absente
// du CSS livre ne produit rien, et rien ne le signale. C'est arrive quatre fois
// (bg-secondary/97, from-primary/8, text-accent-dark, prose-primary).
//
// Ce script croise chaque classe du HTML livre avec les selecteurs du CSS livre.
// Usage :  npm run build && node scripts/classes-inertes.mjs
import fs from 'node:fs';
import path from 'node:path';

const parcourir = (d) => fs.readdirSync(d, { withFileTypes: true }).flatMap((e) => {
  const p = path.join(d, e.name);
  return e.isDirectory() ? parcourir(p) : [p];
});

if (!fs.existsSync('dist')) {
  console.error('Pas de dossier dist/ — lancer `npm run build` d\'abord.');
  process.exit(1);
}

const fichiersHtml = parcourir('dist').filter((f) => f.endsWith('.html'));

// Le CSS livre vit a deux endroits : les feuilles externes, et les blocs
// <style> qu'Astro inline dans la page. Oublier les seconds fait passer pour
// inertes des classes qui fonctionnent (marquee, morph-blob, mask-gradient...).
const css = [
  ...parcourir('dist/_astro').filter((f) => f.endsWith('.css')).map((f) => fs.readFileSync(f, 'utf8')),
  ...fichiersHtml.flatMap((f) => [...fs.readFileSync(f, 'utf8').matchAll(/<style[^>]*>([\s\S]*?)<\/style>/g)].map((m) => m[1])),
].join('\n');

// Tailwind echappe . / : [ ] % # ! , dans ses selecteurs.
const selecteur = (c) => '.' + c.replace(/[.:/[\]%#!,()]/g, (m) => '\\' + m);

// Classes sans regle CSS propre : produites par une lib, un plugin ou le JS.
const ignorees = /^(aos-|swiper|group|peer$|prose$|prose-|mobile-link|calendly)/;

const vues = new Map();
for (const f of fichiersHtml) {
  const src = fs.readFileSync(f, 'utf8');
  for (const m of src.matchAll(/class="([^"]*)"/g)) {
    for (const c of m[1].split(/\s+/).filter(Boolean)) {
      if (!ignorees.test(c) && !vues.has(c)) vues.set(c, path.relative('dist', f));
    }
  }
}

const inertes = [...vues].filter(([c]) => !css.includes(selecteur(c)));
console.log(`${vues.size} classes distinctes dans le build`);
if (!inertes.length) {
  console.log('0 classe inerte');
} else {
  console.log(`${inertes.length} CLASSE(S) INERTE(S) :`);
  for (const [c, f] of inertes) console.log('  ', c, '<-', f);
  process.exitCode = 1;
}

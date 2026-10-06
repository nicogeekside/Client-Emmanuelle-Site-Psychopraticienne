# Site Emmanuelle — psychopraticienne à Saint-Nazaire

Site vitrine d'Emmanuelle Demeulemeester (cliente, tante de Nicolas). Objectif unique : réservation de la séance découverte de 45 min offerte (Calendly).

## Stack
- Astro 5 · Tailwind 3 · Decap CMS (`/admin/`) · Netlify (Forms + déploiement depuis GitHub)

## Commandes
- Dev : `/dev` → `npm run dev`, port 4321
- Preview du build : `npm run build && npm run preview` → port 4322

## Règles du projet
- **Jamais de push sur `main`** sans « go sur main » explicite. Branche par lot : `fix/lot-N-sujet` → `dev`.
- **Emmanuelle publie ses articles seule** via Decap, qui commite **directement sur `main`** → avant de fusionner dev dans main, ramener main dans dev.
- Ne jamais modifier les 20 articles de `src/content/blog/` : c'est son contenu.
- Formulaire = **Netlify Forms** (jamais Formspree). Ne pas renommer le champ `name="email"` (sert au Reply-To).
- Domaine canonique **sans www** (`emma-psychopraticienne.fr`), redirection 301 gérée côté Netlify, pas dans le code.
- Ne jamais inventer un fait (tarif, diplôme, date) : le demander.
- Arbitrages d'apparence demandés avant chaque lot, puis un agent de vérification (Sonnet) avant la fusion dans dev.

## Où trouver quoi
- `PRODUCT.md` : cible, positionnement, infos pratiques (horaires, tarifs)
- `src/data/config.js` : données du site · `src/components/Icon.astro` : icônes lucide
- `docs/ETAT-DES-TRAVAUX.md` : historique détaillé des lots · `docs/BACKLOG-QUALITE.md` : constats

## État
Voir `PROGRESS.md` (court). Le détail est dans `docs/ETAT-DES-TRAVAUX.md`.

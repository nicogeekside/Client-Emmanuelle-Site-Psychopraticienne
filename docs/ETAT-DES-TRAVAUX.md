# État des travaux — à lire en premier

> **Dernière mise à jour : 21 septembre 2026 — lots 1 à 4 fusionnés sur `dev`. Prochaine étape : lot 5, harmoniser les couleurs.**
> Ce fichier est le point d'entrée pour reprendre le travail. Le détail des
> constats est dans [BACKLOG-QUALITE.md](BACKLOG-QUALITE.md).

## Le projet en deux lignes

Site vitrine Astro 5 + Tailwind 3 d'Emmanuelle Demeulemeester, psychopraticienne
à Saint-Nazaire. 17 pages, 20 articles de blog édités par elle via Decap CMS.
Nicolas (son neveu) est le prestataire. Objectif de ce chantier : que le site
cesse de ressembler à « un site fait à la va-vite par une IA ».

## Règles de travail — non négociables

- **On ne pousse JAMAIS sur `main`.** Au maximum sur `dev`.
- **Une branche par lot**, nom explicite : `fix/lot-N-sujet`.
- **Un agent de vérification après chaque lot**, avant la fusion sur `dev`.
  Il a trouvé des régressions introduites par moi-même sur les trois lots.
- **Arbitrages demandés avant chaque lot**, pas de décision unilatérale sur
  l'apparence.
- Le serveur de preview du build de production tourne sur `http://localhost:4322/`
  (`npm run build` pour le rafraîchir). Le dev est sur `:4321`.

## Où on en est

| Lot | Sujet | État | Branche |
|---|---|---|---|
| 1 | Retirer ce qui est faux | ✅ fusionné sur `dev` | `fix/lot-1-credibilite-factuelle` |
| 2 | Réparer ce qui est cassé | ✅ fusionné sur `dev` | `fix/lot-2-bugs-et-accessibilite` |
| 3 | Rendre le texte lisible | ✅ fusionné sur `dev` | `fix/lot-3-lisibilite-et-contrastes` |
| 4 | Remplacer les emoji par des icônes | ✅ fusionné sur `dev` | `fix/lot-4-icones` |
| **5** | **Harmoniser les couleurs** | **⬜ prochaine étape** | — |
| 6 | Alléger les pages | ⬜ à faire | — |
| 7 | Parcours de conversion | ⬜ **attend l'accord d'Emmanuelle** | — |

## Lot 4 — état précis

**Fait, relu, corrigé.**

- `lucide-static` installé ; `src/components/Icon.astro` lit le SVG au build,
  n'inline que la géométrie, trait 1,5, nom validé, glyphes mémoïsés.
  `aria-hidden` par défaut ; prop `label` disponible mais **pas encore utilisée**.
- **Les 99 emoji sont remplacés.** Contrôlé : 0 dans la source, 0 dans le build,
  0 attribut `class` en double, 0 classe inerte, 0 article de blog modifié.
- Les 20 articles de blog sont intacts — c'est le contenu d'Emmanuelle.

**La relecture avait conclu « échoué ». Onze défauts corrigés :**

| | Défaut | Correction |
|---|---|---|
| 🔴 | Deux attributs `class` sur le même `<a>` du pied de page, sur les 37 pages | Fusionné, icône rétablie |
| 🔴 | Un emoji restait en production (le sablier ⏳) | `hourglass` |
| 🔴 | `credit-card` au-dessus de « virement, espèces ou chèque » | `euro` |
| 🔴 | `calendar-check` = créneau réservé, pour « Disponibilités » | `calendar-clock` |
| 🔴 | `globe` pour « Partout en France » | `map` |
| 🔴 | 10 icônes décentrées dans des blocs centrés | `mx-auto` |
| 🔴 | Les 4 cartes rendaient en 38-44 px au lieu de 44 | `shrink-0` |
| 🔴 | Pastilles rondes disparues (conteneur absorbé dans l'icône) | Enveloppe rétablie |
| ⚠️ | `users` pour deux notions de la même liste | `door-open` / `users` |
| ⚠️ | Puces ✓ en 24 px face à du texte de 14 px | 18 px, `shrink-0` |
| ⚠️ | Flèche de lien supprimée sans remplacement | `arrow-right` |

**Contrôle visuel : fait par Nicolas, validé.** Fusionné sur `dev`.

**Dettes transmises :**
- Les icônes des 4 cartes reprennent la couleur d'accent de leur carte, donc les
  palettes étrangères d'origine. **Se corrigera au lot 5.**
- Le HTML s'alourdit de 4 à 20 % selon les pages (+11 à 14 % en gzip). 66 % de ce
  surcoût est le préambule `<svg>` répété. **Dette transmise au lot 6.**
- `'` La prop `label` de `Icon.astro` n'est appelée nulle part : soit l'exercer,
  soit la retirer.

## Lot 5 — ce qui l'attend

Harmoniser les couleurs. Le détail est dans le bloc C2 du backlog.

- **76 classes de 8 familles Tailwind étrangères** à la charte : gray (33),
  emerald (15), blue (15), rose (7), purple/indigo/orange/fuchsia (6).
- **`src/data/config.js:55-93`** — les 4 formats portent chacun un dégradé hors
  charte. C'est le bloc « Un format adapté à votre vie » de l'accueil, soit
  l'argument de positionnement n°1, rendu en quatre couleurs absentes du logo.
  **Les icônes des cartes reprennent désormais ces couleurs** : les corriger ici
  corrige aussi les icônes.
- Ces couleurs sont recopiées à la main dans `index.astro`, `therapie-en-ligne-visio`,
  `therapie-en-marchant` et `therapie-cabinet`.
- `config.js:91` annonce du `purple` pour l'Espace Post-Partum, mais la page cible
  n'utilise jamais de violet.
- Rythme des fonds à unifier sur les 4 pages de format (bloc F1/F2 du backlog).
- Résidus : `theme-color` hors charte, `netlify-identity` chargé hors `/admin`,
  SIRET factice dans une ternaire, commentaire « cache Vercel », import mort.
- Détecteur : 4 `border-l-4` et 1 `animate-bounce` — ce sont des choix de style,
  c'est ici qu'ils se traitent.

## Décisions déjà arbitrées — ne pas reposer la question

| Sujet | Décision |
|---|---|
| Carrousel d'avis | Gardé, mais rendu contrôlable (bouton pause) |
| Collision d'URL EMDR | La page principale garde le sujet ; l'article renommé `/blog/comprendre-la-therapie-emdr-saint-nazaire/` + 301 |
| Animations AOS | `prefers-reduced-motion` respecté, animation retirée du contenu de lecture |
| Terracotta du bouton | `accent-dark #9A5849` |
| Terracotta des grands titres | `accent-display #A07164` |
| Pied de page | Fond `primary-dark`, titres blancs, **filet terracotta `#C88D7D`** |
| Largeur de lecture | ~85 caractères |
| Opacités | 5 paliers `/10 /30 /50 /70 /90` |
| Titre section avis | « Ce qu'on en dit » (épicène) |
| Reformulations déontologiques | Les plus risquées seulement, **validées une par une avec Nicolas** |

## Pièges de ce projet — vérifiés à chaque fois

1. **Classes Tailwind qui ne compilent pas.** Trois occurrences déjà :
   `bg-secondary/97`, `from-primary/8`, `text-accent-dark` avant que le token
   n'existe. **Après chaque lot**, croiser les classes du source avec
   `dist/_astro/*.css`. Le script est dans l'historique des commits.
2. **L'unité `ch` n'est pas un caractère.** Elle vaut la largeur du « 0 », soit
   **1,35×** la largeur moyenne en Lato. `68ch` ≈ 91 caractères, pas 68.
3. **Les opacités de texte ne s'arrondissent pas.** L'échelle à 5 paliers vaut
   pour les fonds, bordures et décorations. Sur du texte, l'opacité est un levier
   de contraste : l'arrondir vers le bas fait passer sous le seuil AA. C'est écrit
   dans `tailwind.config.mjs`.
4. **`accent-display` ne tient que le seuil du grand texte (3,10).** Il ne peut
   recevoir **aucune opacité** et ne doit jamais servir en texte courant.
5. **Les CTA écrits à la main** hors de `Button.astro` échappent aux corrections
   globales. Il y en avait trois.
6. **Les contrôles automatiques ne voient pas les défauts visuels.** Sur le lot 4,
   dix icônes décentrées, des cartes comprimées et des pastilles disparues sont
   passées au travers de vérifications toutes vertes. Un lot qui touche à
   l'apparence exige un regard, pas seulement un `grep`.
7. **Ne jamais écrire « vérifié » sans l'avoir fait.** Ce fichier a affirmé
   « 0 emoji dans le build » et « les cartes rendent en 44 px » alors que les deux
   étaient faux.

## En attente d'Emmanuelle — bloquant

Document qui lui est destiné : `docs/Chantier-1-site-Emmanuelle.pdf`

1. **Assurance RC Pro** — nom + n° de contrat. Non obligatoire à afficher ;
   à défaut, la rubrique reste retirée.
2. **Médiateur de la consommation** — obligation légale depuis 2016, amende
   de 3 000 €. La question est « a-t-elle adhéré ? », pas « quoi afficher ».
3. Formulation « formation en psychothérapie » — **correcte**, vérifié ;
   simple choix éditorial.
4. Tarif du premier rendez-vous d'1 h — absent du site.
5. Dates du groupe post-partum.
6. Les deux nouveaux avis Google (Barder Jacques, Marion Binet) — texte exact,
   nombre d'étoiles, approche concernée.

## Vérifications à lancer après chaque lot

```bash
npm run build                      # 37 pages attendues, 0 avertissement
node /Users/nicolasshahata/.claude/skills/impeccable/scripts/detect.mjs \
  --json src/pages src/components src/layouts
```
Plus le croisement des classes inertes, et un agent de relecture critique.

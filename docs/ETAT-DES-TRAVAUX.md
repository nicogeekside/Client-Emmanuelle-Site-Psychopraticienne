# État des travaux — à lire en premier

> **Dernière mise à jour : 21 septembre 2026, lot 4 terminé, en attente de relecture.**
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
| **4** | **Remplacer les emoji par des icônes** | **✅ fait, agent de relecture à lancer** | `fix/lot-4-icones` |
| 5 | Harmoniser les couleurs | ⬜ à faire | — |
| 6 | Alléger les pages | ⬜ à faire | — |
| 7 | Parcours de conversion | ⬜ **attend l'accord d'Emmanuelle** | — |

## Lot 4 — état précis

**Fait :**
- `lucide-static` installé (2 112 icônes)
- `src/components/Icon.astro` : lit le SVG au build et n'en inline que la
  géométrie, trait 1,5, `aria-hidden` par défaut, prop `label` pour les icônes
  porteuses d'information
- **Les 99 emoji sont remplacés.** Vérifié : 0 emoji dans le build, 0 nom
  d'icône fuité en texte, 83 SVG sur l'accueil
- Les 4 cartes de format rendent en 44 px, trait 1,25

**Reste à faire :** lancer l'agent de relecture critique, puis fusionner sur `dev`.

**Décisions prises avec Nicolas :**
- Jeu d'icônes : **Lucide, inliné au build**
- Les 4 cartes de format de l'accueil : **icônes Lucide, même taille**
- Les emoji des 20 articles de blog (contenu d'Emmanuelle) : **ne pas y toucher**

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

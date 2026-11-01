# Blog : statistiques des 20 articles (source : `audit/analyses/blog-stats.csv`, lecture seule)
**Tableau, trié par nombre de mots**

| Article (slug) | Mots | H2/H3 | H1 dans le corps | Liens internes | Saint-Nazaire |
|---|---|---|---|---|---|
| comprendre-la-therapie-emdr-saint-nazaire | 159 | 2/1 | 0 | 0 | non |
| douleur-chronique-et-therapie-psychocorporelle | 247 | 0/0 | 0 | 0 | non |
| la-therapie-psychocorporelle-saint-nazaire | 248 | 0/0 | 0 | 0 | oui |
| stress-et-cancer-a-saint-nazaire | 261 | 4/1 | 0 | 0 | non |
| la-psychologie-energetique | 268 | 6/1 | 1 | 0 | non |
| psychotraumatismes-saint-nazaire | 277 | 1/0 | 0 | 0 | non |
| les-therapies-breves | 291 | 2/10 | 0 | 0 | oui |
| la-therapie-en-marchant-saint-nazaire | 319 | 3/0 | 0 | 0 | oui |
| la-liberation-de-la-parole-saint-nazaire | 337 | 5/3 | 0 | 0 | oui |
| espace-de-parole-post-partum-saint-nazaire | 407 | 0/0 | 0 | 0 | oui |
| les-croyances-limitantes | 438 | 0/0 | 0 | 0 | non |
| le-therapeute-energetique | 453 | 4/6 | 1 | 3 | oui |
| la-therapie-ifs | 506 | 0/0 | 1 | 0 | non |
| comprendre-le-lien-d-attachement-et-ses-blessures-durables | 546 | 0/0 | 0 | 0 | non |
| cancer-et-therapie-psychocorporelle | 656 | 5/2 | 1 | 2 | oui |
| la-sante-mentale-a-saint-nazaire | 679 | 7/0 | 0 | 0 | non |
| la-premenopause-entre-40-et-50-ans | 883 | 7/6 | 0 | 0 | non |
| le-post-partum | 985 | 7/0 | 0 | 0 | oui |
| post-partum-saint-nazaire | 1196 | 9/2 | 1 | 0 | oui |
| le-controle-coercitif | 2015 | 2/2 | 16 | 0 | non |

**Articles trop courts (moins de 600 mots) : 14 sur 20.** Médiane : 438 mots. Seuls 6 articles dépassent 600. **Sans lien vers une page de séance ni vers la prise de RDV : 20 sur 20 (dans le corps).** Aucun lien vers `/seance-…`, `/therapie-…` ou Calendly. Calendly n'existe que sur `/prendre-rendez-vous-saint-nazaire`. Le gabarit `src/pages/blog/[slug].astro` (l. 60-67) ajoute en bas un bouton « Prendre un premier rendez-vous » : c'est le seul lien RDV.

**Doublons possibles (titres proches)**
- Post-partum : « Espace de parole post-partum… » (juin) et « Post Partum… espace de parole et de soutien » (sept.) traitent le même sujet (ratio 0,50). « Post-partum : la traversée… » s'y ajoute.
- Cancer : « Stress et cancer… » et « Témoignage… en cancérologie » (ratio 0,49).
- Psychologie énergétique : « C'est quoi la psychologie énergétique ? » rejoint « Soulager la douleur chronique… » (0,52) et « Le thérapeute énergétique » (0,51).

**Slugs** : aucun problème dans le champ `slug` (ni accent, ni apostrophe, ni date, ni plus de 60 caractères). Les noms de fichiers en ont, mais ils n'entrent pas dans l'URL.

**Constats principaux**
1. Les articles ne poussent pas vers la séance : 0 lien dans le texte, seul le bouton du gabarit mène à la prise de RDV.
2. Liens anciens : « Le thérapeute énergétique » (3 liens) et « Témoignage… cancérologie » (2) pointent vers `/emdr-saint-nazaire/`, `/eft-saint-nazaire/` ou une URL cassée. Ces chemins n'existent pas dans `src/pages` et ne sont pas dans `public/_redirects` (à vérifier en ligne).
3. Structure : 21 titres H1 dans le corps, dont 16 dans « Contrôle coercitif » (plusieurs H1 par page). 11 articles ne citent jamais Saint-Nazaire, et 14 sont sous 600 mots.

# Analyse Google Search Console (GSC) — site d'Emmanuelle

Produit le 1er nov. 2026 à partir des exports GSC (16 mois : 1er juil. 2025 → 30 oct. 2026) et des comptes Calendly anonymes. Script : `audit/analyses/scripts/gsc.py` (relançable : `python3 -I audit/analyses/scripts/gsc.py`).
Les chiffres GSC = clics et impressions **venus de Google seulement**. Ce n'est pas le nombre de visites du site.

## 1. Avant / après la refonte

Périodes de `audit/PLAN-AUDIT.md` §3 (bascule du 8 juin = hypothèse, à confirmer par Netlify Deploys). Source : `audit/data/gsc/16-mois/Graphique.csv`. Les 2 périodes font 142 jours chacune.

| Période | Clics | Impressions | CTR | Position moy. (pondérée) |
|---|---|---|---|---|
| AVANT (17/01 → 07/06/2026) | 133 | 2 550 | 5,2 % | 15,6 |
| APRÈS (08/06 → 27/10/2026) | 202 | 3 364 | 6,0 % | 13,3 |
| Écart | +69 (+52 %) | +814 (+32 %) | +0,8 pt | 2,3 places gagnées |

Contrôle saisonnier (même fenêtre 1er juil. → 27 oct.) :

| | Clics | Impressions | CTR | Position |
|---|---|---|---|---|
| 2025 | 45 | 483 | 9,3 % | 16,5 |
| 2026 | 184 | 2 781 | 6,6 % | 14,0 |

Lecture : l'APRÈS est meilleur que l'AVANT, et l'été-automne 2026 est très au-dessus de 2025. Mais la base 2025 est minuscule (483 impressions en 4 mois), donc « x4 » est trompeur. On ne peut pas dire que la refonte *cause* la hausse : le site gagne peut-être simplement en ancienneté et en contenu (20 articles publiés juin-sept.). Tendance, pas preuve.

Moyenne par semaine pleine (20 semaines chacune, `gsc-par-semaine.csv`) : AVANT 6,7 clics/semaine ; APRÈS 10,0 clics/semaine. Aucune semaine à 0 clic dans ces deux périodes.

**Mois** (fichier `audit/analyses/gsc-par-mois.csv`, source Graphique.csv) :

| Mois | Clics | Impr. | | Mois | Clics | Impr. |
|---|---|---|---|---|---|---|
| 2025-07 | 2 | 48 | | 2026-03 | 31 | 539 |
| 2025-08 | 17 | 128 | | 2026-04 | 25 | 652 |
| 2025-09 | 17 | 183 | | 2026-05 | 29 | 557 |
| 2025-10 | 9 | 143 | | 2026-06 | 25 | 681 |
| 2025-11 | 24 | 428 | | 2026-07 | 26 | 500 |
| 2025-12 | 17 | 395 | | 2026-08 | 61 | 932 |
| 2026-01 | 33 | 398 | | 2026-09 | 63 | 773 |
| 2026-02 | 21 | 511 | | 2026-10 | 41 | 645 |

Pic août-sept. 2026 (61 et 63 clics) : cause non identifiable avec ces exports (pas de détail par requête dans le temps).

**Semaines à 0 et trous** (`gsc-par-semaine.csv`) :
- Les semaines des 30/06 et 07/07/2025 ont 0 impression ; 26 jours à 0 impression au total : les 19 premiers jours de juil. 2025, puis 7 jours isolés (dernier : 23/09/2025). Probable : site peu visible ou propriété GSC récente à l'époque. À ne pas lire comme une panne.
- Une seule semaine avec impressions mais 0 clic : celle du 28/07/2025.
- Aucune semaine à 0 dans AVANT ni APRÈS.

**Transition 8-13 juin 2026** (Graphique.csv, jour par jour) : clics 2, 0, 1, 1, 2, 0 ; impressions 17, 44, 32, 14, 12, 8. Pas de chute ni de trou visible à la bascule. En semaines : impressions 98 (sem. du 01/06), 146 (08/06), 178 (15/06), 187 (22/06) : montée progressive après la bascule, pas un saut. Les clics par semaine restent entre 4 et 9.

Dernier jour de l'export : 30/10/2026. Les 28-30 oct. (panne DNS/SSL) sont hors période APRÈS ; ces 3 jours totalisent encore 7 clics (Graphique.csv), donc la panne n'apparaît pas encore clairement dans l'export.

## 2. Réponses aux questions d'Emmanuelle (16 mois)

**Totaux 16 mois** : 441 clics, 7 513 impressions, CTR 5,9 %, position 13,7 (Graphique.csv). Pages.csv additionne 447 clics et 9 485 impressions et Requêtes.csv seulement 82 clics et 2 822 impressions : GSC compte différemment selon la vue, et masque les requêtes rares (anonymisées). **Seuls 82 clics sur 441 (19 %) ont un mot-clé visible.**

**Quelles pages sont vues ?** (Pages.csv, clics / impressions)
1. Accueil `/` : 303 / 4 814 (69 % des clics)
2. `/tarifs-et-modalites-de-prise-de-rendez-vous/` : 30 / 441
3. `/cercle-de-parole-saint-nazaire/` : 19 / 113 (CTR 16,8 %)
4. `/premenopause-saint-nazaire/` : 13 / 152
5. `/les-injonctions-faites-aux-femmes-quand-le-sois-toi-meme-deviens-un-labyrinthe/` : 12 / 177
6. `/contact/` : 12 / 158 ; 7. `/therapie-ifs-saint-nazaire/` : 11 / 136
8. `/eft-saint-nazaire/` : 10 / 881 (position 30,6, CTR 1,1 %) ; 10. `/emdr-saint-nazaire/` : 4 / 637 (position 11,3, CTR 0,6 %)

Presque toutes ces pages sont d'**anciennes URL WordPress** (voir plus bas). Les pages EMDR/EFT ont beaucoup d'impressions mais presque aucun clic.

**Quels mots tapés ?** (Requêtes.csv)
- « emmanuelle demeulemeester » : 35 clics / 154 impr., position 1,5 (recherche du nom = les gens la connaissent déjà)
- « emdr saint nazaire » : 17 / 652, position 8,7 ; « emma joubert melle » : 5 / 122 ; « emdr st nazaire » : 4 / 128 ; « demeulemeester » : 3 / 219

Familles (somme des requêtes visibles contenant le mot ; une requête peut compter dans 2 familles) :

| Famille | Requêtes | Clics | Impr. | Position moy. |
|---|---|---|---|---|
| nom (demeul…/emmanuel) | 16 | 42 | 410 | 3,9 |
| emdr | 28 | 25 | 1 113 | 11,9 |
| saint nazaire / st nazaire | 18 | 26 | 1 338 | 14,4 |
| eft / emotional freedom | 23 | 1 | 247 | 45,2 |
| psychopraticien(ne) | 10 | 0 | 75 | 30,7 |

Lecture : on la trouve surtout par son nom, puis par « EMDR Saint-Nazaire ». **EFT : quasi invisible** (1 clic ; les requêtes EFT sont souvent hors secteur : Saumur, Chinon, Ancenis…, position 50-70). « Psychopraticien » : 0 clic (ex. « psychopraticien saint nazaire » : 35 impr., position 21,9). Source : Requêtes.csv.

**Articles du blog.** Les articles actuels vivent sous `/blog/…` (20 fichiers dans `src/content/blog/`, lus sans modification). Deux formes d'URL apparaissent dans GSC : l'ancienne (nom de fichier, ex. `/blog/2026-08-27-comment-savoir…`) et la forme actuelle (slug du fichier). Je les ai regroupées par article. Top 5 par clics (Pages.csv) : tous à **1 clic** seulement.
1. Contrôle coercitif : 1 clic / 40 impr.
2. Thérapie IFS : 1 / 12
3. Comprendre l'EMDR (`comprendre-emdr`) : 1 / 10
4. Thérapie psychocorporelle : 1 / 9
5. (égalité à 0 clic) Thérapie en marchant : 0 / 41 impr. (plus d'impressions du lot)

Articles **jamais vus** sous `/blog/` (aucune ligne dans Pages.csv) : « Comprendre le lien d'attachement et ses blessures durables » et « Quand parler ne suffit plus… » (slug `psychotraumatismes-saint-nazaire`). Attention : l'article sur l'attachement est bien vu, mais sous son **ancienne URL WordPress** (`/comprendre-le-lien-dattachement-et-ses-blessures-durables/` : 8 clics, 310 impr., position 33). Idem pour la préménopause (13 clics), les injonctions (12). Donc le vrai trafic « blog » est encore sur d'anciennes URL, pas sur `/blog/`.

**Anciennes URL WordPress** : 52 URL de Pages.csv ne correspondent à aucune page actuelle (`src/pages/`) ni article actuel : 136 clics et 4 039 impressions au total. Liste dans `audit/analyses/anciennes-url-gsc.txt`. Types : pages à la racine (`/eft-saint-nazaire/`, `/emdr-saint-nazaire/`, `/tarifs-et-modalites-…`), pages Elementor (`/elementor-225/`), doublons (`/eft-duplicate/`, `/accueil-2/`), archives (`/author/…/page/2/`, `/page/2/`), un paramètre `?utm_source=rss`, un emoji dans une URL. Cela rejoint la piste du plan §5 (53 pages en 404 à l'indexation) : il faut vérifier si ces URL redirigent (301) vers les nouvelles pages. Je n'ai pas testé les redirections (hors périmètre de ces exports). Remarque : mon test compare à la liste actuelle des routes ; une URL listée peut quand même être gérée par une redirection Netlify non lue ici.

## 3. Appareils et pays

Appareils (`Appareils.csv`) :
- Mobile : 304 clics, 4 564 impr., CTR 6,7 %, position 7,2
- Ordinateur : 128 clics, 2 854 impr., CTR 4,5 %, position 24,4
- Tablette : 9 clics, 95 impr., CTR 9,5 %, position 6,7

Pays (`Pays.csv`, 75 pays listés) :
- France : 428 clics, 6 872 impr., position 13,2 (97 % des clics)
- Suisse : 4 clics, 29 impr. ; Réunion : 2 clics, 23 impr.
- Espagne 2 clics, Slovaquie 2 clics, Belgique 1 clic / 57 impr. : bruit, volumes négligeables.

## 4. Croisement Calendly

Premiers contacts = rendez-vous non annulés de type « 1er rendez-vous… » ou « Séance découverte… » regroupés par **mois de séance** (`audit/data/calendly/rdv-par-mois-anonyme.csv`). Clics = `Graphique.csv`. Tableau complet : `audit/analyses/gsc-vs-calendly-par-mois.csv`.

| Mois | Clics GSC | Premiers contacts | | Mois | Clics GSC | Premiers contacts |
|---|---|---|---|---|---|---|
| 2025-09 | 17 | 2 | | 2026-05 | 29 | 0 |
| 2025-10 | 9 | 0 | | 2026-06 | 25 | 1 |
| 2025-11 | 24 | 3 | | 2026-07 | 26 | 1 |
| 2025-12 | 17 | 6 | | 2026-08 | 61 | 2 |
| 2026-01 | 33 | 7 | | 2026-09 | 63 | 2 |
| 2026-02 | 21 | 3 | | 2026-10 | 41 | 4 |
| 2026-03 | 31 | 3 | | | | |
| 2026-04 | 25 | 2 | | | | |

Mise en garde : petits volumes, tendance pas preuve. Les deux séries ne bougent pas ensemble (déc.-janv. : beaucoup de premiers contacts avec peu de clics ; août-sept. : clics au plus haut mais 2 premiers contacts). Les liens Calendly du site n'ont aucun UTM (PLAN §5) : on ne sait pas quelles réservations viennent de Google ni du site. Les types ont été renommés le 3 sept. 2026, donc le regroupement est un choix d'analyse. Mois de séance ≠ mois de clic.

## 5. Ce que ces exports ne permettent PAS de dire

- **Pages et requêtes avant vs après** : Pages.csv, Requêtes.csv, Appareils.csv, Pays.csv sont des totaux sur 16 mois. Seul Graphique.csv a une date. Les exports par période (A2 pages, A3 requêtes, avant/après) manquent : on ne sait pas si EMDR/EFT ont gagné ou perdu des places depuis la refonte.
- **Requêtes masquées** : 359 clics sur 441 n'ont pas de requête visible.
- **Cause de la hausse** : refonte, saison, nouveaux articles, ou recherche de son nom ? Non démontrable.
- **Vraies visites** : GSC ne voit pas Bing, les réseaux, les accès directs. Pas d'outil de visites dans ces fichiers.
- **Provenance des rendez-vous** : aucun UTM Calendly.
- **Position à Saint-Nazaire précisément** : la position GSC est une moyenne tous lieux et appareils (mobile 7,2 contre ordinateur 24,4) ; les captures Google/Maps sont nécessaires.
- **Redirections des anciennes URL** : non testées ici.
- **Date exacte de bascule WordPress → Astro** : hypothèse (8 juin) non vérifiée.
- Les fichiers d'indexation (`indexation-*/`) n'ont pas été analysés ici hors des constats du plan.

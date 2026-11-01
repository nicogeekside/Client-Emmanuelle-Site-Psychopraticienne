# Analyse GSC par période — avant / après la refonte

Produit le 1er nov. 2026 par `audit/analyses/scripts/gsc_periodes.py` (`python3 -I audit/analyses/scripts/gsc_periodes.py`, depuis la racine). Sources : `audit/data/gsc/avant/` (17 janv. → 7 juin 2026) et `audit/data/gsc/apres/` (8 juin → 27 oct. 2026), exports Google Search Console, type « Web (textuel) ». Sortie machine : `audit/analyses/gsc-periodes.csv` (lu par `audit/livrable/build.py`).
Les chiffres GSC = apparitions et clics **venus de Google seulement**, pas des visites. Dans les tableaux : clics / impressions / position moyenne.

## 1. Contrôle des totaux (Graphique.csv)

| Période | Jours | Clics | Impressions | CTR | Position (pondérée) |
|---|---|---|---|---|---|
| Avant (2026-01-17 → 2026-06-07) | 142 | 133 | 2 550 | 5,2 % | 15,6 |
| Après (2026-06-08 → 2026-10-27) | 142 | 202 | 3 364 | 6,0 % | 13,3 |

**Aucun écart** avec `01-gsc.md` (133 → 202 clics, 2 550 → 3 364 impressions, positions 15,6 → 13,3) : les exports par période et l'export 16 mois donnent les mêmes totaux.

Attention : la somme des lignes de `Pages.csv` ne vaut pas le total de `Graphique.csv` (Google ne liste pas toutes les lignes) : avant 133 clics / 3 154 impr. contre 133 / 2 550 ; après 206 / 4 162 contre 202 / 3 364. `Requêtes.csv` est encore plus partiel (requêtes rares masquées) : clics visibles 13 sur 133 avant (10 %), 44 sur 202 après (22 %).
Avant + après ne font pas non plus le total « 16 mois » des pages (ex. accueil 303 sur 16 mois) : les deux périodes couvrent 284 jours sur ~487.

## 2. Pages (Pages.csv)

Regroupements « ancienne URL WordPress + nouvelle URL du même sujet » (signalés ✱) : EMDR (`/emdr-saint-nazaire/`, `/emdr/`, `/therapie-emdr-saint-nazaire/`), EFT (`/eft-saint-nazaire/`, `/eft/`, `/seance-eft-gestion-emotions/`), séance découverte psychocorporelle (ancien nom « gratuite » + nouveau), thérapie en marchant (racine + `/therapie-en-marchant-saint-nazaire/`), post-partum (`/post-partum-saint-nazaire/` + `/espace-soutien-post-partum/`). Les articles `/blog/…` sont traités au §4.

| Page | Avant (clics / impr. / pos.) | Après (clics / impr. / pos.) | Évolution clics |
|---|---|---|---|
| Accueil | 76 / 1 507 / 9,1 | 139 / 2 146 / 9,7 | +63 |
| Tarifs et modalités | 13 / 131 / 7,4 | 17 / 260 / 7,7 | +4 |
| Cercle de parole | 8 / 39 / 5,3 | 11 / 74 / 6,4 | +3 |
| Injonctions faites aux femmes | 6 / 67 / 9,6 | 6 / 105 / 8,9 | +0 |
| Préménopause (page) | 8 / 82 / 10,7 | 4 / 68 / 13,6 | −4 |
| Thérapie IFS (page) | 5 / 55 / 14,4 | 5 / 79 / 13,5 | +0 |
| EFT (ancienne → nouvelle page) ✱ | 5 / 512 / 37,2 | 4 / 313 / 17,2 | −1 |
| Contact | 2 / 54 / 7,5 | 7 / 69 / 5,0 | +5 |
| /comprendre-le-lien-dattachement-et-ses-blessures-durables/ | 2 / 64 / 10,3 | 5 / 225 / 39,9 | +3 |
| EMDR (ancienne → nouvelle page) ✱ | 4 / 359 / 10,3 | 0 / 273 / 12,9 | −4 |
| Index du blog | 0 / 29 / 7,8 | 2 / 115 / 3,0 | +2 |
| Séance découverte psychocorporelle (renommée) ✱ | 0 / 58 / 35,5 | 1 / 20 / 21,7 | +1 |
| Prendre rendez-vous | — | 1 / 33 / 4,1 | — |
| /le-poids-du-silence-et-des-non-dits/ | 1 / 27 / 9,4 | 0 / 3 / 2,7 | −1 |
| /les-croyances-limitantes/ | 1 / 20 / 8,9 | — | — |
| /depression-post-partum-saint-nazaire/ | 1 / 12 / 7,8 | — | — |
| /stress-cancer-saint-nazaire/ | 1 / 10 / 17,3 | — | — |
| /elementor-225/ | 0 / 30 / 11,1 | 0 / 19 / 6,8 | +0 |
| /a-propos-emmanuelle/ | — | 0 / 31 / 12,7 | — |
| /therapie-en-ligne-visio/ | — | 0 / 28 / 4,8 | — |
| /therapies-breves/ | 0 / 5 / 10,8 | 0 / 22 / 12,8 | +0 |
| /politique-de-cookies-ue/ | 0 / 17 / 6,4 | 0 / 5 / 8,2 | +0 |

« — » = la page n'a aucune ligne dans l'export de cette période.

Détail des regroupements ✱ (clics / impressions) :

- EFT (ancienne → nouvelle page), avant : `/eft-saint-nazaire/` 5 / 474 ; `/eft/` 0 / 38
- EFT (ancienne → nouvelle page), apres : `/eft-saint-nazaire/` 3 / 279 ; `/seance-eft-gestion-emotions/` 1 / 6 ; `/eft/` 0 / 28
- EMDR (ancienne → nouvelle page), avant : `/emdr-saint-nazaire/` 3 / 337 ; `/emdr/` 1 / 22
- EMDR (ancienne → nouvelle page), apres : `/emdr-saint-nazaire/` 0 / 226 ; `/therapie-emdr-saint-nazaire/` 0 / 31 ; `/emdr/` 0 / 16
- Séance découverte psychocorporelle (renommée), avant : `/seance-decouverte-gratuite-therapie-psychocorporelle-saint-nazaire/` 0 / 58
- Séance découverte psychocorporelle (renommée), apres : `/seance-decouverte-gratuite-therapie-psychocorporelle-saint-nazaire/` 1 / 14 ; `/seance-decouverte-therapie-psychocorporelle-saint-nazaire/` 0 / 6
- Thérapie en marchant (page), avant : `/la-therapie-en-marchant-saint-nazaire/` 0 / 7
- Thérapie en marchant (page), apres : `/therapie-en-marchant-saint-nazaire/` 0 / 8
- Post-partum (page), avant : `/post-partum-saint-nazaire/` 0 / 5
- Post-partum (page), apres : `/espace-soutien-post-partum/` 0 / 12

Lecture : l'accueil passe de 76 à 139 clics et concentre l'essentiel de la hausse ; les pages EFT/EMDR restent très vues et très peu cliquées dans les deux périodes. Les chiffres de page sont de petits nombres (quelques clics) : tendance, pas preuve.

## 3. Mots tapés (Requêtes.csv)

Top requêtes (clics / impressions / position) :

| Avant | Après |
|---|---|
| emdr saint nazaire : 6 / 274 / 9,6 | emmanuelle demeulemeester : 20 / 39 / 1,0 |
| emdr st nazaire : 2 / 49 / 9,2 | emdr saint nazaire : 10 / 288 / 9,3 |
| demeulemeester : 2 / 37 / 4,8 | emma joubert melle : 5 / 100 / 7,7 |
| injonction femme : 1 / 3 / 20,3 | psychologue emdr saint nazaire : 2 / 53 / 7,9 |
| psychologue melle : 1 / 1 / 2,0 | emdr st nazaire : 1 / 61 / 7,4 |
| therapie emdr : 1 / 1 / 2,0 | psychotherapeute saint nazaire : 1 / 24 / 11,2 |
| emotional freedom technique saumur : 0 / 74 / 57,3 | contrôle coercitif : 1 / 6 / 3,3 |
| accompagnement émotionnel saffré : 0 / 40 / 75,8 | blessure d attachement : 1 / 6 / 29,5 |
| therapie saint nazaire : 0 / 34 / 42,5 | psychothérapeute : 1 / 5 / 3,8 |
| emotional freedom technique chinon : 0 / 31 / 72,3 | dates : 1 / 1 / 2,0 |

Familles (somme des requêtes **visibles** qui contiennent le mot ; une requête peut compter dans plusieurs familles ; « autres » = aucune des familles) :

| Famille | Avant : requêtes / clics / impr. / pos. | Après : requêtes / clics / impr. / pos. |
|---|---|---|
| nom (demeul…, emmanuel…) | 9 / 2 / 52 / 4,9 | 7 / 21 / 128 / 3,2 |
| emdr | 9 / 9 / 374 / 9,8 | 19 / 13 / 538 / 9,8 |
| eft | 14 / 0 / 182 / 58,2 | 6 / 0 / 31 / 16,6 |
| psychopraticien(ne) | 2 / 0 / 4 / 9,2 | 7 / 0 / 47 / 18,6 |
| saint nazaire / st nazaire | 10 / 8 / 439 / 13,8 | 17 / 14 / 731 / 16,9 |
| autres | 30 / 2 / 132 / 43,0 | 89 / 9 / 380 / 34,4 |

Recherches suivies :

| Recherche | Avant (clics / impr. / pos.) | Après (clics / impr. / pos.) |
|---|---|---|
| « emdr saint nazaire » | 6 / 274 / 9,6 | 10 / 288 / 9,3 |
| « emdr st nazaire » | 2 / 49 / 9,2 | 1 / 61 / 7,4 |
| « eft saint nazaire » | — | — |
| « emmanuelle demeulemeester » | — | 20 / 39 / 1,0 |
| « demeulemeester » | 2 / 37 / 4,8 | 0 / 84 / 4,1 |
| « psychopraticienne » | — | 0 / 4 / 2,8 |
| « psychopraticien saint nazaire » | — | 0 / 34 / 22,2 |

« — » = la requête n'est pas dans la liste exportée de cette période (trop rare, ou masquée par Google pour confidentialité). « eft saint nazaire » n'apparaît dans aucune des deux listes.

Lecture : « emdr saint nazaire » reste stable (place moyenne 9,6 puis 9,3 ; clics 6 puis 10). La recherche du nom complet « emmanuelle demeulemeester » n'est visible qu'après (20 clics, place 1) : avant, cette requête n'est pas dans la liste (masquée ou trop rare) ; la famille « nom » (toutes variantes visibles) passe de 2 à 21 clics. Les requêtes EFT restent sans clic dans les deux périodes.

## 4. Articles de blog

Regroupement par article : URL `/blog/…` (slug ou nom de fichier, forme actuelle ou ancienne) **plus** l'ancienne URL WordPress à la racine quand le sujet est évident ✱ (liste : `/comprendre-le-lien-dattachement-et-ses-blessures-durables/`, `/les-croyances-limitantes/`, `/therapeute-energetique-saint-nazaire/`, `/therapies-breves/`, `/la-therapie-en-marchant-saint-nazaire/`, `/post-partum-saint-nazaire/`, `/stress-cancer-saint-nazaire/`, `/temoignage-dune-cliente-en-parcours-de-soin-en-cancerologie-et-son-accompagnement-en-therapie-psychocorporelle/`, `/soulager-douleur-chronique-psychologie-energetique/`, `/therapie-psychocorporelle-saint-nazaire/`, `/psychologie-energetique-saint-nazaire/`, `/sante-mentale-saint-nazaire/`, `/premenopause-saint-nazaire/`). Le détail ancienne/nouvelle URL est donné en clics.

| Article | Avant (clics / impr. / pos.) | Après (clics / impr. / pos.) | Après : dont nouvelle URL `/blog/` |
|---|---|---|---|
| Préménopause chez la femme entre 40 et 50 ans : symptômes, émotions et | 8 / 82 / 10,7 | 4 / 74 / 12,9 | 0 |
| Comprendre le lien d’attachement et ses blessures durables | 2 / 64 / 10,3 | 5 / 225 / 39,9 | 0 |
| les croyances limitantes | 1 / 20 / 8,9 | 0 / 20 / 3,5 | 0 |
| Comment savoir si je suis victime de contrôle coercitif ? | — | 1 / 40 / 13,7 | 1 |
| La thérapie psychocorporelle | 0 / 8 / 13,8 | 1 / 13 / 8,6 | 1 |
| La thérapie IFS | — | 1 / 12 / 5,2 | 1 |
| Stress et cancer à Saint-Nazaire : les bienfaits d'une prise en charge | 1 / 10 / 17,3 | 0 / 1 / 69,0 | 0 |
| Comprendre l'EMDR : Comment cette thérapie traite les traumatismes | — | 1 / 10 / 10,4 | 1 |
| La thérapie en marchant sur Saint-Nazaire | 0 / 7 / 39,1 | 0 / 41 / 2,6 | 0 |
| Les thérapies brèves | 0 / 5 / 10,8 | 0 / 40 / 19,4 | 0 |
| Le thérapeute énergétique | 0 / 16 / 10,9 | 0 / 14 / 6,1 | 0 |
| C'est quoi la psychologie énergétique? | 0 / 2 / 7,0 | 0 / 6 / 14,2 | 0 |
| Post Partum à Saint-Nazaire : espace de parole et de soutien | 0 / 5 / 9,4 | 0 / 3 / 24,3 | 0 |
| Témoignage d'une cliente en parcours de soin en cancérologie et son | 0 / 4 / 5,8 | 0 / 3 / 4,3 | 0 |

Articles sans aucune ligne dans les deux périodes (ni nouvelle ni ancienne URL) : 1 : Quand parler ne suffit plus... des approchent qui reparent le corp et l'esprit.

Toutes les URL `/blog/…` des exports ont été rattachées à un des 20 articles.

## 5. « emdr saint nazaire » et « eft saint nazaire »

- « emdr saint nazaire » : avant 6 clics / 274 impr. / place 9,6 ; après 10 clics / 288 impr. / place 9,3.
- « eft saint nazaire » : avant — (absente de la liste) ; après — (absente de la liste).
- La place moyenne GSC est un mélange de lieux et d'appareils ; elle ne dit pas où l'on est à Saint-Nazaire (voir le relevé du 1er nov. 2026 dans `audit/data/serp/`).

## 6. Appareils (Appareils.csv)

| Appareil | Avant (clics / impr. / pos.) | Après (clics / impr. / pos.) |
|---|---|---|
| Mobile | 93 / 1 482 / 7,2 | 136 / 2 024 / 7,7 |
| Ordinateur | 38 / 1 040 / 27,8 | 62 / 1 299 / 22,2 |
| Tablette | 2 / 28 / 6,2 | 4 / 41 / 9,3 |

## 7. Ce que ces exports ne permettent pas de dire

- La cause de la hausse (refonte, saison, nouveaux articles) : non démontrable.
- Les volumes de recherche mensuels : ils ne viennent pas de Search Console.
- La majorité des clics n'a pas de requête visible (voir §1) : les évolutions par mot ne portent que sur la minorité visible.
- Les redirections des anciennes URL : non testées ici.

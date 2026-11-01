# Volumes de recherche autour du site d'Emmanuelle

Source volumes : Semrush, base France, 1er nov. 2026 (`audit/data/semrush-ui/volumes-appels.md`). Source site : Search Console, période « après » (8 juin → 27 oct. 2026, 142 jours = 4,67 mois), `audit/data/gsc/apres/Requêtes.csv` ; colonne 16 mois dans le CSV. Données ligne à ligne : `audit/analyses/06-volumes.csv`.

**À lire avant les chiffres.** Les volumes Semrush sont des estimations, arrondies, et sous-estiment les petites requêtes locales : le site affiche 89 apparitions par mois sur « emdr saint nazaire » (GSC) pour un volume Semrush de 110, alors qu'il n'est qu'en 8e-9e position. Google masque aussi beaucoup de requêtes dans Search Console (voir `05-gsc-avant-apres.md` §1). La « part captée » est donc un ordre de grandeur, pas une mesure. « n/a » = absent de Semrush = trop faible pour être mesuré. Les « variantes proches » GSC regroupées : mêmes mots, accents ou « st » pour « saint » (ex. « emdr st nazaire »).

## 1. Le marché local cœur vs ce que touche le site

Marché local mesurable (sources : phrase_these, blocs A et B) : emdr saint nazaire 110, emdr guérande 30, emdr la baule 20, psychothérapeute saint nazaire 20. Tous les autres (eft × villes, psychopraticienne / thérapeute × villes) : 0 ou n/a. **Total : 180 recherches par mois.**

Ce que le site touche sur ces 4 requêtes : 89,3 apparitions/mois (emdr saint nazaire) + 8,1 (psychothérapeute saint nazaire) = **97 apparitions/mois, soit environ 54 % du volume**, pour environ 2,6 clics/mois (2,36 + 0,21). Sur emdr guérande et emdr la baule : 0 apparition visible.

Avec les formats (bloc C) : + therapie psychocorporelle 20, hypnose saint nazaire 70, psychopraticienne en ligne 10, thérapie en visio 10, emdr en visio 90 = 200 de plus, dont presque rien de local. Le site y touche 0,8 apparition/mois (hypnose 0,2 ; psychopraticienne en ligne 0,6).

Lecture simple : **le marché local écrit « à la main » est minuscule** (≈ 200 à 400 recherches/mois en tout). Emmanuelle y est déjà visible sur le gros mot (emdr saint nazaire) mais cliquée seulement 2,6 % du temps (position 8-9, derrière Doctolib et les annuaires, `matrice-mots-cles.md` ligne 1). Les clients passent plus par la fiche Google / le nom (« emmanuelle demeulemeester » : 154 apparitions sur 16 mois) que par ces requêtes.

Benchmark d'échelle (pas des cibles) : psychologue saint nazaire 880 (KD 25), psy saint nazaire 70, emdr 60 500 (KD 19), eft 9 900 (KD 35), eft thérapie 1 000 (KD 27). Le site touche 8,1 apparitions/mois sur « emdr », 3,4 sur « eft thérapie », 0,9 sur « eft ».

## 2. Top 10 opportunités

Critères : volume correct, KD faible, cohérent avec son offre, site absent ou loin. Volumes et KD : Semrush FR. Site : GSC « après », par mois. Pour les requêtes sans ligne GSC, le site est invisible (0).

| # | Requête | Volume | KD | Site aujourd'hui | Pourquoi |
|---|---|---|---|---|---|
| 1 | baby blues | 5 400 | 18 | non vu | Besoin concret du post-partum (déjà un axe du site), KD bas |
| 2 | tapping eft | 170 | 20 | non vu | Recherche d'une méthode qu'elle pratique |
| 3 | eft thérapie | 1 000 | 27 | 3,4 impr./mois, position 5 (16 mois) | Déjà proche de la 1re page : à pousser |
| 4 | retrouver confiance en soi | 320 | 22 | non vu | Thème de son nuage de mots |
| 5 | faire un deuil / comment faire son deuil | 390 / 320 | 17 / 20 | non vu | Thème « deuil », langage des gens |
| 6 | gérer ses émotions | 140 | 27 | 2,4 impr./mois sur « gestion des émotions saint-nazaire » | Correspond à la page séance EFT |
| 7 | gérer son anxiété | 110 | 30 | non vu | Thème anxiété |
| 8 | emdr en visio | 90 | 4 | non vu | KD très bas, offre en visio |
| 9 | emdr guérande + emdr la baule | 30 + 20 | 0 | non vu | Faible mais sans concurrence : une page « je reçois aussi depuis Guérande / La Baule » (à valider avec elle) |
| 10 | deuil phases | 480 | 23 | non vu | Contenu d'information |

À écarter malgré le volume : « depression post partum » 9 900 mais KD 57 (trop dur, et ton médical) ; « emdr » 60 500 (national, site 8 apparitions/mois, trop général) ; « hypnose saint nazaire » 70 (elle ne propose pas d'hypnose d'après la liste : à confirmer avec elle) ; « psychopraticien(ne) » 5 400 / 3 600, KD 29 : requête de curieux (« c'est quoi »), site à la position 41 (12 apparitions sur 16 mois).

## 3. Idées de thèmes « type post-partum » (besoins concrets)

Surtout des questions d'information, KD souvent bas. Source : phrase_related (appels 3-5) et phrase_these.

- **Post-partum / naissance** : baby blues 5 400 (KD 18) ; postpartum 2 900 (KD 31) ; définition post partum 1 000 (KD 34) ; post accouchement 590 (KD 44) ; post partum c'est quoi 320 (KD 35) ; soutien post partum 30 ; dépression post partum aide 20. Les fautes de frappe (« post portum », « post part ») pèsent 70-210 chacune, inutile de les viser.
- **Deuil** : définition d'un deuil 1 300 (KD 24) ; deuil phases 480 (KD 23) ; en deuil 480 (KD 32) ; faire un deuil 390 (KD 17) ; comment faire son deuil 320 (KD 20) ; comment faire le deuil 170 (KD 19) ; deuil refoulé 90 (KD 15) ; thérapie deuil 10. Les gens cherchent « comment faire », pas « thérapie ».
- **Émotions, stress, estime** : gérer son stress 590 (KD 53, dur) ; retrouver confiance en soi 320 (KD 22) ; gérer ses émotions 140 (KD 27) ; gérer son anxiété 110 (KD 30) ; surmonter une séparation 20.
- **À écarter, volume nul** : toutes les formes « thème + saint nazaire » (deuil, burn out, phobie, stress, périnatalité, etc.) sont absentes de Semrush, donc sous le seuil mesurable. Pareil pour thérapie traumatisme, phobie thérapie, thérapie burn out (0).
- **EMDR local** (appel 5) : peu d'idées nouvelles ; seuls psychologue saint-nazaire 70, psychologie st nazaire 90, neuropsychologue saint nazaire 90.

## 4. Note : se positionner sur « psychologue » sans usurper le titre

Constat : « psychologue saint nazaire » = 880 recherches/mois (KD 25), 10 fois plus que « psychopraticienne saint nazaire » (n/a). Emmanuelle n'est pas psychologue.

**Cadre (à faire valider)** : le titre de psychologue est réservé aux titulaires de certains diplômes (loi du 25 juillet 1985, art. 44, selon le ministère de l'Enseignement supérieur : https://www.enseignementsup-recherche.gouv.fr/fr/psychologue-une-profession-reglementee-en-france-46456). Le titre de psychothérapeute est lui aussi protégé séparément et suppose l'inscription au registre des ARS (source secondaire, cabinet d'avocat : https://www.simonnetavocat.fr/psychiatre-psychologue-psychanalyste-therapeute-quelle-difference/). **Point d'attention** : le site utilise-t-il « psychothérapeute » ? La GSC montre qu'elle apparaît sur « psychothérapeute saint nazaire » (49 apparitions). À vérifier. Je ne cite pas de sanction : non vérifiée sur une source officielle.

**Interdit** (à faire valider par un juriste) :
- se présenter comme psychologue (site, fiche Google, annuaires, cartes, publicités) ;
- mettre « psychologue » dans le nom de la fiche Google ou dans un titre de façon à laisser croire qu'elle l'est ;
- mots-clés ou balises trompeurs, même cachés.

**Stratégies légitimes** :
1. Article « Psychologue, psychothérapeute, psychopraticienne : quelles différences ? » : répond à ceux qui tapent « psychologue », dit honnêtement ce qu'elle est, sans prétendre l'être.
2. Annuaires qui sortent sur ces requêtes (Resalib, Crénolibre, Médoucine, `matrice-mots-cles.md`), avec la **bonne catégorie** (psychopraticienne / thérapeute).
3. Fiche Google : catégorie exacte de son métier (à choisir dans la liste de Google, à faire valider), jamais « psychologue ».
4. Contenu par besoin plutôt que par titre : deuil, baby blues, anxiété, confiance en soi (section 3).
5. Publicité éventuelle : texte par besoin (« EMDR à Saint-Nazaire », « soutien après la naissance ») sans le mot « psychologue ». Les règles de Google Ads sur les professions réglementées sont à vérifier.

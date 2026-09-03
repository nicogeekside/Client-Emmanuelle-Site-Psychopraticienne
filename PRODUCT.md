# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

**Public principal — adultes en phase de comparaison, mixte hommes/femmes.** Ils ont déjà décidé de consulter. Ils comparent deux ou trois praticiens trouvés sur Google, sur la région de Saint-Nazaire ou en visio partout en France. Ils évaluent, dans cet ordre : la légitimité (formations, cadre, sérieux), le lieu et le format, le tarif, puis la personne. Le site doit convaincre autant que rassurer — il n'est pas un simple point de passage après recommandation.

Le job à accomplir : « déterminer si cette praticienne-ci est la bonne pour moi, et franchir le premier pas sans m'engager ».

Motifs de consultation déclarés (`src/data/config.js` → `epreuves`) : traumatismes, deuil, anxiété, périnatalité, phobies, stress, confiance en soi, douleurs chroniques, post-partum, burn-out, troubles du sommeil, séparation, schémas répétitifs, gestion des émotions, blocages émotionnels.

## Product Purpose

Site vitrine et point d'entrée du cabinet d'Emmanuelle Demeulemeester, psychopraticienne à Saint-Nazaire (Loire-Atlantique), spécialisée en EFT clinique et EMDR-DSA.

**Le succès se mesure à une seule action : la réservation de la séance découverte de 45 minutes offerte.** C'est le point d'entrée sans risque du parcours. Le formulaire de contact et le téléphone sont des canaux de repli, pas des objectifs équivalents ; la prise de rendez-vous Calendly est le mécanisme qui sert cet objectif.

## Positioning

Quatre éléments qu'un cabinet voisin ne pourrait pas reprendre tels quels :

1. **Quatre formats de séance réellement proposés, pas trois plus une promesse** — cabinet, visio (France entière), thérapie en marchant autour du bois Joalland, et un groupe de parole post-partum mensuel ouvert aux mères comme aux pères. Le choix du format est un argument de premier plan, pas une note de bas de page.
2. **25 ans dans le monde médical avant la reconversion** — la légitimité ne vient pas d'un diplôme récent isolé, mais d'un parcours professionnel long dans le soin.
3. **Un vécu personnel qui recoupe les motifs de consultation** — post-partum difficile et maladie éprouvante traversés puis dépassés. C'est ce qui rend crédible la spécialisation périnatalité / post-partum et l'accompagnement en parcours de soin oncologique.
4. **Deux certifications datées et nommées** — IFPEC (EFT clinique, 360 h) et AHTMA (EMDR-DSA niveau 2), toutes deux obtenues en octobre 2025, avec adhésion publique à la charte déontologique IFPEC.

## Operating Context

- **Zone** : cabinet au 7 rue de l'étoile du matin, 44600 Saint-Nazaire. Parking gratuit à proximité. Visio disponible partout en France. Séances en marchant au bois Joalland.
- **Horaires** : cabinet lundi et mardi 9 h – 20 h ; visio et extérieur jeudi et vendredi 9 h – 18 h, samedi 9 h – 13 h.
- **Premier rendez-vous** : 1 h, consacrée à faire connaissance, explorer le parcours, clarifier les attentes et poser le cadre.
- **Séance découverte** : 45 min offertes, au cabinet, en visio ou en marchant. Présentation de l'approche et des outils, puis test de l'EFT ou de l'EMDR sur un sujet choisi par la personne.
- **Tarifs** : 60 € l'heure pour les séances suivantes ; 50 € l'heure pour étudiants et demandeurs d'emploi, sur justificatif.
- **Paiement** : espèces, chèque ou virement bancaire. Pas de carte, pas de paiement en ligne.
- **Annulation** : prévenir au moins 48 h à l'avance.
- **Prise de rendez-vous** : par téléphone ou via le site (Calendly + formulaire Netlify redirigeant vers `/merci/`).
- **Édition du contenu** : Emmanuelle publie et met à jour ses articles seule via Decap CMS sur `/admin`, en mode editorial workflow (brouillon puis publication), backend git-gateway sur la branche `main`.

## Capabilities and Constraints

**Pile technique** : Astro 5 statique, Tailwind 3, `@astrojs/sitemap`, `astro-seo`, AOS pour les animations d'apparition, polices Fontsource (Playfair Display, Lato). Déploiement Netlify. Domaine `www.emma-psychopraticienne.fr`.

**Intégrations tierces** : widget Calendly (script externe), formulaire Netlify Forms avec honeypot anti-bot, Decap CMS.

**Contraintes à préserver** (confirmées par l'utilisateur) :

- **SEO local Saint-Nazaire** — les pages par format et par approche et leurs URLs sont un actif de référencement : `/therapie-cabinet-saint-nazaire/`, `/therapie-en-ligne-visio/`, `/therapie-en-marchant-saint-nazaire/`, `/espace-soutien-post-partum/`, `/therapie-emdr-saint-nazaire/`, `/seance-eft-gestion-emotions/`, `/seance-decouverte-therapie-psychocorporelle-saint-nazaire/`, `/a-propos-emmanuelle/`, `/prendre-rendez-vous-saint-nazaire/`. Ne pas renommer ni fusionner sans redirection 301 (`public/_redirects` porte déjà celle de l'ancienne `/contact`). `/merci/` est volontairement exclue du sitemap.
- **Workflow Decap CMS** — toute évolution du blog doit rester éditable par Emmanuelle depuis `/admin`, sans intervention dans le code.
- Le contenu du blog (19 articles) est de la donnée éditoriale, pas de la copie de design : ne pas le réécrire.

**Décisions produit explicitement non tranchées** :

- Le tarif du premier rendez-vous d'1 h n'est indiqué nulle part sur le site — seul celui « des séances suivantes » (60 €) l'est. À clarifier avec Emmanuelle avant tout travail sur la page rendez-vous ; ne pas l'inventer.
- Aucun objectif chiffré (nombre de réservations, taux de conversion, volume de trafic) n'a été fixé.

## Brand Commitments

- **Nom** : Emmanuelle Demeulemeester, psychopraticienne. SIRET 989 070 727 00023.
- **Identité visuelle, contrainte contraignante confirmée** : la palette et les polices proviennent du logo et de la carte de visite déjà en circulation — sauge `#5C7A62`, sauge doux `#829A86`, beige sable `#EBDCCC`, gris taupe `#85827D`, terracotta `#C88D7D` (couleur d'action), anthracite `#2C3E50`, fond blanc cassé `#FAF7F3` ; Playfair Display en titres, Lato en textes. Le site doit rester cohérent avec les supports imprimés qui circulent en main. Ne pas remplacer cette identité ; l'interpréter.
- **Voix** : première personne, tutoiement jamais, vouvoiement constant. Douce, directe, sans jargon thérapeutique non expliqué. Trois valeurs affichées : écoute active, non-jugement, autonomie.
- **Limites déontologiques IFPEC, contraignantes** : aucune promesse de guérison, aucun claim médical, jamais de suggestion d'interrompre un traitement prescrit, aucune prétention à des formations ou pouvoirs non détenus, secret professionnel absolu, aucun témoignage ni chiffre inventé. Le cadre concret (horaires, durée, tarifs, annulation) doit rester explicitement énoncé. Cette charte est publiée sur `/charte-deontologique/`.

## Evidence on Hand

**Réel et utilisable :**

- 5 avis clients Google, 5 étoiles, nommés et taggés par approche (`src/data/config.js` → `reviews`). C'est l'intégralité de la preuve sociale disponible : il n'y en a pas d'autre.
- Deux certifications vérifiables : IFPEC — Psycho-Praticienne en Techniques Énergétiques et Psycho-Corporelles, option EFT Clinique, 360 h, octobre 2025 ; AHTMA — Praticienne en EMDR-DSA niveau 2, octobre 2025.
- Photographies réelles du cabinet, du fauteuil, de la salle d'attente et de l'extérieur ; portraits d'Emmanuelle en intérieur et en extérieur (`src/assets/images/`). Plusieurs fichiers sources dépassent 1,5 Mo et ne sont pas optimisés.
- Logo en deux versions (`logo.png`, `logo-emma-couleurs.png`).
- 19 articles de blog rédigés par Emmanuelle, dont un témoignage client en parcours de soin oncologique.
- Coordonnées complètes et géolocalisation du cabinet, exploitables en données structurées locales.

**Absences que les travaux futurs ne doivent pas combler par de l'invention** : aucun chiffre de patientèle, aucun taux de réussite, aucune étude ou statistique propre, aucune presse, aucun avis au-delà des cinq existants, aucun partenariat ou prescripteur nommé.

## Product Principles

1. **La légitimité avant l'émotion.** Le visiteur compare ; il cherche d'abord des preuves qu'il a affaire à quelqu'un de sérieux. Certifications, cadre, charte et tarifs doivent être trouvables vite, pas relégués en bas de page.
2. **Un seul succès, trois chemins hiérarchisés.** Tout converge vers la séance découverte de 45 minutes offerte. Calendly la sert, le formulaire et le téléphone la rattrapent. Trois appels à l'action de même poids sur un même écran est un défaut, pas une commodité.
3. **Le choix du format est l'argument, pas une option.** Cabinet, visio, en marchant, groupe post-partum : c'est ce que le cabinet voisin n'offre pas. Ce choix mérite d'être posé tôt et clairement, jamais enterré dans un menu déroulant.
4. **Rien qui promette la guérison.** La charte IFPEC n'est pas une page légale à cocher, c'est une contrainte de rédaction sur chaque ligne du site. En cas de doute sur une formulation, la version prudente gagne.
5. **Ne rien inventer, jamais.** Cinq avis, deux certifications, un tarif manquant. Si une preuve manque, on la demande à Emmanuelle ou on conçoit sans — on ne la fabrique pas.

## Accessibility & Inclusion

Une part des visiteurs arrive en détresse émotionnelle, en épuisement post-partum ou en parcours de soin lourd : charge cognitive faible, lisibilité élevée, aucun effet qui surprenne ou presse. Les animations d'apparition doivent respecter `prefers-reduced-motion`. Le public inclut des personnes de 40 à 60 ans (périménopause, deuil, douleurs chroniques) : ne pas descendre sous 16 px pour le texte courant, contrastes conformes AA. L'espace post-partum est explicitement ouvert aux mères comme aux pères — la copie ne doit pas s'adresser aux seules femmes.

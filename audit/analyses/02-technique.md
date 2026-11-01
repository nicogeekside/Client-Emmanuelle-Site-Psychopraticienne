# Audit technique et migration — 1er nov. 2026

Site : https://emma-psychopraticienne.fr (analysé en ligne, lecture seule). Données : `audit/data/crawl/crawl.csv` (36 pages du sitemap) et `audit/analyses/redirections-proposees.csv`.

## En une phrase
Le site est techniquement propre (tout en 200, HTTPS, www géré, canoniques justes). Le vrai problème : **61 anciennes adresses WordPress renvoient une erreur 404** au lieu de rediriger vers la page équivalente. Google les connaît encore, les visiteurs qui les trouvent arrivent sur une page d'erreur.

## 🔴 Grave

### 1. Les anciennes URL WordPress sont en 404 (cause probable des « 53 pages en 404 » de Google)
- 62 anciennes URL « vraies pages » retrouvées (44 via archive.org, 52 via la liste Search Console, 34 en commun). **61 sont en 404 aujourd'hui.** La seule qui redirige : `/contact/` (règle `/contact` dans `public/_redirects`).
- Sur 52 URL vues par Google en 16 mois : 51 sont en 404. Elles totalisent **136 clics et 4 039 impressions** (source : `audit/analyses/anciennes-url-gsc.txt`). Ce trafic est perdu au lieu d'être transféré.
- Exemples : `/eft-saint-nazaire/` (881 impressions, position 30), `/tarifs-et-modalites-de-prise-de-rendez-vous/` (441 impressions, 30 clics), `/emdr-saint-nazaire/` (637 impressions), `/cercle-de-parole-saint-nazaire/` (113 impressions, 19 clics).
- Preuve : `curl -I https://emma-psychopraticienne.fr/eft-saint-nazaire/` → 404.
- Les nouvelles pages ont un autre format d'adresse (articles sous `/blog/…`), donc aucune redirection automatique.
- **Solution : ajouter des 301.** Proposition prête : `audit/analyses/redirections-proposees.csv` (confiance haute : 34, moyenne : 14, basse : 13). Les « basse » sont à valider par Emmanuelle (sujet sans équivalent exact, renvoyé vers `/blog/` ou une page proche).
- Les anciens sitemaps/flux WordPress (`/feed/`, `/wp-sitemap.xml`, `/sitemap.xml`, `/wp-login.php`) sont aussi en 404 : normal, pas besoin de les rediriger.

### 2. Où ajouter les 301
- Il n'y a **pas de `netlify.toml`** dans le dépôt. Les redirections sont gérées dans **`public/_redirects`** (déjà 6 règles : `/contact`, 4 slugs d'articles renommés, `/blog/therapie-emdr-saint-nazaire`). C'est le bon endroit : on y ajoute les lignes de la forme `/ancienne-url  /nouvelle-page/  301`.
- Ces règles fonctionnent avec ou sans `/` final (vérifié : `/blog/comprendre-emdr` et `/blog/comprendre-emdr/` redirigent tous deux).
- Attention : une adresse contient un emoji (`/🌿se-faire-accompagner-en-post-partum-…`) : à écrire en pourcentage-encodé et à tester après déploiement.
- Plusieurs anciennes URL ciblent la même page (ex. `/emdr/` et `/emdr-saint-nazaire/` → page EMDR) : normal et sans risque.

## 🟡 À corriger

### 3. Titres trop longs : 28 pages sur 36 dépassent 60 caractères
Le suffixe « | Blog Emmanuelle Demeulemeester… » ajouté partout allonge les titres. Google les coupe dans les résultats. Plus longs : `/blog/cancer-et-therapie-psychocorporelle/` (144), `/blog/la-premenopause-entre-40-et-50-ans/` (133), `/blog/stress-et-cancer-a-saint-nazaire/` (132). Aucun doublon de titre (bon point). Source : colonne `title_len` de `crawl.csv`. (Les titres des articles sont dans les 20 articles : à ne pas modifier sans accord, mais le suffixe peut être raccourci côté gabarit.)

### 4. Descriptions hors 120-160 caractères : 20 pages sur 36
Trop longues (coupées) : `/therapie-emdr-saint-nazaire/` (248), `/blog/la-psychologie-energetique/` (209), `/a-propos-emmanuelle/` (208), `/blog/emma-psychopraticienne-fr-patient-ressource-cancer/` (197), `/seance-eft-gestion-emotions/` (197). Trop courtes : `/blog/` (110), `/prendre-rendez-vous-saint-nazaire/` (110), `/blog/les-croyances-limitantes/` (118). Aucun doublon de description.

### 5. Plusieurs H1 sur 8 articles
`/blog/le-controle-coercitif/` a **17 balises H1** (chaque question du texte est un H1 dans le contenu, en plus du titre de page) ; 7 autres articles en ont 2 (`/blog/emdr-saint-nazaire/`, `/blog/la-therapie-ifs/`, `/blog/la-psychologie-energetique/`, `/blog/le-therapeute-energetique/`, `/blog/post-partum-saint-nazaire/`, `/blog/cancer-et-therapie-psychocorporelle/`, `/blog/emma-psychopraticienne-fr-patient-ressource-cancer/`). Cause : le texte Markdown de l'article commence par `#` alors que le gabarit pose déjà un H1. Correction possible dans le gabarit d'article (décaler d'un niveau) sans toucher au contenu d'Emmanuelle.

### 6. Pages qui se concurrent sur le même sujet (cannibalisation)
EMDR : `/therapie-emdr-saint-nazaire/`, `/blog/emdr-saint-nazaire/`, `/blog/comprendre-la-therapie-emdr-saint-nazaire/`. Post-partum : `/espace-soutien-post-partum/`, `/blog/le-post-partum/`, `/blog/post-partum-saint-nazaire/`, `/blog/espace-de-parole-post-partum-saint-nazaire/`. Cela peut expliquer en partie que « emdr saint nazaire » fasse sortir l'accueil et non la page EMDR (voir plan §5). À arbitrer avec Emmanuelle (fusion + 301, ou liens internes clairs vers la page principale).

### 7. Maillage interne faible vers les articles
Chaque article n'a qu'**un seul lien entrant** (celui de `/blog/`) ; les pages principales en ont 35 (menu/pied de page). Aucune page orpheline stricte, mais les articles ne se soutiennent pas entre eux ni ne remontent vers les pages de service. Source : colonne `internal_links_in`.

## 🟢 Correct (preuves)
- **robots.txt** : `Allow: /`, `Disallow: /admin/`, référence `https://emma-psychopraticienne.fr/sitemap-index.xml` (identique à `public/robots.txt`).
- **Sitemap** : `/sitemap-index.xml` → `/sitemap-0.xml`, 36 URL, **toutes en 200**, aucune redirection ni 404 dedans. `/merci/` et `/admin/` volontairement exclus (`astro.config` filtre). Le sitemap = les pages réelles, rien d'autre. Les anciennes URL redirigées (`/blog/comprendre-emdr`…) n'y sont pas, bien.
- **http → https** : 1 saut (301). **www → sans www** : 1 saut (301) pour `https://www…` ; **`http://www…` fait 2 sauts** (http→https www puis www→sans www), acceptable mais améliorable côté Netlify.
- **Slash final** : `/blog` → 301 → `/blog/` (1 saut, normal).
- **Page 404 personnalisée** : `/xyz-inexistant` renvoie bien un vrai code 404 avec la page « Page non trouvée | Emmanuelle Demeulemeester ».
- **Canoniques** : présentes sur les 36 pages, auto-référentes, sans www, avec slash final. Robots meta `index, follow` partout ; `/merci/` en `noindex, follow` (correct).
- **Open Graph** : og:title et og:image présents partout (`social-image.jpg` unique, voir note ci-dessous). 
- **Poids HTML** : max 108 Ko. 
- **Données structurées** : Organisation/adresse/horaires partout ; `FAQPage` sur 7 pages de service. Aucun JSON-LD `Article` sur les articles de blog (opportunité).
- **GSC « doublons sans canonique » (4)** et « redirection » (9) : non reproductibles depuis le site actuel (canoniques OK). Probablement des anciennes URL WordPress (`/accueil-2/`, `/eft-duplicate/`…) ou variantes d'URL ; à revérifier dans GSC après les 301 (sans liste d'URL on ne peut pas prouver).
- Note : toutes les pages partagent la même image Open Graph ; les partages sur réseaux sociaux auront tous la même vignette.

## Liens Calendly dans le code
Un seul fichier : `src/pages/prendre-rendez-vous-saint-nazaire/index.astro`
- ligne 45 : lien de repli `https://calendly.com/emma-psychopraticienne`
- ligne 50 : widget intégré `data-url="https://calendly.com/emma-psychopraticienne?hide_gdpr_banner=1"`
- ligne 51 : script `assets.calendly.com/assets/external/widget.js`

**Aucun UTM** (ni `utm_source`, ni `utm_medium`, ni `utm_campaign`) : confirmé. Les autres boutons du site mènent à `/prendre-rendez-vous-saint-nazaire/` (aucun autre lien calendly.com dans `src/`, hors contenu des articles où `grep` ne trouve rien non plus). Conséquence : Calendly ne peut pas distinguer les réservations venues du site. Piste : ajouter `utm_source=site&utm_medium=widget` aux deux URL (lignes 45 et 50), à faire par Nicolas.

## Limites de cette analyse
- Les clics/impressions des anciennes URL viennent du fichier GSC déjà préparé, non re-vérifiés.
- API archive.org : indisponible au premier essai, réussie au second ; elle ne renvoie que 44 URL (capture de mai 2026), donc d'autres anciennes URL peuvent exister (la liste GSC en complète 18).
- Les correspondances « moyenne/basse » sont des suppositions sur le sujet (je n'ai pas relu les anciens contenus WordPress, absents).
- Aucun fichier du site (`src/`, `public/`) n'a été modifié.

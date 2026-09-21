# Backlog qualité — site Emmanuelle Demeulemeester

> Établi le **20 septembre 2026** par une critique Impeccable menée par 5 agents
> indépendants (en aveugle les uns des autres), couvrant les 17 pages et les
> 8 composants du site.
>
> **État au 21 septembre 2026 : lots 1 à 4 faits et fusionnés sur `dev`.**
> Les cases cochées correspondent au travail réellement livré et relu.
> Le point d'entrée pour reprendre est [ETAT-DES-TRAVAUX.md](ETAT-DES-TRAVAUX.md) ;
> ce fichier-ci reste le détail des constats.

## Comment lire ce document

| Marque | Sens |
|---|---|
| `[ ]` / `[x]` | À faire / fait |
| **P0** | Grave — nuit activement à la crédibilité ou casse une fonction |
| **P1** | Important — dégrade l'expérience ou l'accessibilité |
| **P2** | Confort — dette technique, cohérence |
| ✅ **vérifié** | Contrôlé directement dans le code ou en production, pas seulement rapporté |
| 🔒 **bloqué** | Nécessite une information d'Emmanuelle — ne rien inventer |

**Recoupements** : quand plusieurs agents travaillant en aveugle signalent la même
chose, c'est noté `(n/5 agents)`. C'est le signal de gravité le plus fiable du rapport.

---

## Santé globale (heuristiques de Nielsen)

| Périmètre | Score | Fourchette normale |
|---|---|---|
| Parcours de conversion | 19/40 | 20-32 |
| Pages de format | 20/36 (≈22/40) | 20-32 |
| Approches + à-propos | 18/32 (≈22,5/40) | 20-32 |
| Blog + pages légales | **15/40** | 20-32 |

Tout le site est en bas de fourchette ou en dessous.

## Les 5 recoupements inter-agents

| Constat | Agents |
|---|---|
| Bouton d'action à 2,78:1 de contraste | **5/5** |
| Emoji employés comme système d'icônes | **5/5** |
| `prefers-reduced-motion` respecté nulle part | **5/5** |
| Palettes Tailwind étrangères à la charte | **4/5** |
| `MedicalBusiness` usurpé dans le JSON-LD | **3/5** |

---

# BLOC A — Crédibilité factuelle

> Rien d'esthétique ici : uniquement des faits faux ou des trous, **en ligne au
> 20/09/2026**. C'est le bloc qui porte le plus l'objectif « ne pas ressembler à
> un site généré ». Aucun de ces points n'entre en conflit avec l'audit technique.

### A1 — Témoignage fabriqué **P0** ✅ vérifié
- [x] `src/pages/seance-eft-gestion-emotions/index.astro:113-124`

« *Je souffrais d'anxiété généralisée depuis des années…* » — **« Sandrine T., après 4 séances. »**

« Sandrine T. » n'existe **nulle part** : absente des 5 avis réels de `src/data/config.js`
(Karine S., Mumu Shahata, viaud Stephane Nathalie, tyhia angama, Le Berre Valerie),
aucune autre occurrence dans le projet. Introduite au tout premier commit
(`6cf1407`, 24/01/2026) — texte de remplissage jamais remplacé.

La charte IFPEC **publiée sur le site lui-même** interdit les témoignages inventés :
le site se contredit. Et un prospect qui compare ira lire les avis Google ; l'écart
rend les 5 vrais avis suspects à leur tour.

**Correction** : supprimer le bloc. Le remplacer par un avis réel taggé `EFT` de
`config.js` (Karine S. ou Le Berre Valerie), avec mention « Avis Google ».

### A2 — Mentions légales à trous **P0** ✅ ⚠️ partiellement fait (crochets retirés ; assurance et médiateur en attente)
- [ ] `src/pages/mentions-legales/index.astro:88-89` et `:94-95`

Quatre champs de gabarit affichés en clair :
```
Souscrite auprès de : [À COMPLÉTER : Nom de l'assurance]
Numéro de contrat   : [À COMPLÉTER : Numéro]
L'entité de médiation retenue est : [À COMPLÉTER : Nom du médiateur, ex: CNPM Médiation]
Réclamation sur son site : [À COMPLÉTER : Site web du médiateur]
```
Sur la page que consulte précisément le prospect méfiant, et sur l'assurance RC Pro
— l'information qu'il était venu vérifier.

🔒 **Bloqué** : nécessite le nom + numéro de contrat de l'assurance, et le médiateur.
**À défaut : retirer les sections.** Une rubrique absente vaut mieux qu'un crochet affiché.

### A3 — Hébergeur déclaré faux **P0** ✅ vérifié
- [x] `src/pages/mentions-legales/index.astro:47-52`

« Ce site est hébergé par la société **Vercel Inc.** », Walnut CA.
Le site tourne sur **Netlify** (Netlify Forms, `identity.netlify.com`, git-gateway).
Mention légale obligatoire, inexacte.

**Correction** : Netlify Inc., 512 2nd Street, Suite 200, San Francisco, CA 94107.

### A4 — Google affiche de faux horaires **P0** ✅ vérifié en production
- [x] `src/layouts/MainLayout.astro:60-73`

| | Déclaré à Google | Affiché sur le site |
|---|---|---|
| Lundi | 9h – **19h** | 9h – **20h** |
| Mercredi | **ouvert** 9h-19h | **non mentionné** |
| Samedi | 9h – **12h** | 9h – **13h** |

Conséquence : un prospect appelle un mercredi (jour non travaillé), ou renonce à
appeler samedi à 12h30 en croyant que c'est fermé.

**Correction** : générer `openingHoursSpecification` **depuis `src/data/config.js`**
pour que les deux ne puissent plus diverger. Horaires réels : cabinet lundi-mardi
9h-20h ; visio + extérieur jeudi-vendredi 9h-18h, samedi 9h-13h.

### A5 — Le site se déclare établissement médical **P0** ✅ vérifié (3/5 agents)
- [x] `src/layouts/MainLayout.astro:31` et `:75`

```json
"@type": "MedicalBusiness",
"medicalSpecialty": ["EMDR", "EFT", "Psychopratique"]
```
Une psychopraticienne n'est pas un établissement médical. La page visio explique
elle-même que les séances ne sont pas remboursées par la Sécurité sociale : le site
affirme à Google l'inverse de ce qu'il dit à ses visiteurs. Risque déontologique IFPEC.

**Correction** : `ProfessionalService` ou `LocalBusiness`, suppression de
`medicalSpecialty`, ajout de `hasCredential` pour les deux certifications.

### A6 — « Bois Jolland » : le lieu est mal orthographié **P0** ✅ vérifié
- [x] 10 occurrences dans 2 fichiers

Le vrai nom est **Bois Joalland** (vérifié : office de tourisme de Saint-Nazaire,
étang de 44 ha creusé en 1918). Le site l'écrit correctement **une seule fois**
(`prendre-rendez-vous-saint-nazaire/index.astro:61`) et faux 10 fois.

Emplacements les plus coûteux :
- `therapie-en-marchant-saint-nazaire/index.astro:13-14` — `<title>` et meta description → **visible dans Google**
- `:184` — **l'URL de l'iframe Google Maps** cherche un lieu inexistant
- `:41, 160, 162, 170, 190, 274` — h2, corps, FAQ
- `prendre-rendez-vous-saint-nazaire/index.astro:72`

Tout Nazairien connaît ce parc. Le voir écorché dix fois signale que le contenu
n'a pas été écrit ni relu par quelqu'un de la région.

### A7 — Fautes de français **P0** ✅ vérifié
- [x] `src/pages/index.astro:51` — « je **choisi** avec vous » → *choisis* (2ᵉ paragraphe du hero)
- [x] `src/pages/index.astro:48` — « à mes côtés **,** » → espace avant virgule
- [x] `src/pages/index.astro:278` — « **Prête(e)** à faire le premier pas ? » → *Prêt(e)* (titre 36 px)
- [x] `src/pages/index.astro:213` — « plus **profonde** » → *profondes*
- [x] `src/pages/prendre-rendez-vous-saint-nazaire/index.astro:58` — « demandeurs d'**emplois** » → *emploi*

### A8 — Affirmations à risque déontologique **P0**
- [x] ~20 formulations relevées

La charte IFPEC interdit : promesse de guérison, claim médical, chiffre non sourcé.

| Fichier:ligne | Citation | Problème |
|---|---|---|
| `therapie-emdr:39` | « une méthode reconnue pour **guérir** les blessures » | promesse de guérison, en sous-titre H1 |
| `therapie-emdr:140-141` | « pour **guérir** un traumatisme ? » / « **3 à 5 séances suffisent souvent** » | guérison + chiffre non sourcé, **publié en JSON-LD FAQPage → extrait enrichi Google** |
| `therapie-emdr:85` | « mécanismes naturels d'**auto-guérison** » | claim mécanistique |
| `therapie-emdr:82` | « souvenirs **non digérés par le cerveau** » | mécanisme neurologique affirmé comme acquis |
| `therapie-emdr:132` | « la certification **garantit** une pratique rigoureuse » | une certification atteste, ne garantit pas |
| `therapie-emdr:145` | « Non, **jamais**. » | absolu sur une question clinique |
| `seance-eft:72` | « L'EFT : l'**acupuncture émotionnelle** » | emprunte une caution médicale (acte réservé en France), en H2 |
| `seance-eft:77` | « on **rééquilibre le système énergétique** » | effet physiologique affirmé |
| `seance-eft:101` | « douleurs **liées au stress** » | lien de causalité = acte diagnostique |
| `seance-eft:133` | « **souvent plus rapide** que… » | claim comparatif non sourcé |
| `seance-eft:141` | « **Absolument.** Les enfants sont très réceptifs… **efficace** pour… » | claim d'efficacité + public enfant non couvert par les certifications détenues |
| `index.astro:244` | « une méthode **validée scientifiquement** » | claim non sourcé |
| `seance-decouverte:78` | « **Toutes les études** en psychologie montrent » | absolu non sourcé |
| `therapie-en-ligne-visio:89` | « **Les études montrent** que la visio est aussi efficace » | non sourcé |
| `therapie-en-ligne-visio:186` | « résultats **comparables** au présentiel » | claim comparatif |
| `therapie-en-ligne-visio:47` | badge « **Disponible dès maintenant** » | urgence marketing qu'aucun système ne soutient |
| `therapie-en-marchant:87` | « **réduit le cortisol** (hormone du stress) » | claim physiologique chiffré |
| `therapie-en-marchant:77` | « **réduit la tension nerveuse** » | idem |
| `therapie-en-marchant:89` | « **Beaucoup de personnes accompagnées** trouvent que… » | témoignage agrégé implicite |
| `a-propos:33` | « d'une **efficacité remarquable** » | superlatif d'efficacité |
| `a-propos:38` | « **guérir** en profondeur » | récit personnel, mais installe le registre interdit |

**Principe de correction** : passer du registre de l'**effet** à celui du **processus**
(« vise à », « l'approche consiste à », « beaucoup de personnes décrivent »), supprimer
les chiffres de séances, remplacer « garantit » par « atteste de ».

### A9 — « Formation en psychothérapie » 🔒 **P0**
- [ ] `src/pages/a-propos-emmanuelle/index.astro:33`

« J'ai alors suivi deux années de **formation en psychothérapie** »

« Psychothérapeute » est un **titre protégé** en France (décret 2010-534). Les deux
certifications détenues sont « Psycho-Praticienne en Techniques Énergétiques et
Psycho-Corporelles » (IFPEC) et « Praticienne EMDR-DSA niveau 2 » (AHTMA).

🔒 **Bloqué — question à poser à Emmanuelle** : cette formulation décrit-elle
fidèlement sa formation ? Ne pas modifier une affirmation sur son parcours sans elle.

---

# BLOC B — Bugs réels

### B1 — Le fond du header n'existe pas **P0** ✅ vérifié dans le CSS livré
- [x] `src/components/Header.astro:10`

`bg-secondary/97` **n'est pas compilé par Tailwind 3** (opacité hors échelle).
Vérifié dans `dist/_astro/index.OQ3wuFSz.css` : seules les opacités
`/10 /20 /30 /40 /50 /60 /80 /90` existent.

Conséquence : **le header n'a aucun fond.** Sur les 6 pages à héros `bg-primary`,
le nom « Emmanuelle Demeulemeester » (`text-primary`) est à **1,00:1** — invisible.
D'où le `text-shadow: 0 0 15px rgba(255,255,255,1)` en style inline ligne 19 :
quelqu'un a rustiné le symptôme sans voir la cause. C'est l'origine du halo blanc
visible autour du nom.

**Correction** : `bg-secondary/95` (compilé) ou un token opaque dédié, **puis
supprimer le `text-shadow` inline** devenu inutile.

### B2 — Les articles sont invisibles sans JavaScript **P0** ✅ vérifié
- [x] `src/pages/blog/[slug].astro:53-57` (et `:29,47,62,73`, `blog/index.astro:35`)

Le CSS contient `[data-aos^=fade]{opacity:0}`. Le corps de l'article porte
`data-aos="fade-up"` : il part à `opacity: 0` et n'apparaît que si AOS s'initialise.
JS lent, bloqué ou en erreur → **page blanche sur un article**, qui est souvent la
première impression du site depuis Google.

**Correction** : retirer `data-aos` du contenu de lecture + règle globale
`@media (prefers-reduced-motion: reduce){[data-aos]{opacity:1!important;transform:none!important}}`.

### B3 — Sous-menus inaccessibles au clavier **P1** ✅ vérifié
- [x] `src/components/Header.astro:49` et `:75`

Panneaux en `opacity-0 invisible`, révélés uniquement par `group-hover`.
`visibility:hidden` retire les enfants de l'ordre de tabulation, et aucune variante
`group-focus-within:` n'existe.

**6 pages sur 17 — dont les 4 pages de format, l'argument différenciant n°1 —
sont inatteignables au clavier depuis la navigation principale.**

Aggravant : `aria-expanded="false"` codé en dur, jamais mis à jour (`:42`, `:67`).
Un lecteur d'écran annonce « réduit » en permanence.

**Correction** : ajouter `group-focus-within:` en complément du hover, un
gestionnaire JS qui bascule réellement `aria-expanded`, et fermeture sur `Escape`.

### B4 — Carrousel d'avis inarrêtable **P0** (WCAG 2.2.2) ✅ vérifié
- [x] `src/components/Reviews.astro:11,42-51`

`animation: scroll 40s linear infinite`. La pause au survol a été **retirée
volontairement** (commentaire ligne 46 : « Hover pause removed as requested »).
Aucun bouton pause, aucune règle `prefers-reduced-motion` (0 occurrence dans les
97 502 octets du CSS livré).

Deux aggravants :
- `Reviews.astro:13` — les 5 avis sont **dupliqués en 10 cartes** (`[...reviews, ...reviews]`)
  pour alimenter le défilement. Le visiteur voit le même avis passer deux fois :
  fabriquer du volume à partir de 5 avis réels déclenche le soupçon.
- `Reviews.astro:33-37` — **5 pastilles de pagination statiques, non cliquables,
  jamais mises à jour**. De la fausse UI décorative.

**Correction** : grille statique de 5 cartes (il n'y en a que 5), ou carrousel avec
bouton pause + pause au survol et au focus. Supprimer la duplication et les fausses pastilles.

### B5 — Classes d'un plugin non installé **P2** ✅ vérifié
- [x] `src/components/FaqSection.astro:33`

`animate-in fade-in slide-in-from-top-2` appartiennent à `tailwindcss-animate`,
**absent de `package.json`** et du CSS compilé. Ces classes ne font rien.

### B6 — Composant mort **P2** ✅ vérifié
- [x] `src/components/CardService.astro` — 77 lignes, **importé nulle part**.
  Contient un badge « Séance découverte 45 min offerte » codé en dur et une classe
  contradictoire `w-12 … w-0`.

### B7 — Collision d'URL **P1**
- [x] `src/content/blog/comprendre-emdr.md`

L'article déclare `slug: therapie-emdr-saint-nazaire`, donc il est servi sur
`/blog/therapie-emdr-saint-nazaire/` — quasi-jumeau de la page SEO
`/therapie-emdr-saint-nazaire/`. Même sujet, même intention : elles se cannibalisent.

---

# BLOC C — Signaux « fait à la va-vite »

### C1 — 79 emoji comme système d'icônes **P0** (5/5 agents) ✅ vérifié
- [x] 39 glyphes distincts, 13 fichiers

**Le signal n°1 pour l'objectif de crédibilité.** Aggravé par le fait que le site
charge **déjà** des dizaines de SVG inline propres (`Header`, `Footer`, `CardFormat`,
`FaqSection`, `Reviews`) : **deux systèmes d'icônes coexistent sans raison**.

Le rendu des emoji change selon l'OS : le site n'a pas la même identité visuelle
d'un visiteur à l'autre.

**Les plus coûteux** (emoji porteurs d'information, pas décoratifs) :

| Emoji | Fichier:ligne | Rôle | Remplacement Lucide |
|---|---|---|---|
| 🚶‍♀️ 💻 🛋️ 🤱 | `config.js:49,61,73,85` → affiché **56 px** | les 4 formats, page d'accueil | `footprints` `monitor` `armchair` `baby` |
| 👂 🤝 🌱 | `a-propos:98,103,108` (36 px) | les 3 valeurs | `ear` `handshake` `sprout` |
| 💳 🎓 🗓️ | `therapie-cabinet:172,184,195` + visio + marchant | **blocs tarifs** (dupliqués 3×) | `credit-card` `graduation-cap` `calendar-days` |
| 📍 🅿️ 🕘 📞 ✉️ | `therapie-cabinet:90-94` | coordonnées | `map-pin` `circle-parking` `clock` `phone` `mail` |
| 🧠 ✋ 💬 😮‍💨 🌱 👶 | `therapie-cabinet:148-153` | 6 prestations | `brain` `hand` `message-circle` `wind` `sprout` `baby` |
| 🇫🇷 | `therapie-en-ligne-visio:86` | **un drapeau national en puce de liste** | `globe` ou `map` |
| 🧠 ✋ | `index.astro:241,253` | cartes EMDR / EFT | `brain` `hand` |
| ✦ | `Header:91,138` · `Footer:64` · 6 pages | marqueur séance découverte | `sparkles` ou supprimer |
| 📅 👥 📍 👥 💚 | `espace-soutien-post-partum:95-130` | 5 faits pratiques (**👥 doublonné**) | `calendar` `users` `map-pin` `heart` |
| 🤝 👂 💡 🛡️ | `seance-decouverte:88-91` | 4 étapes | `handshake` `ear` `lightbulb` `shield` |
| 🌿 ↔️ 🚶 🔓 | `therapie-en-marchant:87-90` | 4 bénéfices | `leaf` `move-horizontal` `footprints` `lock-open` |

**Note** : les 48 emoji présents dans les articles de blog sont du contenu éditorial
d'Emmanuelle — **hors périmètre**, ne pas y toucher.

### C2 — 76 classes de palettes étrangères **P1** (4/5 agents) ✅ vérifié
- [ ] 8 familles Tailwind, alors que la charte en compte 7 tokens

| Famille | Occ. | Principaux fichiers |
|---|---|---|
| **gray** | 33 | `Header.astro` (8 → sur 17 pages), `mentions-legales` (6), `politique-de-confidentialite` (5), `prendre-rendez-vous` (4), `CardFormat` (3), `FaqSection` (2) |
| **emerald** | 15 | `index` (7), `config.js` (4), `therapie-en-marchant` (4) |
| **blue** | 15 | `index` (7), `therapie-en-ligne-visio` (5), `config.js` (3) |
| **rose** | 7 | `therapie-cabinet` (4), `config.js` (3) |
| **purple / indigo / orange / fuchsia** | 6 | `config.js` |

Deux foyers :
1. **`src/data/config.js:55-93`** — les 4 formats portent chacun un dégradé hors charte.
   C'est le bloc « Un format adapté à votre vie » de l'accueil — **l'argument de
   positionnement n°1** — rendu en quatre couleurs absentes du logo et de la carte de visite.
   Ces couleurs sont ensuite recopiées à la main dans 4 pages.
2. **`gray` (33 occ.)** — gris froid bleuté posé sur du crème `#FAF7F3` : écart de
   température visible. `secondary` et `text-muted` existent pourtant.

**Incohérence supplémentaire** : `config.js:91` annonce du `purple` pour l'Espace
Post-Partum sur la carte d'accueil, mais la page cible n'utilise **jamais** de violet.

### C3 — Composition dupliquée à la main **P2**
- [ ] Sur 6 variantes de `Button`, **`ghost` et `secondary` ne sont jamais utilisées**,
  pendant que les vraies CTA sont réécrites à la main :
  - `inline-flex … border-2 border-white/30 rounded-xl …` × **5**
  - `inline-flex … bg-white text-primary … rounded-full …` × **3**
- [ ] Eyebrow `text-accent font-bold tracking-wider uppercase text-sm` répété × **12**
- [ ] Titre `text-3xl font-serif font-bold text-primary mb-6` répété × **9**
- [ ] **Bloc tarifs complet dupliqué à l'identique × 3** (cabinet, visio, marchant)

→ toute correction de contraste ou de token doit être répétée dans 3 à 12 endroits.
Extraire `SectionHeading`, `PricingCard`, et une variante `Button` fantôme blanche.

### C4 — Images du blog **P1** ✅ vérifié
- [ ] `src/pages/blog/index.astro:36-43` — **34 Mo d'images** sur l'index (20 fichiers),
  sans `loading="lazy"`, sans `width`/`height`, hors pipeline Astro.
  Le `<img>` du logo dans le **même document** a tous ces attributs : la connaissance
  est dans le projet, elle n'a pas été appliquée ici.
- [ ] 14 des 20 couvertures sont en 1024×1536 / 1536×1024 / 2048×2048, PNG de 1,8 à 2,9 Mo
  — dimensions et format de sortie natifs des générateurs d'images, alors que le
  cabinet dispose de vraies photographies dans `src/assets/images/`.
- [ ] `public/images/uploads/istockphoto-1227064104-612x612.jpg` — nom de fichier de
  banque d'images brut, 612×408 affiché dans une colonne de 736 px → upscale visible.
- [ ] Ajouter une contrainte de poids dans `public/admin/config.yml` pour qu'Emmanuelle
  ne puisse plus téléverser 2,9 Mo.

### C5 — Structure de titres cassée **P1** ✅ vérifié
- [ ] `/blog/le-controle-coercitif/` rend **17 `<h1>`**
- [ ] **6 articles affichent leur titre deux fois** (le `#` du Markdown répète le titre
  du gabarit, en 48 px les deux) : `le-controle-coercitif`, `la-psychologie-energetique`,
  `la-therapie-ifs`, `post-partum-saint-nazaire`, `le-therapeute-energetique`,
  `cancer-et-therapie-psychocorporelle` (celui-ci avec un guillemet orphelin en fin de titre)

**Correction** : rétrograder les `h1` du Markdown en `h2` dans le gabarit (plugin rehype),
retirer le `#` de la barre d'outils Decap, nettoyer les 6 articles.

### C6 — Détecteur Impeccable **P2** ✅ vérifié (5 signalements, 0 faux positif)

> **partiellement — le `bounce-easing` est corrigé ; les 4 `border-l-4` relèvent du lot 5**
- [ ] `border-l-4` × 4 — `a-propos:46`, `mentions-legales:70`, `politique-de-confidentialite:39`, `therapie-emdr:129`
- [ ] `animate-bounce` × 1 — `prendre-rendez-vous:23` (rebond permanent, non protégé par reduced-motion)

---

# BLOC D — Accessibilité

### D1 — Contrastes en échec **P0** (5/5 agents) ✅ calculés
- [x] **14 combinaisons sous le seuil AA**

| Combinaison | Ratio | Où |
|---|---|---|
| **blanc sur `accent #C88D7D`** | **2,78:1** | **`Button.astro:16` — le bouton « Prendre RDV », sur les 17 pages** |
| `accent` sur `primary` | **1,71:1** | `Footer.astro:40,48,56,64,71` — titres de colonnes + lien séance découverte |
| `primary` sur `primary` | **1,00:1** | `Header.astro:19` — nom du cabinet, **invisible** (cf. B1) |
| `text-main` sur `primary` | 2,31:1 | `Header.astro:29` — nav sur les 6 pages à héros vert |
| `secondary/50` sur `primary` | 2,00:1 | `Footer.astro:11,83` — bloc légal, copyright |
| `secondary/80` sur `primary` | 2,85:1 | `Footer.astro:44,52,60` — **toute la navigation du pied de page** |
| `accent` sur `secondary` | 2,07:1 | `Header.astro:90` · `index.astro:42-45` — **2ᵉ ligne du H1 de l'accueil** |
| `text-secondary/50` sur `primary` | 2,00:1 | fil d'Ariane des 4 pages de format |
| `accent` sur blanc | 2,78:1 | horaires, liens d'articles, étoiles d'avis |
| `text-main/40` sur blanc | 2,14:1 | `Header.astro:121,144,155` — intitulés du menu mobile |
| `primary/60` sur blanc | 2,31:1 | `Header.astro:170` — téléphone mobile |
| `text-muted` sur `secondary/40` | 3,42:1 | tarif étudiant `therapie-cabinet:184` (12 px) |
| `primary` sur `background` | 4,45:1 | **échec de justesse** — tous les titres sur fond crème |
| `primary-light` sur blanc | 3,04:1 | coches `therapie-en-marchant:119` |

**Le constat central** : la couleur d'action de la marque, `#C88D7D`, **ne porte pas de
texte blanc**. Le bouton unique qui porte l'objectif unique du site échoue AA.

**Correction proposée** : assombrir la terracotta **pour l'usage bouton uniquement**
(`#A5604F` → 5,1:1 avec du blanc), en conservant `#C88D7D` de la carte de visite pour
les aplats, filets et pastilles. L'identité imprimée est préservée — c'est une
déclinaison, pas un remplacement.

**Aggravant systématique** : ce sont les **informations de cadre** qui sont les plus
pâles — tarif réduit, moyens de paiement, délai d'annulation, horaires. Or un cadre
illisible se lit comme un cadre dissimulé.

### D2 — `prefers-reduced-motion` nulle part **P0** (5/5 agents) ✅ vérifié
- [x] **0 occurrence** dans les 97 502 octets du CSS livré

- 106 attributs `data-aos`, `AOS.init()` sans option `disable`
- `animate-scroll` 40 s infini (`Reviews.astro`)
- 3 `animate-pulse` permanents (`index.astro:38`, `CardFormat.astro:36`, `CardService.astro:24`)
- 1 `animate-bounce` (`prendre-rendez-vous:23`)

En contradiction directe avec la contrainte inscrite dans `PRODUCT.md` — le public
inclut des personnes en détresse émotionnelle et en épuisement post-partum.

### D3 — Focus clavier invisible **P1** ✅ vérifié
- [x] `Header.astro:100` — `focus:outline-none` **sans aucun remplacement**
- [x] `Button.astro:11` — aucun style de focus sur **toutes les CTA du site**
- [x] `global.css` fait 17 lignes et ne contient **aucune règle `:focus-visible`**

### D4 — Menu mobile sans piège de focus **P1**

> **non traité — seul `Escape` a été ajouté ; le piège de focus du menu mobile reste ouvert**
- [ ] `Header.astro:188-198` — `openMenu()` ne déplace pas le focus, ne le piège pas,
  ne le restitue pas, ne gère pas `Escape`, pas d'`aria-modal`.
  Le focus reste derrière le panneau plein écran.

### D5 — Texte sous le plancher de 16 px **P1**
- [x] 31 `text-xs` (12 px) + nombreux `text-sm` (14 px)
- [x] **L'intégralité du pied de page** (coordonnées, adresse, navigation) est sous le
  plancher **et** à 2,0-2,9:1 de contraste, sur les 17 pages
- [x] `PRODUCT.md` fixe 16 px minimum pour le texte courant

### D6 — Longueur de ligne **P1** ✅ mesuré
- [x] Cible 65-75 caractères. Mesures réelles (métriques Lato embarquée) :

| Surface | Longueur de ligne | Écart |
|---|---|---|
| Article ≥1024 px | **93,9 car.** | +25 % |
| Mentions légales / Politique ≥768 px | **107,9 car.** | +44 % |
| Mêmes pages < 768 px | **112,5 car.** | +50 % |
| Article iPhone 375 | 41,7 car. | ✅ |

Cause : `blog/[slug].astro:54` applique `max-w-none`, ce qui **désactive explicitement**
le garde-fou natif du plugin typography (`.prose{max-width:65ch}`, présent dans le CSS).
Le garde-fou existait ; il a été retiré.

**Correction** : `max-w-[68ch]` sur le conteneur `prose`, `max-w-[70ch]` dans les pages légales.

- [x] Bonus : `[slug].astro:54` applique aussi `text-text-main/80`, ce qui délave le
  corps de **10,31:1 à 6,02:1**. Supprimer le `/80`.

### D7 — `alt` inexploitables **P2**

> **non traité — les `alt` et le lien d'évitement restent ouverts**
- [ ] Bonne nouvelle : **100 % des 22 images ont un `alt`**. Mais 4 sont à réécrire :
  - `therapie-emdr:48` — `alt="EMDR"` (un acronyme ne décrit pas une image)
  - `prendre-rendez-vous:42` — `alt="Portrait Emma"` (familier, incohérent avec le vouvoiement)
  - `a-propos:132` et `:140` — jugements de valeur (« apaisant », « bienveillant ») ; ces deux images sont décoratives → `alt=""`
- [ ] `blog/index.astro:40` — `alt={post.data.title}` répète le `<h2>` adjacent → `alt=""`
- [ ] Aucun lien d'évitement (« aller au contenu ») dans `MainLayout.astro`

---

# BLOC E — Parcours et conversion

### E1 — La séance découverte est enterrée à 3 clics **P0**
- [ ] L'**unique action de succès** du site.

- Bouton dominant = « Prendre rendez-vous » → **1 clic**, sans jamais dire que c'est gratuit
- Offre gratuite = pastille 14 px → page intermédiaire → Calendly → **3 clics**
- **Absente de `espace-soutien-post-partum`**
- Sur `/prendre-rendez-vous/`, elle apparaît en **4ᵉ paragraphe d'un bloc gris de 14 px**
- La FAQ (`seance-decouverte:165`) demande au visiteur de **« préciser qu'il souhaite
  la séance découverte »** dans un message libre

La hiérarchie est exactement inversée : le chemin le plus engageant est le plus court.

### E2 — Le calendrier Calendly n'a aucun état de repli **P0**
- [ ] `prendre-rendez-vous-saint-nazaire/index.astro:144-151`

Conteneur vide dans le HTML. Aucun message de chargement, aucun `<noscript>`, aucun
lien direct. Script tiers lent ou bloqué par un bloqueur de pub → le visiteur voit un
**rectangle blanc de 600 px** sous un titre qui promet un calendrier.

**Correction** : état par défaut visible en HTML statique (« Chargement du calendrier… »
+ lien direct vers `calendly.com/emma-psychopraticienne` + téléphone), que le widget recouvre.

### E3 — Hiérarchie inversée sur la page de conversion **P0**
- [ ] `prendre-rendez-vous:38, 93, 142` — **trois `<h2>` strictement identiques**.
  Le canal prioritaire (Calendly) est le **dernier**, le plus bas, le seul sans encadré.
  Le canal de repli (formulaire) occupe la moitié de l'écran d'arrivée.

### E4 — Zéro preuve de légitimité sur les 4 pages de format **P0**
- [ ] Vérifié par grep : **aucune occurrence** de IFPEC, AHTMA, « certifi… », « 360 h »,
  « 25 ans », « déontolog… », ni d'avis client dans le corps visible des 4 pages.
- [ ] 3 pages sur 4 n'ont **aucune photo d'Emmanuelle**
- [ ] Aucune ne lie vers `/a-propos-emmanuelle/` ni `/charte-deontologique/`

Le premier critère d'évaluation du prospect n'a rien à se mettre sous la dent.

### E5 — La page « À propos » n'a aucun appel à l'action **P0**
- [ ] `a-propos-emmanuelle:113-147` — la page se termine sur deux photos et le footer.
  C'est pourtant **la page où se décide la confiance**.

### E6 — Les certifications sont décoratives, pas probantes **P0**
- [ ] `a-propos:69-91` — texte à **12 px**, contrastes de **2,61:1** et **3,60:1**.
  La ligne « 360 h de formation · Institut Francophone de Psychologie Énergétique
  Clinique » — **la meilleure preuve disponible sur tout le site** — est le texte le
  plus difficile à lire de la page.
- [ ] Aucun lien vers ifpec.org ou AHTMA, aucun numéro d'attestation, aucun renvoi
  vers `/charte-deontologique/`
- [ ] `index.astro:200-201` — badge « IFPEC & AHTMA » : deux sigles nus, sans date,
  sans volume horaire. **« DSA » n'est développé nulle part sur le site.**
- [ ] `index.astro:67` — « 5 avis 5 étoiles » en texte brut, sans lien vers la fiche
  Google, sans logo, sans date. Un chiffre auto-déclaré sans source est **moins**
  crédible que pas de chiffre du tout.

### E7 — Contradictions visibles par le prospect **P1**
- [ ] **Deux politiques d'annulation sur la même page** : `therapie-cabinet:203`
  « annulation souhaitée 48 h à l'avance » vs `:229` (FAQ, 30 lignes plus bas)
  « peuvent être **facturées** selon les disponibilités ». Souhaitée ou facturée ? Combien ?
- [ ] **Trois délais de réponse** : « dans les plus brefs délais » (`index:280`),
  « sous 48 heures ouvrées » (`merci:32`), rien sur la page RDV
- [ ] **Trois mécanismes de réservation décrits sur une même page** (`visio:56`, `:108`, `:204`)
- [ ] **Sept libellés de CTA pour deux destinations**
- [ ] `therapie-cabinet:225` — « Le cabinet est-il accessible en transport ? — **Oui,
  le cabinet est accessible.** » Aucune ligne, aucun arrêt. Et « accessible » laisse
  croire qu'on va parler PMR (étage ? ascenseur ?), ce qui n'arrive jamais — alors que
  le public inclut des personnes en douleurs chroniques.

### E8 — La page post-partum contredit sa promesse **P1**
- [ ] `:49-51` CTA « **Je veux rejoindre le groupe** » → **Calendly de séance individuelle**
- [ ] `:95-99` et `:116-120` — deux cartes annoncent la **même fréquence**, l'une avec
  un intitulé bricolé (« Durée & Fréquence ») pour éviter le doublon d'étiquette
- [ ] `:102` et `:123` — **le même emoji 👥** pour deux cartes différentes
- [ ] `:130-134` — « **Gratuit** », l'argument le plus fort, en **6ᵉ et dernière position**,
  en `text-sm` gris
- [ ] `:112` et `:172` — « **à mon domicile** » sans adresse, alors que le cabinet
  professionnel existe avec adresse et photos
- [ ] `:98`, `:215` — « dates à confirmer » : 232 lignes pour un service sans aucune date

### E9 — Faux affordances **P1**
- [ ] `index.astro:159-169` — les **15 puces « épreuves »** ont `hover:border-accent/40`,
  `hover:shadow-md`, `group-hover:text-accent` — toutes les affordances d'un lien —
  et `cursor-default`. Un visiteur en post-partum cliquera sur « Post-Partum » ;
  il ne se passera rien, alors que `/espace-soutien-post-partum/` existe.

### E10 — Contenu de remplissage **P1**
- [ ] `index.astro:107-114` — une section entière `py-16` dédiée à « *Au milieu de
  toute difficulté se trouve cachée une opportunité* — Albert Einstein ». Citation
  d'attribution douteuse, sans rapport avec le cabinet, commentée `<!-- INTRO RASSURANTE -->`
  alors qu'elle ne rassure sur rien. **Marqueur canonique de la page générée.**
- [ ] `a-propos:96-112` — bloc « Mes Valeurs » : 3 emoji + 3 affirmations que
  n'importe quel praticien peut écrire et qu'aucun ne peut prouver.
  À ancrer dans des faits vérifiables, ou supprimer.

### E11 — Blog : 20 articles, aucun moyen d'en trouver un **P1**
- [ ] `blog/index.astro:33` — grille antéchronologique unique. Ni catégorie, ni tag,
  ni recherche, ni pagination. `src/content/config.ts:5-11` n'expose aucun champ
  permettant de trier.
- [ ] Aucun sommaire sur un article de 1 965 mots dont les 16 sous-titres sont
  **déjà des ancres `id=`**
- [ ] Aucun temps de lecture, alors que les articles vont de 160 à 1 965 mots
- [ ] Aucun article lié en fin de lecture
- [ ] `[slug].astro:40-42` — signature « Par Emmanuelle Demeulemeester » en italique
  gris à 3,46:1, sans photo, sans qualité, sans lien. **L'endroit le moins cher pour
  poser la légitimité sur la page qui est souvent la première impression du site.**

### E12 — La 404 laisse le visiteur sans navigation **P1** ✅ vérifié
- [ ] `404.astro:6-16` — **ni `<Header/>`, ni `<Footer/>`** (0 `<nav>`, 0 `<header>`,
  0 `<footer>` dans le build). Le visiteur perdu perd aussi le menu.
- [ ] Une seule issue proposée. Le « 404 » décoratif est à **1,24:1**.
- [ ] Sort avec `<meta name="robots" content="index, follow">`

### E13 — La charte déontologique n'est pas exploitée comme preuve **P1**
- [ ] `charte-deontologique/index.astro` — ne mentionne **ni la certification
  d'Emmanuelle, ni sa date, ni son inscription à l'annuaire IFPEC**, alors qu'elle
  cite en ligne 41 que « seuls les membres effectifs… peuvent figurer dans l'annuaire ».
  La preuve est décrite mais jamais apportée.
- [ ] Jargon institutionnel non traduit (« membres effectifs », « instances de l'IFPEC »)
- [ ] Ne mène nulle part : aucun lien vers `/a-propos-emmanuelle/` ni vers la séance découverte
- [ ] La ligne 44 (ne jamais suggérer d'interrompre un traitement médical) est le genre
  d'engagement qui rassure une personne en parcours oncologique — **noyée dans une liste à puces**

### E14 — Pages légales non datées **P2**
- [ ] Aucune des trois pages légales n'affiche de date de dernière mise à jour.

---

# BLOC F — Cohérence entre pages

### F1 — Les 4 pages de format divergent sans raison **P2**

| Élément | Divergence |
|---|---|
| Fond du hero | 3 pages `bg-primary`, post-partum **aucun** |
| Opacité de l'image | `100` / `40` / `25` / `35` — quatre recettes |
| Alignement | cabinet `items-center`, les 3 autres `justify-end` |
| Téléphone en hero | présent sur 3, **absent sur post-partum** |
| Pastille « 45 min offerte » | présente sur 3, **absente sur post-partum** |
| Titre de la FAQ | « Questions fréquentes » × 3, « **Foire Aux Questions** » sur post-partum |
| Fond de la section tarifs | `bg-background` × 2, `bg-secondary/30` × 1 |
| Libellé du CTA final | 4 pages, **3 verbes différents** |
| Liens inter-formats | **0, 0, 1, 0** — l'argument n°1 n'est pas maillé |

### F2 — Rythme des fonds cassé **P2**
- [ ] `therapie-en-marchant` — **trois sections crème consécutives** (`:155`, `:198`, `:220`),
  soit ~1 500 px sans aucune séparation : « Le lieu », « Pour qui » et « Tarifs » se
  collent en une masse indistincte.
- [ ] `therapie-en-ligne-visio` — `secondary/40` puis `secondary/30` : 10 % d'écart,
  frontière imperceptible, lit comme une erreur.
- [ ] `blog/index.astro:22` — `main` porte `bg-secondary/10` mais `body` porte
  `bg-secondary` → **10 % de beige sur du beige = beige plein**. Chaque ajustement
  d'opacité y est sans effet. Même problème sur la 404 (`bg-secondary/30`).

### F3 — Résidus **P2**
- [ ] `MainLayout.astro:126` — `theme-color: #3D5A4E`, couleur **hors charte** (le sauge
  est `#5C7A62`). Sur Android, la barre d'adresse affiche une couleur qui n'existe pas.
- [ ] `MainLayout.astro:135` — `netlify-identity-widget.js` chargé en `is:inline` sur
  **toutes les pages publiques**, alors qu'il ne sert qu'à `/admin`.
- [ ] `mentions-legales:30` — SIRET factice du template resté dans une ternaire
  (`siteInfo.siret === "123 456 789 00000" ? …`)
- [ ] `tailwind.config.mjs:31` — commentaire « Forcer la purge du cache **Vercel** »
  alors que le déploiement est sur Netlify
- [ ] `therapie-emdr:3` — import `illustration-emdr.jpg` **jamais utilisé**
- [ ] `therapie-en-ligne-visio:205` — ajoute `active:scale-95 transition-all` alors que
  `Button.astro:11` les applique déjà
- [ ] `Reviews.astro:7` — « Ce qu'**ils** disent » pour 4 avis sur 5 signés par des femmes
- [ ] `index.astro:75` — téléphone du hero en **texte brut non cliquable**, alors que
  le même numéro est un lien `tel:` partout ailleurs
- [ ] `merci/index.astro:41-44` — priorités inversées : « Retour à l'accueil » en
  `primary`, « Réserver un créneau » en `outline`
- [ ] `blog/index.astro:37,54,61` — **trois liens distincts vers la même URL** par carte

---

# BLOC G — Audit technique (mesures directes)

> Ajouté le 20/09/2026. Les 5 agents d'audit ont échoué sur une limite de session ;
> les dimensions **performance**, **thématisation** et **intégrité** ont été mesurées
> directement et sont fiables. Les dimensions **accessibilité fine** (ARIA, ordre de
> tabulation, formulaire) et **responsive détaillé** (bug du header, cibles tactiles)
> restent à couvrir par agent.

### G1 — Aucune image de partage sur tout le site **P0** ✅ vérifié
- [x] `src/layouts/MainLayout.astro:20` — `image = "/social-image.jpg"`

Le fichier **n'existe pas** : `public/social-image.jpg` absent, et
`https://emma-psychopraticienne.fr/social-image.jpg` renvoie **404**.
Les 17 pages utilisent cette valeur par défaut — **aucune ne passe d'image personnalisée**.

```
og:image      → /social-image.jpg  (404)
twitter:image → /social-image.jpg  (404)
```

Chaque partage sur WhatsApp, Facebook, LinkedIn ou iMessage affiche un bloc vide.
Pour un cabinet dont les patients se recommandent entre eux, c'est un canal entier
qui rend un rectangle cassé — et un lien sans vignette se lit comme un lien douteux.

**Correction** : produire une image de partage 1200×630 (portrait d'Emmanuelle +
nom + « Psychopraticienne · Saint-Nazaire »), la placer dans `public/`, et permettre
aux pages clés de passer la leur.

### G2 — Les 35 Mo d'images viennent uniquement de Decap **P0** ✅ mesuré

| Source | Poids total | Traitement |
|---|---|---|
| Pipeline Astro (`dist/_astro/`) | **1,4 Mo** | optimisé, WebP |
| Téléversements Decap (`public/images/uploads/`) | **35 Mo** | **aucun** |

Rapport de **25 pour 1**. Le pipeline du site fonctionne parfaitement.

| Page | Poids total (1re visite) |
|---|---|
| `/blog/` | **35 Mo** |
| Article type | 2 à 3 Mo |
| `/` (accueil) | 250 Ko |
| `/prendre-rendez-vous-saint-nazaire/` | 130 Ko |

11 PNG de 1,8 à 2,8 Mo dans `uploads/`.

**Le diagnostic n'est donc pas « les images sont lourdes » mais « les uploads Decap
court-circuitent le pipeline ».** Correction : faire passer `public/images/uploads/`
par `<Image>` d'Astro (ou une collection d'assets), recompresser l'existant en WebP,
et contraindre le poids dans `public/admin/config.yml`.

### G3 — Une seule classe Tailwind non compilée ✅ vérifié
- [x] Croisement des **79 classes de tokens** du source avec le CSS compilé :
  **`bg-secondary/97` est la seule** qui ne produit rien. Pas d'iceberg caché.
  (Le correctif reste à faire — voir B1.)

### G4 — 13 pages sur 36 ont une hiérarchie de titres cassée **P1** ✅ mesuré

> **Non traité — relève du CMS et du gabarit d'article, à prévoir avec le lot 6.**

| Page | Anomalie |
|---|---|
| `/blog/le-controle-coercitif` | **17 `<h1>`** (27 titres) |
| `cancer-et-therapie-psychocorporelle`, `la-psychologie-energetique`, `la-therapie-ifs`, `le-therapeute-energetique`, `post-partum-saint-nazaire` | 2 `<h1>` |
| 7 autres articles | sauts de niveau (h1→h3) |

**Toutes des pages de blog.** C'est le schéma de contenu qui ne contraint rien
(`src/content/config.ts`), pas le gabarit. Voir C5.

### G5 — 31 Mo d'images mortes versionnées **P2** ✅ vérifié
- [ ] `src/assets/images/unused/` — **12 Mo, 19 fichiers suivis par git**
- [ ] 5 images jamais référencées dans `src/` : `illustration-eft.jpg` (1,4 Mo),
  `img-soutien.jpg` (1,9 Mo), `cabinet-siege-bleu.png` (1,9 Mo),
  `cabinet-sieges-gris.png` (1,8 Mo), `portrait-manu.jpg` (0,2 Mo)

Le dépôt porte **31 Mo** d'images pour **1,4 Mo** réellement servis.

### G6 — Tarifs dupliqués en dur **P1** ✅ vérifié
- [ ] 60 € et 50 € écrits à la main dans 4 fichiers, jamais lus depuis `config.js` :
  `therapie-en-ligne-visio:139,144` · `therapie-en-marchant:231,236` ·
  `therapie-cabinet:177,182` · `prendre-rendez-vous:55,58`

**Les horaires ont déjà divergé de cette façon** (voir A4). Les tarifs suivront.

**Point rassurant** : téléphone, email et adresse sont correctement centralisés dans
`config.js` — **zéro duplication**. Le réflexe existe, il n'a simplement pas été
appliqué aux tarifs ni aux horaires.

### G7 — Poids des bundles ✅ mesuré
- CSS : **95,2 Ko** · JS : **14,2 Ko**. Corrects pour un site de cette taille.
  Le JS est presque entièrement AOS, dont l'utilité est discutable (voir D2).

---

# ⚠️ Bloqué — informations à obtenir d'Emmanuelle

| # | Information | Pourquoi |
|---|---|---|
| 1 | **Assurance RC Pro** : nom + n° de contrat | A2 — sinon retirer la section |
| 2 | **Médiateur de la consommation** : nom + site | A2 — sinon retirer la section |
| 3 | La formulation « **formation en psychothérapie** » est-elle exacte ? | A9 — titre protégé |
| 4 | **Tarif du premier rendez-vous d'1 h** | Absent du site ; seul celui des séances suivantes (60 €) est affiché. Signalé comme non tranché dans `PRODUCT.md` |
| 5 | Dates réelles du groupe post-partum | E8 — « à confirmer » depuis l'origine |

---

# ✅ Ce qui fonctionne — ne pas casser

- **`src/pages/politique-de-confidentialite/index.astro`** — concrète et nominative
  (Google Meet nommé, 3 ans CNIL vs 10 ans factures, « je suis la seule destinataire »,
  ni compte ni newsletter ni paiement en ligne). **Visiblement écrite, pas générée.
  C'est le modèle sur lequel aligner les deux autres pages légales.**
- **`therapie-en-marchant:105-152`** — « Ce que l'on fait, et ne fait pas, en marchant ».
  Avouer une limite est le signal de sérieux le plus efficace du site. **Devrait être
  le patron rédactionnel des autres pages.**
- **`therapie-emdr:41-45` et `seance-eft:38-42`** — encadré « Comment ça fonctionne
  chez Emmanuelle » : désamorce l'auto-prescription. Du soin, pas du marketing.
- **`src/pages/merci/index.astro`** — une seule carte, une action claire, un engagement
  chiffré et tenable. Zéro décoration parasite.
- **`blog/[slug].astro:62-70`** — CTA de fin d'article, présent sur les 20 articles,
  unique, formulation prudente et conforme.
- **`prendre-rendez-vous:50-85`** — bloc « Informations Pratiques » : le meilleur actif
  de crédibilité du site. Seul tort : présenté en gris 14 px.
- **`seance-decouverte:111-127`** — déroulé en 4 étapes, dont une étape 04 qui rend
  explicitement la décision au visiteur.
- **`FaqSection.astro:31-43`** — `<details>/<summary>` natif : accessible par
  construction, JSON-LD généré depuis les mêmes données que l'affichage.
- **Les tokens** — `tailwind.config.mjs:6-23` reprend exactement les 7 couleurs de
  l'imprimé. **La fondation n'est pas à refaire : le travail est de la faire respecter.**
- **Le socle sémantique** — un `<h1>` unique par page, `lang="fr"`, `aria-label` sur les
  `<nav>`, canonical dérivée d'`Astro.site`, `alt` présent sur 100 % des 22 images.
- **Typographie de l'article** — 18 px / interligne 1,78, au-dessus de la barre pour un
  public de 40-60 ans. Il ne manque que la largeur de colonne.

---

*Ce backlog est la sortie de `/impeccable critique`. L'audit technique
(`/impeccable audit`) viendra le compléter sur l'accessibilité, la performance et le
responsive avant la session de correction.*

---

# 🗺️ PLAN DE CORRECTION — 7 lots

> Ordonnés par **rapport impact / risque**, pas par facilité.
> Chaque lot est indépendant : on peut s'arrêter après n'importe lequel.

| Lot | Titre | Points | État |
|---|---|---|---|
| 1 | Arrêter de dire des choses fausses | A1→A8, G1 | ✅ fusionné — **A2 et A9 attendent Emmanuelle** |
| 2 | Réparer ce qui est cassé | B1→B7, G3 | ✅ fusionné |
| 3 | Rendre le site lisible | D1, D2, D3, D5, D6 | ✅ fusionné |
| 4 | Remplacer les emoji par de vraies icônes | C1 | ✅ fusionné |
| **5** | **Unifier les couleurs** | C2, C6, F1, F2, F3 | **⬜ prochaine étape** |
| 6 | Alléger | G2, G4, G5, C4, C5 | ⬜ à faire |
| 7 | Réparer le parcours de conversion | E1→E14 | ⬜ **attend l'accord d'Emmanuelle** |

**Restent ouverts hors lots :** D4 (piège de focus du menu mobile), D7 (`alt` et
lien d'évitement), C3 (composition dupliquée), E7→E14 (contradictions, blog, 404,
charte déontologique).

## Lot 1 — Arrêter de dire des choses fausses
**Ce qu'on fait** : supprimer le faux témoignage · retirer ou remplir les `[À COMPLÉTER]` ·
corriger l'hébergeur (Vercel → Netlify) · générer les horaires depuis `config.js` ·
passer `MedicalBusiness` → `ProfessionalService` · corriger « Jolland » → « Joalland »
(10×, dont l'URL de la carte) · corriger les 5 fautes de français · reformuler les
~20 affirmations à risque déontologique · créer l'image de partage.

**Pourquoi d'abord** : ce sont des faits faux, en ligne, qui sapent une crédibilité
par ailleurs réelle. Aucun risque visuel — on ne touche qu'à du texte et du balisage.

🔒 **Bloqué partiellement** : assurance, médiateur, et la formulation « psychothérapie ».

## Lot 2 — Réparer ce qui est cassé
`bg-secondary/97` → `/95` + suppression du `text-shadow` rustine · retirer `data-aos`
du corps des articles · `group-focus-within` sur les sous-menus + `aria-expanded` réel +
`Escape` · carrousel d'avis : grille statique ou bouton pause · supprimer `CardService.astro`
et les classes du plugin absent · résoudre la collision d'URL `/blog/therapie-emdr-saint-nazaire/`.

## Lot 3 — Rendre le site lisible
Décliner un terracotta foncé pour les boutons (`#A5604F`, 5,1:1) **en gardant `#C88D7D`
pour les aplats** · corriger les 14 contrastes sous AA · plancher à 16 px pour le cadre
(tarifs, horaires, annulation) · `max-w-[68ch]` sur les articles, `[70ch]` sur les pages
légales · ajouter `prefers-reduced-motion` global · anneau de focus visible partout.

## Lot 4 — Remplacer les emoji par de vraies icônes
79 emoji → jeu Lucide unique, trait 1,5 px, en `currentColor`. Correspondances déjà
établies dans le bloc C1. **Ne pas toucher aux 48 emoji des articles** (contenu éditorial).

## Lot 5 — Unifier les couleurs
Les 4 formats déclinés sur la charte au lieu de emerald/blue/rose/purple · les 33 `gray`
→ `secondary` / `text-muted` · rythme de fonds unifié sur les 4 pages de format ·
`theme-color` → `#5C7A62` · résidus (`netlify-identity` hors `/admin`, SIRET factice,
commentaire Vercel, import mort).

## Lot 6 — Alléger
Faire passer les uploads Decap par le pipeline Astro · recompresser les 35 Mo en WebP ·
`loading="lazy"` + dimensions sur l'index blog · contrainte de poids dans Decap ·
supprimer les 31 Mo d'images mortes du dépôt.

## Lot 7 — Réparer le parcours de conversion
**Le plus délicat : il change ce qu'Emmanuelle connaît de son site.** À valider avec elle.
Remonter la séance découverte en action principale · état de repli pour Calendly ·
inverser la hiérarchie de la page rendez-vous · bande de réassurance (certifications +
avis) sur les 4 pages de format · CTA en fin de page « À propos » · rendre les
certifications lisibles et vérifiables.

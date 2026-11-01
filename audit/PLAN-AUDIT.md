# Plan d'audit SEO + GEO — site d'Emmanuelle

> Version finale du 1er nov. 2026. Ce fichier sert de passation : un agent qui le lit doit pouvoir mener l'audit sans autre contexte.
> Version visuelle : https://claude.ai/artifact/8KGLVLVGut7bv4Ax6RRFTV (copie locale : `audit/plan-audit.html`).

## 1. Contexte

- Site : https://emma-psychopraticienne.fr (sans www). Emmanuelle Demeulemeester, psychopraticienne à Saint-Nazaire. Objectif unique du site : réserver la séance découverte gratuite de 45 min (Calendly).
- Commanditaire : Nicolas (son neveu, qui a refait le site). Lectrice du livrable : **Emmanuelle**, non technique.
- Historique : WordPress chez Hostinger jusqu'à juin 2026, puis Astro sur Netlify, même domaine. DNS chez Hostinger.
- Lire d'abord : `CLAUDE.md` (règles du projet), `PRODUCT.md` (cible, offre).

## 2. Les questions d'Emmanuelle (la colonne vertébrale du livrable)

| Question | Source | Attention |
|---|---|---|
| Combien de vues sur le site ? | Netlify Analytics si activé, sinon GSC | GSC = impressions et clics venus de Google seulement. Si aucun outil de visites, le dire clairement. |
| Quelles pages sont vues ? | GSC Pages | Avant / après la refonte |
| Quels mots tapés pour la trouver ? | GSC Requêtes | Google masque les requêtes rares |
| Quels articles du blog sont les plus vus ? | GSC Pages filtré sur les articles | Top 5 + ceux jamais vus |
| Sa place à Saint-Nazaire sur EFT et EMDR ? | GSC (position moyenne) + Semrush + captures Google et Maps réelles | La place varie selon l'appareil et le lieu |
| Bonus : séances réservées | Calendly | Pas de provenance (voir §6) |

Ensuite seulement : avant/après refonte, concurrents (gros morceau), GEO, technique.

## 3. Périodes

- **AVANT** (WordPress) : 17 janv. → 7 juin 2026 (142 j)
- **APRÈS** (Astro) : 8 juin → 27 oct. 2026 (142 j). Arrêt avant la panne DNS/SSL du 28 oct.
- **Contrôle saisonnier** : 1 juil. → 27 oct. 2025 contre la même fenêtre 2026
- Date de bascule = hypothèse tirée de git (gros lot le 8 juin, sitemap le 13 juin). À confirmer par Netlify Deploys (capture D1).
- Comparer par semaine ou par mois, jamais par jour. Volumes faibles (~28 clics/mois) : parler de tendance, pas de preuve.

## 4. Rangement des données

```
audit/
├─ PLAN-AUDIT.md          ce fichier
├─ plan-audit.html        version visuelle
├─ data/                  ignoré par git (.git/info/exclude) — données brutes
│  ├─ gsc/16-mois/            ✅ reçu (Graphique = jour par jour, Pages, Requêtes, Pays, Appareils)
│  ├─ gsc/avant/              ❌ à recevoir (A2)
│  ├─ gsc/apres/              ❌ à recevoir (A3)
│  ├─ gsc/saison-2025/        ❌ optionnel (A4)
│  ├─ gsc/indexation-toutes-pages/  ✅ reçu
│  ├─ gsc/indexation-sitemap/       ✅ reçu
│  ├─ calendly/               ✅ comptes anonymes par mois (aucun nom)
│  ├─ semrush/                ✅ 12 mots-clés FR du 01/11
│  ├─ pagespeed/  concurrents/  geo/  netlify/  google-business/  captures/
├─ analyses/              notes et tableaux intermédiaires
└─ livrable/              HTML source + PDF final
```

Règle : chaque chiffre du livrable renvoie à un fichier de `data/`. Ce qui n'a pas pu être vérifié est écrit « non vérifié ».

## 5. Déjà constaté (1er nov.)

- GSC 16 mois : 441 clics, 7 510 impressions, CTR 5,9 %, position moyenne 13,7. Mobile : position 7,2 ; ordinateur : 24,4.
- Requêtes : « emmanuelle demeulemeester » 35 clics ; « emdr saint nazaire » 17 clics, 652 impressions, position 8,7 ; EFT quasi absent.
- Pages : l'accueil fait 303 clics sur 441.
- **Indexation : 53 pages en 404**, 9 redirections, 17 « explorée non indexée ». Probablement les anciennes URL WordPress sans redirection 301 : piste n°1 de la migration.
- Semrush : « emdr saint nazaire » 12e (c'est l'accueil qui sort, pas la page EMDR). EFT hors top 100. 9 mots-clés sur 12 viennent de l'article sur l'attachement. Authority Score 2, 7 domaines référents, santé 93 % (8 erreurs, 34 avertissements).
- Calendly : 136 rendez-vous depuis sept. 2025. Types renommés le 3 sept. 2026 (regrouper « 1er rendez-vous… » + « Séance découverte… » sous « premier contact »). Premiers contacts non annulés par mois de séance : 2025-09 : 2, 10 : 0, 11 : 3, 12 : 6, 2026-01 : 7, 02 : 3, 03 : 3, 04 : 2, 05 : 0, 06 : 1, 07 : 1, 08 : 2, 09 : 2, 10 : 4.
- Les liens Calendly du site n'ont **aucun UTM** : impossible de savoir quelles réservations viennent du site. Ce sera une action du rapport.
- Tarif visible dans Calendly : séance individuelle 1 h = 60 €.

## 6. Déroulé

1. **Captures** : demander à Nicolas tout ce qui manque (§9), d'un seul coup, groupé par outil.
2. **Collecte seule** : crawl du site en ligne (titres, descriptions, H1, données structurées, maillage, robots.txt, sitemap) ; liste des 53 URL 404 → test des redirections ; anciennes URL WordPress via archive.org ; sites des concurrents.
3. **Analyses** : réponses aux 5 questions → avant/après → concurrents → blog (lecture seule) → local → GEO → technique.
4. **Histoire** : un fil : où on est trouvé, où on perd des visiteuses avant la séance découverte, quoi faire en premier.
5. **Livrable** (§8), puis relecture par Nicolas.

## 7. Concurrents retenus (thèmes et statuts différents)

| Nom | Site | Pourquoi |
|---|---|---|
| Morgane Houarner | morgane-houarner-therapeute.fr | Leader SEO Semrush, EMDR local (trafic estimé 44) |
| Laurence Martin | à trouver via Semrush | EMDR local (30) |
| Marie-Noëlle Guégan-Leblanc | à trouver | Recherches locales (3) |
| Laure Sablé | à trouver | Zone voisine (Guérande) |

Vérifier ville et statut de chacun avant analyse. Grille identique pour tous : place Google sur EMDR / EFT / psychopraticienne Saint-Nazaire ; Google Maps (top 3, avis, note) ; pages (une par méthode ou ville, FAQ, prix) ; blog ; liens entrants ; citations par les IA. Objectif : **ce qu'ils font de mieux**, et ce qu'Emmanuelle peut copier.

## 8. Livrable

- **PDF aux couleurs du site**, avec des graphiques compréhensibles. Source HTML dans `audit/livrable/`, PDF généré par Chrome en mode sans fenêtre (`--headless --print-to-pdf`), sans nouvelle dépendance.
- Charte (`tailwind.config.mjs`) : sauge `#5C7A62`, sauge profond `#3D5A4E`, beige sable `#EBDCCC`, fond `#FAF7F3`, terracotta `#C88D7D` (aplats uniquement, jamais sous du texte blanc), terracotta profond `#9A5849` (texte), anthracite `#2C3E50`. Polices : Playfair Display (titres), Lato (texte).
- Structure : 1 page de verdict · ses 5 réponses · avant/après en 2 courbes · face aux 4 concurrents · ce que disent les IA · 5 actions maximum, classées · glossaire de 6 mots.
- Ton : tutoiement ou vouvoiement à demander à Nicolas. Zéro jargon sans traduction.

## 9. Ce qui manque encore (à demander au lancement)

| ID | Quoi | Où | Prio |
|---|---|---|---|
| A2 | Export GSC AVANT 17/01 → 07/06/2026 | Performances → dates personnalisées → Exporter CSV | bloquant |
| A3 | Export GSC APRÈS 08/06 → 27/10/2026 | idem | bloquant |

> Pourquoi A2/A3 malgré l'export 16 mois : `Graphique.csv` est jour par jour, donc les **totaux** (clics, impressions) se coupent par période. Mais `Pages.csv` et `Requêtes.csv` sont des totaux sur 16 mois : impossible de savoir quelles pages ou quels mots-clés ont progressé entre avant et après sans un export par période.
| A4 | Export GSC 01/07 → 27/10/2025 | idem | utile |
| A7 | Core Web Vitals mobile + ordinateur | GSC → Expérience | utile |
| A8 | Liens : sites externes + pages les plus liées | GSC → Liens | utile |
| A9 | Annotation « 1 » sur le graphique vers le 9 mai 2026 | survol + capture | bonus |
| A10 | Rapport IA générative | bandeau sous Performances | bonus |
| B0–B4 | Semrush : solde d'unités, audit de site, suivi de position, concurrents, domaines référents | **l'agent les lit lui-même dans l'interface Semrush via Chrome** (0 unité) ; MCP seulement pour ce que l'interface ne montre pas | — |
| C1 | D'où viennent ses patientes (question à Emmanuelle) | message | utile |
| C3 | Google « EMDR Saint-Nazaire » et « EFT Saint-Nazaire » + Maps | **l'agent le fait dans Chrome**. Limite : Google adapte les résultats au lieu de connexion ; le nom de la ville dans la requête limite l'écart. À signaler dans le rapport. | — |
| D1 | Netlify Deploys : premier déploiement production de juin | Netlify | bloquant |
| D2 | Netlify Forms : messages par mois, **noms et messages masqués** | Netlify | utile |
| D3 | Netlify Analytics activé ou non | Netlify | bloquant |
| D4 | Le WordPress existe-t-il encore chez Hostinger ? | Hostinger | utile |
| E1 | Fiche Google Business Profile : existe ? catégories, avis, note | Google | bloquant |
| E2 | Google Business : performances 6 mois | Google | utile |
| E3 | Annuaires où elle est listée | texte | bonus |

Les captures vont dans `audit/data/captures/`, les exports dans le sous-dossier prévu.

## 10. Règles pendant l'audit

- Aucune modification du site ni des 20 articles de `src/content/blog/`. Rien sur `main`. Aucun commit sans demande.
- Aucune nouvelle dépendance ni service payant. Aucun secret dans le chat ni le dépôt.
- **Semrush** : unités limitées (essai). `resource_organic` 12 lignes = 220 unités ; `list_projects` = 400. Lister les appels prévus et leur coût estimé avant de lancer ; préférer les captures. Projet Semrush : 31820446 (Suivi de position + Audit de site activés).
- **Calendly** : lecture seule, compter sans jamais recopier noms, e-mails ou téléphones.
- **Chrome** : autorisé à piloter le Chrome de Nicolas pendant son absence (PageSpeed Insights sur la bonne URL sans www, tests GEO sur ChatGPT, Perplexity, Gemini, Google). Ne jamais cliquer sur un bouton qui ouvre une boîte de dialogue.
- Un outil bloque deux fois → s'arrêter, noter la question pour Nicolas.

## 11. Tests GEO

Environ 20 questions × 4 IA (ChatGPT, Perplexity, Gemini, Google Aperçu IA / Mode IA), 2 essais chacune. Noter : Emmanuelle citée ? quelle page ? quels concurrents ? quelles sources ? Résultats dans `audit/data/geo/` (tableau + captures).
Familles : local direct (psychopraticienne Saint-Nazaire, La Baule, Guérande) · méthodes (EMDR, EFT, psychocorporel) · formats (en marchant, visio) · spécialités (post-partum, cancer) · question en langage de patiente.

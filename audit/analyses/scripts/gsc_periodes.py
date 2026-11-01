"""Analyse GSC avant / après la refonte (exports par période).
Lancer depuis la racine du projet : python3 -I audit/analyses/scripts/gsc_periodes.py
Sorties : audit/analyses/05-gsc-avant-apres.md et audit/analyses/gsc-periodes.csv
(le CSV alimente audit/livrable/build.py : aucune valeur n'est recopiée à la main)."""
import csv, re, os, unicodedata, urllib.parse, datetime as dt, collections

G = 'audit/data/gsc/'; O = 'audit/analyses/'
PER = {'avant': G + 'avant/', 'apres': G + 'apres/'}
DOM = 'https://emma-psychopraticienne.fr'

def rd(p, f):
    with open(p + f, encoding='utf-8') as fh:
        return list(csv.DictReader(fh))
def fl(s): return float(s) if s not in ('', None) else None
def deacc(s): return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')
def fr(n, d=0):
    s = f"{n:,.{d}f}".replace(',', ' ').replace('.', ',')
    return s
def wavg(items):  # items = [(impr, pos)]
    i = sum(a for a, b in items if b is not None)
    return sum(a * b for a, b in items if b is not None) / i if i else None

# ---------- 1. Totaux (Graphique.csv) ----------
tot = {}
for k, p in PER.items():
    rows = rd(p, 'Graphique.csv')
    c = sum(int(r['Clics']) for r in rows); i = sum(int(r['Impressions']) for r in rows)
    pos = wavg([(int(r['Impressions']), fl(r['Position'])) for r in rows])
    tot[k] = dict(jours=len(rows), debut=rows[0]['Date'], fin=rows[-1]['Date'], clics=c, impr=i, ctr=c / i, pos=pos)
REF = dict(avant=(133, 2550, 15.6), apres=(202, 3364, 13.3))  # chiffres de 01-gsc.md
ecarts = []
for k in PER:
    t = tot[k]; rc, ri, rp = REF[k]
    if t['clics'] != rc or t['impr'] != ri or round(t['pos'], 1) != rp:
        ecarts.append(f"{k} : exports {t['clics']} clics / {t['impr']} impr. / pos. {t['pos']:.1f} contre 01-gsc.md {rc} / {ri} / {rp}")

# ---------- 2. Pages ----------
def path(u): return urllib.parse.unquote(urllib.parse.urlparse(u).path).strip('/')
PAGES = {k: [(path(r['Pages les plus populaires']), int(r['Clics']), int(r['Impressions']), fl(r['Position']))
             for r in rd(p, 'Pages.csv')] for k, p in PER.items()}
sums = {k: (sum(x[1] for x in v), sum(x[2] for x in v)) for k, v in PAGES.items()}

# groupes de pages (hors articles /blog/) : ancienne URL WordPress + nouvelle URL du même sujet
PG = {
 'Accueil': [''],
 'Tarifs et modalités': ['tarifs-et-modalites-de-prise-de-rendez-vous'],
 'Cercle de parole': ['cercle-de-parole-saint-nazaire'],
 'Préménopause (page)': ['premenopause-saint-nazaire'],
 'Injonctions faites aux femmes': ['les-injonctions-faites-aux-femmes-quand-le-sois-toi-meme-deviens-un-labyrinthe'],
 'Contact': ['contact'],
 'Thérapie IFS (page)': ['therapie-ifs-saint-nazaire'],
 'EFT (ancienne → nouvelle page)': ['eft-saint-nazaire', 'eft', 'seance-eft-gestion-emotions'],
 'EMDR (ancienne → nouvelle page)': ['emdr-saint-nazaire', 'emdr', 'therapie-emdr-saint-nazaire'],
 'Séance découverte psychocorporelle (renommée)': ['seance-decouverte-gratuite-therapie-psychocorporelle-saint-nazaire', 'seance-decouverte-therapie-psychocorporelle-saint-nazaire'],
 'Thérapie en marchant (page)': ['la-therapie-en-marchant-saint-nazaire', 'therapie-en-marchant-saint-nazaire'],
 'Post-partum (page)': ['post-partum-saint-nazaire', 'espace-soutien-post-partum'],
 'Prendre rendez-vous': ['prendre-rendez-vous-saint-nazaire'],
 'Index du blog': ['blog'],
}
p2g = {p: g for g, ps in PG.items() for p in ps}
def pgroup(per):
    d = collections.OrderedDict()
    for p, c, i, pos in PAGES[per]:
        if p.startswith('blog/'): continue
        g = p2g.get(p, '/' + p + '/')
        x = d.setdefault(g, dict(c=0, i=0, items=[], urls=[]))
        x['c'] += c; x['i'] += i; x['items'].append((i, pos)); x['urls'].append(p)
    for x in d.values(): x['pos'] = wavg(x['items'])
    return d
PGR = {k: pgroup(k) for k in PER}

# ---------- 3. Requêtes ----------
QRY = {k: [(r['Requêtes les plus fréquentes'], int(r['Clics']), int(r['Impressions']), fl(r['Position']))
           for r in rd(p, 'Requêtes.csv')] for k, p in PER.items()}
FAM = [  # l'ordre compte : une requête compte dans chaque famille qu'elle contient
 ('nom (demeul…, emmanuel…)', r'demeul|demeules|demeulester|emmanuel'),
 ('emdr', r'emdr'),
 ('eft', r'\beft\b|emotional freedom'),
 ('psychopraticien(ne)', r'psychopraticien'),
 ('saint nazaire / st nazaire', r'saint[ -]?nazaire|st nazaire'),
]
def fam(per, rx):
    s = [q for q in QRY[per] if re.search(rx, q[0], re.I)]
    return dict(n=len(s), c=sum(q[1] for q in s), i=sum(q[2] for q in s), pos=wavg([(q[2], q[3]) for q in s]))
def autres(per):
    s = [q for q in QRY[per] if not any(re.search(rx, q[0], re.I) for _, rx in FAM)]
    return dict(n=len(s), c=sum(q[1] for q in s), i=sum(q[2] for q in s), pos=wavg([(q[2], q[3]) for q in s]))
def qget(per, name):
    for q in QRY[per]:
        if q[0] == name: return q
    return None
qvis = {k: (sum(q[1] for q in v), sum(q[2] for q in v)) for k, v in QRY.items()}

# ---------- 4. Articles de blog ----------
def nz(s): return re.sub(r'[^a-z0-9]+', '-', deacc(urllib.parse.unquote(s)).lower()).strip('-')
ART = {}  # slug -> (clé de regroupement, titre)
KEYS = {}  # nz(...) -> slug
for fn in sorted(os.listdir('src/content/blog')):
    t = open('src/content/blog/' + fn, encoding='utf-8').read()
    m = re.search(r'^slug:\s*(.+)$', t, re.M); sl = m.group(1).strip().strip('"\'')
    m2 = re.search(r'^title:\s*(.+)$', t, re.M); ti = m2.group(1).strip().strip('"\'')
    ART[sl] = ti
    base = fn[:-3]
    for k in {nz(sl), nz(base), nz(re.sub(r'^\d{4}-\d{2}-\d{2}-', '', base))}: KEYS[k] = sl
WP = {  # ancienne URL WordPress à la racine -> article actuel du même sujet (regroupement signalé)
 'comprendre-le-lien-dattachement-et-ses-blessures-durables': 'comprendre-le-lien-d-attachement-et-ses-blessures-durables',
 'les-croyances-limitantes': 'les-croyances-limitantes',
 'therapeute-energetique-saint-nazaire': 'le-therapeute-energetique',
 'therapies-breves': 'les-therapies-breves',
 'la-therapie-en-marchant-saint-nazaire': 'la-therapie-en-marchant-saint-nazaire',
 'post-partum-saint-nazaire': 'post-partum-saint-nazaire',
 'stress-cancer-saint-nazaire': 'stress-et-cancer-a-saint-nazaire',
 'temoignage-dune-cliente-en-parcours-de-soin-en-cancerologie-et-son-accompagnement-en-therapie-psychocorporelle': 'cancer-et-therapie-psychocorporelle',
 'soulager-douleur-chronique-psychologie-energetique': 'douleur-chronique-et-therapie-psychocorporelle',
 'therapie-psychocorporelle-saint-nazaire': 'la-therapie-psychocorporelle-saint-nazaire',
 'psychologie-energetique-saint-nazaire': 'la-psychologie-energetique',
 'sante-mentale-saint-nazaire': 'la-sante-mentale-a-saint-nazaire',
 'premenopause-saint-nazaire': 'la-premenopause-entre-40-et-50-ans',
}
nonmatch = set()
def art_of(p):
    """retourne (slug, 'nouvelle'|'ancienne') ou None"""
    if p.startswith('blog/'):
        k = nz(p[5:])
        if k in KEYS: return KEYS[k], 'nouvelle'
        nonmatch.add(p); return None
    if p in WP: return WP[p], 'ancienne'
    return None
def agroup(per):
    d = {}
    for p, c, i, pos in PAGES[per]:
        a = art_of(p)
        if not a: continue
        x = d.setdefault(a[0], dict(c=0, i=0, items=[], cn=0, ca=0))
        x['c'] += c; x['i'] += i; x['items'].append((i, pos))
        if a[1] == 'nouvelle': x['cn'] += c
        else: x['ca'] += c
    for x in d.values(): x['pos'] = wavg(x['items'])
    return d
AGR = {k: agroup(k) for k in PER}

# ---------- 5. Appareils ----------
DEV = {k: {r['Appareil']: (int(r['Clics']), int(r['Impressions']), fl(r['Position'])) for r in rd(p, 'Appareils.csv')} for k, p in PER.items()}

# ---------- CSV pour build.py ----------
out = []  # (clé, libellé, avant(c,i,pos)|None, après(c,i,pos)|None)
def pr(d, g, per):
    x = d[per].get(g)
    return (x['c'], x['i'], x['pos']) if x else None
for g in PG:
    out.append(('page:' + g, g, pr(PGR, g, 'avant'), pr(PGR, g, 'apres')))
for sl in ART:
    out.append(('art:' + sl, ART[sl], pr(AGR, sl, 'avant'), pr(AGR, sl, 'apres')))
for q in ['emmanuelle demeulemeester', 'emdr saint nazaire', 'emdr st nazaire', 'eft saint nazaire', 'psychopraticienne', 'psychopraticien saint nazaire']:
    f = lambda per: (lambda r: (r[1], r[2], r[3]) if r else None)(qget(per, q))
    out.append(('req:' + q, q, f('avant'), f('apres')))
for n, rx in FAM:
    out.append(('fam:' + n, n, tuple(fam('avant', rx)[k] for k in ('c', 'i', 'pos')), tuple(fam('apres', rx)[k] for k in ('c', 'i', 'pos'))))
out.append(('fam:autres', 'autres', tuple(autres('avant')[k] for k in ('c', 'i', 'pos')), tuple(autres('apres')[k] for k in ('c', 'i', 'pos'))))
for d in ('Mobile', 'Ordinateur', 'Tablette'):
    out.append(('dev:' + d, d, DEV['avant'].get(d), DEV['apres'].get(d)))
out.append(('tot', 'Ensemble du site', (tot['avant']['clics'], tot['avant']['impr'], tot['avant']['pos']), (tot['apres']['clics'], tot['apres']['impr'], tot['apres']['pos'])))
out.append(('qvis', 'Requêtes visibles (somme)', (qvis['avant'][0], qvis['avant'][1], None), (qvis['apres'][0], qvis['apres'][1], None)))
with open(O + 'gsc-periodes.csv', 'w', newline='', encoding='utf-8') as fh:
    w = csv.writer(fh); w.writerow(['cle', 'libelle', 'avant_clics', 'avant_impr', 'avant_pos', 'apres_clics', 'apres_impr', 'apres_pos'])
    for key, lib, a, b in out:
        def cells(x): return ['', '', ''] if x is None else [x[0], x[1], '' if x[2] is None else f"{x[2]:.2f}"]
        w.writerow([key, lib] + cells(a) + cells(b))

# ---------- Markdown ----------
L = []
A = L.append
def ev(a, b): return f"{b - a:+d}".replace('-', '−') if a is not None else '—'
def pc(a, b): return f"{(b - a) / a * 100:+.0f} %".replace('-', '−') if a else '—'
def ps(x): return '—' if x is None else fr(x, 1)
def cell(x):
    return '—' if x is None else f"{x[0]} / {fr(x[1])} / {ps(x[2])}"

A("# Analyse GSC par période — avant / après la refonte\n")
A("Produit le 1er nov. 2026 par `audit/analyses/scripts/gsc_periodes.py` (`python3 -I audit/analyses/scripts/gsc_periodes.py`, depuis la racine). Sources : `audit/data/gsc/avant/` (17 janv. → 7 juin 2026) et `audit/data/gsc/apres/` (8 juin → 27 oct. 2026), exports Google Search Console, type « Web (textuel) ». Sortie machine : `audit/analyses/gsc-periodes.csv` (lu par `audit/livrable/build.py`).")
A("Les chiffres GSC = apparitions et clics **venus de Google seulement**, pas des visites. Dans les tableaux : clics / impressions / position moyenne.\n")

A("## 1. Contrôle des totaux (Graphique.csv)\n")
A("| Période | Jours | Clics | Impressions | CTR | Position (pondérée) |\n|---|---|---|---|---|---|")
for k, lab in (('avant', 'Avant'), ('apres', 'Après')):
    t = tot[k]
    A(f"| {lab} ({t['debut']} → {t['fin']}) | {t['jours']} | {t['clics']} | {fr(t['impr'])} | {t['ctr'] * 100:.1f} % | {t['pos']:.1f} |".replace('.', ','))
if ecarts: A("\n**ÉCARTS avec 01-gsc.md :** " + " ; ".join(ecarts))
else: A("\n**Aucun écart** avec `01-gsc.md` (133 → 202 clics, 2 550 → 3 364 impressions, positions 15,6 → 13,3) : les exports par période et l'export 16 mois donnent les mêmes totaux.")
A("")
A(f"Attention : la somme des lignes de `Pages.csv` ne vaut pas le total de `Graphique.csv` (Google ne liste pas toutes les lignes) : avant {sums['avant'][0]} clics / {fr(sums['avant'][1])} impr. contre {tot['avant']['clics']} / {fr(tot['avant']['impr'])} ; après {sums['apres'][0]} / {fr(sums['apres'][1])} contre {tot['apres']['clics']} / {fr(tot['apres']['impr'])}. `Requêtes.csv` est encore plus partiel (requêtes rares masquées) : clics visibles {qvis['avant'][0]} sur {tot['avant']['clics']} avant ({qvis['avant'][0] / tot['avant']['clics'] * 100:.0f} %), {qvis['apres'][0]} sur {tot['apres']['clics']} après ({qvis['apres'][0] / tot['apres']['clics'] * 100:.0f} %).")
A("Avant + après ne font pas non plus le total « 16 mois » des pages (ex. accueil 303 sur 16 mois) : les deux périodes couvrent 284 jours sur ~487.\n")

A("## 2. Pages (Pages.csv)\n")
A("Regroupements « ancienne URL WordPress + nouvelle URL du même sujet » (signalés ✱) : EMDR (`/emdr-saint-nazaire/`, `/emdr/`, `/therapie-emdr-saint-nazaire/`), EFT (`/eft-saint-nazaire/`, `/eft/`, `/seance-eft-gestion-emotions/`), séance découverte psychocorporelle (ancien nom « gratuite » + nouveau), thérapie en marchant (racine + `/therapie-en-marchant-saint-nazaire/`), post-partum (`/post-partum-saint-nazaire/` + `/espace-soutien-post-partum/`). Les articles `/blog/…` sont traités au §4.\n")
A("| Page | Avant (clics / impr. / pos.) | Après (clics / impr. / pos.) | Évolution clics |\n|---|---|---|---|")
allg = set(PGR['avant']) | set(PGR['apres'])
def gsc_(g, per): return PGR[per].get(g)
order = sorted(allg, key=lambda g: -((gsc_(g, 'avant') or {'c': 0})['c'] + (gsc_(g, 'apres') or {'c': 0})['c']
                                  + 0.001 * ((gsc_(g, 'avant') or {'i': 0})['i'] + (gsc_(g, 'apres') or {'i': 0})['i'])))
for g in order[:22]:
    a, b = gsc_(g, 'avant'), gsc_(g, 'apres')
    star = ' ✱' if len(PG.get(g, [])) > 1 else ''
    ta = (a['c'], a['i'], a['pos']) if a else None; tb = (b['c'], b['i'], b['pos']) if b else None
    e = ev(a['c'], b['c']) if (a and b) else '—'
    A(f"| {g}{star} | {cell(ta)} | {cell(tb)} | {e} |")
A("\n« — » = la page n'a aucune ligne dans l'export de cette période.")
A("")
A("Détail des regroupements ✱ (clics / impressions) :\n")
for g in PG:
    if len(PG[g]) < 2: continue
    for per in ('avant', 'apres'):
        parts = [f"`/{p}/` {c} / {i}" for p, c, i, _ in PAGES[per] if p in PG[g]]
        A(f"- {g}, {per} : " + ' ; '.join(parts))
A("")
A("Lecture : l'accueil passe de 76 à 139 clics et concentre l'essentiel de la hausse ; les pages EFT/EMDR restent très vues et très peu cliquées dans les deux périodes. Les chiffres de page sont de petits nombres (quelques clics) : tendance, pas preuve.\n")

A("## 3. Mots tapés (Requêtes.csv)\n")
A("Top requêtes (clics / impressions / position) :\n")
A("| Avant | Après |\n|---|---|")
for i in range(10):
    a = sorted(QRY['avant'], key=lambda q: (-q[1], -q[2]))[i]; b = sorted(QRY['apres'], key=lambda q: (-q[1], -q[2]))[i]
    A(f"| {a[0]} : {a[1]} / {a[2]} / {ps(a[3])} | {b[0]} : {b[1]} / {b[2]} / {ps(b[3])} |")
A("\nFamilles (somme des requêtes **visibles** qui contiennent le mot ; une requête peut compter dans plusieurs familles ; « autres » = aucune des familles) :\n")
A("| Famille | Avant : requêtes / clics / impr. / pos. | Après : requêtes / clics / impr. / pos. |\n|---|---|---|")
for n, rx in FAM:
    a, b = fam('avant', rx), fam('apres', rx)
    A(f"| {n} | {a['n']} / {a['c']} / {fr(a['i'])} / {ps(a['pos'])} | {b['n']} / {b['c']} / {fr(b['i'])} / {ps(b['pos'])} |")
a, b = autres('avant'), autres('apres')
A(f"| autres | {a['n']} / {a['c']} / {fr(a['i'])} / {ps(a['pos'])} | {b['n']} / {b['c']} / {fr(b['i'])} / {ps(b['pos'])} |")
A("")
A("Recherches suivies :\n")
A("| Recherche | Avant (clics / impr. / pos.) | Après (clics / impr. / pos.) |\n|---|---|---|")
for q in ['emdr saint nazaire', 'emdr st nazaire', 'eft saint nazaire', 'emmanuelle demeulemeester', 'demeulemeester', 'psychopraticienne', 'psychopraticien saint nazaire']:
    a, b = qget('avant', q), qget('apres', q)
    A(f"| « {q} » | {cell((a[1], a[2], a[3]) if a else None)} | {cell((b[1], b[2], b[3]) if b else None)} |")
A("\n« — » = la requête n'est pas dans la liste exportée de cette période (trop rare, ou masquée par Google pour confidentialité). « eft saint nazaire » n'apparaît dans aucune des deux listes.")
A("")
A("Lecture : « emdr saint nazaire » reste stable (place moyenne 9,6 puis 9,3 ; clics 6 puis 10). La recherche du nom complet « emmanuelle demeulemeester » n'est visible qu'après (20 clics, place 1) : avant, cette requête n'est pas dans la liste (masquée ou trop rare) ; la famille « nom » (toutes variantes visibles) passe de 2 à 21 clics. Les requêtes EFT restent sans clic dans les deux périodes.\n")

A("## 4. Articles de blog\n")
A("Regroupement par article : URL `/blog/…` (slug ou nom de fichier, forme actuelle ou ancienne) **plus** l'ancienne URL WordPress à la racine quand le sujet est évident ✱ (liste : " + ', '.join(f"`/{k}/`" for k in WP) + "). Le détail ancienne/nouvelle URL est donné en clics.\n")
A("| Article | Avant (clics / impr. / pos.) | Après (clics / impr. / pos.) | Après : dont nouvelle URL `/blog/` |\n|---|---|---|---|")
sl_all = set(AGR['avant']) | set(AGR['apres'])
ordr = sorted(sl_all, key=lambda s: -((AGR['avant'].get(s) or {'c': 0})['c'] + (AGR['apres'].get(s) or {'c': 0})['c'] + 0.001 * ((AGR['avant'].get(s) or {'i': 0})['i'] + (AGR['apres'].get(s) or {'i': 0})['i'])))
for s in ordr[:14]:
    a, b = AGR['avant'].get(s), AGR['apres'].get(s)
    ta = (a['c'], a['i'], a['pos']) if a else None; tb = (b['c'], b['i'], b['pos']) if b else None
    A(f"| {ART[s][:70]} | {cell(ta)} | {cell(tb)} | {b['cn'] if b else '—'} |")
vus = sl_all
jamais = [ART[s] for s in ART if s not in vus]
A(f"\nArticles sans aucune ligne dans les deux périodes (ni nouvelle ni ancienne URL) : {len(jamais)} : " + ' ; '.join(jamais) + ".")
if nonmatch: A("\nURL /blog/ non reconnues : " + ', '.join(sorted(nonmatch)))
else: A("\nToutes les URL `/blog/…` des exports ont été rattachées à un des 20 articles.")
A("")
A("## 5. « emdr saint nazaire » et « eft saint nazaire »\n")
for q in ('emdr saint nazaire', 'eft saint nazaire'):
    a, b = qget('avant', q), qget('apres', q)
    A(f"- « {q} » : avant {('%d clics / %d impr. / place %s' % (a[1], a[2], ps(a[3]))) if a else '— (absente de la liste)'} ; après {('%d clics / %d impr. / place %s' % (b[1], b[2], ps(b[3]))) if b else '— (absente de la liste)'}.")
A("- La place moyenne GSC est un mélange de lieux et d'appareils ; elle ne dit pas où l'on est à Saint-Nazaire (voir le relevé du 1er nov. 2026 dans `audit/data/serp/`).\n")

A("## 6. Appareils (Appareils.csv)\n")
A("| Appareil | Avant (clics / impr. / pos.) | Après (clics / impr. / pos.) |\n|---|---|---|")
for d in ('Mobile', 'Ordinateur', 'Tablette'):
    A(f"| {d} | {cell(DEV['avant'].get(d))} | {cell(DEV['apres'].get(d))} |")
A("")
A("## 7. Ce que ces exports ne permettent pas de dire\n")
A("- La cause de la hausse (refonte, saison, nouveaux articles) : non démontrable.")
A("- Les volumes de recherche mensuels : ils ne viennent pas de Search Console.")
A("- La majorité des clics n'a pas de requête visible (voir §1) : les évolutions par mot ne portent que sur la minorité visible.")
A("- Les redirections des anciennes URL : non testées ici.")
with open(O + '05-gsc-avant-apres.md', 'w', encoding='utf-8') as fh:
    fh.write('\n'.join(L) + '\n')
print('ecarts:', ecarts or 'aucun')
print('non reconnues:', sorted(nonmatch))
print('sums pages', sums, 'qvis', qvis)

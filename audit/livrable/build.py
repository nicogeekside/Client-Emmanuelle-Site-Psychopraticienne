#!/usr/bin/env python3
"""Génère rapport.html (stdlib seule). Lancer : python3 -I audit/livrable/build.py
Pronoms d'adresse : changer PRON pour passer au tutoiement (les verbes conjugués
sont écrits à la 3e personne ou à l'impératif impersonnel quand c'est possible)."""
import csv, os
HERE = os.path.dirname(os.path.abspath(__file__))
AN = os.path.join(HERE, "..", "analyses")

PRON = {  # vouvoiement provisoire
    "[[Vous]]": "Vous", "[[vous]]": "vous", "[[votre]]": "votre", "[[Votre]]": "Votre",
    "[[vos]]": "vos", "[[Vos]]": "Vos", "[[vous-meme]]": "vous-même",
}
# Tutoiement : {"[[Vous]]":"Tu","[[vous]]":"tu","[[votre]]":"ton","[[Votre]]":"Ton","[[vos]]":"tes","[[Vos]]":"Tes","[[vous-meme]]":"toi-même"}

def rows(name):
    with open(os.path.join(AN, name), encoding="utf-8") as f:
        return list(csv.DictReader(f))

SAUGE, PROF, SABLE, FOND = "#5C7A62", "#3D5A4E", "#EBDCCC", "#FAF7F3"
TERRA, TERRA_P, ANTH = "#C88D7D", "#9A5849", "#2C3E50"

MOIS = ["janv.", "févr.", "mars", "avr.", "mai", "juin", "juil.", "août", "sept.", "oct.", "nov.", "déc."]
def lab(m):
    y, mm = m.split("-"); return MOIS[int(mm) - 1] + " " + y[2:]

def line_chart(data, key, title, color, ymax_step, W=400, H=300, step=3, fs=13):
    L, R, T, B = 40, 14, 40, 40
    n = len(data); vals = [int(r[key]) for r in data]
    ymax = ((max(vals) // ymax_step) + 1) * ymax_step
    x = lambda i: L + i * (W - L - R) / (n - 1)
    y = lambda v: T + (H - T - B) * (1 - v / ymax)
    gid = "g" + key
    s = [f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="{title}">',
         f'<defs><linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{color}" stop-opacity="0.22"/><stop offset="1" stop-color="{color}" stop-opacity="0"/></linearGradient></defs>']
    i6 = [r["mois"] for r in data].index("2026-06")
    s.append(f'<rect x="{x(i6):.1f}" y="{T}" width="{W-R-x(i6):.1f}" height="{H-T-B}" fill="{SABLE}" opacity="0.5" rx="3"/>')
    for g in range(0, ymax + 1, ymax_step):
        s.append(f'<line x1="{L}" x2="{W-R}" y1="{y(g):.1f}" y2="{y(g):.1f}" stroke="#e3d9cc" stroke-width="{1 if g==0 else 0.6}"/>')
        s.append(f'<text x="{L-8}" y="{y(g)+4:.1f}" text-anchor="end" font-size="{fs}" fill="#4a5a68">{g}</text>')
    pts = " ".join(f"{x(i):.1f},{y(v):.1f}" for i, v in enumerate(vals))
    s.append(f'<polygon points="{x(0):.1f},{y(0):.1f} {pts} {x(n-1):.1f},{y(0):.1f}" fill="url(#{gid})"/>')
    s.append(f'<line x1="{x(i6):.1f}" x2="{x(i6):.1f}" y1="{T-12}" y2="{H-B}" stroke="{TERRA_P}" stroke-width="1.4" stroke-dasharray="4 3"/>')
    lx = x(i6)
    s.append(f'<rect x="{lx-182:.1f}" y="{T-32}" width="176" height="21" rx="10.5" fill="#f4e6df"/>')
    s.append(f'<text x="{lx-94:.1f}" y="{T-17.5}" text-anchor="middle" font-size="{fs}" fill="{TERRA_P}" font-weight="700">Nouveau site (juin 2026)</text>')
    s.append(f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="2.8" stroke-linejoin="round" stroke-linecap="round"/>')
    mi = vals.index(max(vals))
    for i, v in enumerate(vals):
        s.append(f'<circle cx="{x(i):.1f}" cy="{y(v):.1f}" r="{4.4 if i==mi else 3}" fill="{"#fff" if i!=mi else color}" stroke="{color}" stroke-width="2"/>')
    for i, r in enumerate(data):
        if i % step == 0:
            s.append(f'<text x="{x(i):.1f}" y="{H-B+20}" text-anchor="middle" font-size="{fs-1}" fill="#4a5a68">{lab(r["mois"])}</text>')
    s.append(f'<text x="{x(mi):.1f}" y="{y(vals[mi])-11:.1f}" text-anchor="middle" font-size="{fs+1}" font-weight="700" fill="{PROF}">{vals[mi]}</text>')
    s.append('</svg>')
    return "".join(s)

mois = rows("gsc-par-mois.csv")
cal = rows("gsc-vs-calendly-par-mois.csv")

CSS = f'''
@page {{ size: A4; margin: 16mm 16mm 18mm 16mm; background: {FOND};
  @bottom-left {{ content: "Audit de visibilité — brouillon"; font: 400 8pt Lato, Arial, sans-serif; color: #5b6b78; }}
  @bottom-right {{ content: counter(page); font: 400 8pt Lato, Arial, sans-serif; color: #5b6b78; }} }}
@page :first {{ margin: 0; background: {FOND}; @bottom-left {{ content: none; }} @bottom-right {{ content: none; }} }}
* {{ box-sizing: border-box; }}
html {{ background:{FOND}; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
body {{ margin:0; background:{FOND}; color:{ANTH}; font-family:'Lato',Arial,sans-serif; font-size:10.4pt; line-height:1.5; }}
h1,h2,h3 {{ font-family:'Playfair Display',Georgia,serif; color:{PROF}; margin:0 0 .3em; line-height:1.18; font-weight:600; }}
h2 {{ font-size:20pt; margin-bottom:.35em; }}
h2::after {{ content:""; display:block; width:38px; height:3px; background:{TERRA}; border-radius:2px; margin-top:7px; }}
h3 {{ font-size:12.5pt; margin-top:1em; }}
p {{ margin:.3em 0 .6em; }}
b {{ font-weight:700; }}
section {{ break-after: page; }}
section:last-child {{ break-after: auto; }}
.cover {{ height:297mm; padding:30mm 24mm 24mm; display:flex; flex-direction:column; background:{FOND}; position:relative; overflow:hidden; break-after:page; }}
.cover::before {{ content:""; position:absolute; right:-60mm; top:-50mm; width:150mm; height:150mm; border-radius:50%; background:{SABLE}; opacity:.7; }}
.cover::after {{ content:""; position:absolute; right:12mm; top:96mm; width:34mm; height:34mm; border-radius:50%; background:{TERRA}; opacity:.55; }}
.cover > * {{ position:relative; z-index:1; }}
.cover .kick {{ font-size:9.5pt; letter-spacing:.22em; text-transform:uppercase; color:{TERRA_P}; font-weight:700; margin-top:58mm; }}
.cover h1 {{ font-size:38pt; line-height:1.1; margin:6mm 0 8mm; max-width:140mm; }}
.cover .rule {{ width:54px; height:3px; background:{TERRA}; border-radius:2px; margin-bottom:8mm; }}
.cover .lead {{ font-size:12pt; max-width:125mm; color:{ANTH}; line-height:1.6; }}
.cover .bandeau {{ margin-top:auto; align-self:flex-start; background:{SABLE}; color:{TERRA_P}; font-size:9pt; font-weight:700; padding:6px 14px; border-radius:14px; }}
.bandeau {{ background:{SABLE}; color:{TERRA_P}; }}
.cols {{ display:flex; gap:14px; }} .cols > div {{ flex:1; }}
.colh {{ font-family:'Playfair Display',serif; font-size:13pt; font-weight:600; margin:0 0 8px; display:flex; align-items:center; gap:8px; }}
.colh::before {{ content:""; width:10px; height:10px; border-radius:50%; background:{SAUGE}; }}
.colh.warm {{ color:{TERRA_P}; }} .colh.warm::before {{ background:{TERRA}; }}
.card {{ background:#fff; border:1px solid #eadfd2; border-radius:8px; padding:11px 13px; margin-bottom:10px; break-inside:avoid; }}
.good {{ border-left:4px solid {SAUGE}; }} .bad {{ border-left:4px solid {TERRA}; }}
.card h3 {{ margin:0 0 4px; font-size:11.5pt; }} .card p {{ margin:0; font-size:9.8pt; }}
.q {{ margin:0 0 14px; padding:13px 15px 6px; background:#fff; border:1px solid #eadfd2; border-radius:8px; break-inside:avoid; }}
.q b.t {{ display:block; font-family:'Playfair Display',serif; color:{PROF}; font-size:13pt; font-weight:600; margin-bottom:8px; }}
.q p {{ margin:.4em 0; }}
.kpi {{ display:flex; align-items:center; gap:14px; background:{FOND}; border-radius:8px; padding:9px 14px; margin:2px 0 10px; }}
.kpi .v {{ font-family:'Playfair Display',serif; font-size:27pt; color:{PROF}; line-height:1; font-weight:600; }}
.kpi .v.old {{ color:#6b7a86; font-size:20pt; }}
.kpi .arr {{ color:{TERRA_P}; font-size:15pt; }}
.kpi .lbl {{ font-size:9pt; color:#4a5a68; line-height:1.3; }}
.kpi .up {{ margin-left:auto; text-align:right; font-weight:700; color:{PROF}; font-size:10.5pt; background:#dfe9e1; padding:3px 11px; border-radius:12px; white-space:nowrap; }}
table {{ border-collapse:separate; border-spacing:0; width:100%; font-size:9.3pt; background:#fff; margin:4px 0 8px; }}
th,td {{ padding:6px 9px; vertical-align:top; text-align:left; border-bottom:1px solid #efe6db; }}
th {{ color:{PROF}; font-weight:700; font-size:8.6pt; letter-spacing:.03em; border-bottom:2px solid {SABLE}; background:transparent; vertical-align:bottom; }}
tr {{ break-inside:avoid; }}
tr:last-child td {{ border-bottom:0; }}
td.me, th.me {{ background:#f1f5f1; }} th.me {{ color:{PROF}; }}
td.av {{ white-space:nowrap; }}
.venir {{ display:inline-block; font-size:8pt; font-weight:700; color:{TERRA_P}; background:#f6ebe5; padding:1px 8px; border-radius:9px; }}
td.pos b {{ color:{PROF}; }}
.note {{ font-size:8.8pt; color:#4a5a68; line-height:1.45; }}
.warn {{ background:#fff; border:1px solid #eadfd2; border-left:4px solid {TERRA}; border-radius:6px; padding:9px 13px; font-size:9.4pt; margin:.7em 0; break-inside:avoid; }}
.tag {{ display:inline-block; font-size:8pt; font-weight:700; padding:1px 8px; border-radius:9px; background:#f6ebe5; color:{TERRA_P}; }}
ul {{ margin:.3em 0 .5em 1.1em; padding:0; }} li {{ margin:.2em 0; }}
ol.small {{ list-style:none; counter-reset:c; margin:.4em 0 0; padding:0; }}
ol.small li {{ counter-increment:c; position:relative; padding-left:30px; margin:0 0 7px; }}
ol.small li::before {{ content:counter(c); position:absolute; left:0; top:0; width:21px; height:21px; border-radius:50%; background:{PROF}; color:#fff; font-size:9pt; font-weight:700; text-align:center; line-height:21px; }}
dl {{ margin:0; }} dt {{ font-family:'Playfair Display',serif; font-weight:600; color:{PROF}; font-size:12pt; margin-top:.8em; }} dd {{ margin:.1em 0 0; }}
.chart {{ background:#fff; border:1px solid #eadfd2; border-radius:8px; padding:6px 10px 2px; margin-bottom:10px; break-inside:avoid; }}
.chart h3 {{ margin:6px 0 0; font-size:11.5pt; }}
.small li {{ font-size:9.5pt; }}
#concurrentes table {{ font-size:9.9pt; }} #concurrentes td, #concurrentes th {{ padding:8px 9px; }} #concurrentes .small li {{ font-size:10.3pt; margin-bottom:9px; }} #sources .small li {{ font-size:10pt; margin:.5em 0; }}
.gloss {{ margin-top:8mm; break-inside:avoid; }}
.charts {{ gap:10px; margin-bottom:6px; }} .charts .chart {{ margin:0; min-width:0; }}
.verdict .card {{ padding:20px 18px; margin-bottom:20px; border-radius:10px; }} .verdict .card h3 {{ font-size:14pt; margin-bottom:8px; }} .verdict .card p {{ font-size:11.4pt; line-height:1.6; }}
.verdict > .note {{ font-size:9.6pt; margin-top:14mm; }}
.verdict .colh {{ font-size:14.5pt; margin-bottom:12px; }}
'''

BODY = f'''
<div class="cover">
<div class="kick">Emmanuelle Demeulemeester · Saint-Nazaire</div>
<h1>Audit de visibilité de [[votre]] site</h1>
<div class="rule"></div>
<p class="lead">Emmanuelle Demeulemeester, psychopraticienne à Saint-Nazaire. Relevés du 1er novembre 2026. Objectif du site : que des personnes réservent la séance découverte offerte de 45 minutes.</p>
<div class="bandeau">BROUILLON — en attente des données Netlify et des exports Google par période</div>
</div>

<section id="verdict" class="verdict">
<h2>Le verdict en une page</h2>
<div class="cols">
 <div>
  <p class="colh">Trois bonnes nouvelles</p>
  <div class="card good"><h3>1. Google [[vous]] montre un peu plus</h3><p>Depuis le nouveau site : <b>202 clics</b> venus de Google, contre <b>133</b> avant (mêmes durées de 142 jours). C'est une tendance, pas une preuve : les volumes sont petits.</p></div>
  <div class="card good"><h3>2. [[Vous]] êtes n°1 sur Google Maps</h3><p>Pour « psychopraticienne Saint-Nazaire », [[votre]] fiche est première : <b>5,0 sur 5 (20 avis)</b>. Elle est aussi première du bloc « carte » pour « EFT Saint-Nazaire ».</p></div>
  <div class="card good"><h3>3. [[Votre]] site se distingue</h3><p>Sur les 4 praticiennes comparées, [[vous]] êtes la seule à avoir un blog, une séance découverte offerte et une page par méthode.</p></div>
 </div>
 <div>
  <p class="colh warm">Trois points d'attention</p>
  <div class="card bad"><h3>1. L'EMDR est un point faible</h3><p>Pour « EMDR Saint-Nazaire », le site n'est pas sur la 1re page de Google classique (place moyenne 8,7 selon Google Search Console) et [[vous]] n'apparaissez pas dans le résumé que Google affiche en haut. [[Votre]] fiche Maps est 3e.</p></div>
  <div class="card bad"><h3>2. L'EFT est vue, mais peu cliquée</h3><p>La page EFT apparaît 881 fois dans Google mais ne reçoit que 10 clics ; les recherches contenant « EFT » ne rapportent qu'1 clic en tout.</p></div>
  <div class="card bad"><h3>3. Les concurrentes réservent plus vite</h3><p>Chez elles, un seul clic suffit pour réserver, avec le prix affiché. Chez [[vous]], il en faut 2 depuis l'accueil.</p></div>
 </div>
</div>
<p class="note" style="margin-top:14mm">Les chiffres de clics viennent de Google seulement (voir page suivante). Les points marqués « à confirmer » n'ont pas pu être vérifiés.</p>
</section>

<section id="questions">
<h2>[[Vos]] 5 questions, réponses simples</h2>
<p class="note">Avant = 17 janv. → 7 juin 2026 ; après = 8 juin → 27 oct. 2026 (142 jours chacun). « À venir » : l'export Google par période n'est pas encore reçu.</p>
<div class="q"><b class="t">1. Combien de vues sur le site ?</b>
<div class="kpi"><div class="v old">133</div><div class="arr">→</div><div class="v">202</div><div class="lbl">clics depuis Google<br>avant → après</div><div class="up">+52 %</div></div>
<table><tr><th></th><th>Avant</th><th>Après</th><th>Évolution</th></tr>
<tr><td>Clics depuis Google</td><td>133</td><td>202</td><td><b>+69 (+52 %)</b></td></tr>
<tr><td>Apparitions dans Google (impressions)</td><td>2 550</td><td>3 364</td><td><b>+814 (+32 %)</b></td></tr>
<tr><td>Part des apparitions qui donnent un clic</td><td>5,2 %</td><td>6,0 %</td><td>+0,8 point</td></tr>
<tr><td>Place moyenne dans Google</td><td>15,6</td><td>13,3</td><td>2,3 places gagnées</td></tr></table>
<p><b>On ne sait mesurer que ce qui vient de Google.</b> Aucun outil de comptage des visites n'est activé à ce jour : <span class="tag">à confirmer</span>. Les visites directes, par Bing ou par les réseaux sociaux ne sont donc pas comptées.</p>
<p class="note">Sur les 16 mois (1er juil. 2025 → 30 oct. 2026) : 7 513 apparitions, 441 clics (5,9 %). 97 % des clics viennent de France ; 304 sur mobile, 128 sur ordinateur.</p></div>
<div class="q"><b class="t">2. Quelles pages sont vues ?</b>
<div class="kpi"><div class="v">69 %</div><div class="lbl">des clics (303 sur 441) vont à l'accueil</div></div>
<table><tr><th>Page</th><th>Clics sur 16 mois</th><th>Avant</th><th>Après</th><th>Évolution</th></tr>
<tr><td>Accueil</td><td>303 sur 441 (69 %)</td><td>à venir</td><td>à venir</td><td>à venir</td></tr>
<tr><td>Tarifs et modalités</td><td>30</td><td>à venir</td><td>à venir</td><td>à venir</td></tr>
<tr><td>Cercle de parole</td><td>19</td><td>à venir</td><td>à venir</td><td>à venir</td></tr>
<tr><td>Préménopause</td><td>13</td><td>à venir</td><td>à venir</td><td>à venir</td></tr>
<tr><td>Injonctions faites aux femmes</td><td>12</td><td>à venir</td><td>à venir</td><td>à venir</td></tr>
<tr><td>Contact</td><td>12</td><td>à venir</td><td>à venir</td><td>à venir</td></tr>
<tr><td>Thérapie IFS</td><td>11</td><td>à venir</td><td>à venir</td><td>à venir</td></tr>
<tr><td>EFT</td><td>10 (881 apparitions)</td><td>à venir</td><td>à venir</td><td>à venir</td></tr>
<tr><td>EMDR</td><td>4 (637 apparitions)</td><td>à venir</td><td>à venir</td><td>à venir</td></tr></table>
<p class="note">Les pages EFT et EMDR sont très vues dans Google mais très peu cliquées.</p></div>
<div class="q"><b class="t">3. Quels mots tape-t-on pour [[vous]] trouver ?</b>
<div class="kpi"><div class="v">19 %</div><div class="lbl">des clics (82 sur 441) ont un mot visible</div></div>
<table><tr><th>Recherche</th><th>Clics sur 16 mois</th><th>Avant</th><th>Après</th><th>Évolution</th></tr>
<tr><td>« emmanuelle demeulemeester » (1re ou 2e place)</td><td>35</td><td>à venir</td><td>à venir</td><td>à venir</td></tr>
<tr><td>« emdr saint nazaire » (place moyenne 8,7 ; 652 apparitions)</td><td>17</td><td>à venir</td><td>à venir</td><td>à venir</td></tr>
<tr><td>« emdr st nazaire »</td><td>4</td><td>à venir</td><td>à venir</td><td>à venir</td></tr>
<tr><td>Recherches « EFT » (souvent hors secteur : Saumur, Chinon, Ancenis…)</td><td>1</td><td>à venir</td><td>à venir</td><td>à venir</td></tr>
<tr><td>« psychopraticien(ne) »</td><td>0</td><td>à venir</td><td>à venir</td><td>à venir</td></tr></table>
<p class="note">Les gens qui tapent [[votre]] nom [[vous]] connaissent déjà. Google cache les mots peu fréquents : seuls 82 clics sur 441 (19 %) ont un mot visible.</p></div>
<div class="q"><b class="t">4. Quels articles du blog sont les plus vus ?</b>
<div class="kpi"><div class="v">1</div><div class="lbl">clic, au mieux, par article sur 16 mois</div></div>
<table><tr><th>Article</th><th>Clics sur 16 mois</th><th>Avant</th><th>Après</th><th>Évolution</th></tr>
<tr><td>Contrôle coercitif ; thérapie IFS ; comprendre l'EMDR ; psychocorporel (+1 autre)</td><td>1 chacun</td><td>à venir</td><td>à venir</td><td>à venir</td></tr>
<tr><td>Thérapie en marchant</td><td>0 (41 apparitions)</td><td>à venir</td><td>à venir</td><td>à venir</td></tr>
<tr><td>Lien d'attachement ; « Quand parler ne suffit plus… »</td><td>0 : jamais vus</td><td>à venir</td><td>à venir</td><td>à venir</td></tr></table>
<p class="note">Aucun article ne se détache : le blog attire encore très peu.</p></div>
<div class="q"><b class="t">5. Quelle est [[votre]] place sur l'EFT et l'EMDR à Saint-Nazaire ?</b>
<div class="kpi"><div class="v old">15,6</div><div class="arr">→</div><div class="v">13,3</div><div class="lbl">place moyenne dans Google<br>avant → après</div><div class="up">2,3 places gagnées</div></div>
<table><tr><th>Place moyenne dans Google (Search Console)</th><th>Avant</th><th>Après</th><th>Évolution</th></tr>
<tr><td>Ensemble du site</td><td>15,6</td><td>13,3</td><td>2,3 places gagnées</td></tr>
<tr><td>« emdr saint nazaire » (8,7 sur 16 mois, référence)</td><td>à venir</td><td>à venir</td><td>à venir</td></tr></table>
<p class="note">Relevé du jour (1er nov. 2026, après la refonte) depuis Saint-Nazaire ; la place change selon l'appareil et le lieu.</p>
<table><tr><th>Recherche</th><th>Google classique</th><th>Carte Google (Maps)</th><th>Résumé affiché en haut de Google</th></tr>
<tr><td>« EMDR Saint-Nazaire »</td><td>Absente de la 1re page</td><td>3e (derrière Morgane Houarner et le cabinet Hypnose &amp; EMDR-DSA)</td><td>[[Vous]] n'y êtes pas citée</td></tr>
<tr><td>« EFT Saint-Nazaire »</td><td>2e (après Resalib)</td><td><b>1re</b></td><td>Pas de résumé relevé</td></tr>
<tr><td>« Psychopraticienne Saint-Nazaire »</td><td>3e (après psychopraticienne-saint-nazaire.com et Resalib)</td><td><b>1re</b> (carte Maps) ; absente du bloc local de la page Google</td><td>Non lu (à revérifier)</td></tr></table>
<p class="note">Les relevés Maps et Google du jour n'existent pas « avant » : seule la colonne Search Console permet la comparaison.</p></div>
<div class="gloss"><h2>Mots utilisés</h2>
<dl>
<dt>Impression</dt><dd>Une fois où [[votre]] site s'affiche dans les résultats de Google, que la personne clique ou non.</dd>
<dt>Clic</dt><dd>Une personne qui clique sur [[votre]] site dans les résultats Google. C'est la seule « visite » que nous mesurons.</dd>
<dt>Place moyenne</dt><dd>La position moyenne du site dans les résultats Google (1 = tout en haut), selon Google Search Console.</dd>
<dt>Pack local</dt><dd>Les 3 fiches avec carte qui s'affichent en haut de Google pour une recherche près de chez soi (Google Maps).</dd>
</dl>
</div>
</section>

<section id="avant-apres">
<h2>Avant / après le nouveau site</h2>
<p>Le site est passé de WordPress à un nouveau site en <b>juin 2026</b> (date de bascule : 8 juin, <span class="tag">à confirmer</span>). On compare deux périodes de 142 jours.</p>
<div class="kpi"><div class="v old">133</div><div class="arr">→</div><div class="v">202</div><div class="lbl">clics depuis Google<br>avant → après</div><div class="up">+52 %</div></div>
<table style="margin-bottom:6px"><tr><th></th><th>Avant (17 janv. → 7 juin)</th><th>Après (8 juin → 27 oct.)</th><th>Écart</th></tr>
<tr><td>Clics depuis Google</td><td>133</td><td>202</td><td><b>+69 (+52 %)</b></td></tr>
<tr><td>Apparitions dans Google</td><td>2 550</td><td>3 364</td><td><b>+814 (+32 %)</b></td></tr>
<tr><td>Place moyenne</td><td>15,6</td><td>13,3</td><td>2,3 places gagnées</td></tr></table>
<div class="cols charts"><div class="chart"><h3>Clics par mois</h3>
{line_chart(mois, "clics", "Clics par mois", SAUGE, 20)}</div>
<div class="chart"><h3>Apparitions dans Google par mois</h3>
{line_chart(mois, "impressions", "Impressions par mois", PROF, 200)}</div></div>
<div class="warn"><b>Mise en garde.</b> Ce sont de petits chiffres (une trentaine de clics par mois). Le site monte, mais on ne peut pas dire que le nouveau site en est la cause : 20 articles ont aussi été publiés, et le site gagne en ancienneté. Même fenêtre juillet → octobre : 45 clics en 2025 contre 184 en 2026, mais la base 2025 est minuscule. Le pic d'août-septembre 2026 reste inexpliqué. Aucune chute n'apparaît au moment de la bascule.</div>
<div class="warn"><b>Bonus : les réservations Calendly.</b> Chiffres de <u>toutes</u> les réservations, quelle que soit leur origine (site, fiche Google, bouche-à-oreille) : on ne peut <b>pas</b> savoir lesquelles viennent du site, aucun marqueur de provenance n'existant. Découpage au mois (5 mois chacun, pas exactement les 142 jours) : <b>avant = janv. → mai 2026, après = juin → oct. 2026</b>.
<table style="margin-top:4px"><tr><th></th><th>Avant</th><th>Après</th><th>Évolution</th></tr>
<tr><td>Réservations maintenues, tous types</td><td>46</td><td>29</td><td>-17</td></tr>
<tr><td>Dont premiers contacts</td><td>15</td><td>10</td><td>-5</td></tr></table>
Cela ne dit rien sur le site : ce sont de petits chiffres, et les rendez-vous ont été renommés en sept. 2026 (regroupement « premier contact » = choix d'analyse). <span class="tag">à confirmer en demandant aux patientes</span></div>
</section>

<section id="concurrentes">
<h2>Face aux 4 autres praticiennes</h2>
<table>
<tr><th>Critère</th><th class="me">[[Vous]]</th><th>Morgane Houarner</th><th>Laurence Martin</th><th>M.-N. Guégan-Leblanc</th><th>Laure Sablé</th></tr>
<tr><td>Métier affiché</td><td class="me">Psychopraticienne</td><td>Psychopraticienne EMDR</td><td>Hypnothérapeute</td><td>Psychologue clinicienne</td><td>Psychothérapeute (Guérande et Saint-Nazaire)</td></tr>
<tr><td>Fiche Google</td><td class="me"><b>5,0 (20 avis)</b></td><td>4,9 (40 avis)</td><td colspan="3">non relevé</td></tr>
<tr><td>Blog</td><td class="me"><b>~20 articles</b></td><td>0</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>Séance offerte</td><td class="me"><b>Oui (45 min)</b></td><td>Non</td><td>Non</td><td>Non</td><td>Non</td></tr>
<tr><td>Prix affiché sur le site</td><td class="me">60 € (page RDV) ; 1er RDV d'1 h : <span class="tag">à confirmer</span></td><td>75 €</td><td>80 €</td><td>60 €</td><td>55 €</td></tr>
<tr><td>Clics pour réserver</td><td class="me">2</td><td>pas de réservation sur le site</td><td>1 (appel)</td><td>1 (Doctolib)</td><td>1 (Doctolib)</td></tr>
<tr><td>Page par méthode, FAQ</td><td class="me">Oui</td><td>Oui, sans FAQ</td><td>Non, FAQ oui</td><td>Non</td><td>Non</td></tr>
</table>
<p class="note">Marie-Noëlle Guégan-Leblanc est psychologue (titre protégé, public plus médical) : à ne pas appeler « psychopraticienne ». Morgane Houarner paie aussi des annonces Google sur 3 recherches sur 4 relevées.</p>
<h3>Ce qu'elles font mieux</h3>
<ol class="small" style="margin:.2em 0 0 1.2em;padding:0">
<li><b>Réservation en 1 clic</b> depuis l'accueil, avec un bouton répété dans la page.</li>
<li><b>Le prix à côté du bouton</b> (Laure Sablé affiche 3 lignes de prix juste avant « prendre rendez-vous »).</li>
<li><b>Un lien « voir les avis Google »</b> bien visible (Laurence Martin). [[Vous]] avez 20 avis sur Google mais le site n'y renvoie pas.</li>
<li><b>La fiche Google comme porte de réservation</b> (Morgane Houarner).</li>
<li><b>Une présence dans les annuaires</b> où l'on compare les praticiennes (Doctolib, Resalib, etc.).</li>
<li><b>Une FAQ sur l'accueil</b> pour lever la peur du premier pas (« dois-je tout raconter ? »).</li>
</ol>
<p class="note">À ne pas copier : les témoignages anonymes. Morgane Houarner est de loin la plus visible sur l'EMDR à Saint-Nazaire. Place exacte de chacune sur Google : seulement relevée pour 4 recherches.</p>
</section>

<section id="sources">
<h2>Sources</h2>
<p class="note">Chaque chiffre vient de ces fichiers du dossier d'audit (fichiers bruts non joints au rapport). Ce qui n'a pas pu être vérifié est écrit « à confirmer ».</p>
<ul class="small">
<li><b>audit/analyses/01-gsc.md</b>, <b>gsc-par-mois.csv</b>, <b>gsc-vs-calendly-par-mois.csv</b>, <b>audit/data/calendly/rdv-par-mois-anonyme.csv</b> : clics, impressions, pages, mots tapés, avant/après, Calendly (exports Google Search Console, 16 mois, et comptes Calendly anonymes).</li>
<li><b>audit/analyses/03-concurrents.md</b> : comparaison des 4 praticiennes (lecture de leurs sites publics).</li>
<li><b>audit/analyses/04-blog.md</b>, <b>blog-stats.csv</b> : état des 20 articles (lecture seule).</li>
<li><b>audit/data/serp/serp.md</b> : relevé Google et Maps du 1er nov. 2026.</li>
</ul>
<h3>Reste à confirmer</h3>
<ul class="small">
<li>Aucun outil de visites activé : à confirmer.</li>
<li>Date exacte de bascule du site (8 juin 2026) : à confirmer.</li>
<li>Pages et mots tapés avant / après : exports Google par période à recevoir.</li>
<li>Tarif du 1er RDV d'1 h : à confirmer.</li>
<li>Origine des réservations Calendly : à confirmer auprès des patientes.</li>
<li>Fiche Google des 3 autres concurrentes : non relevée.</li>
<li>Effet de la panne du site du 28 octobre : non mesuré (hors des périodes comparées).</li>
</ul>
</section>
'''

import re
BODY = BODY.replace('<td>à venir</td>', '<td class="av"><span class="venir">à venir</span></td>')
BODY = re.sub(r'<td><b>(\+\d)', r'<td class="pos"><b>\1', BODY)
for k, v in PRON.items():
    BODY = BODY.replace(k, v)

HTML = f'''<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><title>Audit de visibilité — brouillon</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Lato:wght@400;700&family=Playfair+Display:wght@600;700&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>{BODY}</body></html>'''
with open(os.path.join(HERE, "rapport.html"), "w", encoding="utf-8") as f:
    f.write(HTML)
print("ok")

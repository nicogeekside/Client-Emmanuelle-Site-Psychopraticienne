#!/usr/bin/env python3
"""Génère rapport.html (stdlib seule). Lancer : python3 -I audit/livrable/build.py
Le rapport s'adresse à Emmanuelle en la tutoyant (PRON ne sert plus qu'au cas où un
marqueur [[…]] resterait dans le texte). Les chiffres avant/après viennent de
audit/analyses/gsc-periodes.csv (produit par scripts/gsc_periodes.py)."""
import csv, os
HERE = os.path.dirname(os.path.abspath(__file__))
AN = os.path.join(HERE, "..", "analyses")

PRON = {  # tutoiement (décision du 1er nov. 2026) ; les verbes sont écrits à la main dans le texte
    "[[Vous]]": "Tu", "[[vous]]": "tu", "[[votre]]": "ton", "[[Votre]]": "Ton",
    "[[vos]]": "tes", "[[Vos]]": "Tes", "[[vous-meme]]": "toi-même",
}

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
    s = [f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="{title}" font-family="Lato, sans-serif">',
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

def fr(n, d=0):
    return f"{n:,.{d}f}".replace(",", "\u00a0").replace(".", ",")
PER = {}
for r in rows("gsc-periodes.csv"):  # produit par scripts/gsc_periodes.py
    def trio(p):
        return None if r[p + "_clics"] == "" else (int(r[p + "_clics"]), int(r[p + "_impr"]), float(r[p + "_pos"]) if r[p + "_pos"] else None)
    PER[r["cle"]] = (trio("avant"), trio("apres"))
def cl(n): return f"{n} clic" + ("s" if n > 1 else "")
def cell(x, note="", ap="appar."):
    """cellule avant / après : clics en gras, puis apparitions et place"""
    if x is None: return f'<td>—{(" <span class=note>" + note + "</span>") if note else ""}</td>'
    sub = f"{fr(x[1])} {ap}" + (f" · place {fr(x[2], 1)}" if x[2] is not None else "")
    return f'<td><b>{cl(x[0])}</b><br><span class="note">{sub}</span></td>'
def evo(a, b, plain=False):
    if a is None or b is None: return "<td>—</td>"
    d = b[0] - a[0]
    if d == 0: return "<td>0 clic de plus ou de moins</td>" if a[0] else "<td>0 clic des deux côtés</td>"
    txt = f"{d:+d} clic" + ("s" if abs(d) > 1 else "")
    txt = txt.replace("-", "\u2212")
    return f'<td class="pos"><b>{txt}</b></td>' if d > 0 else f"<td>{txt}</td>"
def ligne(lib, k, seize="", note_a="", note_b=""):
    a, b = PER[k]
    return f"<tr><td>{lib}</td>" + (f"<td>{seize}</td>" if seize != "" else "") + cell(a, note_a) + cell(b, note_b) + evo(a, b) + "</tr>"
def pos_ev(a, b):
    d = a[2] - b[2]
    if abs(d) < 0.05: return "<td>stable</td>"
    return f'<td class="pos"><b>{fr(d, 1)} place{"s" if d >= 2 else ""} gagnée{"s" if d >= 2 else ""}</b></td>' if d > 0 else f"<td>{fr(-d, 1)} place{'s' if -d >= 2 else ''} perdue{'s' if -d >= 2 else ''}</td>"
def ligne_pos(lib, k, extra=""):
    a, b = PER[k]
    return f"<tr><td>{lib}</td><td><b>{fr(a[2], 1)}</b><br><span class=\"note\">{cl(a[0])} · {fr(a[1])} appar.</span></td><td><b>{fr(b[2], 1)}</b><br><span class=\"note\">{cl(b[0])} · {fr(b[1])} appar.</span></td>{pos_ev(a, b)}</tr>"
TA, TB = PER["tot"]
ACC_A, ACC_B = PER["page:Accueil"]
PART_A, PART_B = round(ACC_A[0] / TA[0] * 100), round(ACC_B[0] / TB[0] * 100)
QV_A, QV_B = PER["qvis"]
MA, MB = PER["dev:Mobile"]; OA, OB = PER["dev:Ordinateur"]
mois = rows("gsc-par-mois.csv")
cal = rows("gsc-vs-calendly-par-mois.csv")

CSS = f'''
@page {{ size: A4; margin: 16mm 16mm 18mm 16mm; background: {FOND};
  @bottom-left {{ content: "Audit de visibilité"; font: 400 8pt Lato, Arial, sans-serif; color: #5b6b78; }}
  @bottom-right {{ content: counter(page); font: 400 8pt Lato, Arial, sans-serif; color: #5b6b78; }} }}
@page :first {{ margin: 0; background: {FOND}; @bottom-left {{ content: none; }} @bottom-right {{ content: none; }} }}
* {{ box-sizing: border-box; }}
html {{ background:{FOND}; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
body {{ margin:0; background:{FOND}; color:{ANTH}; font-family:'Lato',Arial,sans-serif; font-size:10.4pt; line-height:1.55; }}
h1,h2,h3 {{ font-family:'Playfair Display',Georgia,serif; color:{PROF}; margin:0 0 .3em; line-height:1.18; font-weight:600; }}
h2 {{ font-size:20pt; margin-bottom:.35em; }}
h2::after {{ content:""; display:block; width:38px; height:3px; background:{TERRA}; border-radius:2px; margin-top:7px; }}
h3 {{ font-size:12.5pt; margin-top:1em; }}
p {{ margin:.4em 0 .8em; }}
b {{ font-weight:700; }}
section {{ break-after: page; }}
section:last-child {{ break-after: auto; }}
.cover {{ height:297mm; padding:30mm 24mm 24mm; display:flex; flex-direction:column; background:{FOND}; position:relative; overflow:hidden; break-after:page; }}
.cover::before {{ content:""; position:absolute; right:-60mm; top:-50mm; width:150mm; height:150mm; border-radius:50%; background:{SABLE}; opacity:.7; }}
.cover::after {{ content:""; position:absolute; right:12mm; top:96mm; width:34mm; height:34mm; border-radius:50%; background:{TERRA}; opacity:.55; }}
.cover > * {{ position:relative; z-index:1; }}
.cover .kick {{ font-size:9.5pt; letter-spacing:.22em; text-transform:uppercase; color:{TERRA_P}; font-weight:700; margin-top:30mm; }}
.cover h1 {{ font-size:38pt; line-height:1.1; margin:6mm 0 8mm; max-width:140mm; }}
.cover .rule {{ width:54px; height:3px; background:{TERRA}; border-radius:2px; margin-bottom:8mm; }}
.cover .lead {{ font-size:12pt; max-width:125mm; color:{ANTH}; line-height:1.6; }}
.cover {{ text-align:center; align-items:center; }}
.cover .rule {{ margin-left:auto; margin-right:auto; }}
.cover .method {{ margin-top:auto; width:100%; background:#fff; border:1px solid #eadfd2; border-radius:10px; padding:12px 18px 10px; }}
.method h3 {{ margin:0 0 4px; font-size:12.5pt; }}
.method p {{ font-size:9.6pt; margin:.25em 0; text-align:center; }}
.frise {{ display:flex; margin:10px 0 4px; position:relative; padding-bottom:22px; }}
.frise .seg {{ flex:1; padding:7px 6px; display:flex; flex-direction:column; align-items:center; line-height:1.3; }}
.frise .seg.a {{ background:{SABLE}; border-radius:8px 0 0 8px; }}
.frise .seg.b {{ background:#dfe9e1; border-radius:0 8px 8px 0; }}
.frise .seg b {{ color:{PROF}; font-size:10pt; }} .frise .seg span {{ font-size:9pt; }} .frise .seg small {{ font-size:8.4pt; color:#4a5a68; }}
.frise .mark {{ position:absolute; left:50%; transform:translateX(-50%); bottom:0; font-size:8.6pt; font-weight:700; color:{TERRA_P}; white-space:nowrap; }}
.frise .mark::before {{ content:""; position:absolute; left:50%; top:-24px; height:20px; border-left:2px dashed {TERRA_P}; }}
.intro {{ text-align:center; }}
.meaning {{ text-align:center; background:#f1f5f1; border-radius:8px; padding:12px 18px; font-size:10pt; margin:1em 0; break-inside:avoid; break-before:avoid; page-break-before:avoid; }}
h2, h3, .q b.t, .gloss h2 {{ text-align:center; }}
h2::after {{ margin-left:auto; margin-right:auto; }}
.colh {{ justify-content:center; }}
.cols .card {{ text-align:center; }}
.kpi {{ justify-content:center; }} .kpi .up {{ margin-left:0; }}
.warn {{ break-inside:avoid; }}
.cols {{ display:flex; gap:14px; }} .cols > div {{ flex:1; }}
.colh {{ font-family:'Playfair Display',serif; font-size:13pt; font-weight:600; margin:0 0 8px; display:flex; align-items:center; gap:8px; }}
.colh::before {{ content:""; width:10px; height:10px; border-radius:50%; background:{SAUGE}; }}
.colh.warm {{ color:{TERRA_P}; }} .colh.warm::before {{ background:{TERRA}; }}
.card {{ background:#fff; border:1px solid #eadfd2; border-radius:8px; padding:15px 17px; margin-bottom:14px; break-inside:avoid; }}
.good {{ border-left:4px solid {SAUGE}; }} .bad {{ border-left:4px solid {TERRA}; }}
.card h3 {{ margin:0 0 6px; font-size:11.5pt; }} .card p {{ margin:0; font-size:10pt; line-height:1.6; }}
.q {{ margin:0 0 14px; padding:14px 18px 6px; background:#fff; border:1px solid #eadfd2; border-radius:8px; break-inside:avoid; }}
.q b.t {{ display:block; font-family:'Playfair Display',serif; color:{PROF}; font-size:13pt; font-weight:600; margin-bottom:8px; }}
.q p {{ margin:.4em 0; }}
.kpi {{ display:flex; align-items:center; gap:14px; background:{FOND}; border-radius:8px; padding:10px 16px; margin:2px 0 10px; }}
.kpi .v {{ font-family:'Playfair Display',serif; font-size:30pt; color:{PROF}; line-height:1; font-weight:600; }}
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
td.pos b {{ color:{PROF}; }}
.note {{ font-size:8.8pt; color:#4a5a68; line-height:1.45; }}
.warn {{ background:#fff; border:1px solid #eadfd2; border-left:4px solid {TERRA}; border-radius:6px; padding:13px 17px; font-size:9.8pt; margin:1.1em 0; break-inside:avoid; break-before:avoid; page-break-before:avoid; }}
.tag {{ display:inline-block; font-size:8pt; font-weight:700; padding:1px 8px; border-radius:9px; background:#f6ebe5; color:{TERRA_P}; }}
ul {{ margin:.3em 0 .5em 1.1em; padding:0; }} li {{ margin:.2em 0; }}
ol.small {{ list-style:none; counter-reset:c; margin:.4em 0 0; padding:0; }}
ol.small li {{ counter-increment:c; position:relative; padding-left:30px; margin:0 0 7px; }}
ol.small li::before {{ content:counter(c); position:absolute; left:0; top:0; width:21px; height:21px; border-radius:50%; background:{PROF}; color:#fff; font-size:9pt; font-weight:700; text-align:center; line-height:21px; }}
dl {{ margin:0; }} dt {{ font-family:'Playfair Display',serif; font-weight:600; color:{PROF}; font-size:12pt; margin-top:.8em; }} dd {{ margin:.1em 0 0; }}
.chart {{ background:#fff; border:1px solid #eadfd2; border-radius:8px; padding:6px 10px 2px; margin-bottom:10px; break-inside:avoid; }}
.chart h3 {{ margin:6px 0 0; font-size:11.5pt; }}
.small li {{ font-size:9.5pt; }}
#concurrentes table {{ font-size:9.9pt; }} #concurrentes td, #concurrentes th {{ padding:6px 8px; }} #concurrentes .small li {{ font-size:10.3pt; margin-bottom:9px; }} #sources .small li {{ font-size:10pt; margin:.5em 0; }}
.gloss {{ margin-top:8mm; break-inside:avoid; }}
.charts {{ gap:10px; margin-bottom:6px; }} .charts .chart {{ margin:0; min-width:0; }}
.verdict .card {{ padding:22px 20px; margin-bottom:22px; border-radius:10px; }} .verdict .card h3 {{ font-size:14pt; margin-bottom:8px; }} .verdict .card p {{ font-size:11.4pt; line-height:1.6; }}
.verdict > .note {{ font-size:9.6pt; margin-top:14mm; }}
.verdict .colh {{ font-size:14.5pt; margin-bottom:12px; }}
.colh.mid::before {{ background:#D9B25F; }} .colh.grey::before {{ background:#C9C2B8; }}
.mid-c {{ border-left:4px solid #D9B25F; }} .grey-c {{ border-left:4px solid #C9C2B8; }}
.rk {{ font-family:'Playfair Display',serif; font-weight:600; color:{PROF}; }}
.pg .card p {{ font-size:10.2pt; }} .pg .card {{ padding:13px 15px; }}
.pg .why {{ margin:.3em 0 0; font-size:9.3pt; color:#4a5a68; }}
.next .card {{ padding:12px 14px; }} .next .card h3 {{ font-size:11.5pt; }}
.pg li {{ font-size:10.2pt; }}
ul.nl {{ margin:.3em 0 .5em 1.2em; font-size:9.4pt; color:#4a5a68; line-height:1.55; }} ul.nl li {{ margin:.25em 0; }}
.funnel {{ margin:14px 0 8px; display:flex; flex-direction:column; align-items:center; gap:4px; }}
.fn {{ border-radius:10px; text-align:center; padding:9px 18px; }}
.fn .n {{ display:block; font-family:'Playfair Display',serif; font-size:26pt; line-height:1; font-weight:600; color:{PROF}; }}
.fn .t {{ display:block; font-size:10pt; margin-top:5px; }}
.fn.f1 {{ width:100%; background:{SABLE}; }} .fn.f2 {{ width:78%; background:#dfe9e1; }} .fn.f3 {{ width:56%; background:#f4e6df; }} .fn.f3 .n {{ color:{TERRA_P}; }}
.fa {{ color:{TERRA_P}; font-size:14pt; line-height:1; }}
.tg {{ background:#fff; border:1px solid #eadfd2; border-radius:10px; padding:12px 16px 8px; margin-bottom:16px; break-inside:avoid; }}
.tg h3 {{ margin:0 0 6px; text-align:center; }}
ul.vl {{ list-style:none; margin:0; padding:0; }} ul.vl li {{ display:flex; justify-content:space-between; gap:10px; padding:6px 0; border-bottom:1px solid #efe6db; margin:0; font-size:10pt; }} ul.vl li:last-child {{ border-bottom:0; }}
ul.vl b {{ font-family:'Playfair Display',serif; color:{PROF}; font-size:11pt; white-space:nowrap; }} ul.vl li.soft {{ color:#6b7a86; }}
.topics td:nth-child(2), .topics th:nth-child(2) {{ text-align:right; white-space:nowrap; }}
.topics td.big {{ font-family:'Playfair Display',serif; font-weight:600; color:{PROF}; font-size:11.5pt; }}
#questions .q {{ break-inside:auto; }} #questions .q b.t, #questions .kpi {{ break-after:avoid; }} thead {{ display:table-header-group; }}
'''

BODY = f'''
<div class="cover">
<div class="kick">Emmanuelle Demeulemeester · Saint-Nazaire</div>
<h1>Audit de visibilité du site</h1>
<div class="rule"></div>
<p class="lead">Emmanuelle Demeulemeester, psychopraticienne à Saint-Nazaire. Relevés du 1er novembre 2026. Objectif du site : que des personnes réservent la séance découverte offerte de 45 minutes.</p>
<div class="method"><h3>Comment lire ce rapport</h3>
<p>L'analyse porte sur <b>284 jours</b>, du 17 janvier au 27 octobre 2026. Le nouveau site a été mis en ligne le <b>8 juin 2026</b>, au milieu de cette période.</p>
<p>On compare donc <b>142 jours avant</b> (17 janvier → 7 juin) et <b>142 jours après</b> (8 juin → 27 octobre) : même durée des deux côtés, pour une comparaison juste.</p>
<div class="frise"><div class="seg a"><b>Avant</b><span>142 jours</span><small>17 janv. → 7 juin</small></div><div class="seg b"><b>Après</b><span>142 jours</span><small>8 juin → 27 oct.</small></div><div class="mark">Mise en ligne du nouveau site · 8 juin 2026</div></div>
<p class="note">Les chiffres viennent de Google (Search Console). Il n'y a pas de compteur de visites sur le site.</p></div>
</div>

<section id="verdict" class="verdict">
<h2>Le verdict en une page</h2>
<div class="cols">
 <div>
  <p class="colh">Trois bonnes nouvelles</p>
  <div class="card good"><h3>1. Le site apparaît un peu plus sur Google</h3><p><b>202 clics</b> venus de Google, contre <b>133</b> avant (142 jours chacun).<br>C'est une tendance, pas une preuve.</p></div>
  <div class="card good"><h3>2. La fiche Google est n°1 sur Maps</h3><p><b>5,0 sur 5 (20 avis)</b>.<br>Première pour « psychopraticienne Saint-Nazaire », et première du bloc « carte » pour « EFT Saint-Nazaire ».</p></div>
  <div class="card good"><h3>3. Le site se distingue</h3><p>Sur 4 praticiennes comparées, aucune autre ne cumule blog, séance découverte offerte et page par méthode.</p></div>
 </div>
 <div>
  <p class="colh warm">Trois points d'attention</p>
  <div class="card bad"><h3>1. L'EMDR est un point faible</h3><p>Pour « EMDR Saint-Nazaire » : place moyenne <b>8,7</b> (Search Console), hors de la 1re page.<br>Le site n'est pas dans le résumé affiché en haut. La fiche Maps est 3e.</p></div>
  <div class="card bad"><h3>2. L'EFT est vue, mais peu cliquée</h3><p>La page EFT apparaît <b>881</b> fois dans Google, pour <b>10</b> clics.<br>Les recherches contenant « EFT » ne rapportent qu'1 clic en tout.</p></div>
  <div class="card bad"><h3>3. Les concurrentes réservent plus vite</h3><p>Chez elles, 1 clic suffit pour réserver, prix affiché.<br>Sur le site, il en faut 2 depuis l'accueil.</p></div>
 </div>
</div>
<p class="meaning" style="margin-top:10mm"><b>Ce que ça veut dire :</b> le site progresse et la fiche Google est solide. Les efforts portent sur l'EMDR et sur la réservation.</p>
<p class="note intro">Les clics viennent de Google seulement. Les points « à confirmer » n'ont pas pu être vérifiés.</p>
</section>

<section id="questions">
<h2>Cinq questions, cinq réponses</h2>
<p class="note intro">Avant = 17 janv. → 7 juin 2026. Après = 8 juin → 27 oct. 2026 (142 jours chacun).<br>« — » : donnée absente de l'export Google. Les petits chiffres sont des tendances, pas des preuves.</p>
<div class="q"><b class="t">1. Combien de vues sur le site ?</b>
<div class="kpi"><div class="v old">133</div><div class="arr">→</div><div class="v">202</div><div class="lbl">clics depuis Google<br>avant → après</div><div class="up">+52 %</div></div>
<table><tr><th></th><th>Avant</th><th>Après</th><th>Évolution</th></tr>
<tr><td>Clics depuis Google</td><td>133</td><td>202</td><td><b>+69 (+52 %)</b></td></tr>
<tr><td>Apparitions dans Google (impressions)</td><td>2 550</td><td>3 364</td><td><b>+814 (+32 %)</b></td></tr>
<tr><td>Part des apparitions qui donnent un clic</td><td>5,2 %</td><td>6,0 %</td><td>+0,8 point</td></tr>
<tr><td>Place moyenne dans Google</td><td>15,6</td><td>13,3</td><td>2,3 places gagnées</td></tr></table>
<p><b>Seul ce qui vient de Google est mesuré.</b> Sans compteur de visites, les visites directes, Bing et réseaux sociaux ne sont pas comptés.</p>
<p class="meaning"><b>Ce que ça veut dire :</b> un peu plus de personnes trouvent le site depuis Google, mais les volumes restent petits.</p>
<ul class="nl"><li>Avant → après : {MA[0]} → {MB[0]} clics sur mobile, {OA[0]} → {OB[0]} sur ordinateur.</li><li>Sur 16 mois (1er juil. 2025 → 30 oct. 2026) : 7 513 apparitions, 441 clics (5,9 %).</li><li>97 % des clics viennent de France ; 304 sur mobile, 128 sur ordinateur.</li></ul></div>
<div class="q"><b class="t">2. Quelles pages sont vues ?</b>
<div class="kpi"><div class="v">69 %</div><div class="lbl">des clics (303 sur 441, sur 16 mois) vont à l'accueil</div></div>
<table><tr><th>Page</th><th>Clics sur 16 mois</th><th>Avant</th><th>Après</th><th>Évolution</th></tr>
{ligne("Accueil", "page:Accueil", "303 sur 441 (69 %)")}
{ligne("Tarifs et modalités", "page:Tarifs et modalités", "30")}
{ligne("Cercle de parole", "page:Cercle de parole", "19")}
{ligne("Préménopause", "page:Préménopause (page)", "13")}
{ligne("Injonctions faites aux femmes", "page:Injonctions faites aux femmes", "12")}
{ligne("Contact", "page:Contact", "12")}
{ligne("Thérapie IFS", "page:Thérapie IFS (page)", "11")}
{ligne("EFT (ancienne page + nouvelle page)", "page:EFT (ancienne → nouvelle page)", "10 (881 apparitions)")}
{ligne("EMDR (ancienne page + nouvelle page)", "page:EMDR (ancienne → nouvelle page)", "4 (637 apparitions)")}</table>
<ul class="nl"><li>Part de l'accueil dans les clics : {PART_A} % avant, {PART_B} % après.</li><li>EFT et EMDR regroupent l'ancienne adresse WordPress et la nouvelle.</li><li>La colonne « 16 mois » couvre plus de jours que « avant » + « après » : ne pas additionner.</li><li>Pages EFT et EMDR : très vues dans Google, très peu cliquées, avant comme après.</li></ul>
<p class="meaning"><b>Ce que ça veut dire :</b> presque toutes les visites passent par l'accueil.</p></div>
<div class="q"><b class="t">3. Quels mots tape-t-on pour trouver le site ?</b>
<div class="kpi"><div class="v">19 %</div><div class="lbl">des clics (82 sur 441, sur 16 mois) ont un mot visible</div></div>
<table><tr><th>Recherche</th><th>Clics sur 16 mois</th><th>Avant</th><th>Après</th><th>Évolution</th></tr>
{ligne("« emmanuelle demeulemeester » (1re ou 2e place)", "req:emmanuelle demeulemeester", "35", "absente de la liste")}
{ligne("Toutes les variantes du nom (demeulemeester, emmanuelle…)", "fam:nom (demeul…, emmanuel…)", "42")}
{ligne("« emdr saint nazaire »", "req:emdr saint nazaire", "17 (652 apparitions, place 8,7)")}
{ligne("« emdr st nazaire »", "req:emdr st nazaire", "4")}
{ligne("Recherches « EFT » (souvent hors secteur : Saumur, Chinon, Ancenis…)", "fam:eft", "1")}
{ligne("« psychopraticien(ne) »", "fam:psychopraticien(ne)", "0")}</table>
<ul class="nl"><li>Qui tape le nom d'Emmanuelle la connaît déjà.</li><li>Google cache les mots peu fréquents : 82 clics sur 441 (19 %) ont un mot visible sur 16 mois.</li><li>Par période : {QV_A[0]} clics sur {TA[0]} avant, {QV_B[0]} sur {TB[0]} après. La hausse des clics « nom » vient en partie de l'export.</li><li>« emmanuelle demeulemeester » est absente de la liste « avant » (masquée ou trop rare).</li></ul>
<p class="meaning"><b>Ce que ça veut dire :</b> le nom d'Emmanuelle domine parmi les mots visibles. Les thérapies rapportent peu de clics.</p></div>
<div class="q"><b class="t">4. Quels articles du blog sont les plus vus ?</b>
<div class="kpi"><div class="v">1</div><div class="lbl">clic, au mieux, par article sous /blog/ sur 16 mois</div></div>
<table><tr><th>Article</th><th>Clics sur 16 mois</th><th>Avant</th><th>Après</th><th>Évolution</th></tr>
{ligne("Contrôle coercitif", "art:le-controle-coercitif", "1", "pas encore dans la liste")}
{ligne("Thérapie IFS (article)", "art:la-therapie-ifs", "1", "pas encore dans la liste")}
{ligne("Comprendre l'EMDR", "art:comprendre-la-therapie-emdr-saint-nazaire", "1")}
{ligne("Thérapie psychocorporelle (article)", "art:la-therapie-psychocorporelle-saint-nazaire", "1")}
{ligne("Thérapie en marchant", "art:la-therapie-en-marchant-saint-nazaire", "0 (41 apparitions)")}
{ligne("Lien d'attachement (vu surtout via l'ancienne adresse WordPress)", "art:comprendre-le-lien-d-attachement-et-ses-blessures-durables", "0 sous /blog/ ; 8 via l'ancienne adresse")}
{ligne("« Quand parler ne suffit plus… »", "art:psychotraumatismes-saint-nazaire", "0 : jamais vu", "aucune ligne", "aucune ligne")}</table>
<ul class="nl"><li>Chaque article regroupe son adresse /blog/ et l'ancienne adresse WordPress du même texte.</li><li>Les rares visites passent encore par les anciennes adresses (préménopause : {PER["art:la-premenopause-entre-40-et-50-ans"][0][0] + PER["art:la-premenopause-entre-40-et-50-ans"][1][0]} clics sur les deux périodes ; lien d'attachement : {PER["art:comprendre-le-lien-d-attachement-et-ses-blessures-durables"][0][0] + PER["art:comprendre-le-lien-d-attachement-et-ses-blessures-durables"][1][0]}).</li><li>Aucun article ne se détache.</li></ul>
<p class="meaning"><b>Ce que ça veut dire :</b> les articles ne rapportent presque aucune visite.</p></div>
<div class="q"><b class="t">5. Où en est le site sur l'EFT et l'EMDR à Saint-Nazaire ?</b>
<div class="kpi"><div class="v old">15,6</div><div class="arr">→</div><div class="v">13,3</div><div class="lbl">place moyenne dans Google<br>avant → après</div><div class="up">2,3 places gagnées</div></div>
<table style="break-inside:avoid"><tr><th>Place moyenne dans Google (Search Console)</th><th>Avant</th><th>Après</th><th>Évolution</th></tr>
<tr><td>Ensemble du site</td><td><b>15,6</b></td><td><b>13,3</b></td><td class="pos"><b>2,3 places gagnées</b></td></tr>
{ligne_pos("« emdr saint nazaire » (8,7 sur 16 mois)", "req:emdr saint nazaire")}
{ligne_pos("Pages EMDR (ancienne + nouvelle)", "page:EMDR (ancienne → nouvelle page)")}
{ligne_pos("Pages EFT (ancienne + nouvelle)", "page:EFT (ancienne → nouvelle page)")}
<tr><td>« eft saint nazaire »</td><td>—</td><td>—</td><td>—</td></tr></table>
<ul class="nl"><li>« eft saint nazaire » est absente des deux listes de Google (trop rare ou masquée).</li><li>La place des pages EFT et EMDR est une moyenne sur toutes les recherches qui les affichent, pas seulement celles de Saint-Nazaire.</li><li>Le relevé ci-dessous (1er nov. 2026, depuis Saint-Nazaire) change selon l'appareil et le lieu.</li></ul>
<table style="break-inside:avoid"><tr><th>Recherche</th><th>Google classique</th><th>Carte Google (Maps)</th><th>Résumé affiché en haut de Google</th></tr>
<tr><td>« EMDR Saint-Nazaire »</td><td>Absente de la 1re page</td><td>3e (derrière Morgane Houarner et le cabinet Hypnose &amp; EMDR-DSA)</td><td>Le site n'y est pas cité</td></tr>
<tr><td>« EFT Saint-Nazaire »</td><td>2e (après Resalib)</td><td><b>1re</b></td><td>Pas de résumé relevé</td></tr>
<tr><td>« Psychopraticienne Saint-Nazaire »</td><td>3e (après psychopraticienne-saint-nazaire.com et Resalib)</td><td><b>1re</b> (carte Maps) ; absente du bloc local de la page Google</td><td>Non lu (à revérifier)</td></tr></table>
<p class="note">Ce relevé n'existe pas « avant » : seule la colonne Search Console permet la comparaison.</p>
<p class="meaning"><b>Ce que ça veut dire :</b> le site reste en retrait sur l'EMDR ; la fiche Google est première sur l'EFT.</p></div>
<div class="gloss"><h2>Mots utilisés</h2>
<dl>
<dt>Impression</dt><dd>Une fois où le site s'affiche dans les résultats de Google, que la personne clique ou non.</dd>
<dt>Clic</dt><dd>Une personne qui clique sur le site dans les résultats Google. C'est la seule « visite » que nous mesurons.</dd>
<dt>Place moyenne</dt><dd>La position moyenne du site dans les résultats Google (1 = tout en haut), selon Google Search Console.</dd>
<dt>Pack local</dt><dd>Les 3 fiches avec carte qui s'affichent en haut de Google pour une recherche près de chez soi (Google Maps).</dd>
</dl>
</div>
</section>

<section id="avant-apres">
<h2>Avant / après le nouveau site</h2>
<p class="intro">Le site est passé de WordPress à un nouveau site le <b>8 juin 2026</b>.<br>On compare deux périodes de 142 jours.</p>
<div class="kpi"><div class="v old">133</div><div class="arr">→</div><div class="v">202</div><div class="lbl">clics depuis Google<br>avant → après</div><div class="up">+52 %</div></div>
<table style="margin-bottom:6px"><tr><th></th><th>Avant (17 janv. → 7 juin)</th><th>Après (8 juin → 27 oct.)</th><th>Écart</th></tr>
<tr><td>Clics depuis Google</td><td>133</td><td>202</td><td><b>+69 (+52 %)</b></td></tr>
<tr><td>Apparitions dans Google</td><td>2 550</td><td>3 364</td><td><b>+814 (+32 %)</b></td></tr>
<tr><td>Place moyenne</td><td>15,6</td><td>13,3</td><td>2,3 places gagnées</td></tr></table>
<div class="cols charts"><div class="chart"><h3>Clics par mois</h3>
{line_chart(mois, "clics", "Clics par mois", SAUGE, 20, H=200)}</div>
<div class="chart"><h3>Apparitions dans Google par mois</h3>
{line_chart(mois, "impressions", "Impressions par mois", PROF, 200, H=200)}</div></div>
<p class="meaning"><b>Ce que ça veut dire :</b> la tendance est positive, sans preuve qu'elle vienne du nouveau site.</p>
<div class="warn"><b>Mise en garde.</b> Une trentaine de clics par mois : de petits chiffres.<ul class="nl" style="color:inherit;font-size:inherit"><li>Le nouveau site n'est pas forcément la cause : 20 articles ont aussi été publiés.</li><li>Juillet → octobre : 45 clics en 2025, 184 en 2026 (base 2025 minuscule).</li><li>Le pic d'août-septembre 2026 reste inexpliqué.</li><li>Aucune chute au moment de la bascule.</li></ul></div>
<div class="warn"><b>Bonus : les réservations Calendly.</b> Elles comptent <u>toutes</u> les origines (site, fiche Google, bouche-à-oreille) : impossible de savoir lesquelles viennent du site.<br>Découpage au mois (5 mois chacun) : <b>avant = janv. → mai 2026, après = juin → oct. 2026</b>.
<table style="margin-top:4px"><tr><th></th><th>Avant</th><th>Après</th><th>Évolution</th></tr>
<tr><td>Réservations maintenues, tous types</td><td>46</td><td>29</td><td>-17</td></tr>
<tr><td>Dont premiers contacts</td><td>15</td><td>10</td><td>-5</td></tr></table>
<p style="margin:.6em 0 .4em;font-size:inherit">Cela ne dit rien sur le site : petits chiffres, et rendez-vous renommés en sept. 2026. <span class="tag">à confirmer en demandant aux patientes</span></p></div>
</section>

<section id="concurrentes">
<h2>Face aux 4 autres praticiennes</h2>
<p class="meaning"><b>Ce que ça veut dire :</b> le site a des atouts rares. L'écart se joue sur la réservation.</p>
<table>
<tr><th>Critère</th><th class="me">Emmanuelle</th><th>Morgane Houarner</th><th>Laurence Martin</th><th>M.-N. Guégan-Leblanc</th><th>Laure Sablé</th></tr>
<tr><td>Métier affiché</td><td class="me">Psychopraticienne</td><td>Psychopraticienne EMDR</td><td>Hypnothérapeute</td><td>Psychologue clinicienne</td><td>Psychothérapeute (Guérande et Saint-Nazaire)</td></tr>
<tr><td>Fiche Google</td><td class="me"><b>5,0 (20 avis)</b></td><td>4,9 (40 avis)</td><td colspan="3">non relevé</td></tr>
<tr><td>Blog</td><td class="me"><b>~20 articles</b></td><td>0</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>Séance offerte</td><td class="me"><b>Oui (45 min)</b></td><td>Non</td><td>Non</td><td>Non</td><td>Non</td></tr>
<tr><td>Prix affiché sur le site</td><td class="me">60 € (page RDV) ; 1er RDV d'1 h : <span class="tag">à confirmer</span></td><td>75 €</td><td>80 €</td><td>60 €</td><td>55 €</td></tr>
<tr><td>Clics pour réserver</td><td class="me">2</td><td>pas de réservation sur le site</td><td>1 (appel)</td><td>1 (Doctolib)</td><td>1 (Doctolib)</td></tr>
<tr><td>Page par méthode, FAQ</td><td class="me">Oui</td><td>Oui, sans FAQ</td><td>Non, FAQ oui</td><td>Non</td><td>Non</td></tr>
</table>
<ul class="nl"><li>Marie-Noëlle Guégan-Leblanc est psychologue (titre protégé) : ne pas l'appeler « psychopraticienne ».</li><li>Morgane Houarner paie aussi des annonces Google sur 3 recherches sur 4 relevées.</li></ul>
<h3>Ce qu'elles font mieux</h3>
<ol class="small" style="margin:.2em 0 0 1.2em;padding:0">
<li><b>Réservation en 1 clic</b> depuis l'accueil, bouton répété dans la page.</li>
<li><b>Prix à côté du bouton</b> (Laure Sablé).</li>
<li><b>Lien « voir les avis Google »</b> visible (Laurence Martin). Le site n'y renvoie pas, malgré 20 avis.</li>
<li><b>Fiche Google comme porte de réservation</b> (Morgane Houarner).</li>
<li><b>Présence dans les annuaires</b> (Doctolib, Resalib, etc.).</li>
<li><b>FAQ sur l'accueil</b> pour lever la peur du premier pas.</li>
</ol>
<ul class="nl"><li>À ne pas copier : les témoignages anonymes.</li><li>Morgane Houarner est de loin la plus visible sur l'EMDR à Saint-Nazaire.</li><li>Place exacte sur Google : relevée pour 4 recherches seulement.</li></ul>
</section>

<section id="morgane" class="pg">
<h2>Pourquoi Morgane Houarner apparaît partout</h2>
<p class="intro">Relevé du 1er nov. 2026 sur 24 recherches locales : Morgane Houarner est très visible.<br>Voici ce qui l'explique.</p>
<p class="meaning"><b>Ce que ça veut dire :</b> son avance vient de la publicité et des avis, pas de son site.</p>
<div class="card bad"><h3>1. Elle paie de la publicité Google</h3><p>Annonce « sponsorisée » sur <b>8 recherches sur 24</b>, tout en haut de la page.<br>Elle <b>paie</b> cette place : cela ne prouve pas que son site est meilleur.</p></div>
<div class="card bad"><h3>2. Sa fiche Google a deux fois plus d'avis</h3><p><b>40 avis</b> (note 4,9) contre <b>20</b> (note 5,0), et elle répond à chaque avis récent.<br>Dans le bloc des 3 fiches : présente sur 4 recherches sur 24, contre 3 pour Emmanuelle (n°1 sur « EFT » et « psychopraticienne »). L'écart est faible.</p></div>
<div class="card bad"><h3>3. Elle est dans deux annuaires où Emmanuelle n'est pas</h3><p><b>Crénolibre</b> et <b>Psychologue.net</b> : sa fiche Crénolibre sort 2e sur « psychopraticien Saint-Nazaire ».<br>Les assistants IA les citent souvent (Crénolibre 6 fois, Psychologue.net 8 fois dans nos tests).<br>Emmanuelle est sur Resalib (5,0), pas sur ces deux-là.</p></div>
<div class="card good"><h3>Ce qui n'explique pas son avance</h3><p><b>L'ancienneté :</b> les deux sites sont jeunes (archivés en sept. 2023 pour elle, oct. 2024 pour Emmanuelle).<br><b>Son site :</b> dans les 10 premiers résultats sur <b>aucune</b> des 24 recherches.<br><b>Le contenu :</b> celui d'Emmanuelle est plus complet (accueil d'environ 1 200 mots contre 130, une vingtaine d'articles, une FAQ).</p></div>
<h3>Ce qui peut être rattrapé</h3>
<table>
<tr><th>Levier</th><th>Rattrapable ?</th><th>Coût</th></tr>
<tr><td>Avis Google (de 20 vers 40) et publications sur la fiche</td><td><b>Oui</b></td><td>Gratuit</td></tr>
<tr><td>Fiches Crénolibre et Psychologue.net</td><td><b>Oui</b></td><td>À vérifier avant</td></tr>
<tr><td>Fiche Resalib à compléter (EMDR, avis)</td><td><b>Oui</b></td><td>À vérifier</td></tr>
<tr><td>Publicité Google</td><td>Seulement avec un budget</td><td>Payant : à décider ensemble</td></tr></table>
</section>

<section id="recherches" class="pg">
<h2>Sur quelles recherches le site apparaît</h2>
<p class="note intro">Relevé du 1er nov. 2026 depuis Saint-Nazaire, 24 recherches, <b>page 1 de Google seulement</b> (places 11 à 20 non lues).<br>Cela bouge d'un jour à l'autre.</p>
<div class="cols">
<div>
 <p class="colh">Déjà bien placée</p>
 <div class="card good"><h3><span class="rk">1re</span> thérapie en marchant</h3><p>Site 1er.</p></div>
 <div class="card good"><h3><span class="rk">1re</span> soutien post-partum</h3><p>Site 1er.</p></div>
 <div class="card good"><h3><span class="rk">2e</span> EFT Saint-Nazaire</h3><p>Site 2e ; fiche Google n°1.</p></div>
 <div class="card good"><h3><span class="rk">3e</span> psychopraticienne Saint-Nazaire</h3><p>Site 3e ; fiche Google n°1.</p></div>
 <div class="card good"><h3><span class="rk">3e</span> thérapie psychocorporelle</h3><p>Site 3e.</p></div>
</div>
<div>
 <p class="colh mid">À portée de main</p>
 <div class="card mid-c"><h3>EMDR Saint-Nazaire</h3><p>Fiche Google <b>3e</b> du bloc des 3 fiches. Place moyenne du site : <b>8,7</b> (16 mois).<br>Au relevé du 1er nov., hors des 10 premiers résultats.</p><p class="why">110 recherches par mois (Semrush).</p></div>
 <div class="card mid-c"><h3>Psychopraticien, thérapie brève, anxiété, EMDR Pornichet</h3><p>Présent dans le bloc « sites web associés », mais hors des 10 premiers résultats.</p></div>
</div>
<div>
 <p class="colh grey">Pas encore visible</p>
 <div class="card grey-c"><h3>Les autres villes</h3><p>La Baule, Guérande, Pornichet : EMDR La Baule, EMDR Guérande, psychopraticienne La Baule et Guérande, thérapeute Pornichet.</p></div>
 <div class="card grey-c"><h3>Les autres thèmes</h3><p>Traumatisme, burn-out, couple, hypnose, thérapie en visio, et les mots très généraux (« psy », « psychologue », « thérapeute »).</p></div>
</div>
</div>
<div class="warn"><b>Priorité n°1 : l'EMDR.</b><ul class="nl" style="color:inherit;font-size:inherit"><li>La fiche Google est dans le bloc des 3 fiches.</li><li>L'ancienne page EMDR est apparue 637 fois en 16 mois, pour 4 clics.</li><li>Renforcer cette page peut faire passer de « visible » à « choisi ».</li></ul></div>
</section>

<section id="volumes" class="vol">
<h2>Combien de personnes cherchent ?</h2>
<p class="note intro">Sur le cœur de l'offre locale : EMDR à Saint-Nazaire, La Baule et Guérande, plus une recherche voisine. Ordre de grandeur, par mois.</p>
<div class="funnel">
<div class="fn f1"><span class="n">180</span><span class="t">recherches par mois</span></div><div class="fa">▼</div>
<div class="fn f2"><span class="n">~97</span><span class="t">apparitions du site sur ces recherches (environ 54 %)</span></div><div class="fa">▼</div>
<div class="fn f3"><span class="n">~2,6</span><span class="t">clics par mois</span></div>
</div>
<p class="meaning"><b>Ce que ça veut dire :</b> le site est déjà vu par une bonne part des personnes qui cherchent l'EMDR près de Saint-Nazaire. Très peu cliquent, car il est en bas de la 1re page. Gagner quelques places compte plus que d'être vu davantage.</p>
<div class="warn"><b>À savoir.</b><ul class="nl" style="color:inherit;font-size:inherit"><li>Les recherches locales sont peu nombreuses : beaucoup de mots sont à 0 ou trop faibles pour être mesurés (dont EFT et psychopraticienne avec une ville).</li><li>Ces chiffres sont des estimations (Semrush) : à lire comme des ordres de grandeur.</li></ul></div>
</section>

<section id="sujets" class="vol">
<h2>Les sujets les plus recherchés</h2>
<p class="note intro">Recherches par mois, dans toute la France (Semrush, estimations).</p>
<div class="cols tcols">
<div>
 <div class="tg"><h3>Post-partum</h3><ul class="vl"><li><span>baby blues</span><b>5 400</b></li><li><span>postpartum</span><b>2 900</b></li><li><span>définition post partum</span><b>1 000</b></li><li><span>post accouchement</span><b>590</b></li><li><span>post partum c'est quoi</span><b>320</b></li><li class="soft"><span>dépression post partum</span><b>9 900</b></li></ul><p class="note">« dépression post partum » : très concurrentiel.</p></div>
 <div class="tg"><h3>Émotions et confiance</h3><ul class="vl"><li><span>retrouver confiance en soi</span><b>320</b></li><li><span>gérer ses émotions</span><b>140</b></li><li><span>gérer son anxiété</span><b>110</b></li></ul></div>
</div>
<div>
 <div class="tg"><h3>Deuil</h3><ul class="vl"><li><span>définition d'un deuil</span><b>1 300</b></li><li><span>deuil phases</span><b>480</b></li><li><span>en deuil</span><b>480</b></li><li><span>faire un deuil</span><b>390</b></li><li><span>comment faire son deuil</span><b>320</b></li></ul></div>
 <div class="tg"><h3>Méthodes</h3><ul class="vl"><li><span>EFT thérapie</span><b>1 000</b></li><li><span>tapping EFT</span><b>170</b></li><li><span>EMDR en visio</span><b>90</b></li></ul></div>
</div>
</div>
<ul class="nl"><li>Ce sont des recherches dans toute la France.</li><li>Elles amènent des lectrices au blog. Elles deviennent patientes surtout via la visio, ou si elles habitent la région.</li><li>Idée : un article par sujet, qui renvoie vers la séance (cabinet ou visio).</li></ul>
</section>

<section id="maintenant" class="pg next">
<h2>Les prochaines étapes</h2>
<div class="cols">
<div>
 <p class="colh">À faire de ton côté (sans technique)</p>
 <div class="card good"><h3>Demander des avis Google</h3><p>Proposer aux patientes satisfaites de laisser un avis, puis répondre à chacun.<br>Passer de 20 à 40 avis est le levier le plus simple.</p></div>
 <div class="card good"><h3>Publier sur la fiche Google</h3><p>Une courte publication de temps en temps (une actualité, un atelier, un thème).</p></div>
 <div class="card good"><h3>Créer deux fiches d'annuaire</h3><p>Crénolibre et Psychologue.net, où est Morgane Houarner. <b>Vérifier le coût</b> avant toute inscription.</p></div>
 <div class="card good"><h3>Compléter la fiche Resalib</h3><p>Ajouter l'EMDR comme spécialité et recueillir des avis.</p></div>
</div>
<div>
 <p class="colh warm">À améliorer sur le site</p>
 <div class="card bad"><h3>Renforcer la page EMDR</h3><p>Pour qu'elle sorte sur « EMDR Saint-Nazaire », la recherche prioritaire.</p></div>
 <div class="card bad"><h3>Réserver plus directement</h3><p>Un seul clic pour prendre rendez-vous, avec le prix visible. <b>Information attendue : le tarif du 1er rendez-vous d'1 h.</b></p></div>
 <div class="card bad"><h3>Retrouver les anciennes pages</h3><p>Les anciennes adresses doivent mener vers les nouvelles.<br>52 d'entre elles sont encore vues sur Google : 136 clics.</p></div>
 <div class="card bad"><h3>Relier le blog aux séances</h3><p>Chaque article renverra vers la page de séance qui correspond.</p></div>
 <div class="card bad"><h3>Écrire sur les sujets les plus recherchés</h3><p>Écrire des articles sur les sujets les plus recherchés (post-partum, deuil, confiance en soi).</p></div>
</div>
</div>
<div class="warn" style="border-left-color:#5C7A62"><b>Point dans 3 mois</b>, avec les mêmes chiffres qu'aujourd'hui.
<table style="margin-top:6px"><tr><th></th><th>Aujourd'hui</th><th>Dans 3 mois</th></tr>
<tr><td>Clics depuis Google (142 jours après la bascule)</td><td>202</td><td>—</td></tr>
<tr><td>Place moyenne dans Google</td><td>13,3</td><td>—</td></tr>
<tr><td>Place moyenne de « emdr saint nazaire » (16 mois)</td><td>8,7</td><td>—</td></tr>
<tr><td>« EMDR Saint-Nazaire » : place de la fiche Google</td><td>3e</td><td>—</td></tr>
<tr><td>Avis Google</td><td>20</td><td>—</td></tr></table></div>
</section>

<section id="sources">
<h2>Sources</h2>
<p class="note">Chaque chiffre vient de ces fichiers du dossier d'audit (fichiers bruts non joints au rapport). Ce qui n'a pas pu être vérifié est écrit « à confirmer ».</p>
<ul class="small">
<li><b>audit/analyses/05-gsc-avant-apres.md</b>, <b>gsc-periodes.csv</b>, <b>audit/data/gsc/avant/</b> et <b>audit/data/gsc/apres/</b> (Pages, Requêtes, Appareils, Graphique) : pages, mots tapés, articles, appareils et place moyenne avant / après (exports Google Search Console par période, 142 jours chacune).</li>
<li><b>audit/analyses/01-gsc.md</b>, <b>gsc-par-mois.csv</b>, <b>gsc-vs-calendly-par-mois.csv</b>, <b>audit/data/calendly/rdv-par-mois-anonyme.csv</b> : clics, impressions, pages, mots tapés, avant/après, Calendly (exports Google Search Console, 16 mois, et comptes Calendly anonymes).</li>
<li><b>audit/analyses/03-concurrents.md</b> : comparaison des 4 praticiennes (lecture de leurs sites publics).</li>
<li><b>audit/analyses/04-blog.md</b>, <b>blog-stats.csv</b> : état des 20 articles (lecture seule).</li>
<li><b>audit/data/serp/serp.md</b>, <b>matrice-mots-cles.md</b> : relevé Google et Maps du 1er nov. 2026 (4 puis 24 recherches).</li>
<li><b>audit/data/concurrents/morgane-pourquoi.md</b> : pourquoi Morgane Houarner est très visible (annonces, fiche Google, annuaires).</li>
<li><b>audit/analyses/06-volumes.md</b>, <b>06-volumes.csv</b> : volumes de recherche par mois et sujets les plus recherchés (Semrush, estimations nov. 2026).</li>
<li><b>audit/data/semrush-ui/semrush-mcp-2026-11-01.md</b>, <b>plan-audit.html</b> : volume de recherche de « emdr saint nazaire » (110 par mois, Semrush).</li>
</ul>
<h3>Reste à confirmer</h3>
<ul class="small">
<li>Tarif du 1er RDV d'1 h : à confirmer.</li>
<li>Origine des réservations Calendly : à confirmer auprès des patientes.</li>
<li>Fiche Google des 3 autres concurrentes : non relevée.</li>
<li>Effet de la panne du site du 28 octobre : non mesuré (hors des périodes comparées).</li>
</ul>
</section>
'''

import re
BODY = re.sub(r'<table([^>]*)><tr>(<th.*?</tr>)', r'<table\1><thead><tr>\2</thead>', BODY, flags=re.S)
BODY = re.sub(r'<td><b>(\+\d)', r'<td class="pos"><b>\1', BODY)
for k, v in PRON.items():
    BODY = BODY.replace(k, v)

HTML = f'''<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><title>Audit de visibilité</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Lato:wght@400;700&family=Playfair+Display:wght@600;700&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>{BODY}</body></html>'''
with open(os.path.join(HERE, "rapport.html"), "w", encoding="utf-8") as f:
    f.write(HTML)
print("ok")

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

def line_chart(data, key, title, color, ymax_step):
    W, H, L, R, T, B = 700, 250, 46, 16, 22, 46
    n = len(data); vals = [int(r[key]) for r in data]
    ymax = ((max(vals) // ymax_step) + 1) * ymax_step
    x = lambda i: L + i * (W - L - R) / (n - 1)
    y = lambda v: T + (H - T - B) * (1 - v / ymax)
    s = [f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="{title}">']
    for g in range(0, ymax + 1, ymax_step):
        s.append(f'<line x1="{L}" x2="{W-R}" y1="{y(g):.1f}" y2="{y(g):.1f}" stroke="#d9cfc2" stroke-width="0.7"/>')
        s.append(f'<text x="{L-6}" y="{y(g)+3:.1f}" text-anchor="end" font-size="9" fill="{ANTH}">{g}</text>')
    # bascule juin 2026
    i6 = [r["mois"] for r in data].index("2026-06")
    s.append(f'<rect x="{x(i6):.1f}" y="{T}" width="{W-R-x(i6):.1f}" height="{H-T-B}" fill="{SABLE}" opacity="0.45"/>')
    s.append(f'<line x1="{x(i6):.1f}" x2="{x(i6):.1f}" y1="{T-8}" y2="{H-B}" stroke="{TERRA_P}" stroke-width="1.6" stroke-dasharray="5 3"/>')
    s.append(f'<text x="{x(i6)-5:.1f}" y="{T-10}" text-anchor="end" font-size="10" fill="{TERRA_P}" font-weight="700">Nouveau site (juin 2026)</text>')
    pts = " ".join(f"{x(i):.1f},{y(v):.1f}" for i, v in enumerate(vals))
    s.append(f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="2.6" stroke-linejoin="round"/>')
    for i, v in enumerate(vals):
        s.append(f'<circle cx="{x(i):.1f}" cy="{y(v):.1f}" r="3.2" fill="{color}"/>')
    for i, r in enumerate(data):
        if i % 2 == 0 or i == n - 1:
            s.append(f'<text x="{x(i):.1f}" y="{H-B+16}" text-anchor="middle" font-size="9" fill="{ANTH}">{lab(r["mois"])}</text>')
    # valeurs max
    mi = vals.index(max(vals))
    s.append(f'<text x="{x(mi):.1f}" y="{y(vals[mi])-8:.1f}" text-anchor="middle" font-size="10" font-weight="700" fill="{PROF}">{vals[mi]}</text>')
    s.append('</svg>')
    return "".join(s)

def hbars(items, maxv, color, unit="", w=640):
    """items = [(label, value, texte_valeur)]"""
    lh, lw = 26, 190
    H = lh * len(items) + 4
    s = [f'<svg viewBox="0 0 {w} {H}" width="100%" role="img">']
    for i, (l, v, t) in enumerate(items):
        yy = i * lh + 2
        bw = (w - lw - 70) * v / maxv
        s.append(f'<text x="{lw-8}" y="{yy+16}" text-anchor="end" font-size="11" fill="{ANTH}">{l}</text>')
        s.append(f'<rect x="{lw}" y="{yy+4}" width="{max(bw,2):.1f}" height="16" rx="2" fill="{color}"/>')
        s.append(f'<text x="{lw+max(bw,2)+6:.1f}" y="{yy+16}" font-size="11" font-weight="700" fill="{PROF}">{t}</text>')
    s.append('</svg>')
    return "".join(s)

def calendly_chart(cal):
    cal = [r for r in cal if r["mois"] >= "2025-09"]
    W, H, L, R, T, B = 700, 190, 30, 10, 14, 34
    n = len(cal); bw = (W - L - R) / n
    mc = max(int(r["clics_gsc"]) for r in cal)
    s = [f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="clics Google et premiers contacts par mois">']
    for i, r in enumerate(cal):
        c, p = int(r["clics_gsc"]), int(r["premiers_contacts_calendly"])
        x0 = L + i * bw
        hc = (H - T - B) * c / mc
        s.append(f'<rect x="{x0+3:.1f}" y="{H-B-hc:.1f}" width="{bw/2-3:.1f}" height="{hc:.1f}" fill="{SAUGE}"/>')
        hp = (H - T - B) * p / mc * 3  # échelle x3 pour lisibilité (annoncée dans la légende)
        s.append(f'<rect x="{x0+bw/2:.1f}" y="{H-B-hp:.1f}" width="{bw/2-3:.1f}" height="{hp:.1f}" fill="{TERRA}"/>')
        s.append(f'<text x="{x0+bw/2+ (bw/2-3)/2:.1f}" y="{H-B-hp-3:.1f}" text-anchor="middle" font-size="9" font-weight="700" fill="{TERRA_P}">{p}</text>')
        s.append(f'<text x="{x0+bw/2:.1f}" y="{H-B+13}" text-anchor="middle" font-size="8" fill="{ANTH}">{lab(r["mois"])}</text>')
    s.append('</svg>')
    return "".join(s)

def sign_svg():
    return f'''<svg viewBox="0 0 700 215" width="100%" role="img" aria-label="Panneau de déviation">
<rect x="0" y="150" width="700" height="46" fill="#d9d2c7"/>
<line x1="0" y1="173" x2="700" y2="173" stroke="#fff" stroke-width="3" stroke-dasharray="18 12"/>
<text x="95" y="18" text-anchor="middle" font-size="12" font-weight="700" fill="{ANTH}">Avant : rien n'est prévu</text>
<rect x="30" y="30" width="130" height="38" rx="4" fill="{SABLE}"/><text x="95" y="54" text-anchor="middle" font-size="11" fill="{ANTH}">Google [[vous]] envoie</text>
<rect x="30" y="100" width="130" height="38" rx="4" fill="{SABLE}"/><text x="95" y="124" text-anchor="middle" font-size="10" fill="{ANTH}">/eft-saint-nazaire/</text>
<path d="M95 68 V98" stroke="{ANTH}" stroke-width="2" marker-end="url(#a)"/>
<g transform="translate(205,68)"><rect x="-6" y="0" width="12" height="82" fill="#8a8a8a"/><circle cx="0" cy="-8" r="30" fill="#fff" stroke="{TERRA_P}" stroke-width="7"/><line x1="-19" y1="-8" x2="19" y2="-8" stroke="{TERRA_P}" stroke-width="7"/></g>
<text x="205" y="164" text-anchor="middle" font-size="11" font-weight="700" fill="{TERRA_P}">Route barrée (404)</text>
<line x1="350" y1="20" x2="350" y2="140" stroke="#bbb" stroke-dasharray="3 4"/>
<text x="520" y="18" text-anchor="middle" font-size="12" font-weight="700" fill="{PROF}">Après : un panneau de déviation (301)</text>
<rect x="380" y="100" width="130" height="38" rx="4" fill="{SABLE}"/><text x="445" y="124" text-anchor="middle" font-size="10" fill="{ANTH}">/eft-saint-nazaire/</text>
<rect x="380" y="30" width="130" height="38" rx="4" fill="{SABLE}"/><text x="445" y="54" text-anchor="middle" font-size="11" fill="{ANTH}">Google [[vous]] envoie</text>
<path d="M445 68 V98" stroke="{ANTH}" stroke-width="2" marker-end="url(#a)"/>
<g transform="translate(540,85)"><rect x="0" y="0" width="64" height="30" fill="{PROF}" rx="4"/><path d="M8 15 H44 M36 8 L46 15 L36 22" stroke="#fff" stroke-width="3" fill="none"/></g>
<path d="M510 119 H536" stroke="{ANTH}" stroke-width="2" marker-end="url(#a)"/>
<rect x="620" y="100" width="72" height="38" rx="4" fill="{SAUGE}"/><text x="656" y="116" text-anchor="middle" font-size="9" fill="#fff" font-weight="700">Page EFT</text><text x="656" y="129" text-anchor="middle" font-size="9" fill="#fff">actuelle</text>
<path d="M604 100 H618" stroke="{ANTH}" stroke-width="2" marker-end="url(#a)"/>
<defs><marker id="a" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0 0 L8 4 L0 8z" fill="{ANTH}"/></marker></defs>
</svg>'''

mois = rows("gsc-par-mois.csv")
cal = rows("gsc-vs-calendly-par-mois.csv")

CSS = f'''
@page {{ size: A4; margin: 13mm 14mm 14mm 14mm; }}
* {{ box-sizing: border-box; }}
html {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
body {{ margin:0; background:{FOND}; color:{ANTH}; font-family:'Lato',Arial,sans-serif; font-size:10.3pt; line-height:1.42; }}
h1,h2,h3 {{ font-family:'Playfair Display',Georgia,serif; color:{PROF}; margin:0 0 .3em; line-height:1.15; }}
h1 {{ font-size:25pt; }} h2 {{ font-size:18pt; border-bottom:2px solid {TERRA}; padding-bottom:3px; margin-bottom:.5em; }}
h3 {{ font-size:12.5pt; margin-top:.8em; }}
p {{ margin:.3em 0 .55em; }}
section {{ page-break-after: always; break-after: page; }}
section:last-child {{ page-break-after: auto; break-after: auto; }}
.bandeau {{ background:{SABLE}; color:{TERRA_P}; font-size:8.5pt; text-align:center; padding:3px 8px; border-radius:3px; margin-bottom:8px; font-weight:700; letter-spacing:.02em; }}
.cols {{ display:flex; gap:12px; }} .cols > div {{ flex:1; }}
.card {{ background:#fff; border:1px solid {SABLE}; border-radius:6px; padding:9px 11px; break-inside:avoid; }}
.good {{ border-top:5px solid {SAUGE}; }} .bad {{ border-top:5px solid {TERRA}; }}
.card h3 {{ margin-top:0; font-size:11.5pt; }}
.big {{ font-family:'Playfair Display',serif; font-size:22pt; color:{PROF}; line-height:1; }}
.first {{ background:{PROF}; color:#fff; border-radius:6px; padding:11px 14px; margin-top:10px; }}
.first h3 {{ color:#fff; margin:0 0 3px; }}
table {{ border-collapse:collapse; width:100%; font-size:9pt; background:#fff; }}
th,td {{ border:1px solid {SABLE}; padding:4px 6px; vertical-align:top; text-align:left; }}
th {{ background:{PROF}; color:#fff; font-weight:700; }}
td.me, th.me {{ background:#f3ece3; }} th.me {{ background:{PROF}; }}
.note {{ font-size:8.8pt; color:#4a5a68; }}
.warn {{ background:#fff; border-left:5px solid {TERRA}; padding:5px 10px; font-size:9.3pt; margin:.5em 0; break-inside:avoid; }}
.tag {{ display:inline-block; font-size:8pt; font-weight:700; padding:1px 6px; border-radius:9px; background:{SABLE}; color:{TERRA_P}; }}
.tag.ok {{ background:#dfe9e1; color:{PROF}; }}
.q {{ margin:0 0 7px; padding:6px 10px; background:#fff; border:1px solid {SABLE}; border-radius:5px; break-inside:avoid; }}
.q b.t {{ font-family:'Playfair Display',serif; color:{PROF}; font-size:11.2pt; }}
.q p {{ margin:.15em 0; }}
ul {{ margin:.2em 0 .4em 1.1em; padding:0; }} li {{ margin:.1em 0; }}
.act {{ display:flex; gap:10px; margin-bottom:7px; background:#fff; border:1px solid {SABLE}; border-radius:6px; padding:7px 10px; break-inside:avoid; }}
.num {{ flex:0 0 34px; height:34px; border-radius:50%; background:{PROF}; color:#fff; font-family:'Playfair Display',serif; font-size:16pt; text-align:center; line-height:34px; }}
.act h3 {{ margin:0 0 2px; font-size:11.5pt; }} .act p {{ margin:.15em 0; font-size:9.5pt; }}
.who {{ font-size:8.8pt; color:{TERRA_P}; font-weight:700; }}
dl {{ margin:0; }} dt {{ font-family:'Playfair Display',serif; font-weight:700; color:{PROF}; font-size:12pt; margin-top:.7em; }} dd {{ margin:.1em 0 0; }}
.small li {{ font-size:9.3pt; }}
'''

BODY = f'''
<section id="verdict">
<div class="bandeau">BROUILLON — en attente des données Netlify, Semrush et des exports GSC par période</div>
<h1>Audit de visibilité de [[votre]] site</h1>
<p class="note">Emmanuelle Demeulemeester, psychopraticienne à Saint-Nazaire. Relevés du 1er novembre 2026. Objectif du site : que des personnes réservent la séance découverte offerte de 45 minutes.</p>
<h2>Le verdict en une page</h2>
<div class="cols">
 <div>
  <p><b style="color:{PROF}">Trois bonnes nouvelles</b></p>
  <div class="card good"><h3>1. Google [[vous]] montre un peu plus</h3><p>Depuis le nouveau site : <b>202 clics</b> venus de Google, contre <b>133</b> avant (mêmes durées de 142 jours). C'est une tendance, pas une preuve : les volumes sont petits.</p></div><br>
  <div class="card good"><h3>2. [[Vous]] êtes n°1 sur Google Maps</h3><p>Pour « psychopraticienne Saint-Nazaire », [[votre]] fiche est première : <b>5,0 sur 5 (20 avis)</b>. Elle est aussi première du bloc « carte » pour « EFT Saint-Nazaire ».</p></div><br>
  <div class="card good"><h3>3. [[Votre]] site est en avance</h3><p>Sur les 4 praticiennes comparées, [[vous]] êtes la seule à avoir un blog, une séance découverte offerte et une page par méthode. Le site est très rapide (notes de 96 à 100 sur 100).</p></div>
 </div>
 <div>
  <p><b style="color:{TERRA_P}">Trois problèmes</b></p>
  <div class="card bad"><h3>1. Des anciennes adresses mènent à une impasse</h3><p><b>61 adresses de l'ancien site</b> affichent « page introuvable ». Google les connaît encore : elles ont reçu <b>136 clics</b> en 16 mois.</p></div><br>
  <div class="card bad"><h3>2. L'EMDR est un point faible</h3><p>Aucune des 4 intelligences artificielles testées ne [[vous]] cite sur l'EMDR, et le site n'est pas sur la 1re page de Google pour « EMDR Saint-Nazaire ». L'EFT reçoit 1 clic seulement.</p></div><br>
  <div class="card bad"><h3>3. Le chemin vers la réservation est long</h3><p>Il faut 2 clics depuis l'accueil, aucun prix n'est près du bouton, et <b>aucun des 20 articles</b> ne renvoie vers la séance dans son texte. De plus, on ne sait pas d'où viennent les réservations.</p></div>
 </div>
</div>
<div class="first"><h3>La première action</h3><p style="margin:0">Mettre en place des <b>redirections</b> (des « panneaux de déviation ») pour que les anciennes adresses mènent aux bonnes pages. La liste est déjà prête. C'est rapide, gratuit, et cela récupère ce que Google envoie déjà.</p></div>
<p class="note" style="margin-top:8px">Les chiffres de clics viennent de Google seulement (voir page suivante). Les points marqués « à confirmer » n'ont pas pu être vérifiés.</p>
</section>

<section id="questions">
<h2>[[Vos]] 5 questions, réponses simples</h2>
<div class="q"><b class="t">1. Combien de vues sur le site ?</b>
<p><b>On ne sait mesurer que ce qui vient de Google.</b> Aucun outil de comptage des visites n'est activé à ce jour : <span class="tag">à confirmer (Nicolas, Netlify)</span>. Les visites directes, par Bing ou par les réseaux sociaux ne sont donc pas comptées.</p>
<p>Ce que Google nous donne, du 1er juillet 2025 au 30 octobre 2026 (16 mois) : <b>7 513 fois</b> où le site est apparu dans une recherche (« impressions ») et <b>441 clics</b> pour y entrer. Soit 5,9 % des apparitions. 97 % des clics viennent de France ; 304 sur mobile, 128 sur ordinateur.</p></div>
<div class="q"><b class="t">2. Quelles pages sont vues ?</b>
<p>L'accueil fait tout : <b>303 clics sur 441</b> (69 %). Ensuite : la page tarifs et modalités (30), le cercle de parole (19), la préménopause (13), les injonctions faites aux femmes (12), la page contact (12), la thérapie IFS (11), l'EFT (10) et l'EMDR (4). Attention : presque toutes ces pages sont d'<b>anciennes adresses</b> (voir page 5). Les pages EFT et EMDR sont très vues (881 et 637 apparitions) mais très peu cliquées.</p>
<p class="note">Comparer « avant / après » page par page n'est pas encore possible : il manque les exports Google par période (à recevoir).</p></div>
<div class="q"><b class="t">3. Quels mots tape-t-on pour [[vous]] trouver ?</b>
<ul class="small"><li>Son nom : « emmanuelle demeulemeester » : 35 clics, en 1re ou 2e place. Les gens [[vous]] connaissent déjà.</li>
<li>« emdr saint nazaire » : 17 clics sur 652 apparitions (place moyenne 8,7). Variantes : « emdr st nazaire », 4 clics.</li>
<li>EFT : 1 clic en tout. Les recherches EFT qui [[vous]] montrent sont souvent hors secteur (Saumur, Chinon, Ancenis…).</li>
<li>« psychopraticien(ne) » : 0 clic.</li></ul>
<p class="note">Google cache les mots peu fréquents : seuls 82 clics sur 441 (19 %) ont un mot visible.</p></div>
<div class="q"><b class="t">4. Quels articles du blog sont les plus vus ?</b>
<p>Aucun ne se détache : les 5 premiers n'ont qu'<b>1 clic</b> chacun (contrôle coercitif, thérapie IFS, comprendre l'EMDR, psychocorporel ; la thérapie en marchant a 0 clic mais 41 apparitions). Deux articles n'ont <b>jamais été vus</b> : celui sur le lien d'attachement (sous sa nouvelle adresse) et « Quand parler ne suffit plus… ». Le vrai trafic « blog » est encore sur d'anciennes adresses (l'attachement : 8 clics ; la préménopause : 13).</p></div>
<div class="q"><b class="t">5. Quelle est [[votre]] place sur l'EFT et l'EMDR à Saint-Nazaire ?</b>
<table><tr><th>Recherche</th><th>Google classique</th><th>Carte Google (Maps)</th><th>IA</th></tr>
<tr><td>« EMDR Saint-Nazaire »</td><td>Absente de la 1re page</td><td>3e (derrière Morgane Houarner et le cabinet Hypnose &amp; EMDR-DSA)</td><td>Absente de l'Aperçu IA de Google et des 4 IA testées</td></tr>
<tr><td>« EFT Saint-Nazaire »</td><td>2e (après Resalib)</td><td><b>1re</b></td><td>Citée par les 4 IA (question « EFT »)</td></tr>
<tr><td>« Psychopraticienne Saint-Nazaire »</td><td>2e ou 3e</td><td><b>1re</b> (carte Maps) ; absente du bloc local de la page Google</td><td>Citée par 3 IA sur 4</td></tr></table>
<p class="note">Relevé du 1er nov. 2026 depuis Saint-Nazaire. La place change selon l'appareil et le lieu. Google indique 8,7 en place moyenne sur « emdr saint nazaire » : c'est une moyenne sur 16 mois, pas une place du jour.</p></div>
</section>

<section id="bonus">
<h2>Bonus : les réservations de séance découverte</h2>
<p>Voici, mois par mois, les clics venus de Google (vert) et les « premiers contacts » réservés sur Calendly (rose, barres étirées pour être lisibles ; le chiffre est écrit au-dessus). Calendly a compté <b>136 rendez-vous depuis septembre 2025</b>, tous types confondus ; <b>36 premiers contacts</b> non annulés (somme des mois), sans aucun nom.</p>
{calendly_chart(cal)}
<div class="warn"><b>Ce qu'on ne peut pas dire.</b> Les deux courbes ne bougent pas ensemble : en décembre et janvier, beaucoup de premiers contacts (6 et 7) pour peu de clics ; en août et septembre, des clics au plus haut (61 et 63) mais 2 premiers contacts. Les réservations viennent peut-être d'ailleurs (bouche-à-oreille, fiche Google, annuaires) : <span class="tag">à confirmer en demandant aux patientes</span>. Les liens Calendly du site n'ont aucun marqueur de provenance : impossible de savoir lesquelles viennent du site. Petits volumes : lire une tendance, pas une preuve.</div>
<p class="note">Mois = mois de la séance, pas du clic. Les types de rendez-vous ont été renommés le 3 sept. 2026 : le regroupement « premier contact » est un choix d'analyse.</p>
</section>

<section id="avant-apres">
<h2>Avant / après le nouveau site</h2>
<p>Le site est passé de WordPress à un nouveau site en <b>juin 2026</b> (date de bascule : 8 juin, <span class="tag">à confirmer (historique Netlify)</span>). On compare deux périodes de 142 jours.</p>
<table style="margin-bottom:8px"><tr><th></th><th>Avant (17 janv. → 7 juin)</th><th>Après (8 juin → 27 oct.)</th><th>Écart</th></tr>
<tr><td>Clics depuis Google</td><td>133</td><td>202</td><td><b>+69 (+52 %)</b></td></tr>
<tr><td>Apparitions dans Google</td><td>2 550</td><td>3 364</td><td><b>+814 (+32 %)</b></td></tr>
<tr><td>Place moyenne</td><td>15,6</td><td>13,3</td><td>2,3 places gagnées</td></tr></table>
<h3>Clics par mois</h3>
{line_chart(mois, "clics", "Clics par mois", SAUGE, 20)}
<h3>Apparitions dans Google par mois</h3>
{line_chart(mois, "impressions", "Impressions par mois", PROF, 200)}
<div class="warn"><b>Mise en garde.</b> Ce sont de petits chiffres (une trentaine de clics par mois). Le site monte, mais on ne peut pas dire que le nouveau site en est la cause : 20 articles ont aussi été publiés, et le site gagne en ancienneté. Même fenêtre juillet → octobre : 45 clics en 2025 contre 184 en 2026, mais la base 2025 est minuscule. Le pic d'août-septembre 2026 reste inexpliqué. Aucune chute n'apparaît au moment de la bascule.</div>
</section>

<section id="adresses">
<h2>Le problème des anciennes adresses</h2>
<p>Chaque page d'un site a une adresse. En passant de WordPress au nouveau site, <b>les adresses ont changé</b>. Mais Google, et les liens déposés ailleurs, utilisent encore les anciennes. Résultat : la personne clique, et tombe sur « page introuvable ». C'est une route barrée sans panneau de déviation.</p>
{sign_svg()}
<div class="cols" style="margin-top:8px">
<div class="card bad"><h3>Les chiffres</h3><ul class="small">
<li><b>61</b> anciennes adresses retrouvées affichent une erreur 404 (sur 62 testées). Seule <i>/contact/</i> redirige.</li>
<li>Google signale <b>53 pages en erreur 404</b> dans son rapport d'indexation.</li>
<li>Sur 52 anciennes adresses vues par Google : <b>136 clics</b> et <b>4&nbsp;039&nbsp;apparitions</b> en 16 mois.</li>
<li>Exemples : /eft-saint-nazaire/ (881 apparitions), /tarifs-et-modalites-de-prise-de-rendez-vous/ (30 clics), /emdr-saint-nazaire/ (637), /cercle-de-parole-saint-nazaire/ (19 clics).</li></ul></div>
<div class="card good"><h3>La solution</h3><ul class="small">
<li>Ajouter des redirections « 301 » : <i>« cette page a déménagé ici »</i>.</li>
<li>Une liste prête de 61 correspondances : 34 sûres, 14 probables, 13 à valider par [[vous-meme]] (sujet sans équivalent exact).</li>
<li>Quelques liens dans des articles pointent aussi vers ces anciennes adresses : ils seront réparés en même temps.</li>
<li>Après correction, Google mettra quelques semaines à tout mettre à jour.</li></ul></div>
</div>
<p class="note">Autres points techniques, par ordre de priorité plus faible : titres de 28 pages sur 36 trop longs ; plusieurs titres principaux sur 8 articles ; articles concurrents sur le même sujet (EMDR, post-partum) ; peu de liens entre articles. Le reste est correct (HTTPS, plan du site, page d'erreur).</p>
</section>

<section id="concurrentes">
<h2>Face aux 4 autres praticiennes</h2>
<table>
<tr><th>Critère</th><th class="me">[[Vous]]</th><th>Morgane Houarner</th><th>Laurence Martin</th><th>M.-N. Guégan-Leblanc</th><th>Laure Sablé</th></tr>
<tr><td>Métier affiché</td><td class="me">Psychopraticienne</td><td>Psychopraticienne EMDR</td><td>Hypnothérapeute</td><td>Psychologue clinicienne</td><td>Psychothérapeute (Guérande et Saint-Nazaire)</td></tr>
<tr><td>Fiche Google</td><td class="me"><b>5,0 (20 avis)</b></td><td>4,9 (40 avis)</td><td colspan="3">non relevé</td></tr>
<tr><td>Blog</td><td class="me"><b>~20 articles</b></td><td>0</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>Séance offerte</td><td class="me"><b>Oui (45 min)</b></td><td>Non</td><td>Non</td><td>Non</td><td>Non</td></tr>
<tr><td>Prix affiché sur le site</td><td class="me">60 € (page RDV) ; 1er RDV d'1 h : tarif à afficher (à nous transmettre)</td><td>75 €</td><td>80 €</td><td>60 €</td><td>55 €</td></tr>
<tr><td>Clics pour réserver</td><td class="me">2</td><td>pas de réservation sur le site</td><td>1 (appel)</td><td>1 (Doctolib)</td><td>1 (Doctolib)</td></tr>
<tr><td>Page par méthode, FAQ</td><td class="me">Oui</td><td>Oui, sans FAQ</td><td>Non, FAQ oui</td><td>Non</td><td>Non</td></tr>
<tr><td>Citée par les IA</td><td class="me">Oui, par endroits</td><td><b>Très souvent</b></td><td>Parfois</td><td>Parfois</td><td>Jamais</td></tr>
</table>
<p class="note">Marie-Noëlle Guégan-Leblanc est psychologue (titre protégé, public plus médical) : à ne pas appeler « psychopraticienne ». Morgane Houarner paie aussi des annonces Google sur 3 recherches sur 4 relevées.</p>
<h3>Ce qu'elles font mieux (et que [[vous]] pouvez copier)</h3>
<ol class="small" style="margin:.2em 0 0 1.2em;padding:0">
<li><b>Réserver en 1 clic</b> depuis l'accueil, avec un bouton répété dans la page.</li>
<li><b>Le prix à côté du bouton</b> (Laure Sablé affiche 3 lignes de prix juste avant « prendre rendez-vous »).</li>
<li><b>Un lien « voir les avis Google »</b> bien visible (Laurence Martin). [[Vous]] avez 20 avis sur Google mais le site n'y renvoie pas.</li>
<li><b>La fiche Google comme porte de réservation</b> (Morgane Houarner).</li>
<li><b>Être dans les annuaires</b> où l'on compare les praticiennes (Doctolib, Resalib, etc.).</li>
<li><b>Une FAQ sur l'accueil</b> pour lever la peur du premier pas (« dois-je tout raconter ? »).</li>
</ol>
<p class="note">À ne pas copier : les témoignages anonymes. Sur la vitesse du site, [[vous]] faites mieux : Morgane Houarner affiche 89 sur 100 contre 96 à 100 pour [[votre]] site. Place exacte de chacune sur Google : seulement relevée pour 4 recherches.</p>
</section>

<section id="ia">
<h2>Ce que disent les intelligences artificielles</h2>
<p>De plus en plus de personnes demandent à ChatGPT, Perplexity, Gemini ou à Google (« Mode IA ») au lieu de chercher sur des sites. Nous avons posé <b>12 questions</b> à chacune, comme le ferait une patiente. Voici sur 11 questions (hors celle qui cite [[votre]] nom) combien de fois [[vous]] êtes citée.</p>
{hbars([("Google Mode IA", 4, "4 sur 11"), ("Perplexity", 3, "3 sur 11"), ("ChatGPT", 3, "3 sur 11"), ("Gemini", 1, "1 sur 11")], 11, SAUGE)}
<p class="note">Un seul essai par question (2 essais sur quelques-unes) ; les réponses des IA varient d'un essai à l'autre. Gemini a été testé depuis un autre lieu que Saint-Nazaire, ce qui peut fausser. Aucune capture d'écran conservée.</p>
<div class="cols">
<div class="card good"><h3>Où [[vous]] êtes citée</h3><ul class="small"><li>« Psychopraticienne Saint-Nazaire » et « EFT » : stable sur plusieurs essais.</li><li>Thérapie en marchant (ChatGPT, Google), soutien post-partum (Google).</li><li>Les 4 IA [[vous]] décrivent correctement dans l'ensemble quand on cite [[votre]] nom.</li></ul></div>
<div class="card bad"><h3>Le trou EMDR</h3><ul class="small"><li>Question « EMDR à Saint-Nazaire » : <b>jamais citée</b>, sur les 2 essais de ChatGPT et Perplexity.</li><li>Aucune IA ne renvoie vers [[votre]] page EMDR.</li><li>Absente aussi sur psychocorporel, visio, cancer, traumatisme.</li><li>Morgane Houarner est de très loin la plus citée.</li></ul></div>
</div>
<h3>Les sites que les IA lisent (où il faut être)</h3>
{hbars([("[[votre]] site", 14, "14 réponses"), ("Resalib", 9, "9"), ("Psychologue.net", 8, "8"), ("Doctolib", 7, "7"), ("Crénolibre", 6, "6"), ("Médoucine", 5, "5"), ("annuaire IFPEC", 4, "4")], 14, TERRA)}
<p class="note">Nombre de réponses (sur 51) qui citent chaque site. [[Votre]] fiche IFPEC existe déjà. Pour Resalib, Psychologue.net, Médoucine, Crénolibre et Doctolib : fiches à vérifier ou à créer, <span class="tag">à confirmer</span> (Resalib et Paralib apparaissent avec [[votre]] nom dans Google).</p>
<div class="warn"><b>À vérifier avec [[vous-meme]].</b> Perplexity affirme que [[vous]] recevez « à domicile » et que [[votre]] cabinet existe « depuis septembre 2025 ». Nous ne retrouvons pas cela sur le site : <span class="tag">à vérifier</span>. Une IA qui se trompe sur [[vous]] peut être corrigée en rendant l'information claire sur le site.</div>
</section>

<section id="actions">
<h2>Les 5 actions, par impact sur la réservation</h2>
<div class="act"><div class="num">1</div><div><h3>Rediriger les anciennes adresses</h3><p>Ajouter les redirections 301 (liste prête) pour récupérer les clics perdus, dont ceux des pages EFT, tarifs et cercle de parole.</p><p class="who">Nicolas : ajoute et teste. Emmanuelle : valide les 13 correspondances incertaines. Effort : faible à moyen (quelques heures).</p></div></div>
<div class="act"><div class="num">2</div><div><h3>Raccourcir le chemin vers la séance découverte</h3><p>Un bouton « Réserver ma séance découverte » qui ouvre directement le calendrier, le prix à côté, 3 questions de FAQ sur l'accueil, un lien vers la séance dans chaque article.</p><p class="who">Nicolas : le site. Emmanuelle : nous transmettre le tarif du 1er RDV d'1 h (tarif à afficher, à nous transmettre) et valider les textes. Effort : moyen.</p></div></div>
<div class="act"><div class="num">3</div><div><h3>Faire sortir la page EMDR</h3><p>Aujourd'hui c'est l'accueil, pas la page EMDR, qui apparaît. Clarifier les 3 pages qui parlent d'EMDR (une page principale, les autres y renvoient) et enrichir la page : questions fréquentes, avis.</p><p class="who">Nicolas : structure et liens. Emmanuelle : valide le contenu, choisit la page principale. Effort : moyen.</p></div></div>
<div class="act"><div class="num">4</div><div><h3>Soigner la fiche Google et les annuaires</h3><p>Mettre le lien de réservation dans la fiche Google ; demander des avis aux patientes qui le souhaitent ; compléter ou créer les fiches Resalib, Psychologue.net, Médoucine, Crénolibre (Doctolib : à décider ensemble, certains annuaires sont payants).</p><p class="who">Emmanuelle : fiches et demande d'avis. Nicolas : aide et lien suivi. Effort : faible, étalé sur quelques semaines.</p></div></div>
<div class="act"><div class="num">5</div><div><h3>Mesurer enfin ce qui marche</h3><p>Ajouter un marqueur de provenance aux liens Calendly, activer un compteur de visites simple (Netlify : à confirmer), demander « comment m&#39;avez-vous connue ? » à la réservation.</p><p class="who">Nicolas : marqueur et compteur. Emmanuelle : poser la question aux patientes. Effort : faible. Sans outil payant ni nouveau service sans accord.</p></div></div>
<p class="note">Cet ordre est une proposition. Les gains attendus ne sont pas chiffrés : les volumes sont trop petits pour une prévision sérieuse.</p>
</section>

<section id="glossaire">
<h2>Glossaire</h2>
<dl>
<dt>Impression</dt><dd>Une fois où [[votre]] site s'affiche dans les résultats de Google, que la personne clique ou non.</dd>
<dt>Clic</dt><dd>Une personne qui clique sur [[votre]] site dans les résultats Google. C'est la seule « visite » que nous mesurons.</dd>
<dt>Redirection (301)</dt><dd>Un panneau de déviation : « cette page a déménagé, voici la nouvelle ». Visiteurs et Google sont envoyés au bon endroit.</dd>
<dt>Erreur 404</dt><dd>Le message « page introuvable » : l'adresse n'existe plus.</dd>
<dt>Pack local</dt><dd>Les 3 fiches avec carte qui s'affichent en haut de Google pour une recherche près de chez soi (Google Maps).</dd>
<dt>GEO (recherche par IA)</dt><dd>Être citée quand quelqu'un pose sa question à ChatGPT, Perplexity, Gemini ou au Mode IA de Google plutôt que de taper des mots-clés.</dd>
</dl>
</section>

<section id="sources">
<h2>Sources</h2>
<p class="note">Chaque chiffre vient de ces fichiers du dossier d'audit (fichiers bruts non joints au rapport). Ce qui n'a pas pu être vérifié est écrit « à confirmer ».</p>
<ul class="small">
<li><b>audit/PLAN-AUDIT.md</b> : périodes, questions, règles, constats initiaux (Semrush, Calendly).</li>
<li><b>audit/analyses/01-gsc.md</b>, <b>gsc-par-mois.csv</b>, <b>gsc-vs-calendly-par-mois.csv</b> : clics, impressions, pages, mots tapés, avant/après, Calendly (exports Google Search Console, 16 mois, et comptes Calendly anonymes).</li>
<li><b>audit/analyses/02-technique.md</b>, <b>redirections-proposees.csv</b>, <b>anciennes-url-gsc.txt</b> : anciennes adresses, redirections, points techniques.</li>
<li><b>audit/analyses/03-concurrents.md</b> : comparaison des 4 praticiennes (lecture de leurs sites publics).</li>
<li><b>audit/analyses/04-blog.md</b>, <b>blog-stats.csv</b> : état des 20 articles (lecture seule).</li>
<li><b>audit/data/serp/serp.md</b> : relevé Google et Maps du 1er nov. 2026.</li>
<li><b>audit/data/pagespeed/pagespeed.md</b> : vitesse du site (PageSpeed Insights).</li>
<li><b>audit/data/geo/geo.md</b> : tests des IA du 1er nov. 2026.</li>
</ul>
<h3>Reste à confirmer</h3>
<ul class="small">
<li>Aucun outil de visites activé : à confirmer (Netlify).</li>
<li>Date exacte de bascule du site (8 juin 2026) : à confirmer (historique Netlify).</li>
<li>Pages et mots tapés avant / après : exports Google par période à recevoir.</li>
<li>Données Semrush détaillées et fiche Google (performances, propriétaire) : à confirmer.</li>
<li>Tarif du 1er RDV d'1 h : à nous transmettre.</li>
<li>« À domicile » et « cabinet depuis sept. 2025 » (affirmés par Perplexity) : à vérifier avec Emmanuelle.</li>
<li>Pas de capture d'écran conservée pour les tests IA ; place Google variable selon le lieu.</li>
<li>Effet de la panne du site du 28 octobre : non mesuré (hors des périodes comparées).</li>
</ul>
</section>
'''
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

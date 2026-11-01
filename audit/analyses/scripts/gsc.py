import csv, re, os, sys, datetime as dt, collections, urllib.parse
R='audit/data/gsc/16-mois/'; O='audit/analyses/'
def pct(s): return float(s.strip('%'))/100 if s else 0
rows=[]
for r in csv.DictReader(open(R+'Graphique.csv',encoding='utf-8')):
    d=dt.date.fromisoformat(r['Date']); c=int(r['Clics']); i=int(r['Impressions'])
    p=float(r['Position']) if r['Position'] else None
    rows.append((d,c,i,p))
def agg(f):
    c=i=0; pw=0
    for d,cc,ii,p in rows:
        if f(d):
            c+=cc;i+=ii
            if p is not None: pw+=p*ii
    return c,i,(c/i if i else 0),(pw/i if i else 0)
def D(s): return dt.date.fromisoformat(s)
def show(n,f):
    c,i,ctr,p=agg(f); print(f"{n}: clics={c} impr={i} ctr={ctr:.2%} pos={p:.2f}")
show('AVANT',lambda d:D('2026-01-17')<=d<=D('2026-06-07'))
show('APRES',lambda d:D('2026-06-08')<=d<=D('2026-10-27'))
show('2025 1/7-27/10',lambda d:D('2025-07-01')<=d<=D('2025-10-27'))
show('2026 1/7-27/10',lambda d:D('2026-07-01')<=d<=D('2026-10-27'))
show('2025-07-01..2026-01-16 (avant AVANT)',lambda d:d<D('2026-01-17'))
show('TOTAL',lambda d:True)
print('first/last',rows[0][0],rows[-1][0],len(rows))
# mois
m=collections.OrderedDict()
for d,c,i,p in rows:
    k=d.strftime('%Y-%m'); x=m.setdefault(k,[0,0,0.0,0]); x[0]+=c;x[1]+=i;x[3]+=1
    if p is not None:x[2]+=p*i
with open(O+'gsc-par-mois.csv','w',newline='') as f:
    w=csv.writer(f);w.writerow(['mois','jours','clics','impressions','ctr','position_ponderee'])
    for k,(c,i,pw,n) in m.items(): w.writerow([k,n,c,i,f"{c/i:.4f}" if i else '',f"{pw/i:.2f}" if i else ''])
wk=collections.OrderedDict()
for d,c,i,p in rows:
    s=d-dt.timedelta(days=d.weekday()); x=wk.setdefault(s,[0,0,0.0,0]); x[0]+=c;x[1]+=i;x[3]+=1
    if p is not None:x[2]+=p*i
with open(O+'gsc-par-semaine.csv','w',newline='') as f:
    w=csv.writer(f);w.writerow(['lundi_semaine','jours','clics','impressions','ctr','position_ponderee'])
    for k,(c,i,pw,n) in wk.items(): w.writerow([k,n,c,i,f"{c/i:.4f}" if i else '',f"{pw/i:.2f}" if i else ''])
print('semaines 0 impr:',[str(k) for k,v in wk.items() if v[1]==0])
print('semaines 0 clic (avec impr):',[str(k) for k,v in wk.items() if v[0]==0 and v[1]>0][:60], sum(1 for v in wk.values() if v[0]==0 and v[1]>0))
for k,v in wk.items():
    if D('2026-05-18')<=k<=D('2026-06-29'): print(k,v)
print('jours 0 impr:',sum(1 for r in rows if r[2]==0), [str(r[0]) for r in rows if r[2]==0][:5], [str(r[0]) for r in rows if r[2]==0][-3:])
# AVANT/APRES par semaines moyenne
for n,a,b in [('AVANT','2026-01-17','2026-06-07'),('APRES','2026-06-08','2026-10-27')]:
    ws=[v for k,v in wk.items() if D(a)<=k and k+dt.timedelta(days=6)<=D(b)]
    print(n,'semaines pleines',len(ws),'clics moy/sem',sum(v[0] for v in ws)/len(ws),'0 clic',sum(1 for v in ws if v[0]==0))
print('mois'); 
for k,v in m.items(): print(k,v[3],v[0],v[1],round(v[2]/v[1],1) if v[1] else '')
# pages
P=list(csv.DictReader(open(R+'Pages.csv',encoding='utf-8')))
Q=list(csv.DictReader(open(R+'Requêtes.csv',encoding='utf-8')))
print('pages',len(P),sum(int(r['Clics']) for r in P),sum(int(r['Impressions']) for r in P))
print('requetes',len(Q),sum(int(r['Clics']) for r in Q),sum(int(r['Impressions']) for r in Q))
fam={'emdr':r'emdr','eft':r'\beft\b|emotional freedom','psychopraticien':r'psychopraticien','saint nazaire':r'saint[ -]?nazaire|st nazaire','demeulemeester':r'demeul|demeules|demeulester|emmanuel'}
for n,rx in fam.items():
    s=[r for r in Q if re.search(rx,r['Requêtes les plus fréquentes'],re.I)]
    c=sum(int(r['Clics']) for r in s);i=sum(int(r['Impressions']) for r in s)
    pw=sum(float(r['Position'])*int(r['Impressions']) for r in s)/i if i else 0
    print(f"FAMILLE {n}: {len(s)} requetes clics={c} impr={i} pos={pw:.1f}")
    for r in sorted(s,key=lambda r:-int(r['Impressions']))[:4]: print('   ',r['Requêtes les plus fréquentes'],r['Clics'],r['Impressions'],r['Position'])
# blog
bl={}
for fn in os.listdir('src/content/blog'):
    t=open('src/content/blog/'+fn,encoding='utf-8').read()
    m2=re.search(r'^slug:\s*(.+)$',t,re.M); sl=m2.group(1).strip().strip('"\'') if m2 else None
    bl[fn[:-3]]=sl
def norm(u):
    u=urllib.parse.unquote(urllib.parse.urlparse(u).path).strip('/'); return u
art=collections.defaultdict(lambda:[0,0,[]])
unmatched=[]
fn_by_slug={v:k for k,v in bl.items() if v}
for r in P:
    u=norm(r['Pages les plus populaires'])
    if u.startswith('blog/') and u!='blog':
        s=u[5:]
        key=fn_by_slug.get(s) or (s if s in bl else None)
        if key is None: unmatched.append(u); continue
        a=art[key];a[0]+=int(r['Clics']);a[1]+=int(r['Impressions']);a[2].append(u)
print('BLOG non reconnus',unmatched)
print('TOP articles')
for k,a in sorted(art.items(),key=lambda x:(-x[1][0],-x[1][1]))[:8]: print(k,bl[k],a[0],a[1],len(a[2]))
print('JAMAIS VUS')
for k in bl:
    if k not in art: print(k,bl[k])
# old urls
routes={'','blog','404','a-propos-emmanuelle','charte-deontologique','espace-soutien-post-partum','mentions-legales','merci','prendre-rendez-vous-saint-nazaire','seance-decouverte-therapie-psychocorporelle-saint-nazaire','seance-eft-gestion-emotions','therapie-cabinet-saint-nazaire','therapie-emdr-saint-nazaire','therapie-en-ligne-visio','therapie-en-marchant-saint-nazaire','politique-de-confidentialite'}
old=[]
for r in P:
    raw=r['Pages les plus populaires']; u=norm(raw)
    if u.startswith('blog/') : 
        s=u[5:]
        if (fn_by_slug.get(s) or s in bl): continue
        old.append((raw,r,'blog/ avec slug inconnu (ancien format ou slug supprimé)')); continue
    if u in routes and '?' not in raw: continue
    why='page WordPress sans /blog/ (absente de src/pages)'
    if '?' in raw: why='paramètre dans l URL ('+raw.split('?')[1][:30]+')'
    elif 'elementor' in u: why='page Elementor (WordPress)'
    elif u.startswith('author/') or u.startswith('page/'): why='archive WordPress (auteur/pagination)'
    elif 'duplicate' in u or u.endswith('-2') or u.endswith('-3'): why='doublon WordPress'
    old.append((raw,r,why))
with open(O+'anciennes-url-gsc.txt','w',encoding='utf-8') as f:
    f.write("URL de Pages.csv (16 mois) qui ne correspondent à aucune page actuelle de src/pages ni à un article actuel de src/content/blog.\nColonnes : clics | impressions | position | URL | raison. Source : audit/data/gsc/16-mois/Pages.csv\n\n")
    for raw,r,why in old: f.write(f"{r['Clics']} | {r['Impressions']} | {r['Position']} | {raw} | {why}\n")
    f.write(f"\nTotal : {len(old)} URL, {sum(int(x[1]['Clics']) for x in old)} clics, {sum(int(x[1]['Impressions']) for x in old)} impressions\n")
print('anciennes',len(old),sum(int(x[1]['Clics']) for x in old),sum(int(x[1]['Impressions']) for x in old))
# calendly croisement
cal=collections.Counter()
for r in csv.DictReader(open('audit/data/calendly/rdv-par-mois-anonyme.csv',encoding='utf-8')):
    if r['statut']=='active' and re.match(r'(1er rendez-vous|Séance découverte)',r['type_evenement']): cal[r['mois_seance']]+=int(r['nb'])
print('calendly premiers contacts',dict(sorted(cal.items())))
with open(O+'gsc-vs-calendly-par-mois.csv','w',newline='') as f:
    w=csv.writer(f);w.writerow(['mois','clics_gsc','impressions_gsc','premiers_contacts_calendly'])
    for k,v in m.items(): w.writerow([k,v[0],v[1],cal.get(k,0)])

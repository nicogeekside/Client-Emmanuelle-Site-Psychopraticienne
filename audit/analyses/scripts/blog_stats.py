#!/usr/bin/env python3
"""Statistiques des articles de blog (lecture seule).

Produit audit/analyses/blog-stats.csv (une ligne par article) et affiche
sur stdout les paires de titres proches (pour l'analyse des doublons).
Bibliothèque standard uniquement. Ne modifie rien dans src/.
"""
import csv
import difflib
import os
import re
import unicodedata
from urllib.parse import urlparse

ROOT = "/Users/nicolasshahata/Desktop/Site Psychopraticienne"
BLOG_DIR = os.path.join(ROOT, "src", "content", "blog")
PAGES_DIR = os.path.join(ROOT, "src", "pages")
PUBLIC_DIR = os.path.join(ROOT, "public")
OUT_CSV = os.path.join(ROOT, "audit", "analyses", "blog-stats.csv")

# Dossiers de src/pages qui ne sont pas des pages de destination.
NON_PAGES = {"blog", "admin", "404.astro", "merci", "mentions-legales",
             "politique-de-confidentialite", "charte-deontologique"}
# Pages de séance / prise de RDV : dossiers commençant par ces préfixes.
SEANCE_PREFIXES = ("seance-", "therapie-", "prendre-rendez-vous")
EMMA_HOST = "emma-psychopraticienne.fr"


def page_dirs():
    dirs = set()
    for name in os.listdir(PAGES_DIR):
        if name in NON_PAGES or name.startswith("."):
            continue
        if os.path.isdir(os.path.join(PAGES_DIR, name)):
            dirs.add(name)
    return dirs


def parse_frontmatter(text):
    """Parse le frontmatter YAML simple (clé: valeur, valeurs entre guillemets,
    lignes indentées = suite de la valeur)."""
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return {}, text
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return {}, text
    data = {}
    key = None
    for raw in lines[1:end]:
        if not raw.strip():
            continue
        m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", raw)
        if m and not raw.startswith((" ", "\t")):
            key = m.group(1)
            data[key] = m.group(2).strip()
        elif key is not None:
            data[key] = (data[key] + " " + raw.strip()).strip()
    for k, v in list(data.items()):
        data[k] = unquote(v)
    body = "\n".join(lines[end + 1:])
    return data, body


def unquote(v):
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        inner = v[1:-1]
        if v[0] == '"':
            inner = inner.replace('\\"', '"')
        else:
            inner = inner.replace("''", "'")
        return inner
    return v


def strip_accents(s):
    return "".join(c for c in unicodedata.normalize("NFD", s)
                   if unicodedata.category(c) != "Mn")


def count_words(body):
    t = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", body)          # images
    t = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", t)           # liens -> texte
    t = re.sub(r"<[^>]+>", " ", t)                           # balises HTML
    t = re.sub(r"https?://\S+", " ", t)                      # URL nues
    t = re.sub(r"[#*_>`~|-]+", " ", t)                       # marqueurs md
    tokens = [w for w in t.split() if re.search(r"[\w]", w)]
    return len(tokens)


def collect_hrefs(body):
    """Liens markdown, attributs href, puis URL nues restantes (sans double comptage)."""
    hrefs = []
    md = r"(?<!!)\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)"
    hrefs += re.findall(md, body)
    rest = re.sub(md, " ", body)
    hrefs += re.findall(r"href=[\"']([^\"']+)[\"']", rest)
    rest = re.sub(r"href=[\"'][^\"']+[\"']", " ", rest)
    hrefs += re.findall(r"https?://[^\s)\"'<>\]]+", rest)
    return hrefs


def classify(hrefs, seance_dirs_all):
    internes, pages, calendly = 0, set(), False
    for h in hrefs:
        if "calendly.com" in h:
            calendly = True
        if h.startswith("//") or h.startswith("mailto:") or h.startswith("tel:"):
            continue
        if h.startswith("http://") or h.startswith("https://"):
            p = urlparse(h)
            if not p.netloc.endswith(EMMA_HOST):
                continue
            path = p.path
        elif h.startswith("/"):
            path = urlparse(h).path
        else:
            continue
        internes += 1
        first = path.strip("/").split("/")[0]
        if first and first in seance_dirs_all:
            pages.add(first)
    return internes, pages, calendly


def slug_problems(slug):
    probs = []
    if any(ord(c) > 127 for c in slug):
        probs.append("accents")
    if "'" in slug or "’" in slug:
        probs.append("apostrophe")
    if re.search(r"(19|20)\d{2}", slug):
        probs.append("date")
    if len(slug) > 60:
        probs.append("longueur>60")
    return probs


def main():
    pages = page_dirs()
    seance_dirs = {d for d in pages if d.startswith(SEANCE_PREFIXES)}
    print("Dossiers de pages recensés :", ", ".join(sorted(pages)))
    print("Pages de séance / RDV :", ", ".join(sorted(seance_dirs)))

    rows = []
    for fname in sorted(os.listdir(BLOG_DIR)):
        if not fname.endswith(".md"):
            continue
        with open(os.path.join(BLOG_DIR, fname), encoding="utf-8") as f:
            text = f.read()
        fm, body = parse_frontmatter(text)
        slug_fm = fm.get("slug", "").strip()
        slug = slug_fm or os.path.splitext(fname)[0]
        title = fm.get("title", "")
        desc = fm.get("description", "")
        pub = fm.get("pubDate", "")[:10]
        image = fm.get("image", "").strip()

        lines = body.split("\n")
        h2 = sum(1 for l in lines if re.match(r"^##\s", l))
        h3 = sum(1 for l in lines if re.match(r"^###\s", l))
        h1 = sum(1 for l in lines if re.match(r"^#\s", l))
        internes, page_hits, calendly = classify(collect_hrefs(body), seance_dirs)
        if image:
            img_exists = os.path.exists(os.path.join(PUBLIC_DIR, image.lstrip("/")))
        else:
            img_exists = False

        probs = slug_problems(slug)
        if not slug_fm:
            probs.append("slug_absent_nom_fichier")

        rows.append({
            "fichier": fname,
            "slug": slug,
            "title": title,
            "longueur_title": len(title),
            "description": desc,
            "longueur_description": len(desc),
            "date": pub,
            "mots_corps": count_words(body),
            "nb_h2": h2,
            "nb_h3": h3,
            "nb_h1_corps": h1,
            "liens_internes": internes,
            "liens_pages_seance": "|".join(sorted(page_hits)),
            "nb_liens_pages_seance": len(page_hits),
            "lien_calendly": "oui" if calendly else "non",
            "mention_saint_nazaire": "oui" if re.search(r"saint[- ]nazaire", body, re.I) else "non",
            "image_couverture": "oui" if image else "non",
            "image_fichier_present": "oui" if img_exists else "non",
            "slug_problemes": ";".join(probs),
        })

    fields = list(rows[0].keys())
    with open(OUT_CSV, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    print("Articles :", len(rows), "->", OUT_CSV)

    # Paires de titres proches (doublons possibles)
    print("\nPaires de titres proches (ratio >= 0.30 ou mot-clé commun fort):")
    norm = [(r["fichier"], r["title"], strip_accents(r["title"].lower())) for r in rows]
    for i in range(len(norm)):
        for j in range(i + 1, len(norm)):
            ratio = difflib.SequenceMatcher(None, norm[i][2], norm[j][2]).ratio()
            wi = set(re.findall(r"[a-z]{4,}", norm[i][2])) - {"saint", "nazaire", "dans", "avec", "pour", "dune", "quoi", "comment", "entre", "chez"}
            wj = set(re.findall(r"[a-z]{4,}", norm[j][2])) - {"saint", "nazaire", "dans", "avec", "pour", "dune", "quoi", "comment", "entre", "chez"}
            common = wi & wj
            if ratio >= 0.30 or len(common) >= 2:
                print(f"{ratio:.2f} | {norm[i][1]} || {norm[j][1]} | communs: {', '.join(sorted(common))}")


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""Layer 1: resolve every DOI against CrossRef and compare title/year."""
import json, io, re, time, urllib.request, urllib.parse, difflib, sys

MAILTO = "bisu9082@gmail.com"

def clean(s):
    s = re.sub(r"\\[&%_#]", lambda m: m.group(0)[1], s or "")
    s = re.sub(r"[{}]", "", s)
    s = re.sub(r"\\\w+\s*", "", s)
    return " ".join(s.split())

def norm(s):
    return re.sub(r"[^a-z0-9 ]", " ", (s or "").lower()).split()

def fetch(doi):
    url = "https://api.crossref.org/works/" + urllib.parse.quote(doi, safe="")
    req = urllib.request.Request(url, headers={"User-Agent": f"citation-audit/1.0 (mailto:{MAILTO})"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)["message"]

es = json.load(io.open("verify/entries.json", encoding="utf-8"))
todo = [e for e in es if e["class"] == "doi"]
out = []
for i, e in enumerate(todo, 1):
    doi = clean(e["doi"])
    rec = {"key": e["key"], "doi": doi, "bib_title": clean(e.get("title","")),
           "bib_year": clean(e.get("year",""))}
    try:
        m = fetch(doi)
        ct = " ".join(m.get("title") or [])
        cy = ""
        for k in ("published-print","published-online","issued","created"):
            if m.get(k, {}).get("date-parts"):
                cy = str(m[k]["date-parts"][0][0]); break
        sim = difflib.SequenceMatcher(None, " ".join(norm(rec["bib_title"])),
                                      " ".join(norm(ct))).ratio()
        rec.update(status="RESOLVED", cr_title=ct, cr_year=cy,
                   cr_container=" ".join(m.get("container-title") or []),
                   title_sim=round(sim,3),
                   year_match=(rec["bib_year"] == cy) if cy else None)
    except Exception as ex:
        rec.update(status="FAIL", error=str(ex)[:90])
    out.append(rec)
    print(f"[{i:2d}/{len(todo)}] {rec['status']:8s} sim={rec.get('title_sim','--')} {e['key']}")
    time.sleep(0.35)
json.dump(out, io.open("verify/crossref_results.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
ok = [r for r in out if r["status"]=="RESOLVED"]
print(f"\nresolved {len(ok)}/{len(out)}")
print("title sim <0.75:", [r['key'] for r in ok if r['title_sim']<0.75])
print("year mismatch  :", [(r['key'],r['bib_year'],r['cr_year']) for r in ok if r['year_match'] is False])

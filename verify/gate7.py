# -*- coding: utf-8 -*-
"""GATE 7 — 인용 무결성. 본 원고(main_v9)에서 실제 인용된 엔트리만 대상."""
import re,json,sys,urllib.request,urllib.parse,time
s=open('tex/main_v10.tex',encoding='utf-8').read()
cited=set()
for g in re.findall(r'\\cite[a-z]*\{([^}]*)\}',s):
    cited |= {x.strip() for x in g.split(',')}
bib=open('tex/myref_v3.bib',encoding='utf-8').read()
ent={m.group(2).strip():m.group(3) for m in re.finditer(r'@(\w+)\{([^,]+),(.*?)\n\}',bib,re.S)}
rows=[]
for k in sorted(cited):
    if k not in ent: rows.append((k,'MISSING_ENTRY','')); continue
    b=ent[k]
    doi=re.search(r'doi\s*=\s*\{([^}]*)\}',b)
    url=re.search(r'url\s*=\s*\{([^}]*)\}',b)
    note=re.search(r'note\s*=\s*\{([^}]*)\}',b,re.S)
    if doi:
        d=doi.group(1).replace('\\&','&')
        try:
            req=urllib.request.Request('https://api.crossref.org/works/'+urllib.parse.quote(d,safe='')+'?mailto=bisu9082@gmail.com',
                                       headers={'User-Agent':'refcheck/1.0 (mailto:bisu9082@gmail.com)'})
            json.load(urllib.request.urlopen(req,timeout=25))
            rows.append((k,'DOI_CROSSREF_OK',d))
        except Exception:
            rows.append((k,'DOI_NOT_IN_CROSSREF',d))
        time.sleep(0.35)
    elif url: rows.append((k,'OFFICIAL_URL',url.group(1)[:70]))
    else:
        ok = bool(note) or re.search(r'(organization|howpublished|journal)\s*=',b)
        rows.append((k,'DESIGNATION_ONLY' if ok else 'NO_IDENTIFIER',''))
import collections
c=collections.Counter(r[1] for r in rows)
print(f"인용 엔트리 {len(cited)}")
for k,v in c.most_common(): print(f"  {k:22s}{v:>3}")
bad=[r for r in rows if r[1] in ('MISSING_ENTRY','NO_IDENTIFIER')]
print(f"\n허구·미식별 인용: {len(bad)}건")
for r in bad: print('  ✘',r)
odd=[r for r in rows if r[1]=='DOI_NOT_IN_CROSSREF']
print(f"\nCrossRef 미등재 DOI(별도 확인 필요): {len(odd)}건")
for r in odd: print('  ⚠',r[0],r[2])
score = 1.0 - (len(bad)/max(1,len(cited)))
print(f"\n무결성 점수 {score:.3f}  (GATE 7 기준 ≥ 0.8) · hallucinated {len(bad)}")
json.dump(rows,open('verify/gate7_v9.json','w'),ensure_ascii=False,indent=1)

# -*- coding: utf-8 -*-
"""엣지 v3 = v2 + 장/절 구조 + 무번호 구조참조(this Chapter/Section/Regulation)."""
import re, json, importlib.util, sys
sys.path.insert(0,'graph')
import chapters
E=[tuple(e) for e in json.load(open('graph/edges2.json',encoding='utf-8'))]
N=json.load(open('graph/nodes2.json',encoding='utf-8'))
cn, ce = chapters.build()
N.update(cn)
E += [e for e in ce if e[1] in N]
# 무번호 구조참조: 항 노드 → 소속 장/절 허브
art2cpt={}
for a,b,k in ce:
    if k=='cpt_contain': art2cpt.setdefault(b,set()).add(a)
add=[]
for nid,txt in N.items():
    doc,unit=nid.split('::',1)
    # 2026-09-20 정정: MID·LED가 누락되어 있었고 'this Directive'가 패턴에 없었다.
    #   MID 제7조제2항 "only if they satisfy the requirements of this Directive"가
    #   구조참조를 얻지 못해 평가에 도달하지 못했다.
    if doc not in ('EU945','EU947','EU1139','EUAI','MID','LED') or '.' not in unit: continue
    hub=nid.rsplit('.',1)[0]
    if re.search(r'\bthis (Chapter|Section)\b',txt):
        for c in art2cpt.get(hub,()): add.append((nid,c,'struct_ref'))
    if re.search(r'\bthis (?:Regulation|Directive)\b',txt):
        for c in [k for k in N if k.startswith(doc+'::cpt_') and '.' not in k.split('::')[1]]:
            add.append((nid,c,'struct_ref'))
E=sorted(set(E)|set(add))
json.dump(E,open('graph/edges3.json','w',encoding='utf-8'),ensure_ascii=False)
json.dump(N,open('graph/nodes3.json','w',encoding='utf-8'),ensure_ascii=False)
from collections import Counter
c=Counter(k for _,_,k in E)
print(f"노드 {len(N)} (장/절 {len(cn)} 추가)")
for k,n in c.most_common(): print(f"  {k:14s} {n:>6}")
print(f"  {'TOTAL':14s} {len(E):>6}")

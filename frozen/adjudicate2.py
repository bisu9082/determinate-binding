# -*- coding: utf-8 -*-
"""판정 v2 — 패싯 연언 등록부(facets_mg/facets_ma) + F-5 단일 인가조항 정의.
v1(공표본) 결과와 나란히 보고한다. 명세: stpa/facetspec.md"""
import re,json,sys
from collections import Counter,defaultdict
sys.path.insert(0,'stpa'); sys.path.insert(0,'probe')
from carveout import N,ap_nodes,build,tier_of
from uca_mg import UCA as UG
from uca_ma import UCA as UA
from scenarios import SCEN
from accountability import ELEMENTS, FUNC as FAC
from facets_mg import FACETS as FG
from facets_ma import FACETS as FA
from facetmatch import match
from scope import admissible
apset,_=ap_nodes(); acset=set(N); AC,AP=build(acset),build(apset)

def judge_f(sc,facets,allowed,ADJ):
    hit=[k for k in sorted(allowed) if admissible(sc,k) and match(facets,k,N,ADJ,allowed)]
    tiers={k:tier_of(k,ADJ,allowed) for k in hit}
    auth=[k for k,t in tiers.items() if t is not None]
    t2=[k for k in auth if tiers[k]==2]; t1=[k for k in auth if tiers[k]==1]
    c='개념 부재' if not hit else ('인가조항 아님' if not auth else ('영점' if not t2 else '확정 결속'))
    return dict(hits=len(hit),auth=len(auth),t2=len(t2),t1=len(t1),cls=c,ex=sorted(t2)[:3])

def judge_p(sc,pats,allowed,ADJ):      # 책무성 7요소는 v1 패턴 유지(단일 개념 목록)
    R=re.compile("|".join(pats),re.I)
    hit=[k for k in sorted(allowed) if admissible(sc,k) and R.search(N[k])]
    tiers={k:tier_of(k,ADJ,allowed) for k in hit}
    auth=[k for k,t in tiers.items() if t is not None]
    t2=[k for k in auth if tiers[k]==2]; t1=[k for k in auth if tiers[k]==1]
    c='개념 부재' if not hit else ('인가조항 아님' if not auth else ('영점' if not t2 else '확정 결속'))
    return dict(hits=len(hit),auth=len(auth),t2=len(t2),t1=len(t1),cls=c,ex=sorted(t2)[:3])

OUT={'M-G':[],'M-A':[],'CC':[],'AC':[]}
for u in UG:
    sc=u[5].split(':')[0]
    if sc in FG: OUT['M-G'].append(dict(sc=sc,text=u[5].split(':',1)[1].strip(),**judge_f(sc,FG[sc],acset,AC)))
for u in UA:
    sc=u[5].split(':')[0]
    if sc not in FA: continue
    a=judge_f(sc,FA[sc],acset,AC); b=judge_f(sc,FA[sc],apset,AP)
    if a['hits']==0 and b['hits']==0: d='양쪽 개념 부재'
    elif a['hits']>0 and b['hits']==0: d='규범 소멸'
    elif a['auth']>0 and b['auth']==0: d='결속 상실'
    elif a['t2']>b['t2']: d='결속 강등'
    elif b['t2']>a['t2']: d='역전'
    else: d='불변'
    OUT['M-A'].append(dict(sc=sc,text=u[5].split(':',1)[1].strip(),AC=a,AP=b,delta=d))
for e in ELEMENTS:
    OUT['AC'].append(dict(sc=e[0],name=e[1],**judge_p(e[0],FAC[e[0]],acset,AC)))
for s in SCEN:
    OUT['CC'].append(dict(sc=s[4].split(':')[0],text=s[4].split(':',1)[1].strip(),maps=s[5],judged=False))
json.dump(OUT,open('frozen/ADJUDICATION_v2.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)

v1=json.load(open('frozen/ADJUDICATION.json',encoding='utf-8'))
g1={r['sc']:r for r in v1['M-G']}
print("=== M-G 30건 · v1(공표) → v2(패싯 연언) ===")
print(f"{'제약':10s}{'v1매칭':>7s}{'v2매칭':>7s}  {'v1판정':10s}→ {'v2판정'}")
print('-'*66)
for r in OUT['M-G']:
    a=g1[r['sc']]
    mark='  ←' if a['cls']!=r['cls'] else ''
    print(f"{r['sc']:10s}{a['hits']:>7}{r['hits']:>7}  {a['cls']:10s}→ {r['cls']}{mark}")
print('-'*66)
c1=Counter(r['cls'] for r in v1['M-G']); c2=Counter(r['cls'] for r in OUT['M-G'])
for k in ('확정 결속','영점','인가조항 아님','개념 부재'):
    print(f"  {k:12s} v1 {c1[k]:>3}  →  v2 {c2[k]:>3}")
print(f"\n미결속 v1 {30-c1['확정 결속']}/30 → v2 {30-c2['확정 결속']}/30")
h=[r for r in OUT['M-G'] if r['sc']=='SC-09-1'][0]
print(f"헤드라인 SC-09-1: 매칭 {h['hits']} · 인가항 {h['auth']} · T2 {h['t2']} · {h['cls']}")
print(f"확정 결속: {[(r['sc'],r['ex'][0] if r['ex'] else '') for r in OUT['M-G'] if r['cls']=='확정 결속']}")
print("\n=== M-A 14건 ===")
d1=Counter(r['delta'] for r in v1['M-A']); d2=Counter(r['delta'] for r in OUT['M-A'])
for k in set(d1)|set(d2): print(f"  {k:12s} v1 {d1[k]:>3}  →  v2 {d2[k]:>3}")
print(f"  AC 확정결속 v1 {sum(1 for x in v1['M-A'] if x['AC']['t2']>0)} → v2 {sum(1 for x in OUT['M-A'] if x['AC']['t2']>0)}")
print(f"  AP 확정결속 v1 {sum(1 for x in v1['M-A'] if x['AP']['t2']>0)} → v2 {sum(1 for x in OUT['M-A'] if x['AP']['t2']>0)}")
print("\n=== 책무성 7요소 (F-5 적용 후) ===")
a1={r['sc']:r for r in v1['AC']}
for r in OUT['AC']:
    o=a1[r['sc']]
    print(f"  {r['sc']} {r['name']:12s} 인가항 {o['auth']:>2}→{r['auth']:>2} · T2 {o['t2']}→{r['t2']} · {o['cls']} → {r['cls']}")

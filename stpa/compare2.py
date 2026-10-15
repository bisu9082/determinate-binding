# -*- coding: utf-8 -*-
import re,json,sys
sys.path.insert(0,'stpa'); sys.path.insert(0,'probe')
from carveout import N,ap_nodes,build,tier_of
from uca_ma import UCA
from compare import FUNC
apset,_=ap_nodes(); acset=set(N); AC,AP=build(acset),build(apset)
def ev(sc,allowed,ADJ):
    R=re.compile("|".join(FUNC[sc]),re.I)
    hits=[k for k in allowed if R.search(N[k])]
    tiers=[t for t in (tier_of(k,ADJ,allowed) for k in hits) if t is not None]
    return len(hits),(max(tiers) if tiers else None)
def cls(na,ta,np_,tp):
    if na==0 and np_==0: return '양쪽 개념 부재'
    if na>0 and np_==0:  return '규범 소멸'
    if ta is not None and tp is None:  return '결속 상실'
    if ta is not None and tp is not None:
        if tp<ta: return '결속 강등'
        if tp>ta: return '역전'
    return '불변'
rows=[]
for u in UCA:
    sc=u[5].split(':')[0]
    na,ta=ev(sc,acset,AC); np_,tp=ev(sc,apset,AP)
    rows.append((sc,na,ta,np_,tp,cls(na,ta,np_,tp),u[5].split(':',1)[1].strip()))
from collections import Counter
C=Counter(r[5] for r in rows)
print(f"{'안전제약':11s}{'AC매칭':>6s}{'AC':>4s}{'AP매칭':>7s}{'AP':>4s}   판정")
print('-'*66)
f=lambda x:'—' if x is None else str(x)
for r in rows: print(f"{r[0]:11s}{r[1]:>6}{f(r[2]):>4}{r[3]:>7}{f(r[4]):>4}   {r[5]}")
print('-'*66)
for k in ['규범 소멸','결속 상실','결속 강등','불변','양쪽 개념 부재','역전']:
    if C[k]: print(f"  {k:14s}{C[k]:>3}건")
loss=C['규범 소멸']+C['결속 상실']+C['결속 강등']
print(f"\n★ 경찰경로에서 잃는 제약 {loss}/14 · 역전 {C['역전']}건")
print("\n=== 사라지는 것 ===")
for r in rows:
    if r[5] in ('규범 소멸','결속 상실'): print(f"  {r[0]}  {r[6][:92]}")
print("\n=== 남는 것 ===")
for r in rows:
    if r[5]=='불변': print(f"  {r[0]}  {r[6][:92]}")
json.dump([dict(sc=r[0],ac_hits=r[1],ac_tier=r[2],ap_hits=r[3],ap_tier=r[4],cls=r[5]) for r in rows],
          open('stpa/compare_ma.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)

# -*- coding: utf-8 -*-
"""동결 규칙으로 63개 제약 전체 재판정. 출력이 논문 Results의 원자료가 된다."""
import re,json,sys
from collections import Counter,defaultdict
sys.path.insert(0,'stpa'); sys.path.insert(0,'probe')
from carveout import N,ap_nodes,build,tier_of
from uca_mg import UCA as UG
from uca_ma import UCA as UA
from scenarios import SCEN
from accountability import ELEMENTS, FUNC as FAC
from match_mg import FUNC as FG
from compare import FUNC as FA
from scope import admissible
apset,_=ap_nodes(); acset=set(N); AC,AP=build(acset),build(apset)
def judge(sc,pats,allowed,ADJ):
    R=re.compile("|".join(pats),re.I)
    hit=[k for k in sorted(allowed) if admissible(sc,k) and R.search(N[k])]
    tiers={k:tier_of(k,ADJ,allowed) for k in hit}
    auth=[k for k,t in tiers.items() if t is not None]
    t2=[k for k in auth if tiers[k]==2]; t1=[k for k in auth if tiers[k]==1]
    if not hit: c='개념 부재'
    elif not auth: c='인가조항 아님'
    elif not t2: c='영점'
    else: c='확정 결속'
    return dict(hits=len(hit),auth=len(auth),t2=len(t2),t1=len(t1),cls=c,ex=sorted(t2)[:3])
OUT={'M-G':[],'M-A':[],'CC':[],'AC':[]}
for u in UG:
    sc=u[5].split(':')[0]
    if sc in FG: OUT['M-G'].append(dict(sc=sc,text=u[5].split(':',1)[1].strip(),**judge(sc,FG[sc],acset,AC)))
for u in UA:
    sc=u[5].split(':')[0]
    r_ac=judge(sc,FA[sc],acset,AC); r_ap=judge(sc,FA[sc],apset,AP)
    if r_ac['hits']==0 and r_ap['hits']==0: d='양쪽 개념 부재'
    elif r_ac['hits']>0 and r_ap['hits']==0: d='규범 소멸'
    elif r_ac['auth']>0 and r_ap['auth']==0: d='결속 상실'
    elif r_ac['t2']>r_ap['t2']: d='결속 강등'
    elif r_ap['t2']>r_ac['t2']: d='역전'
    else: d='불변'
    OUT['M-A'].append(dict(sc=sc,text=u[5].split(':',1)[1].strip(),AC=r_ac,AP=r_ap,delta=d))
for e in ELEMENTS:
    OUT['AC'].append(dict(sc=e[0],name=e[1],**judge(e[0],FAC[e[0]],acset,AC)))
for s in SCEN:
    OUT['CC'].append(dict(sc=s[4].split(':')[0],text=s[4].split(':',1)[1].strip(),maps=s[5],judged=False))
json.dump(OUT,open('frozen/ADJUDICATION.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print("=== M-G 안전제약 30건 ===")
c=Counter(r['cls'] for r in OUT['M-G'])
for k,v in c.most_common(): print(f"  {k:12s}{v:>3}")
h=[r for r in OUT['M-G'] if r['sc']=='SC-09-1'][0]
print(f"  ★ SC-09-1  매칭 {h['hits']} · 인가항 {h['auth']} · Tier2 {h['t2']} · Tier1 {h['t1']}")
print(f"  확정 결속: {[r['sc']+' → '+(r['ex'][0] if r['ex'] else '') for r in OUT['M-G'] if r['cls']=='확정 결속']}")
print("\n=== M-A 면제 대조 14건 ===")
c=Counter(r['delta'] for r in OUT['M-A'])
for k,v in c.most_common(): print(f"  {k:12s}{v:>3}")
print("\n=== 책무성 7요소 ===")
for r in OUT['AC']: print(f"  {r['sc']} {r['name']:12s} 매칭 {r['hits']:>3} · 인가항 {r['auth']:>2} · T2 {r['t2']} · {r['cls']}")
print(f"\n=== 인과제약 12건 — 판정 대상 아님 (조작자 자격·인간기계 적합성은 규범 탐색이 아니라 설계 요건) ===")
tot=len(OUT['M-G'])+len(OUT['M-A'])+len(OUT['CC'])+len(OUT['AC'])
print(f"\n총 제약 {tot}건 (M-G {len(OUT['M-G'])} · M-A {len(OUT['M-A'])} · 인과 {len(OUT['CC'])} · 책무성 {len(OUT['AC'])})")

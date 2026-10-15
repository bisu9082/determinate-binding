# -*- coding: utf-8 -*-
"""보류 집합 검증 — 독립 분석자(눈가림)가 재작성한 패싯으로 같은 판정을 하면
   같은 결과 분류가 나오는가. 명세 F-6의 후속 조치.
표본: seed 20260920 무작위 12건 (SC-09-1 포함, 강제편입 불요했음)."""
import json,sys,collections
sys.path.insert(0,'stpa'); sys.path.insert(0,'probe'); sys.path.insert(0,'holdout')
from carveout import N,build,tier_of,ap_nodes
from facets_mg import FACETS as MINE_G
from facets_ma import FACETS as MINE_A
import facets_blind as B
from facetmatch import match
from scope import admissible
MINE={**MINE_G,**MINE_A}
acset=set(N); AC=build(acset)
apset,_=ap_nodes(); AP=build(apset)
def judge(sc,f,allowed,ADJ):
    hit=[k for k in sorted(allowed) if admissible(sc,k) and match(f,k,N,ADJ,allowed)]
    t={k:tier_of(k,ADJ,allowed) for k in hit}
    auth=[k for k,v in t.items() if v is not None]
    t2=[k for k in auth if t[k]==2]
    c='개념 부재' if not hit else ('인가조항 아님' if not auth else ('영점' if not t2 else '확정 결속'))
    return c,len(hit),len(auth),len(t2)
hold=sorted(B.FACETS)
rows=[]
for sc in hold:
    al,ad=(apset,AP) if False else (acset,AC)   # M-A도 민간경로(AC) 기준으로 비교
    a=judge(sc,MINE[sc],al,ad); b=judge(sc,B.FACETS[sc],al,ad)
    rows.append((sc,a,b))
print(f"보류 집합 {len(rows)}건 · 독립 분석자 눈가림 재작성 vs 본 등록부\n")
print(f"{'제약':10s}{'본 매칭':>7s}{'독립 매칭':>9s}   {'본 판정':10s}{'독립 판정':10s} 일치")
print('-'*62)
agree=0
for sc,a,b in rows:
    ok = a[0]==b[0]; agree+=ok
    print(f"{sc:10s}{a[1]:>7}{b[1]:>9}   {a[0]:10s}{b[0]:10s} {'○' if ok else '✗'}")
print('-'*62)
n=len(rows)
print(f"결과분류 일치 {agree}/{n} = {agree/n*100:.1f}%")
# 4분류 명목 일치도: 우연일치 보정 (Cohen's kappa)
ca=collections.Counter(a[0] for _,a,_ in rows); cb=collections.Counter(b[0] for _,_,b in rows)
pe=sum(ca[k]*cb[k] for k in set(ca)|set(cb))/(n*n)
po=agree/n
kappa=(po-pe)/(1-pe) if pe<1 else float('nan')
print(f"우연일치 기대 {pe:.3f} · Cohen's κ = {kappa:.3f}")
# 반증 방향: 독립 분석자가 확정결속을 냈는데 본 등록부가 못 낸 경우
flip=[(sc,a[0],b[0]) for sc,a,b in rows if b[0]=='확정 결속' and a[0]!='확정 결속']
print(f"\n▸ 반증 방향(독립=확정결속, 본=아님): {len(flip)}건 {flip}")
h=[r for r in rows if r[0]=='SC-09-1']
if h:
    sc,a,b=h[0]
    print(f"▸ 헤드라인 SC-09-1: 본 {a[0]}(매칭{a[1]}·T2 {a[3]}) vs 독립 {b[0]}(매칭{b[1]}·T2 {b[3]})")
json.dump([{'sc':s,'mine':a,'blind':b} for s,a,b in rows],
          open('verify/holdout_result.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)

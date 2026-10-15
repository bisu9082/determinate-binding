# -*- coding: utf-8 -*-
"""민감도 S-SCOPE — 적용범위 제한(stpa/scope.py)이 결과를 만드는가.
이 제한은 개발 실행 중 추가되었고(항공 제약이 한국 지상로봇 변경인증에 매칭),
58건 중 44건의 확정결속을 보유한 항공 기관을 지상임무에서 제외한다.
= 파이프라인에서 가장 결과결정적인 재량 선택. 검증 6종에 빠져 있었다."""
import json,sys,collections
sys.path.insert(0,'stpa'); sys.path.insert(0,'probe')
from carveout import N,build,tier_of,ap_nodes
from facets_mg import FACETS as FG
from facets_ma import FACETS as FA
from facetmatch import match
from scope import admissible, DOMAIN, MISSION_SCOPE
acset=set(N); AC=build(acset)
def judge(sc,facets,allowed,ADJ,use_scope=True):
    hit=[k for k in sorted(allowed) if (admissible(sc,k) if use_scope else True) and match(facets,k,N,ADJ,allowed)]
    t={k:tier_of(k,ADJ,allowed) for k in hit}
    auth=[k for k,v in t.items() if v is not None]
    t2=[k for k in auth if t[k]==2]
    c='개념 부재' if not hit else ('인가조항 아님' if not auth else ('영점' if not t2 else '확정 결속'))
    return c,len(hit),len(auth),len(t2)
rows=[]
for sc,f in FG.items():
    a=judge(sc,f,acset,AC,True); b=judge(sc,f,acset,AC,False)
    rows.append((sc,a,b))
print("=== M-G 30건 · 적용범위 제한 유(공표) vs 무 ===")
print(f"{'제약':10s}{'제한有 매칭':>9s}{'제한無 매칭':>9s}   {'제한有':10s}→ {'제한無'}")
print('-'*66)
chg=0
for sc,a,b in rows:
    m='  ←' if a[0]!=b[0] else ''
    if m: chg+=1
    print(f"{sc:10s}{a[1]:>9}{b[1]:>9}   {a[0]:10s}→ {b[0]}{m}")
print('-'*66)
c1=collections.Counter(a[0] for _,a,_ in rows); c2=collections.Counter(b[0] for _,_,b in rows)
for k in ('확정 결속','영점','인가조항 아님','개념 부재'):
    print(f"  {k:12s} 제한有 {c1[k]:>3}  →  제한無 {c2[k]:>3}")
print(f"\n판정 변동 {chg}건 · 미결속 제한有 {30-c1['확정 결속']}/30 → 제한無 {30-c2['확정 결속']}/30")
# 지상임무가 실제로 탐색한 범위
g_docs=[d for d,v in DOMAIN.items() if v in MISSION_SCOPE['M-G']]
g_nodes=sum(1 for k in N if DOMAIN[k.split('::')[0]] in MISSION_SCOPE['M-G'])
juris={'KR':0,'JP':0,'EU':0,'US':0}
for d in g_docs:
    j='KR' if d.startswith('KR') else ('JP' if d.startswith('JP') else ('EU' if d in ('LED','EUAI') else 'US'))
    juris[j]+=1
print(f"\n▸ 지상임무 실제 탐색 범위: 기관 {len(g_docs)}개 · 노드 {g_nodes} · 관할 {[k for k,v in juris.items() if v]}")
print(f"  (원고가 '14기관 4관할'이라 쓴 자리 — 정정 필요)")

# -*- coding: utf-8 -*-
"""민감도 S-NONDET: 비확정연산자 캡을 완전히 제거했을 때 제약 수준 판정이 바뀌는가.
문단 입도에서 DET와 NONDET가 같은 단위에 공존하면 서로 다른 절을 지배하더라도 tier1로 강등된다.
이 규칙이 결속을 과소계상하는 방향(= 본고 주장에 유리한 방향)이므로 상한을 계측한다."""
import json,re,sys
from collections import defaultdict,deque,Counter
sys.path.insert(0,'stpa'); sys.path.insert(0,'probe')
from lex2 import EVAL,AUTH,DET,NONDET,PENALTY,DET_EXCLUDE
from carveout import N,E,ap_nodes
from uca_mg import UCA as UG
from uca_ma import UCA as UA
from accountability import ELEMENTS, FUNC as FAC
from match_mg import FUNC as FG
from compare import FUNC as FA
from scope import admissible
R=lambda L: re.compile("|".join(L),re.I)
rE,rA,rD,rN,rP,rX=R(EVAL),R(AUTH),R(DET),R(NONDET),R(PENALTY),R(DET_EXCLUDE)
L={k:{'e':bool(rE.search(v)),'a':bool(rA.search(v)),'d':bool(rD.search(v)) and not rX.search(v),
      'n':bool(rN.search(v)),'p':bool(rP.search(v))} for k,v in N.items()}
def build(allowed):
    A=defaultdict(set)
    for a,b,_ in E:
        if a in allowed and b in allowed: A[a].add(b)
    return A
def tier_nocap(s,ADJ,allowed,hop=4):
    if s not in allowed: return None
    l=L[s]
    if not l['a'] or l['p']: return None
    if l['e'] and l['d']: return 2
    cap=2 if l['d'] else 1
    q=deque([(s,0)]); seen={s}; best=0
    while q:
        cur,d=q.popleft()
        if L[cur]['e']:
            best=max(best,cap)
            if cap==2: return 2
        if d>=hop: continue
        for nx in ADJ.get(cur,()):
            if nx in seen or nx not in allowed: continue
            seen.add(nx); q.append((nx,d+1))
    return best
apset,_=ap_nodes(); acset=set(N); AC,AP=build(acset),build(apset)
def judge(sc,pats,allowed,ADJ):
    Rr=re.compile("|".join(pats),re.I)
    hit=[k for k in sorted(allowed) if admissible(sc,k) and Rr.search(N[k])]
    t={k:tier_nocap(k,ADJ,allowed) for k in hit}
    auth=[k for k,v in t.items() if v is not None]
    t2=[k for k in auth if t[k]==2]
    if not hit: return '개념 부재',0
    if not auth: return '인가조항 아님',0
    return ('영점' if not t2 else '확정 결속'), len(t2)
base=json.load(open('frozen/ADJUDICATION.json',encoding='utf-8'))
chg=[]
for u in UG:
    sc=u[5].split(':')[0]
    if sc not in FG: continue
    c,_=judge(sc,FG[sc],acset,AC)
    b=[r for r in base['M-G'] if r['sc']==sc][0]['cls']
    if c!=b: chg.append(('M-G',sc,b,c))
for u in UA:
    sc=u[5].split(':')[0]
    for lab,al,ad,key in (('AC',acset,AC,'AC'),('AP',apset,AP,'AP')):
        c,_=judge(sc,FA[sc],al,ad)
        b=[r for r in base['M-A'] if r['sc']==sc][0][key]['cls']
        if c!=b: chg.append(('M-A/'+lab,sc,b,c))
for e in ELEMENTS:
    c,_=judge(e[0],FAC[e[0]],acset,AC)
    b=[r for r in base['AC'] if r['sc']==e[0]][0]['cls']
    if c!=b: chg.append(('AC',e[0],b,c))
print("=== 민감도 S-NONDET: 비확정연산자 캡 완전 제거 ===")
print(f"제약 수준 판정 변동: {len(chg)}건")
for x in chg: print('  ',x)
h=[r for r in base['M-G'] if r['sc']=='SC-09-1'][0]
c,n2=judge('SC-09-1',FG['SC-09-1'],acset,AC)
print(f"헤드라인 SC-09-1: 본판정 {h['cls']} (T2 {h['t2']}) → 캡 제거 시 {c} (T2 {n2})")

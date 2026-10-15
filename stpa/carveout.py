# -*- coding: utf-8 -*-
"""면제 = 그래프의 노드 삭제. AC(민간경로) vs AP(경찰경로)를 동일 임무·동일 제약으로 비교한다.
배제 규칙은 전부 원문 근거를 단다. 경계 사례는 AP에 유리하게(=보수적으로) 남긴다."""
import re, json, sys
from collections import defaultdict, deque
sys.path.insert(0,'probe'); from lex2 import EVAL,AUTH,DET,NONDET,PENALTY,DET_EXCLUDE
R=lambda L: re.compile("|".join(L),re.I)
rE,rA,rD,rN,rP,rX=R(EVAL),R(AUTH),R(DET),R(NONDET),R(PENALTY),R(DET_EXCLUDE)
N=json.load(open('graph/nodes3.json',encoding='utf-8'))
E=[tuple(e) for e in json.load(open('graph/edges3.json',encoding='utf-8'))]

# ---- 배제 규칙 (AP 경로에서 사라지는 규범) ----
CFR_SUBPART_C = [f"107.{n}" for n in (52,53,56,57,59,61,63,64,65,67,69,71,73,74,77,79)]
CFR_SUBPART_D = [f"107.{n}" for n in (100,105,110,115,120,125,130,135,140,145,150,155,160,165)]
EXCLUSIONS = [
 ("EU1139", lambda k: k.startswith('EU1139::'),
  "Reg (EU) 2018/1139 Art 2(3)(a): does not apply to aircraft … and equipment to control aircraft "
  "remotely … carrying out … police … activities, and the personnel and organisations involved"),
 ("EU947",  lambda k: k.startswith('EU947::'),
  "Implementing Reg (EU) 2019/947 rests on Reg 2018/1139; excluded with its basis"),
 ("EU945",  lambda k: k.startswith('EU945::'),
  "Delegated Reg (EU) 2019/945 rests on Reg 2018/1139; excluded with its basis"),
 ("CFR-C",  lambda k: any(k.startswith(f"US107::{s}") for s in CFR_SUBPART_C),
  "AC 00-1.1B ¶12: PAO may self-certify standards for … pilot certification, qualification, and medical standards"),
 ("CFR-D",  lambda k: any(k.startswith(f"US107::{s}") for s in CFR_SUBPART_D),
  "AC 00-1.1B ¶12: PAO may self-certify standards for unmanned aircraft (UA) airworthiness"),
]
# 보수적 유지: Subpart A/B(NAS 공통 운항규칙) · Subpart E(웨이버) · LED · 조례 · 한국·일본 지상법규

def ap_nodes():
    drop=set()
    for _,f,_ in EXCLUSIONS: drop |= {k for k in N if f(k)}
    return set(N)-drop, drop

L={k:{'e':bool(rE.search(v)),'a':bool(rA.search(v)),
      'd':bool(rD.search(v)) and not rX.search(v),
      'n':bool(rN.search(v)),'p':bool(rP.search(v))} for k,v in N.items()}
def is_para(nid):
    """F-5: 인가조항은 항(paragraph) 노드여야 한다. 조 캡션(허브)은 규범 문언이 없다.
    graph/paths3.py의 starts()와 동일한 조건을 여기에 이식한다(2026-09-20 정정)."""
    return '.' in nid.split('::')[1]
def tier_of(s,ADJ,allowed,hop=4):
    if s not in allowed: return None
    l=L[s]
    if not l['a'] or l['p'] or not is_para(s): return None
    if l['e'] and l['d'] and not l['n']: return 2
    cap=2 if l['d'] else 1
    q=deque([(s,0,l['n'])]); seen={s}; best=0
    while q:
        cur,d,nd=q.popleft()
        if L[cur]['e']:
            t=2 if (cap==2 and not nd) else 1
            best=max(best,t)
            if t==2: return 2
        if d>=hop: continue
        for nx in ADJ.get(cur,()):
            if nx in seen or nx not in allowed: continue
            seen.add(nx); q.append((nx,d+1,nd or L[nx]['n']))
    return best
def build(allowed):
    """인접 리스트 정렬 — BFS 순서 고정(2026-09-20)."""
    A=defaultdict(set)
    for a,b,_ in E:
        if a in allowed and b in allowed: A[a].add(b)
    return {k:sorted(v) for k,v in A.items()}
if __name__=='__main__':
    apset,drop=ap_nodes()
    print(f"전체 노드 {len(N)} · AP 배제 {len(drop)} · AP 잔존 {len(apset)}")
    from collections import Counter
    print("  배제 내역:",dict(Counter(k.split('::')[0] for k in drop)))
    print("\n배제 근거:")
    for name,f,src in EXCLUSIONS:
        n=sum(1 for k in N if f(k)); print(f"  {name:8s} {n:>4}노드  {src[:96]}")

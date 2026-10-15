# -*- coding: utf-8 -*-
"""경로 탐색 v3 — 확정연산자는 **출발(인가) 노드**에 있어야 한다 + 벌칙 출발 제외."""
import json,re,sys
from collections import defaultdict,deque,Counter
sys.path.insert(0,'probe'); from lex2 import EVAL,AUTH,DET,NONDET,PENALTY,DET_EXCLUDE
R=lambda L: re.compile("|".join(L),re.I)
rE,rA,rD,rN,rP,rX=R(EVAL),R(AUTH),R(DET),R(NONDET),R(PENALTY),R(DET_EXCLUDE)
N=json.load(open('graph/nodes3.json',encoding='utf-8'))
E=[tuple(e) for e in json.load(open('graph/edges3.json',encoding='utf-8'))]
L={k:{'e':bool(rE.search(v)),'a':bool(rA.search(v)),'d':bool(rD.search(v)) and not rX.search(v),
      'n':bool(rN.search(v)),'p':bool(rP.search(v))} for k,v in N.items()}
# 변경 ⑩ (부록 A): 명세 F-5 는 인가항이 '항 노드' 일 것을 요구한다. 조 표제는
# 규범 본문을 담지 않기 때문이다. 구현은 식별자에 마침표가 있는지를 보았다.
# 한국·일본 법령에는 맞는 판정이다 — 조가 43, 항이 43.1 이다. 미국 법령에는
# 틀리다 — 조 식별자 자체에 마침표가 있다. 107.13 이 조이고 107.13(a) 가 항이다.
# 그래서 Part 107·89 에는 규칙이 아예 적용되지 않았고, 자기 자식을 가진 조 표제
# 다섯 개가 인가 모집단에 서 있었다: 14 CFR §§ 107.13, 107.69, 89.215, 89.510,
# 89.515. 명세가 실제로 말한 조건, 즉 '그래프에 자식 노드가 없다' 로 바꾼다.
# 이 판정은 식별자 관습에 의존하지 않으므로 열여섯 기관에 똑같이 적용된다.
_KIDS={k.rsplit('.',1)[0] for k in L if '.' in k.split('::')[1]}
def _is_para(k):
    return k not in _KIDS
def starts():
    return [k for k,l in sorted(L.items())
            if l['a'] and not l['p'] and '.' in k.split('::')[1] and _is_para(k)]
def classify(s,ADJ,hop=4):
    l=L[s]
    if not l['d']:                    # 확정연산자 없는 인가 = Tier1 후보 또는 0
        tier_cap=1
    else: tier_cap=2
    if l['e'] and l['d'] and not l['n']: return (2,[s])
    q=deque([(s,[s],0,l['n'])]); seen={s}; best=0; bp=[s]
    while q:
        cur,path,d,nd=q.popleft()
        if L[cur]['e']:
            t=2 if (tier_cap==2 and not nd) else 1
            if t>best: best,bp=t,path
            if t==2: return (2,path)
        if d>=hop: continue
        for nx in ADJ.get(cur,()):
            if nx in seen or nx not in L: continue
            seen.add(nx); q.append((nx,path+[nx],d+1,nd or L[nx]['n']))
    return (best,bp)
def run(edges,hop=4):
    """인접 리스트를 정렬해 BFS 순서를 고정한다(2026-09-20 정정).
    종전에는 set 순회라 tier는 안정적이나 기록되는 path가 실행마다 달라져
    'bit-identical' 주장이 성립하지 않았다."""
    tmp=defaultdict(set)
    for a,b,_ in edges: tmp[a].add(b)
    ADJ={k:sorted(v) for k,v in tmp.items()}
    return {s:classify(s,ADJ,hop) for s in sorted(starts())}
if __name__=='__main__':
    print(f"{'조건':26s}{'인가항':>8s}{'Tier2':>7s}{'Tier1':>7s}{'Tier0':>7s}")
    print('-'*56)
    for lab,edg,h in [("엣지0 (조문 고립)",[],4),("hop=1",E,1),("hop=2",E,2),
                      ("hop=3",E,3),("hop=4",E,4),("hop=5",E,5),
                      ("hop=4 · 구조참조 제외",[e for e in E if e[2] not in ('struct_ref','cpt_contain')],4)]:
        r=run(edg,h); c=Counter(v[0] for v in r.values())
        print(f"{lab:26s}{len(r):>8}{c[2]:>7}{c[1]:>7}{c[0]:>7}")
    res=run(E,4)
    json.dump({k:{'tier':v[0],'path':v[1]} for k,v in res.items()},
              open('graph/paths3.json','w',encoding='utf-8'),ensure_ascii=False)
    byd=defaultdict(Counter)
    for k,v in res.items(): byd[k.split('::')[0]][v[0]]+=1
    print(f"\n{'문서':22s}{'인가항':>7s}{'Tier2':>7s}{'Tier1':>7s}{'Tier0':>7s}")
    print('-'*50)
    for d in sorted(byd,key=lambda x:-sum(byd[x].values())):
        c=byd[d]; print(f"{d:22s}{sum(c.values()):>7}{c[2]:>7}{c[1]:>7}{c[0]:>7}")

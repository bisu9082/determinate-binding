# -*- coding: utf-8 -*-
"""경로 탐색 v2 — 길이 정의를 hop 수로 통일. Tier2/1/0 판정."""
import json,re,sys
from collections import defaultdict,deque,Counter
sys.path.insert(0,'probe'); from lex import EVAL,AUTH,DET,NONDET
R=lambda L: re.compile("|".join(L),re.I); rE,rA,rD,rN=R(EVAL),R(AUTH),R(DET),R(NONDET)
N=json.load(open('graph/nodes2.json',encoding='utf-8'))
E=[tuple(e) for e in json.load(open('graph/edges2.json',encoding='utf-8'))]
ADJ=defaultdict(set)
for a,b,_ in E: ADJ[a].add(b)
def op(t): return 'DET' if rD.search(t) else ('NONDET' if rN.search(t) else 'NONE')
L={k:{'e':bool(rE.search(v)),'a':bool(rA.search(v)),'o':op(v)} for k,v in N.items()}
def classify(s,hop=4):
    l=L[s]; best=(0,[s])
    q=deque([(s,[s],0,l['o']=='DET',l['o']=='NONDET')]); seen={s}
    while q:
        cur,path,d,det,nd=q.popleft()
        if L[cur]['e']:
            t=2 if (det and not nd) else 1
            if t>best[0]: best=(t,path)
            if t==2: return best
        if d>=hop: continue
        for nx in ADJ.get(cur,()):
            if nx in seen or nx not in L: continue
            seen.add(nx); o=L[nx]['o']
            q.append((nx,path+[nx],d+1,det or o=='DET',nd or o=='NONDET'))
    return best
def run(hop=4, edges=None):
    global ADJ
    if edges is not None:
        ADJ=defaultdict(set)
        for a,b,_ in edges: ADJ[a].add(b)
    res={}
    for k,l in L.items():
        if not l['a'] or '.' not in k.split('::')[1]: continue   # 항 노드만 판정
        res[k]=classify(k,hop)
    return res
if __name__=='__main__':
    print(f"{'조건':26s}{'인가항':>8s}{'Tier2':>7s}{'Tier1':>7s}{'Tier0':>7s}")
    print('-'*56)
    for lab,edg,h in [("엣지0 (조문 고립)",[],4),
                      ("포함엣지만",[e for e in E if e[2]=='contain'],4),
                      ("전체 엣지 hop=1",E,1),("전체 엣지 hop=2",E,2),
                      ("전체 엣지 hop=3",E,3),("전체 엣지 hop=4",E,4),("전체 엣지 hop=5",E,5)]:
        r=run(h,edg); c=Counter(v[0] for v in r.values())
        print(f"{lab:26s}{len(r):>8}{c[2]:>7}{c[1]:>7}{c[0]:>7}")
    res=run(4,E)
    json.dump({k:{'tier':v[0],'path':v[1]} for k,v in res.items()},
              open('graph/paths2.json','w',encoding='utf-8'),ensure_ascii=False)
    byd=defaultdict(Counter)
    for k,v in res.items(): byd[k.split('::')[0]][v[0]]+=1
    print(f"\n{'문서':22s}{'인가항':>7s}{'Tier2':>7s}{'Tier1':>7s}{'Tier0':>7s}")
    print('-'*50)
    for d in sorted(byd,key=lambda x:-sum(byd[x].values())):
        c=byd[d]; print(f"{d:22s}{sum(c.values()):>7}{c[2]:>7}{c[1]:>7}{c[0]:>7}")

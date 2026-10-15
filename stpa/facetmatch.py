# -*- coding: utf-8 -*-
"""패싯 매처 v2 — 명세 stpa/facetspec.md F-1(2026-09-20 개정).
subject 패싯은 후보 조문 본문에서 발화(앵커), 나머지 패싯은 hop≤4 도달 이웃에서 충족 가능.
판정(tier_of)과 동일한 도달가능성 위에서 정의한다."""
import re
from collections import deque
_c={}
def _rx(pats):
    k=tuple(pats)
    if k not in _c: _c[k]=re.compile("|".join(pats),re.I)
    return _c[k]

def reach(nid, ADJ, allowed, hop=4):
    """nid 포함, hop 이내 도달 노드 집합 (판정과 동일 방향·동일 상한)"""
    q=deque([(nid,0)]); seen={nid}
    while q:
        cur,d=q.popleft()
        if d>=hop: continue
        for nx in ADJ.get(cur,()):
            if nx in seen or nx not in allowed: continue
            seen.add(nx); q.append((nx,d+1))
    return seen

def match(facets, nid, N, ADJ, allowed, hop=1):
    if 'subject' not in facets:
        raise ValueError('F-2: subject 패싯 필수 — '+str(list(facets)))
    if not _rx(facets['subject']).search(N[nid]): return False
    rest=[p for n,p in facets.items() if n!='subject']
    if not rest: return True
    R=reach(nid,ADJ,allowed,hop)
    blob=' '.join(N[k] for k in R)
    return all(_rx(p).search(blob) for p in rest)

def which(facets, nid, N, ADJ, allowed, hop=1):
    out={}
    out['subject']=(_rx(facets['subject']).search(N[nid]) or [None])
    out['subject']=out['subject'].group(0) if hasattr(out['subject'],'group') else None
    R=reach(nid,ADJ,allowed,hop); blob=' '.join(N[k] for k in R)
    for n,p in facets.items():
        if n=='subject': continue
        m=_rx(p).search(N[nid]) or _rx(p).search(blob)
        out[n]=(m.group(0)+('' if _rx(p).search(N[nid]) else ' [경로]')) if m else None
    return out

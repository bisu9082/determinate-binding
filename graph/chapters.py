# -*- coding: utf-8 -*-
"""EU 장/절 구조 → 장 허브 노드 + 장→조문 포함엣지 (D-5)."""
import re, json
FILES=[('euc_02019R0945-20250624.html','EU945'),('euc_02019R0947-20250501.html','EU947'),
       ('euc_02018R1139-20260802.html','EU1139'),
       ('eu_32014L0032.html','MID')]   # 2026-09-20 편입
def build():
    nodes={}; edges=[]
    for f,doc in FILES:
        s=open('corpus/'+f,encoding='utf-8',errors='replace').read()
        cut=s.find('id="anx_'); body=s[:cut] if cut>0 else s
        ev=sorted([(m.group(1),m.start(),'cpt') for m in re.finditer(r'<div id="(cpt_[^"]*)"',body)]
                 +[(m.group(1),m.start(),'art') for m in re.finditer(r'<div class="eli-subdivision" id="(art_[0-9a-z]+)"',body)],
                 key=lambda x:x[1])
        cur=None
        for name,pos,kind in ev:
            if kind=='cpt':
                cur=f"{doc}::{name}"; nodes[cur]=f"{doc} {name}"
            elif cur:
                edges.append((cur,f"{doc}::{name}",'cpt_contain'))
                # 절이면 상위 장에도 연결
                if '.' in cur.split('::')[1]:
                    top=f"{doc}::{cur.split('::')[1].split('.')[0]}"
                    if top in nodes: edges.append((top,f"{doc}::{name}",'cpt_contain'))
    return nodes, sorted(set(edges))
if __name__=='__main__':
    n,e=build(); print(len(n),'장/절 노드 ·',len(e),'포함엣지')

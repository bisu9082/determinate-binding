# -*- coding: utf-8 -*-
"""전체 데이터 정합성 검증 — 이번 세션에서 보고한 모든 수치를 원자료에서 재도출."""
import json,re,os,sys,subprocess
OK=[];NG=[];NA=[]
def chk(label, got, want, note=''):
    (OK if got==want else NG).append((label,got,want,note))
def na(label,why): NA.append((label,why))

# ---- 1. v7 코딩 (G/AC/AP 인터페이스 계층) ----
try:
    d=json.load(open('v7/coding_v7.json',encoding='utf-8'))
    for path,want_D,want_P,want_N in [('G',2,15,5),('AC',6,10,5),('AP',2,12,7)]:
        cells=d[path]
        itf=[v[2] for v in cells.values()] if isinstance(next(iter(cells.values())),(list,tuple)) else None
        if itf is None: na(f'v7 {path}','coding_v7.json 구조 불일치'); continue
        from collections import Counter
        c=Counter(itf)
        chk(f'v7 {path} 인터페이스 D/P/N', (c.get('D',0),c.get('P',0),c.get('N',0)), (want_D,want_P,want_N))
except Exception as e: na('v7 코딩',str(e))

# ---- 2. 민감도 AC<AP = 0 ----
try:
    r=subprocess.run([sys.executable,'sens.py'],capture_output=True,text=True,timeout=120,cwd='v7')
    rows=re.findall(r'^S\d[^\n]*?\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s*$',r.stdout,re.M)
    chk('민감도 시나리오 수', len(rows), 6)
    chk('민감도 AC<AP 전 시나리오 0', sorted({x[4] for x in rows}), ['0'])
    chk('S1 관측 G/AC/AP Direct', tuple(rows[0][:3]) if rows else None, ('2','6','2'))
except Exception as e: na('민감도',str(e))

# ---- 3. 신규 문헌 term counts ----
def cnt(path, terms, lig=True):
    t=open(path,encoding='utf-8',errors='replace').read()
    if lig: t=t.replace('ﬁ','fi').replace('ﬂ','fl').replace('ﬀ','ff').replace('ﬃ','ffi')
    low=t.lower(); return {k:low.count(k) for k in terms}
try:
    n=cnt('nov/nasirov.txt',['converter','conformity','certif','police','aviation','drone','keyness','hardening'])
    chk('Nasirov converter', n['converter'], 40); chk('Nasirov conformity', n['conformity'], 5)
    chk('Nasirov certif', n['certif'], 5); chk('Nasirov police', n['police'], 0)
    chk('Nasirov aviation', n['aviation'], 0); chk('Nasirov drone', n['drone'], 0)
except Exception as e: na('Nasirov',str(e))
try:
    s=cnt('nov/scott.txt',['state aircraft','police','law enforcement','public aircraft'])
    chk('Scott state aircraft', s['state aircraft'], 0); chk('Scott police', s['police'], 0)
    chk('Scott law enforcement', s['law enforcement'], 0); chk('Scott public aircraft', s['public aircraft'], 0)
except Exception as e: na('Scott',str(e))

# ---- 4. 서지 90건 ----
try:
    b=open('tex/myref_v2.bib',encoding='utf-8',errors='replace').read()
    chk('myref_v2.bib 엔트리', len(re.findall(r'^@\w+\{',b,re.M)), 90)
except Exception as e: na('bib',str(e))

# ---- 5. 그래프 v3 ----
try:
    N=json.load(open('graph/nodes3.json',encoding='utf-8'))
    E=json.load(open('graph/edges3.json',encoding='utf-8'))
    chk('그래프 노드', len(N), 5190); chk('그래프 엣지', len(E), 7873)
    P=json.load(open('graph/paths3.json',encoding='utf-8'))
    from collections import Counter
    c=Counter(v['tier'] for v in P.values())
    chk('인가 항', len(P), 856); chk('Tier2', c[2], 58); chk('Tier1', c[1], 443); chk('Tier0', c[0], 355)
    multi=sum(1 for v in P.values() if v['tier']==2 and len(v['path'])>1)
    chk('경로로만 성립 Tier2', multi, 11)
    ext={d:sum(1 for k,v in P.items() if k.startswith(d+'::') and v['tier']==2)
         for d in ['LED','SMC1418','CAGOV','USAC']}
    chk('EXT층 Tier2 합', sum(ext.values()), 0, str(ext))
except Exception as e: na('그래프',str(e))

# ---- 6. 코퍼스 해시 ----
import hashlib
try:
    man=json.load(open('corpus/MANIFEST.json',encoding='utf-8'))
    bad=[m['file'] for m in man if not os.path.exists('corpus/'+m['file'])
         or hashlib.sha256(open('corpus/'+m['file'],'rb').read()).hexdigest()!=m['sha256']]
    chk('코퍼스 SHA256 불일치', len(bad), 0, str(bad))
except Exception as e: na('코퍼스',str(e))

print(f"{'✔ 일치':6s} {len(OK)}건 / {'✘ 불일치':8s} {len(NG)}건 / {'⚠ 확인불가':10s} {len(NA)}건\n")
if NG:
    print("=== 불일치 ===")
    for l,g,w,n in NG: print(f"  ✘ {l:32s} 실측={g}  보고={w}  {n}")
if NA:
    print("\n=== 확인 불가 ===")
    for l,w in NA: print(f"  ⚠ {l:32s} {w}")
print("\n=== 일치 항목 ===")
for l,g,w,n in OK: print(f"  ✔ {l:32s} {g}")

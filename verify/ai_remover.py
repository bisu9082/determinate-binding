# -*- coding: utf-8 -*-
"""AI 문체 스캐너 — feedback_no_ai_style 규칙 기반. 탐지만 하고 수정은 사람이 확인 후."""
import re,sys,os,json
BAN_WORD = {
 'delve':r'\bdelv(e|es|ing|ed)\b', 'notably':r'\b[Nn]otably\b', 'crucially':r'\b[Cc]rucially\b',
 'remarkably':r'\b[Rr]emarkably\b', 'intriguingly':r'\b[Ii]ntriguingly\b',
 'worth noting':r'[Ii]t is worth noting', 'crucial/pivotal role':r'plays? an? (crucial|pivotal|key|vital) role',
 'paves the way':r'paves? the way', 'sheds light':r'sheds? light on',
 'leverage(동사)':r'\bleverag(e|es|ing|ed)\b', 'landscape(은유)':r'\blandscape\b',
 'holistic':r'\bholistic\b', 'seamless':r'\bseamless\w*\b', 'robust(장식)':r'\brobust\b',
 'comprehensive(장식)':r'\bcomprehensive\b', 'underscore':r'\bunderscor(e|es|ing|ed)\b',
 'highlight(남발)':r'\bhighlight(s|ed|ing)?\b', 'moreover':r'\b[Mm]oreover\b',
 'furthermore':r'\b[Ff]urthermore\b', 'in conclusion':r'\b[Ii]n conclusion\b',
 'it should be noted':r'[Ii]t should be noted', 'a testament to':r'a testament to',
 'navigate(은유)':r'\bnavigat(e|es|ing|ed)\b(?! to)', 'realm':r'\brealm\b',
 'pivotal':r'\bpivotal\b', 'myriad':r'\bmyriad\b', 'tapestry':r'\btapestry\b',
 'crucial':r'\bcrucial\b', 'vital':r'\bvital\b', 'significantly(비통계)':r'\bsignificantly\b',
}
def scan(path):
    t=open(path,encoding='utf-8',errors='replace').read()
    body=re.sub(r'(?m)^\s*%.*$','',t)                     # 주석 제외
    hits={}
    for name,pat in BAN_WORD.items():
        ms=[(m.start(),m.group(0)) for m in re.finditer(pat,body)]
        if ms: hits[name]=ms
    # 구조 지표
    emd=len(re.findall(r'---|—',body))
    first_second=len(re.findall(r'(?m)^\s*(First|Second|Third)\b',body))
    tri=len(re.findall(r'\b\w+, \w+,? and \w+\b',body))
    return t,body,hits,dict(em_dash=emd, first_second=first_second, triads=tri,
                            words=len(body.split()))
if __name__=='__main__':
    for p in sys.argv[1:]:
        if not os.path.exists(p): print(f"[없음] {p}"); continue
        t,body,hits,st=scan(p)
        tot=sum(len(v) for v in hits.values())
        print(f"\n=== {p} ({st['words']:,}단어) — 금지어휘 {tot}건 ===")
        for k,v in sorted(hits.items(), key=lambda x:-len(x[1])):
            ex=', '.join(sorted({w for _,w in v})[:3])
            print(f"  {k:24s} {len(v):>3}회   {ex}")
        print(f"  [구조] em-dash {st['em_dash']} · First/Second 문단머리 {st['first_second']} · 삼항나열 {st['triads']}")

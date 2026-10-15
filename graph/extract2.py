# -*- coding: utf-8 -*-
"""조문 노드 추출 v2 — 항(paragraph) 입도 + 부속서 절단 + 보일러플레이트 제외.
노드 id: DOC::art_N (허브, 제목만) / DOC::art_N.P (항)
허브→항 방향 포함엣지만 두고, 형제 항 사이는 연결하지 않는다(연산자 누출 차단)."""
import re, html, json, os, xml.etree.ElementTree as ET
C='corpus/'
def _t(s):
    s=re.sub(r'(?is)<(script|style|head)[^>]*>.*?</\1>',' ',s)
    return re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',s))).strip()

# ---- 사전등록 보일러플레이트 제외 규칙 (결과 보기 전 고정) ----
BOILER_TITLE = re.compile(r'(Entry into force|Final provisions|Addressees|Repeal|Transitional provisions'
                          r'|AC FEEDBACK FORM|Feedback Form)', re.I)
BOILER_KR     = re.compile(r'^제\d+조(?:의\d+)?\((벌칙|과태료|양벌규정|과태료의 부과|규제의 재검토)')
BOILER_JP     = re.compile(r'^（?(罰則|附則)')
def boiler(nid, txt):
    if BOILER_TITLE.search(txt[:160]): return True
    if nid.startswith('KR') and BOILER_KR.match(txt): return True
    if nid.startswith('JP') and BOILER_JP.match(txt): return True
    return False

def eu(path, doc):
    s=open(C+path,encoding='utf-8',errors='replace').read()
    cut=s.find('id="anx_')                       # ← 부속서 절단
    body = s[:cut] if cut>0 else s
    spans=[(m.group(1),m.start()) for m in re.finditer(r'<div class="eli-subdivision" id="(art_[0-9a-z]+)"', body)]
    out={}
    for i,(aid,st) in enumerate(spans):
        en = spans[i+1][1] if i+1<len(spans) else len(body)
        seg=body[st:en]
        title=_t(re.search(r'<p class="stitle-article-norm">(.*?)</p>',seg,re.S).group(1)) if re.search(r'<p class="stitle-article-norm">',seg) else ''
        hub=f"{doc}::{aid}"
        out[hub]=f"Article {aid.split('_')[1]} {title}".strip()
        paras=[(m.group(1), m.start()) for m in re.finditer(r'<span class="no-parag">\s*(\d+)\.',seg)]
        if not paras:   # 신판 EUR-Lex 마크업 (<div id="005.001">)
            paras=[(str(int(m.group(2))), m.start()) for m in re.finditer(r'<div id="(\d{3})\.(\d{3})"',seg)]
        if paras:
            for j,(pn,ps) in enumerate(paras):
                pe = paras[j+1][1] if j+1<len(paras) else len(seg)
                t=_t(seg[ps:pe])
                if len(t)>25: out[f"{hub}.{pn}"]=t
        else:
            t=_t(seg)
            # 변경 ⑦ (부록 A): 번호 항이 없는 조문을 한 노드로 쥐고 있어, EU 정의조문이
            # 각각 인가항 하나로 세어지고 그 안 어디에 있는 용어든 전부에 발화했다.
            # 가장 큰 것이 EUAI 제3조로 17,101자·정의 68개였다. 번호 정의로 쪼갠다.
            # 쪼개는 기준은 (N) 뒤에 따옴표가 오는 정의 머리뿐이고, 1부터 빠짐없이
            # 이어질 때만 적용한다. 정의 본문 안의 교차참조 (3) 같은 것에 걸리지 않는다.
            defs=[(int(m.group(1)),m.start()) for m in
                  re.finditer(r'\((\d+)\)\s*[\u2018\u2019\u201c\u201d\'"]',t)]
            seq=[x for i,x in enumerate(defs) if x[0]==i+1]
            if len(seq)>=5 and len(seq)==len(defs):
                for j,(dn,ds) in enumerate(seq):
                    de=seq[j+1][1] if j+1<len(seq) else len(t)
                    d=t[ds:de].strip()
                    if len(d)>25: out[f"{hub}.{dn}"]=d
            elif len(t)>40: out[f"{hub}.1"]=t
    # 부속서를 별도 노드로
    if cut>0:
        anx=s[cut:]
        parts=[(m.group(1),m.start()) for m in re.finditer(r'\b(PART\s+[0-9IVXA-Z]{1,4})\b', _t(anx)[:0] or '')]
        out[f"{doc}::ANNEX"]=_t(anx)[:6000]
    return out

# ── 변경 ⑤ (부록 A): 미국 조문의 최상위 항 letter 판정 ─────────────────
# 종전 패턴 \(([a-z])\) 는 괄호 안 소문자 한 글자를 전부 항으로 올렸다. 그래서
# 로마숫자 하위항 (i) 가 독립 항으로 승격했고, 존재하지 않는 §89.530(i) 가 인가
# 모집단에 들어갔다. 더 나쁜 것은 승격이 부모를 절단한 것이다 — §89.530(b)·(c) 와
# §107.140(c)·(d) 가 승격 항 뒤의 본문을 잃었다.
# CFR 의 항 letter 는 a→b→c 로 이어진다. 직전 letter 의 후속일 때만 항으로 본다.
def _next_letter(prev):
    if prev is None: return 'a'
    return chr(ord(prev)+1) if prev<'z' else None

def _top_para(t,prev):
    """t 가 최상위 항의 시작이면 그 letter, 아니면 None."""
    m=re.match(r'\(([a-z])\)\s',t)
    if not m: return None
    return m.group(1) if m.group(1)==_next_letter(prev) else None

def us107():
    """eCFR <P> 구조 기반 분해. (a)(b)(c)로 시작하는 P가 새 항, (1)(2)/(i)(ii)는 직전 항에 귀속."""
    s=open(C+'us_14CFR107.xml',encoding='utf-8',errors='replace').read(); out={}
    for m in re.finditer(r'<DIV8[^>]*N="(107\.\d+)"[^>]*>(.*?)</DIV8>', s, re.S):
        sec=m.group(1); seg=m.group(2); hub=f"US107::{sec}"
        head=re.search(r'<HEAD>(.*?)</HEAD>',seg,re.S)
        out[hub]=_t(head.group(1)) if head else sec
        ps=[_t(x) for x in re.findall(r'<P>(.*?)</P>', seg, re.S)]
        cur=None; buf=[]
        for t in ps:
            lt=_top_para(t,cur)
            if lt:
                if cur and buf: out[f"{hub}.{cur}"]=' '.join(buf)
                cur=lt; buf=[t]
            else: buf.append(t)
        if cur and buf: out[f"{hub}.{cur}"]=' '.join(buf)
        elif buf and len(' '.join(buf))>40: out[f"{hub}.a"]=' '.join(buf)
    return {k:v for k,v in out.items() if len(v)>20}

def usac():
    t=open(C+'us_ac0011b.txt',encoding='utf-8',errors='replace').read()
    cut=t.find('AC FEEDBACK FORM')
    if cut>0: t=t[:cut]
    out={}; cur=None; buf=[]
    for line in t.split('\n'):
        m=re.match(r'\s*(\d+(?:\.\d+){0,2})\s+(\S.*)$', line)
        if m and len(m.group(1))<=8:
            if cur and buf: out[f"USAC::{cur}"]=re.sub(r'\s+',' ',' '.join(buf)).strip()
            cur=m.group(1); buf=[m.group(2)]
        elif cur: buf.append(line.strip())
    if cur and buf: out[f"USAC::{cur}"]=re.sub(r'\s+',' ',' '.join(buf)).strip()
    return {k:v for k,v in out.items() if len(v)>30}

KRDOC={'kr_도로교통법.xml':'KR도로교통법','kr_도로교통법_시행규칙.xml':'KR도로교통법시행규칙',
       'kr_지능형로봇법.xml':'KR지능형로봇법','kr_지능형로봇_개발_및_보급_촉진법_시행령.xml':'KR지능형로봇법시행령'}
def kr(fn):
    doc=KRDOC[fn]; r=ET.parse(C+fn).getroot(); out={}
    for a in r.findall('.//조문단위'):
        n=a.findtext('조문번호') or ''; g=a.findtext('조문가지번호')
        if not n: continue
        uid=n+('의'+g if g else ''); hub=f"{doc}::{uid}"
        head=re.sub(r'\s+',' ',(a.findtext('조문내용') or '')).strip()
        hs=[re.sub(r'\s+',' ',(h.findtext('항내용') or '')).strip() for h in a.findall('.//항')]
        hs=[h for h in hs if len(h)>15]
        out[hub]=head or uid
        if hs:
            for i,h in enumerate(hs,1): out[f"{hub}.{i}"]=h
        elif len(head)>25: out[f"{hub}.1"]=head
    return out

def us89():
    """govinfo CFR XML(Part 89). eCFR의 DIV8과 구조가 달라 SECTION/SECTNO/P로 분해한다."""
    s=open(C+'us_14CFR89.xml',encoding='utf-8',errors='replace').read(); out={}
    for m in re.finditer(r'<SECTION>(.*?)</SECTION>', s, re.S):
        seg=m.group(1)
        mn=re.search(r'<SECTNO>[^0-9]*?(89\.\d+)</SECTNO>', seg)
        if not mn: continue
        sec=mn.group(1); hub=f"US89::{sec}"
        subj=re.search(r'<SUBJECT>(.*?)</SUBJECT>', seg, re.S)
        out[hub]=f"{sec} {_t(subj.group(1)) if subj else ''}".strip()
        ps=[_t(x) for x in re.findall(r'<P>(.*?)</P>', seg, re.S)]
        cur=None; buf=[]
        for t in ps:
            lt=_top_para(t,cur)
            if lt:
                if cur and buf: out[f"{hub}.{cur}"]=' '.join(buf)
                cur=lt; buf=[t]
            else: buf.append(t)
        if cur and buf: out[f"{hub}.{cur}"]=' '.join(buf)
        # 변경 ⑥ (부록 A): 번호 없는 단일 항으로 된 조문에 대비한 폴백이 Part 89
        # 추출기에만 없었다. 그래서 여섯 조문이 본문 없는 표제로 들어왔고, 그중
        # §89.105 는 Part 전체의 작동 금지 조항이다. Part 107 쪽이 이미 가진
        # 폴백을 같게 준다.
        elif buf and len(' '.join(buf))>40: out[f"{hub}.a"]=' '.join(buf)
    return {k:v for k,v in out.items() if len(v)>20}

def jp():
    s=open(C+'jp_api_1.xml',encoding='utf-8',errors='replace').read(); out={}
    # 변경 ① (부록 A): 附則 제외가 일본 법률에서 실행되지 않았다. 추출기가 조를
    # 번호만으로 키를 잡았고, 이 법은 본문 355조 · 附則 221조이며 附則의 고유번호
    # 42개 중 34개가 본문과 충돌한다. 뒤에 오는 것이 앞을 덮어써서 본문 1,011개
    # 항 노드 중 52개가 자기 본문 대신 附則 본문을 들고 있었고, 본문에 없는 附則
    # 항 26개가 노드로 들어왔다. 지운 것은 없다 — 마지막이 이기는 사전은 키의
    # 내용을 바꾸고 키를 없애지 않는다.
    # 수선: 본문(MainProvision) 범위로 한정한다. 附則 제외가 본래 하려던 일이다.
    _i=s.find('<MainProvision'); _j=s.find('</MainProvision>')
    if _i>=0 and _j>_i: s=s[_i:_j]
    for m in re.finditer(r'<Article\b[^>]*Num="([0-9_:]+)"[^>]*>(.*?)</Article>', s, re.S):
        num=m.group(1); seg=m.group(2); hub=f"JP道交法::{num}"
        cap=re.search(r'<ArticleCaption>(.*?)</ArticleCaption>',seg,re.S)
        out[hub]=re.sub(r'<[^>]+>','',cap.group(1)) if cap else num
        ps=re.findall(r'<Paragraph\b[^>]*Num="(\d+)"[^>]*>(.*?)</Paragraph>',seg,re.S)
        for pn,pt in ps:
            t=re.sub(r'\s+',' ',re.sub(r'<[^>]+>','',pt)).strip()
            if len(t)>20: out[f"{hub}.{pn}"]=t
    return out

def smc():
    t=open(C+'us_smc_14_18.txt',encoding='utf-8',errors='replace').read(); out={}
    secs=[(m.group(1),m.start()) for m in re.finditer(r'(14\.18\.\d{3})',t)]
    for i,(sid,st) in enumerate(secs):
        en=secs[i+1][1] if i+1<len(secs) else len(t)
        body=re.sub(r'\s+',' ',t[st:en]).strip()
        if len(body)<60: continue
        hub=f"SMC1418::{sid}"; out[hub]=sid
        subs=[(m.group(1),m.start()) for m in re.finditer(r'\b([A-Z])\.\s',body)]
        if len(subs)>=2:
            for j,(pn,ps) in enumerate(subs):
                pe=subs[j+1][1] if j+1<len(subs) else len(body)
                if pe-ps>50: out[f"{hub}.{pn}"]=body[ps:pe]
        else: out[f"{hub}.A"]=body
    return out

def cagov():
    out={}
    for n in range(7070,7076):
        p=f'{C}us_ca_gov{n}.html'
        if not os.path.exists(p): continue
        t=_t(open(p,encoding='utf-8',errors='replace').read()); i=t.find(f'{n}.')
        if i<0: continue
        body=re.split(r'\(Amended by|\(Added by|\(Repealed', t[i:i+9000])[0].strip()
        hub=f"CAGOV::{n}"; out[hub]=str(n)
        subs=[(m.group(1),m.start()) for m in re.finditer(r'\(([a-z])\)\s',body)]
        if len(subs)>=2:
            for j,(pn,ps) in enumerate(subs):
                pe=subs[j+1][1] if j+1<len(subs) else len(body)
                if pe-ps>50: out[f"{hub}.{pn}"]=body[ps:pe]
        else: out[f"{hub}.a"]=body
    return out

def led():
    t=_t(open(C+'eu_32016L0680_oj.xhtml',encoding='utf-8',errors='replace').read()); out={}
    spans=[(m.group(1),m.start()) for m in re.finditer(r'\bArticle (\d+)\b(?=\s+[A-Z])',t)]
    for i,(a,st) in enumerate(spans):
        en=spans[i+1][1] if i+1<len(spans) else min(len(t),st+9000)
        seg=t[st:en]
        if len(seg)<60: continue
        hub=f"LED::art_{a}"; out[hub]=f"Article {a}"
        subs=[(m.group(1),m.start()) for m in re.finditer(r'(?:^|\s)(\d)\.\s+[A-Z]',seg)]
        if len(subs)>=2:
            for j,(pn,ps) in enumerate(subs):
                pe=subs[j+1][1] if j+1<len(subs) else len(seg)
                if pe-ps>50: out[f"{hub}.{pn}"]=seg[ps:pe]
        else: out[f"{hub}.1"]=seg
    return out

def build():
    N={}
    N.update(eu('euc_02019R0947-20250501.html','EU947'))
    N.update(eu('euc_02019R0945-20250624.html','EU945'))
    N.update(eu('euc_02018R1139-20260802.html','EU1139'))
    N.update(eu('eu_32024R1689.html','EUAI'))
    N.update(eu('eu_32014L0032.html','MID'))      # 법정계량: 측정기기 지침 (2026-09-20 편입)
    N.update(us107()); N.update(us89()); N.update(usac())
    for f in KRDOC: N.update(kr(f))
    N.update(jp()); N.update(smc()); N.update(cagov()); N.update(led())
    drop=[k for k,v in N.items() if boiler(k,v)]
    for k in drop:
        N.pop(k,None)
        for kk in [x for x in N if x.startswith(k+'.')]: N.pop(kk,None)
    return N, len(drop)

if __name__=='__main__':
    N,d=build()
    json.dump(N,open('graph/nodes2.json','w',encoding='utf-8'),ensure_ascii=False)
    from collections import Counter
    import statistics as st
    c=Counter(k.split('::')[0] for k in N)
    print(f"{'문서':22s}{'노드':>6s}{'중앙자수':>9s}{'최대':>9s}")
    print('-'*48)
    for dd,n in c.most_common():
        L=[len(v) for k,v in N.items() if k.startswith(dd+'::')]
        print(f"{dd:22s}{n:>6}{int(st.median(L)):>9,}{max(L):>9,}")
    print('-'*48)
    print(f"{'합계':20s}{len(N):>6}   보일러플레이트 제외 {d}건")

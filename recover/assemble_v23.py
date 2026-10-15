# -*- coding: utf-8 -*-
"""복원본 조립. 2026-10-14.

v22 조판본이 유일한 증거이므로 본문은 거기서 나온 문단을 그대로 쓴다.
복원하는 것은 마크업과 플로트뿐이다. 확실하지 않은 것은 [복원 필요] 로 남긴다."""
import json,re,os,subprocess,sys
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))

P=json.load(open('recover/paras.json',encoding='utf-8'))
T=json.load(open('recover/tables.json',encoding='utf-8'))
RM=json.load(open('recover/refmap.json',encoding='utf-8'))['hit']

AUTH={}
for ent,key in RM.items():
    m=re.match(r'^(.*?),\s*(\d{4})([a-z]?)\.',ent)
    if not m: continue
    a,yr,sfx=m.groups(); first=re.split(r',|\s+and\s+',a)[0].strip()
    AUTH[(first,yr+sfx)]=key; AUTH.setdefault((first,yr),key)

UNI={'\u00a7':'\\S{}','\u2713':'\\checkmark{}','\u2715':'$\\times$','\u00d7':'$\\times$',
     '\u2212':'$-$','\u2264':'$\\le$','\u2265':'$\\ge$','\u03ba':'$\\kappa$',
     '\u00b7':'\\textperiodcentered{}','\u2192':'$\\rightarrow$','\u2217':'$*$',
     '\u2026':'\\ldots{}','\u2019':"'",'\u2018':'`','\u201c':'``','\u201d':"''",
     '\u2013':'--','\ufb01':'fi','\ufb02':'fl','\u00a0':' ',
     'u\u0304':'\\={u}','o\u0304':'\\={o}','p\u0302':'$\\hat{p}$'}
def uni(t):
    for a,b in UNI.items(): t=t.replace(a,b)
    return t

def esc(t):
    for a,b in (('&','\\&'),('%','\\%'),('#','\\#'),('$$','\\$')): t=t.replace(a,b)
    return t

PATHRX=re.compile(r'\b((?:verify|graph|corpus|probe|stpa|labels|frozen|fig2026|tex)/'
                  r'[A-Za-z0-9_./-]+|REPRODUCIBILITY\.md|RULESET_FROZEN(?:_v\d+)?\.json)')
# 인용 치환. 2026-10-14: 정규식으로 "(성, 연도)" 를 잡는 방식은 기관 저자
# ("European Parliament and Council of the European Union, 2024") 를 한 건도 못
# 잡았고, 그 결과 42건 중 11건만 참고문헌에 실렸다. 조판본의 참고문헌 42건에서
# 저자 표기를 그대로 떠서 문자열 치환한다. 추측이 없다.
_CK=json.load(open('recover/citekeys.json',encoding='utf-8'))
CTBL=[(a,b) for a,b in _CK['tbl']]
unres=[]
_BYAUTH={}
for _r in _CK['rows']: _BYAUTH[(_r['auth'],_r['year'])]=_r['key']
# 조판본은 기관 저자를 전체 표기로, 사람 저자를 성 또는 'X et al.' 로 적는다.
_ALIAS={}
for _r in _CK['rows']:
    _a=_r['auth']
    _sur=[x.strip() for x in _a.split(',') if not re.fullmatch(r'(?:[A-Z]\.)+',x.strip())]
    _v=set()
    if len(_sur)==1: _v.add(_sur[0])
    if len(_sur)==2: _v.add(f'{_sur[0]} and {_sur[1]}')
    if len(_sur)>=2: _v.add(f'{_sur[0]} et al.')
    _ALIAS[_a]=_v
    for _x in _v: _BYAUTH.setdefault((_x,_r['year']),_r['key'])
def _multi(m):
    auth=m.group(1); yrs=[m.group(2),m.group(3)]
    ks=[_BYAUTH.get((auth,y)) for y in yrs]
    if all(ks): return '\\citep{'+','.join(ks)+'}'
    return m.group(0)
def _years(tail):
    """'2022, 2021a,b, 2024, 2025' → ['2022','2021a','2021b','2024','2025']"""
    toks=[x.strip() for x in re.split(r'[,\s]+',tail) if x.strip()]
    ys=[]; last=None
    for x in toks:
        if re.fullmatch(r'\d{4}[a-z]?',x): ys.append(x); last=x[:4]
        elif re.fullmatch(r'[a-z]',x) and last: ys.append(last+x)
        else: return None
    return ys or None

def _seg(seg):
    """'ASTM International, 2022, 2021a,b' → 키 목록. 실패하면 None."""
    m=re.match(r'^\s*([A-Z][^,]*(?:,\s*[A-Z][^,]*)*?)\s*,\s*((?:\d{4}[a-z]?|[a-z])'
               r'(?:\s*,\s*(?:\d{4}[a-z]?|[a-z]))*)\s*$',seg)
    if not m:
        m=re.match(r'^\s*(.+?)\s*,\s*((?:\d{4}[a-z]?|[a-z])'
                   r'(?:\s*,\s*(?:\d{4}[a-z]?|[a-z]))*)\s*$',seg)
        if not m: return None
    auth,tail=m.group(1).strip(),m.group(2)
    ys=_years(tail)
    if not ys: return None
    ks=[_BYAUTH.get((auth,y)) for y in ys]
    if all(ks): return ks
    # 저자 표기 변형(성만, et al.)도 본다
    for a2 in _ALIAS.get(auth,()):
        ks=[_BYAUTH.get((a2,y)) for y in ys]
        if all(ks): return ks
    return None

def _paren(m):
    inner=m.group(1)
    segs=[x for x in inner.split(';')]
    keys=[]
    for sg in segs:
        k=_seg(sg)
        if not k: return m.group(0)
        keys+=k
    return '\\citep{'+','.join(keys)+'}'

def cite(t):
    # 괄호 인용 전체를 한 번에 본다. 세미콜론으로 여러 출처, 쉼표로 여러 연도가 온다.
    t=re.sub(r'\(([^()]{4,200}?)\)',_paren,t)
    for pat,rep in CTBL:
        if pat in t: t=t.replace(pat,rep)
    # 남은 "(... , 연도)" 꼴을 보고한다
    for m in re.finditer(r'\(([A-Z][^()]{2,80}?),\s*(\d{4}[a-z]?)\)',t):
        unres.append((m.group(1)[:50],m.group(2)))
    return t

SECLBL={}   # "2.7" → sec:2.7
def xref(t):
    t=re.sub(r'\bSection~?(\d+\.\d+)\b',lambda m:f'Section~\\ref{{sec:{m.group(1)}}}',t)
    t=re.sub(r'\bSection~?(\d+)\b(?!\.)',lambda m:f'Section~\\ref{{sec:{m.group(1)}}}',t)
    t=re.sub(r'\bAppendix Appendix ([AB])\b',r'Appendix \1',t)   # v22 조판 버그
    t=re.sub(r'\bAppendix~?([AB])\b',
             lambda m:'Appendix~\\ref{app:'+('changes' if m.group(1)=='A' else 'gates')+'}',t)
    t=re.sub(r'\bTables?~?(\d+)\s+and\s+(\d+)\b',
             lambda m:f'Tables~\\ref{{tab:t{m.group(1)}}} and \\ref{{tab:t{m.group(2)}}}',t)
    t=re.sub(r'\bTable~?(\d+)\b',lambda m:f'Table~\\ref{{tab:t{m.group(1)}}}',t)
    t=re.sub(r'\bFig\.~?(\d+)([a-d])?\b',
             lambda m:f'Fig.~\\ref{{fig:f{m.group(1)}}}'+(m.group(2) or ''),t)
    return t

# 경로가 아닌 식별자에도 밑줄이 있다(art_3.1, _ruleset). 조판본에서는 \texttt 로
# 찍혀 있었지만 추출에서 서체 정보가 사라졌으므로, 밑줄만 이스케이프해 수식 모드
# 오류를 막고 식별자인 것이 분명한 꼴은 \texttt 로 되돌린다.
IDENT=re.compile(r'\b((?:[a-z][a-z0-9]*_[a-z0-9_.]+|_[a-z][a-z0-9_]*))\b')
def conv(t):
    t=uni(t); t=esc(t)
    t=PATHRX.sub(lambda m:'\\texttt{'+m.group(1).replace('_','\\_')+'}',t)
    t=IDENT.sub(lambda m:'\\texttt{'+m.group(1).replace('_','\\_')+'}',t)
    t=re.sub(r'(?<!\\)_',r'\\_',t)
    return xref(cite(t))

# ── 표 ─────────────────────────────────────────────────────────────
def tabular(n):
    d=T[str(n)]; rows=[r[:] for r in d['rows']]
    cap=conv(re.sub(r'^Table \d+:\s*','',d['caption']))
    w=max(len(r) for r in rows)
    num=lambda s:bool(re.fullmatch(r'[\d,.%\[\]\s$\\a-z-]*',s))
    # 긴 글자열 열이 있으면 tabularx 의 X 로 접는다. 고정폭 tabular 로 두면 열이
    # 페이지를 넘어 잘린다(복원 1차에서 표 1 의 682/109/32 이 잘렸다).
    longest=max((max(len(r[k]) for r in rows if k<len(r)) for k in range(w)),default=0)
    wide=longest>40
    if wide:
        tc=max(range(w),key=lambda k:max((len(r[k]) for r in rows if k<len(r)),default=0))
        align='@{}'+''.join('X' if k==tc else ('l' if k==0 else 'r') for k in range(w))+'@{}'
    else:
        align='@{}l'+'r'*(w-1)+'@{}'
    body=[]
    for i,r in enumerate(rows):
        cells=[conv(c) for c in r]
        if len(cells)<w:
            cells=[f'\\multicolumn{{{w-len(cells)+1}}}{{@{{}}l}}{{{cells[0]}}}']+cells[1:]
        body.append(' & '.join(cells)+' \\\\')
        if i==0: body.append('\\midrule')
    env='tabularx' if wide else 'tabular'
    arg='{\\textwidth}'+f'{{{align}}}' if wide else f'{{{align}}}'
    return ('\\begin{table}[!htb]\n\\centering\n'
            f'\\caption{{{cap}}}\n\\label{{tab:t{n}}}\n'
            + ('\\footnotesize\n' if wide else '\\small\n') +
            f'\\begin{{{env}}}{arg}\n\\toprule\n'+'\n'.join(body)+
            f'\n\\bottomrule\n\\end{{{env}}}\n\\end{{table}}')

# B4(2026-10-15)에서 도판 4장을 측정에서 다시 그렸다. 플레이스홀더 상자를 걷는다.
# 이 자리를 .tex 에서 고치면 다음 조립에서 되돌아간다(F-13). 조립기 자체를 고쳐야 한다.
FIGSRC={1:'FigC',2:'FigM',3:'FigR',4:'FigS'}
def figure(n,cap):
    src=FIGSRC[n]
    if not os.path.exists(f'tex/{src}.pdf'):
        raise SystemExit(f'조립 중단: tex/{src}.pdf 가 없다. 도판을 먼저 생성하라.')
    return ('\\begin{figure*}[!t]\n\\centering\n'
            f'\\includegraphics[width=\\textwidth]{{{src}}}\n'
            f'\\caption{{{conv(cap)}}}\n\\label{{fig:f{n}}}\n\\end{{figure*}}')

HEAD=re.compile(r'^(?:(Abstract)|(Highlights)|(References)|Appendix ([AB])\.\s*(.*)|'
                r'(\d+)\.(?:(\d+)\.)?\s+(.*))$')
TCAP=re.compile(r'^Table (\d+):')
FCAP=re.compile(r'^Figure (\d+):')
BULLET=re.compile(r'^\u2022\s*(.*)$')
LBL={'1':'sec:1','2':'sec:2','3':'sec:3','4':'sec:4','5':'sec:5'}

bounds=[(i,m) for i,p in enumerate(P) if (m:=HEAD.match(p))]
parts={'front':[],'methods':[],'results':[],'discussion':[],'appendix':[]}
cur='front'; pend=[]
def flush(tgt):
    global pend
    if pend:
        tgt.append('\\begin{itemize}\n'+'\n'.join('\\item '+conv(x) for x in pend)+'\n\\end{itemize}')
        pend=[]

for n,(i,m) in enumerate(bounds):
    j=bounds[n+1][0] if n+1<len(bounds) else len(P)
    g=m.groups()
    if g[2]=='References': break
    if g[0]=='Abstract':
        ab=P[i][len('Abstract '):]
        parts['front'].append('%% ABSTRACT\n'+conv(ab))
        body=P[i+1:j]
    elif g[3]:
        cur='appendix'
        lbl='app:changes' if g[3]=='A' else 'app:gates'
        parts[cur].append(f'\\section{{{conv(g[4])}}}\\label{{{lbl}}}')
        body=P[i+1:j]
    else:
        a,b2,title=g[5],g[6],g[7]
        if b2 is None:
            cur={'1':'front','2':'methods','3':'results','4':'discussion','5':'discussion'}[a]
            parts[cur].append(f'\\section{{{conv(title)}}}\\label{{{LBL[a]}}}')
        else:
            parts[cur].append(f'\\subsection{{{conv(title)}}}\\label{{sec:{a}.{b2}}}')
        body=P[i+1:j]
    for p in body:
        mb=BULLET.match(p)
        if mb: pend.append(mb.group(1)); continue
        flush(parts[cur])
        mt=TCAP.match(p)
        if mt: parts[cur].append(tabular(int(mt.group(1)))); continue
        mf=FCAP.match(p)
        if mf:
            parts[cur].append(figure(int(mf.group(1)),re.sub(r'^Figure \d+:\s*','',p))); continue
        parts[cur].append(conv(p))
    flush(parts[cur])

for k,v in parts.items():
    open(f'tex/{k}_v23.tex','w',encoding='utf-8').write('\n\n'.join(v)+'\n')
    print(f'tex/{k}_v23.tex {len(v)}블록 {sum(map(len,v)):,}자')
if unres:
    from collections import Counter
    print('인용 미대응:',Counter(unres).most_common(10))

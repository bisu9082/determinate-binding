# -*- coding: utf-8 -*-
import re,html,os,sys,json,xml.etree.ElementTree as ET
sys.path.insert(0,'probe'); from lex import EVAL,AUTH,DET,NONDET
R=lambda L: re.compile("|".join(L), re.I)
rE,rA,rD,rN=R(EVAL),R(AUTH),R(DET),R(NONDET)

def flat(p):
    s=open(p,encoding='utf-8',errors='replace').read()
    s=re.sub(r'(?is)<(script|style|head)[^>]*>.*?</\1>',' ',s)
    if p.endswith(('.html','.xhtml','.xml')): s=html.unescape(re.sub(r'<[^>]+>',' ',s))
    return re.sub(r'\s+',' ',s)

def u_kr(p):
    r=ET.parse(p).getroot(); out=[]
    for a in r.findall('.//조문단위'):
        h=re.sub(r'\s+',' ',(a.findtext('조문내용') or '')).strip()
        if len(h)>15: out.append(h)
        for x in a.findall('.//항'):
            t=re.sub(r'\s+',' ',(x.findtext('항내용') or '')).strip()
            if len(t)>15: out.append(t)
    return out

def u_jp(p):
    s=open(p,encoding='utf-8',errors='replace').read()
    out=[]
    for m in re.finditer(r'<ParagraphSentence>(.*?)</ParagraphSentence>',s,re.S):
        t=re.sub(r'\s+',' ',re.sub(r'<[^>]+>','',m.group(1))).strip()
        if len(t)>15: out.append(t)
    return out or [x for x in re.split(r'(?<=。)',flat(p)) if len(x.strip())>25]

def u_en(p):
    t=flat(p)
    return [u.strip() for u in re.split(r'(?<=[.;])\s+(?=[A-Z0-9(])',t) if 40<len(u.strip())<2000]

DOCS=[
 ("US","CORE","14 CFR Part 107",        "corpus/us_14CFR107.xml",u_en),
 ("EU","CORE","2019/947 통합본",         "corpus/euc_02019R0947-20250501.html",u_en),
 ("EU","CORE","2019/945 통합본",         "corpus/euc_02019R0945-20250624.html",u_en),
 ("EU","CORE","2018/1139 통합본",        "corpus/euc_02018R1139-20260802.html",u_en),
 ("KR","CORE","도로교통법",               "corpus/kr_도로교통법.xml",u_kr),
 ("KR","CORE","도로교통법 시행규칙",       "corpus/kr_도로교통법_시행규칙.xml",u_kr),
 ("KR","CORE","지능형로봇법",             "corpus/kr_지능형로봇법.xml",u_kr),
 ("KR","CORE","지능형로봇법 시행령",       "corpus/kr_지능형로봇_개발_및_보급_촉진법_시행령.xml",u_kr),
 ("JP","CORE","道路交通法",               "corpus/jp_api_1.xml",u_jp),
 ("US","EXT","AC 00-1.1B (PAO)",        "ac.txt",u_en),
 ("US","EXT","Cal. Gov. §7070 (AB481)", "corpus/us_ca_gov7070.html",u_en),
 ("US","EXT","Cal. Gov. §7071",         "corpus/us_ca_gov7071.html",u_en),
 ("US","EXT","Cal. Gov. §7072",         "corpus/us_ca_gov7072.html",u_en),
 ("US","EXT","Cal. Gov. §7073",         "corpus/us_ca_gov7073.html",u_en),
 ("US","EXT","Seattle SMC 14.18",       "smc1418.txt",u_en),
 ("EU","EXT","LED 2016/680",            "led_official.xhtml",u_en),
 ("UK","EXT","Bridges [2020] EWCA",     "bridges.txt",u_en),
]
rows=[];detail={}
for j,sc,name,p,fn in DOCS:
    if not os.path.exists(p): rows.append((j,sc,name,0,0,0,0)); continue
    us=fn(p)
    co=[u for u in us if rE.search(u) and rA.search(u)]
    t2=[u for u in co if rD.search(u)]
    t1=[u for u in co if not rD.search(u) and rN.search(u)]
    rows.append((j,sc,name,len(us),len(co),len(t2),len(t1)))
    detail[name]=dict(t2=t2[:20],t1=t1[:20])
json.dump(dict(rows=rows,detail=detail),open('probe/result.json','w'),ensure_ascii=False,indent=1)
print(f"{'관할':4s}{'범위':6s}{'문서':26s}{'단위':>7s}{'평가+인가':>10s}{'Tier2':>7s}{'Tier1':>7s}")
print("-"*72)
for r in rows: print(f"{r[0]:4s}{r[1]:6s}{r[2]:26s}{r[3]:>7,}{r[4]:>10}{r[5]:>7}{r[6]:>7}")
for s in ("CORE","EXT"):
    g=[r for r in rows if r[1]==s]
    print(f"\n[{s}] 문서 {len(g)} · 단위 {sum(r[3] for r in g):,} · 평가+인가 {sum(r[4] for r in g)} · Tier2 {sum(r[5] for r in g)} · Tier1 {sum(r[6] for r in g)}")
a=[r for r in rows if r[1]=="CORE"]; b=rows
print(f"\nA안(CORE만)      : 단위 {sum(r[3] for r in a):,} · Tier2 {sum(r[5] for r in a)} · Tier1 {sum(r[6] for r in a)} · 관할 {len({r[0] for r in a})}")
print(f"B안(CORE+EXT)    : 단위 {sum(r[3] for r in b):,} · Tier2 {sum(r[5] for r in b)} · Tier1 {sum(r[6] for r in b)} · 관할 {len({r[0] for r in b})}")

# -*- coding: utf-8 -*-
"""Methods(v8) 본문에 적힌 모든 수치를 원자료와 대조한다. [C-3]"""
import json,re,sys,collections,subprocess,hashlib
sys.path.insert(0,'stpa'); sys.path.insert(0,'probe')
T=open('tex/methods_v8.tex',encoding='utf-8').read()
def has(pat):
    return bool(re.search(pat,T))
N=json.load(open('graph/nodes3.json',encoding='utf-8'))
E=[tuple(e) for e in json.load(open('graph/edges3.json',encoding='utf-8'))]
EC=collections.Counter(k for _,_,k in E)
NC=collections.Counter(k.split('::')[0] for k in N)
from structure import LOSSES,HAZARDS,MISSIONS
from uca_mg import UCA as U1
from uca_ma import UCA as U2
from scenarios import SCEN
from accountability import ELEMENTS
ADJ=json.load(open('frozen/ADJUDICATION.json',encoding='utf-8'))
RS=json.load(open('frozen/RULESET_FROZEN.json',encoding='utf-8'))
MAN=json.load(open('corpus/MANIFEST.json',encoding='utf-8'))
ing=[e for e in MAN if e.get('in_graph')]
P=json.load(open('graph/paths3.json',encoding='utf-8'))
tier=collections.Counter(v['tier'] for v in P.values())
term=subprocess.run([sys.executable,'stpa/termproc.py'],capture_output=True,text=True).stdout
cov=subprocess.run([sys.executable,'stpa/coverage.py'],capture_output=True,text=True).stdout
car=subprocess.run([sys.executable,'stpa/carveout.py'],capture_output=True,text=True).stdout
hop=subprocess.run([sys.executable,'graph/paths3.py'],capture_output=True,text=True).stdout
old=json.load(open('graph/nodes.json',encoding='utf-8'))

CK=[]
def c(label, claim, actual):
    CK.append((label, claim, actual, claim==actual))

c('손실 L1-L6', 6, len(LOSSES))
c('위험 H1-H7', 7, len(HAZARDS))
c('제어행위 합계 18', 18, sum(len(m['control_actions']) for m in MISSIONS))
c('  M-G 11', 11, len(MISSIONS[0]['control_actions']))
c('  M-A 7', 7, len(MISSIONS[1]['control_actions']))
c('안전제약 44', 44, len(U1)+len(U2))
c('  M-G 30', 30, len(U1)); c('  M-A 14', 14, len(U2))
c('인과제약 12', 12, len(SCEN))
c('책무성 7', 7, len(ELEMENTS))
c('총 제약 63', 63, len(U1)+len(U2)+len(SCEN)+len(ELEMENTS))
c('판정대상 51', 51, len(U1)+len(U2)+len(ELEMENTS))
c('코퍼스 기관 14', 14, len({e['doc_id'] for e in ing}))
c('코퍼스 파일 19', 19, len(ing))
c('코퍼스 바이트 12,777,351', 12777351, sum(e['bytes'] for e in ing))
c('노드 5,190', 5190, len(N))
c('엣지 7,873', 7873, len(E))
c('포함엣지 3,831', 3831, EC['contain'])
c('장포함 320', 320, EC['cpt_contain'])
c('번호참조 2,536', 2536, sum(EC[k] for k in ('eu_in','jp_in','kr_in','us_in','smc_in','ca_in','ac_in')))
c('기관간참조 36', 36, EC['eu_xdoc']+EC['kr_xdoc'])
c('구조참조 709', 709, EC['struct_ref'])
c('시행령→모법 187', 187, EC['kr_parent'])
c('부속서 151', 151, EC['eu_annex'])
c('역위임 103', 103, EC['kr_deleg'])
c('art_141 114,362자', 114362, len(old.get('EU1139::art_141','')))
c('인가항 856', 856, len(P))
c('Tier2 58', 58, tier[2]); c('Tier1 443', 443, tier[1]); c('Tier0 355', 355, tier[0])
c('AP 배제 1,065', 1065, int(re.search(r'AP 배제 (\d+)',car).group(1)))
c('AP 잔존 4,125', 4125, int(re.search(r'AP 잔존 (\d+)',car).group(1)))
d=eval(re.search(r'배제 내역: (\{.*\})',car).group(1))
c('  EU1139 649', 649, d['EU1139']); c('  EU945 193', 193, d['EU945']); c('  EU947 99', 99, d['EU947'])
c('  US107 소계 124', 124, d['US107'])
c('  Subpart C 68', 68, int(re.search(r'CFR-C\s+(\d+)노드',car).group(1)))
c('  Subpart D 56', 56, int(re.search(r'CFR-D\s+(\d+)노드',car).group(1)))
tot,t1,t2=re.search(r'합계\s+(\d+)\s+(\d+)\s+(\d+)',term).groups()
c('패턴 154', 154, int(tot)); c('T1유래 68', 68, int(t1)); c('T2인간 86', 86, int(t2))
c('기계 44%', 44, round(int(t1)/int(tot)*100)); c('인간 56%', 56, round(int(t2)/int(tot)*100))
c('구성타당도 22/22', 22, int(re.search(r'재현한 것 (\d+)/22',cov).group(1)))
c('매핑 60', 60, int(re.search(r'매핑된 제약 (\d+)건',cov).group(1)))
c('신규 3', 3, int(re.search(r'매핑 안 된 제약 (\d+)건',cov).group(1)))
c('신규 목록', "['AC-3', 'AC-6', 'SCA-02-2']", re.search(r"신규.*?: (\[.*?\])",cov).group(1))
c('동결 파일 19', 19, len(RS['files']))
c('ruleset 해시 앞 8', 'ff76f822', RS['ruleset_sha256'][:8])
c('ruleset 해시 뒤 5', '5f8681', RS['ruleset_sha256'][-6:])
# hop 표
for lab,exp in [('엣지0 (조문 고립)',(47,224,585)),('hop=1',(49,284,523)),('hop=2',(55,387,414)),
                ('hop=3',(56,407,393)),('hop=4',(58,443,355)),('hop=5',(59,448,349)),
                ('hop=4 · 구조참조 제외',(57,441,358))]:
    m=re.search(re.escape(lab)+r'\s+856\s+(\d+)\s+(\d+)\s+(\d+)',hop)
    c('표2 '+lab, exp, tuple(int(x) for x in m.groups()))
ok=sum(1 for x in CK if x[3]); ng=len(CK)-ok
print(f"Methods 수치 검증: ✔ {ok} / ✘ {ng}  (총 {len(CK)})")
for lab,cl,ac,good in CK:
    if not good: print(f"  ✘ {lab}: 본문 {cl} vs 실제 {ac}")
print()
for lab,cl,ac,good in CK:
    if good: print(f"  ✔ {lab:28s} {ac}")

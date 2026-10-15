# -*- coding: utf-8 -*-
"""Discussion(v8) + Results 민감도 문단의 수치 대조. [C-3]"""
import json,re,sys,subprocess,collections
sys.path.insert(0,'stpa'); sys.path.insert(0,'graph')
A=json.load(open('frozen/ADJUDICATION.json',encoding='utf-8'))
P=json.load(open('graph/paths3.json',encoding='utf-8'))
N=json.load(open('graph/nodes3.json',encoding='utf-8'))
CK=[]
def c(l,claim,act): CK.append((l,claim,act,claim==act))
tier=collections.Counter(v['tier'] for v in P.values())
byd=collections.defaultdict(collections.Counter)
for k,v in P.items(): byd[k.split('::')[0]][v['tier']]+=1
c('인가항 856',856,len(P)); c('Tier2 58',58,tier[2])
c('항공 Tier2 44',44,sum(byd[d][2] for d in ('EU1139','EU947','EU945','US107')))
c('SC-09-1 인가항 16',16,[r for r in A['M-G'] if r['sc']=='SC-09-1'][0]['auth'])
c('SC-09-1 Tier2 0',0,[r for r in A['M-G'] if r['sc']=='SC-09-1'][0]['t2'])
# 민감도
o=subprocess.run([sys.executable,'verify/sens_nondet.py'],capture_output=True,text=True).stdout
c('민감도 변동 5건',5,int(re.search(r'판정 변동: (\d+)건',o).group(1)))
c('민감도 SC-09-1 불변','영점',re.search(r'캡 제거 시 (\S+)',o).group(1))
# 상한 72
sys.path.insert(0,'probe')
import re as _re
from collections import defaultdict,deque
from lex2 import EVAL,AUTH,DET,NONDET,PENALTY,DET_EXCLUDE
R=lambda L:_re.compile("|".join(L),_re.I)
rE,rA,rD,rN,rP,rX=R(EVAL),R(AUTH),R(DET),R(NONDET),R(PENALTY),R(DET_EXCLUDE)
E=[tuple(e) for e in json.load(open('graph/edges3.json',encoding='utf-8'))]
L={k:{'e':bool(rE.search(v)),'a':bool(rA.search(v)),'d':bool(rD.search(v)) and not rX.search(v),
      'n':bool(rN.search(v)),'p':bool(rP.search(v))} for k,v in N.items()}
ADJ=defaultdict(set)
for a,b,_ in E: ADJ[a].add(b)
def t2n(s,hop=4):
    l=L[s]
    if not l['d']: return False
    if l['e']: return True
    q=deque([(s,0)]); seen={s}
    while q:
        cu,d=q.popleft()
        if L[cu]['e']: return True
        if d>=hop: continue
        for nx in ADJ.get(cu,()):
            if nx not in seen and nx in L: seen.add(nx); q.append((nx,d+1))
    return False
st=[k for k,l in L.items() if l['a'] and not l['p'] and '.' in k.split('::')[1]]
up=sum(1 for k in st if P[k]['tier']<2 and t2n(k))
c('캡 제거 상한 Tier2 72',72,tier[2]+up)
# AI Act 조문 문언
c('Art5(2) only if 문언',True,'authorised only if' in N['EUAI::art_5.2'])
c('Art5(2) FRIA 참조',True,'fundamental rights impact assessment as provided for in Article 27' in N['EUAI::art_5.2'])
c('Art5(3) 사전 사법승인',True,'prior authorisation granted by a judicial authority or an independent administrative authority' in N['EUAI::art_5.3'])
c('Art27(1) 6개 항목',True, all(x in N['EUAI::art_27.1'] for x in
  ["description of the deployer","period of time within which","categories of natural persons",
   "specific risks of harm","human oversight measures","internal governance and complaint mechanisms"]))
c('Art27 성능요건 부재',False, bool(_re.search(r'accuracy|performance', N['EUAI::art_27.1'], _re.I)))
# 패턴 154/86
tm=subprocess.run([sys.executable,'stpa/termproc.py'],capture_output=True,text=True).stdout
tot,t1,t2=_re.search(r'합계\s+(\d+)\s+(\d+)\s+(\d+)',tm).groups()
c('패턴 154',154,int(tot)); c('인간추가 86',86,int(t2))
# 인과제약 중 조작자역량 2건
from scenarios import SCEN
c('인과제약 12',12,len(SCEN))
txt={x[4].split(':')[0]:x[4].split(':',1)[1] for x in SCEN}
c('CC-05-1 조작자역량/열화조건',True,
  'Operator qualification must be demonstrated against the degraded conditions' in txt['CC-05-1'])
c('CC-05-2 보호장비 착용 조작성',True,
  'actuatable in the protective equipment prescribed for that zone' in txt['CC-05-2'])
# MOTIE 고시 원문 대조 (hwp/notice.txt)
try:
    nt=open('hwp/notice.txt',encoding='utf-8',errors='replace').read()
    arts=_re.findall(r'제(\d+)조\(',nt)
    c('MOTIE 고시 16개 조',16,max(int(x) for x in arts))
    c('MOTIE 별표 4개',4,len(set(_re.findall(r'\[별표\s*(\d+)\]',nt))))
    c('MOTIE 조작자 자격 어휘 0',0,sum(nt.count(w) for w in ('운전자','조작자','운영자','자격','교육','숙련','면허','종사자')))
    c('MOTIE 인증기관 명시',True,'인증기관' in nt)
    c('MOTIE 처리기간 고정',True,'처리기간' in nt)
    c('MOTIE 이의신청 절차',True,'이의신청' in nt)
except FileNotFoundError:
    print('  [확인 불가] hwp/notice.txt 없음')
ok=sum(1 for x in CK if x[3])
print(f"Discussion 수치 검증: ✔ {ok} / ✘ {len(CK)-ok}  (총 {len(CK)})")
for l,cl,ac,g in CK:
    if not g: print(f"  ✘ {l}: 본문 {cl} vs 실제 {ac}")

# -*- coding: utf-8 -*-
"""Abstract/Introduction/§2 및 Highlights·Cover letter 수치 대조. [C-3]"""
import json,re,sys,collections,subprocess
sys.path.insert(0,'stpa'); sys.path.insert(0,'graph')
A=json.load(open('frozen/ADJUDICATION.json',encoding='utf-8'))
P=json.load(open('graph/paths3.json',encoding='utf-8'))
N=json.load(open('graph/nodes3.json',encoding='utf-8'))
E=json.load(open('graph/edges3.json',encoding='utf-8'))
MAN=json.load(open('corpus/MANIFEST.json',encoding='utf-8'))
CK=[]
def c(l,claim,act): CK.append((l,claim,act,claim==act))
tier=collections.Counter(v['tier'] for v in P.values())
from uca_mg import UCA as UG
from uca_ma import UCA as UA
from scenarios import SCEN
from accountability import ELEMENTS
c('제약 63',63,len(UG)+len(UA)+len(SCEN)+len(ELEMENTS))
c('안전제약 44',44,len(UG)+len(UA)); c('인과 12',12,len(SCEN)); c('책무성 7',7,len(ELEMENTS))
ing=[e for e in MAN if e.get('in_graph')]
c('기관 14',14,len({e['doc_id'] for e in ing}))
juris={e['jurisdiction'] for e in ing}
c('국가관할 4',4,len({j for j in juris if '-' not in j}))
c('하위관할 2',2,len({j for j in juris if '-' in j}))
c('노드 5,190',5190,len(N)); c('엣지 7,873',7873,len(E))
c('인가항 856',856,len(P)); c('Tier2 58',58,tier[2])
import paths3 as PM
iso=PM.run([],4); full=PM.run(PM.E,4)
c('격리 판독이 놓치는 Tier2 11',11,len([k for k in full if full[k][0]==2 and iso[k][0]<2]))
cls=collections.Counter(r['cls'] for r in A['M-G'])
c('M-G 30',30,sum(cls.values())); c('M-G 미결속 29',29,30-cls['확정 결속'])
c('M-A 14',14,len(A['M-A']))
c('M-A AC 확정 1',1,sum(1 for x in A['M-A'] if x['AC']['t2']>0))
c('M-A AP 확정 0',0,sum(1 for x in A['M-A'] if x['AP']['t2']>0))
o=subprocess.run([sys.executable,'verify/sens_nondet.py'],capture_output=True,text=True).stdout
c('민감도 SC-09-1 불변','영점',re.search(r'캡 제거 시 (\S+)',o).group(1))
# 본문 문자열 존재 검사
f=open('tex/front_v8.tex',encoding='utf-8').read()
for t in ['5,190 provision nodes','7,873 cross-reference edges','856 authorising provisions',
          '58 are determinate bindings','misses 11 of them','29 are unbound',
          'one is bound on the civil route and none on the police route','to 72']:
    c('초록 문구: '+t[:34],True,t in f)
h=open('tex/highlights.tex',encoding='utf-8').read()
c('Highlights 29/30',True,'29 are unbound' in h)
c('Highlights 16개 조문',True,'Sixteen provisions' in h)
cl=open('tex/cover_letter.tex',encoding='utf-8').read()
c('커버레터 11 of the 58',True,'11 of the 58' in cl)
c('커버레터 58 to 72',True,'from 58 to 72' in cl)
ok=sum(1 for x in CK if x[3])
print(f"Front 수치 검증: ✔ {ok} / ✘ {len(CK)-ok}  (총 {len(CK)})")
for l,cl_,ac,g in CK:
    if not g: print(f"  ✘ {l}: 본문 {cl_} vs 실제 {ac}")

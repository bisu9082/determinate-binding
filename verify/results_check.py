# -*- coding: utf-8 -*-
"""Results(v8) 본문 수치 전수 대조. [C-3]"""
import json,re,sys,collections,subprocess
sys.path.insert(0,'stpa'); sys.path.insert(0,'graph'); sys.path.insert(0,'probe')
A=json.load(open('frozen/ADJUDICATION.json',encoding='utf-8'))
P=json.load(open('graph/paths3.json',encoding='utf-8'))
G={r['sc']:r for r in A['M-G']}; MA={r['sc']:r for r in A['M-A']}; AC={r['sc']:r for r in A['AC']}
CK=[]
def c(l,claim,act): CK.append((l,claim,act,claim==act))
cls=collections.Counter(r['cls'] for r in A['M-G'])
c('M-G 개념 부재 12',12,cls['개념 부재']); c('M-G 인가조항 아님 6',6,cls['인가조항 아님'])
c('M-G 영점 11',11,cls['영점']); c('M-G 확정 결속 1',1,cls['확정 결속'])
for sc,exp in [('SC-09-1',(22,16,16,0)),('SC-02-2',(52,17,14,0)),('SC-09-2',(46,15,8,0)),('SC-08-3',(65,14,6,0))]:
    r=G[sc]; c(sc,exp,(r['hits'],r['auth'],r['t1'],r['t2']))
c('SC-09-4 결속처','KR지능형로봇법::40의2.3',G['SC-09-4']['ex'][0])
tier=collections.Counter(v['tier'] for v in P.values())
c('인가항 856',856,len(P)); c('Tier2 58',58,tier[2]); c('Tier1 443',443,tier[1]); c('Tier0 355',355,tier[0])
import paths3 as PM
iso=PM.run([],4); full=PM.run(PM.E,4)
i2=sum(1 for v in iso.values() if v[0]==2); i1=sum(1 for v in iso.values() if v[0]==1)
only2=[k for k in full if full[k][0]==2 and iso[k][0]<2]
c('격리 Tier2 47',47,i2); c('격리 Tier1 224',224,i1)
c('경로로만 Tier2 11',11,len(only2))
c('Tier1 증가 219',219,tier[1]-i1)
c('경로 비중 19%',19,round(len(only2)/tier[2]*100))
c('Tier>=1 신규비중 46%',46,round((tier[2]+tier[1]-i2-i1)/(tier[2]+tier[1])*100))
c('사라진 Tier2 0',0,sum(1 for k in full if full[k][0]<2 and iso[k][0]==2))
hd=collections.Counter(len(full[k][1])-1 for k in only2)
c('홉수 1:2',2,hd[1]); c('홉수 2:6',6,hd[2]); c('홉수 3:1',1,hd[3]); c('홉수 4:2',2,hd[4])
byd=collections.defaultdict(collections.Counter)
for k,v in P.items(): byd[k.split('::')[0]][v['tier']]+=1
T={d:(sum(byd[d].values()),byd[d][2],byd[d][1],byd[d][0]) for d in byd}
for d,exp in [('JP道交法',(348,4,162,182)),('EU1139',(109,32,67,10)),('EUAI',(99,2,56,41)),
              ('KR도로교통법시행규칙',(69,2,39,28)),('KR도로교통법',(67,3,32,32)),('EU947',(40,3,29,8)),
              ('US107',(34,8,10,16)),('EU945',(33,1,25,7)),('KR지능형로봇법',(14,3,7,4)),
              ('LED',(14,0,2,12)),('SMC1418',(9,0,3,6)),('KR지능형로봇법시행령',(8,0,6,2)),
              ('CAGOV',(7,0,2,5)),('USAC',(5,0,3,2))]:
    c('표3 '+d,exp,T[d])
c('항공 Tier2 44',44,T['EU1139'][1]+T['EU947'][1]+T['EU945'][1]+T['US107'][1])
c('경찰기기 인가항 16',16,T['SMC1418'][0]+T['CAGOV'][0])
c('경찰기기 Tier2 0',0,T['SMC1418'][1]+T['CAGOV'][1])
r=MA['SCA-03-1']; c('SCA-03-1 AC',(19,7,5),(r['AC']['hits'],r['AC']['auth'],r['AC']['t2']))
c('SCA-03-1 AP 매칭 0',0,r['AP']['hits'])
d=collections.Counter(x['delta'] for x in A['M-A'])
c('규범 소멸 6',6,d['규범 소멸']); c('결속 상실 1',1,d['결속 상실'])
c('불변 4',4,d['불변']); c('양쪽 부재 3',3,d['양쪽 개념 부재']); c('역전 0',0,d['역전'])
c('AC 경로 확정결속 1건',1,sum(1 for x in A['M-A'] if x['AC']['t2']>0))
c('AP 경로 확정결속 0건',0,sum(1 for x in A['M-A'] if x['AP']['t2']>0))
r=MA['SCA-01-1']; c('SCA-01-1 AP 매칭2 인가0',(2,0),(r['AP']['hits'],r['AP']['auth']))
for k,exp in [('AC-2',(33,2)),('AC-3',(50,5)),('AC-4',(23,2)),('AC-5',(3,2)),('AC-7',(38,7)),
              ('AC-1',(10,0)),('AC-6',(19,0))]:
    r=AC[k]
    c('책무성 '+k,exp,((r['auth'],r['t2']) if k in ('AC-2','AC-3','AC-4') else
                     ((r['hits'],r['auth']) if k in ('AC-5','AC-1','AC-6') else (r['hits'],r['auth']))))
c('AC-7 매칭38 인가7',(38,7),(AC['AC-7']['hits'],AC['AC-7']['auth']))
nos=PM.run([e for e in PM.E if e[2] not in ('struct_ref','cpt_contain')],4)
c('구조엣지 제거 Tier2 57',57,sum(1 for v in nos.values() if v[0]==2))
cov=subprocess.run([sys.executable,'stpa/coverage.py'],capture_output=True,text=True).stdout
c('구성타당도 22',22,int(re.search(r'재현한 것 (\d+)/22',cov).group(1)))
c('매핑 60',60,int(re.search(r'매핑된 제약 (\d+)건',cov).group(1)))
c('신규 3',3,int(re.search(r'매핑 안 된 제약 (\d+)건',cov).group(1)))
c('AP 삭제 1,065',1065,5190-len(__import__('carveout').ap_nodes()[0]))
ok=sum(1 for x in CK if x[3])
print(f"Results 수치 검증: ✔ {ok} / ✘ {len(CK)-ok}  (총 {len(CK)})")
for l,cl,ac,g in CK:
    if not g: print(f"  ✘ {l}: 본문 {cl} vs 실제 {ac}")

# -*- coding: utf-8 -*-
"""main_v10 본문 수치 전수 대조. [C-3]"""
import json,re,sys,collections,subprocess,math
sys.path.insert(0,'stpa'); sys.path.insert(0,'graph'); sys.path.insert(0,'probe')
from scope import DOMAIN
import paths3 as P
from carveout import ap_nodes, EXCLUSIONS
N=P.N; E=P.E
MAN=json.load(open('corpus/MANIFEST.json',encoding='utf-8'))
ing=[e for e in MAN if e.get('in_graph')]
CK=[]
def c(l,claim,act): CK.append((l,claim,act,claim==act))
full=P.run(E,4); iso=P.run([],4)
t=collections.Counter(v[0] for v in full.values()); i=collections.Counter(v[0] for v in iso.values())
c('인가항 1,016',1016,len(full)); c('T2 78',78,t[2]); c('T1 504',504,t[1]); c('T0 434',434,t[0])
c('T2 비율 7.7%',7.7,round(t[2]/len(full)*100,1))
c('격리 T2 59',59,i[2]); c('격리 T1 265',265,i[1])
only=[k for k in full if full[k][0]==2 and iso[k][0]<2]
c('경로로만 19',19,len(only)); c('경로 비중 24.4%',24.4,round(len(only)/t[2]*100,1))
c('T1 증가 239',239,t[1]-i[1]); c('소실 0',0,sum(1 for k in full if full[k][0]<2 and iso[k][0]==2))
c('tier>=1 신규 44%',44.3,round(((t[2]+t[1])-(i[2]+i[1]))/(t[2]+t[1])*100,1))
tot=collections.Counter(); d2=collections.Counter()
for k,v in full.items():
    dm=DOMAIN[k.split('::')[0]]; tot[dm]+=1
    if v[0]==2: d2[dm]+=1
c('항공 241/46',(241,46),(tot['aviation'],d2['aviation']))
c('지상 614/29',(614,29),(tot['ground'],d2['ground']))
c('횡단 161/3',(161,3),(tot['crosscut'],d2['crosscut']))
c('항공 19.1%',19.1,round(d2['aviation']/tot['aviation']*100,1))
c('지상 4.7%',4.7,round(d2['ground']/tot['ground']*100,1))
c('횡단 1.9%',1.9,round(d2['crosscut']/tot['crosscut']*100,1))
pa,pg=d2['aviation']/tot['aviation'],d2['ground']/tot['ground']
c('비율 4.04',4.04,round(pa/pg,2))
h=abs(2*math.asin(math.sqrt(pa))-2*math.asin(math.sqrt(pg)))
c("Cohen's h 0.466",0.466,round(h,3))
g=[k for k,v in full.items() if v[0]==2 and DOMAIN[k.split('::')[0]]=='ground']
gc=collections.Counter(k.split('::')[0] for k in g)
c('지상 중 도로교통 26',26,gc['JP道交法']+gc['KR도로교통법']+gc['KR도로교통법시행규칙'])
c('지상 중 지능형로봇법 3',3,gc['KR지능형로봇법'])
c('LED 인가항 14 T2 0',(14,0),(sum(1 for k in full if k.startswith('LED')),sum(1 for k,v in full.items() if k.startswith('LED') and v[0]==2)))
c('경찰장비 16 T2 0',(16,0),(sum(1 for k in full if k.split('::')[0] in ('SMC1418','CAGOV')),
                            sum(1 for k,v in full.items() if k.split('::')[0] in ('SMC1418','CAGOV') and v[0]==2)))
apset,drop=ap_nodes()
apf=P.run([e for e in E if e[0] in apset and e[1] in apset],4)
apf={k:v for k,v in apf.items() if k in apset}
av_ac=[k for k,v in full.items() if v[0]==2 and DOMAIN[k.split('::')[0]]=='aviation']
av_ap=[k for k,v in apf.items() if v[0]==2 and DOMAIN[k.split('::')[0]]=='aviation']
c('민간 46',46,len(av_ac)); c('경찰 2',2,len(av_ap))
c('96% 제거',96,round((1-len(av_ap)/len(av_ac))*100))
c('생존 2건',['US89::89.310.g','US89::89.320.g'],sorted(av_ap))
c('면제 삭제 1,065',1065,len(drop))
c('Part89 삭제 0',0,sum(1 for k in drop if k.startswith('US89')))
c('기관 16',16,len({e['doc_id'] for e in ing})); c('파일 21',21,len(ing))
c('바이트 14,276,114',14276114,sum(e['bytes'] for e in ing))
c('노드 5,548',5548,len(N)); c('엣지 8,554',8554,len(E))
ec=collections.Counter(k for _,_,k in E)
c('포함 4,087',4087,ec['contain']); c('장포함 374',374,ec['cpt_contain'])
c('번호참조 2,647',2647,sum(ec[k] for k in ('eu_in','jp_in','kr_in','us_in','smc_in','ca_in','ac_in')))
c('기관간 36',36,ec['eu_xdoc']+ec['kr_xdoc']); c('구조참조 940',940,ec['struct_ref'])
c('모법 187',187,ec['kr_parent']); c('부속서 180',180,ec['eu_annex']); c('역위임 103',103,ec['kr_deleg'])
for lab,hp,exp in [('hop0',0,(59,265,692)),('hop1',1,(61,338,617)),('hop2',2,(71,444,501)),
                   ('hop3',3,(73,466,477)),('hop4',4,(78,504,434)),('hop5',5,(79,511,426))]:
    r=P.run([] if hp==0 else E, hp if hp else 4); cc=collections.Counter(v[0] for v in r.values())
    c('표2 '+lab,exp,(cc[2],cc[1],cc[0]))
ns=P.run([e for e in E if e[2] not in ('struct_ref','cpt_contain')],4)
cc=collections.Counter(v[0] for v in ns.values()); c('표2 구조제외',(76,502,438),(cc[2],cc[1],cc[0]))
d=dict(collections.Counter(k.split('::')[0] for k in drop))
c('면제 내역',{'EU1139':649,'EU945':193,'EU947':99,'US107':124},d)
o=subprocess.run([sys.executable,'verify/lex_validation.py'],capture_output=True,text=True).stdout
c('위음성 11.1%',True,'11.1%' in o); c('CI [4.4, 25.3]',True,'[ 4.4,  25.3]' in o)
o2=subprocess.run([sys.executable,'verify/holdout_check.py'],capture_output=True,text=True).stdout
c('보류 5/12',True,'일치 5/12' in o2); c('κ 0.192',True,'0.192' in o2)
ok=sum(1 for x in CK if x[3])
print(f"main_v10 수치 검증: ✔ {ok} / ✘ {len(CK)-ok}  (총 {len(CK)})")
for l,cl,ac,g_ in CK:
    if not g_: print(f"  ✘ {l}: 본문 {cl} vs 실제 {ac}")

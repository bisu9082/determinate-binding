# -*- coding: utf-8 -*-
"""B5-a 재번호용 파생 계산. 추정기는 먼저 구판 수치로 대조(control)한 뒤에만 신판에 쓴다."""
import json,math,os
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
from scipy import stats
M=json.load(open('verify/fig_measures.json',encoding='utf-8'))

def wilson(k,n,z=1.96):
    if n==0: return (0.0,0.0)
    p=k/n; d=1+z*z/n; c=(p+z*z/(2*n))/d
    m=z/d*math.sqrt(p*(1-p)/n+z*z/(4*n*n))
    return (max(0.0,c-m),min(1.0,c+m))

def fisher(a,b,c,d):
    o,p=stats.fisher_exact([[a,b],[c,d]])
    return o,p

print('='*64)
print('추정기 대조 — 구판 라벨(34)로 공개 수치를 재현하는가')
print('='*64)
lo,hi=wilson(34,91); print(f'  Wilson(34/91)  = [{lo:.3f}, {hi:.3f}]   공개 [0.281, 0.476]  {"OK" if (round(lo,3),round(hi,3))==(0.281,0.476) else "불일치"}')
lo,hi=wilson(23,241); print(f'  Wilson(23/241) = [{lo*100:.1f}, {hi*100:.1f}]   공개 [6.4, 13.9]    {"OK" if (round(lo*100,1),round(hi*100,1))==(6.4,13.9) else "불일치"}')
o,p=fisher(23,241-23,9,574-9); print(f'  Fisher 항공vs도로 p={p:.2e} OR={o:.2f}   공개 p=5.5e-07 OR=6.6  {"OK" if abs(p-5.5e-7)<6e-8 and abs(o-6.6)<0.1 else "불일치"}')
o2,p2=fisher(23,241-23,0,139); print(f'  Fisher 항공vs수평 p={p2:.2e}            공개 p=2.3e-05        {"OK" if abs(p2-2.3e-5)<3e-6 else "불일치"}')
print(f'  비율비 9.5/1.8 = {(23/241)/(11/604):.2f}            공개 5.24           {"OK" if abs((23/241)/(11/604)-5.24)<0.01 else "불일치"}')
cav=241*0.500; print(f'  보정 항공률 23/{cav:.1f} = {23/cav*100:.1f}%        공개 19.2%          {"OK" if abs(23/cav*100-19.2)<0.1 else "불일치"}')
plo,phi=wilson(12,24); print(f'  보정구간 [{23/(241*phi)*100:.1f}, {23/(241*plo)*100:.1f}]       공개 [13.9, 30.4]   {"OK" if (round(23/(241*phi)*100,1),round(23/(241*plo)*100,1))==(13.9,30.4) else "불일치"}')

print()
print('  * 보정률 추정기 확정: 분모를 먼저 정수로 반올림한 뒤 나눈다 (23/120=19.2, 23/120.5=19.1)')
print()
print('='*64)
print('신판(결속 41) 파생값')
print('='*64)
S={s['subject']:s for s in M['by_subject']}; D={d['domain']:d for d in M['by_domain']}
H=M['by_hop']; CO=M['carveout']
AV=S['Aviation certification']; GR=D['ground']; RT=S['Road traffic, drivers']
RB=S['Robot certification']; HZ=S['Horizontal product law']
print('[표 2] hop별 감사')
for key,lab in [('no_edges','간선 없음'),('hop1','hop<=1'),('hop2','hop<=2'),('hop3','hop<=3'),('hop4','hop<=4 (채택)')]:
    h=H[key]; print(f'  {lab:14s} 결속 {h["audited"]:3d}  위양성 {h["returned"]-h["audited"]:3d}  반환 {h["returned"]:3d}  정밀도 {h["audited"]/h["returned"]:.3f}')
lo,hi=wilson(H['hop4']['audited'],H['hop4']['returned'])
print(f'  정밀도 Wilson = [{lo:.3f}, {hi:.3f}]   (구판 [0.281, 0.476])')
print()
print('[표 9] 주제별')
for nm,s in [('항공 인증 (6)',AV),('로봇 인증 (2)',RB),('도로교통·운전자 (3)',RT),('경찰 직무 (3)',S['Police conduct']),('수평 제품법 (2)',HZ)]:
    lo,hi=wilson(s['audited'],s['auth'])
    print(f'  {nm:18s} 인가 {s["auth"]:4d}  결속 {s["audited"]:2d}  {s["audited"]/s["auth"]*100:5.1f}%  Wilson [{lo*100:.1f}, {hi*100:.1f}]')
print()
print('[표 10] 도메인별')
for nm,d in [('항공 (6)',D['aviation']),('지상 (5)',GR),('교차 (5)',D['crosscut'])]:
    print(f'  {nm:10s} 인가 {d["auth"]:4d}  반환 {d["returned"]:2d}  결속 {d["audited"]:2d}  {d["audited"]/d["auth"]*100:5.1f}%  정밀도 {d["audited"]/d["returned"] if d["returned"] else 0:.3f}')
print(f'  {"합계":10s} 인가 1014  반환 {H["hop4"]["returned"]}  결속 {H["hop4"]["audited"]}  {H["hop4"]["audited"]/1014*100:.1f}%  정밀도 {H["hop4"]["precision"]:.3f}')
print()
print('[표 4] 분모 보정 (분모감사 0.494 등은 공개값 그대로 승계 — 라벨셋 소실)')
rows=[('항공',AV['audited'],241,12,24),('지상',GR['audited'],604,22,40),('교차',0,169,5,15),('합계',H['hop4']['audited'],1014,39,79)]
for nm,b,n,dk,dn in rows:
    pr=dk/dn; corr=round(n*pr); rate=b/corr*100 if corr else 0
    plo,phi=wilson(dk,dn)
    ci=f'[{b/(n*phi)*100:.1f}, {b/(n*plo)*100:.1f}]' if b else ''
    print(f'  {nm:5s} 결속 {b:2d}  인가 {n:5d}  명목 {b/n*100:4.1f}%  분모정밀도 {dk}/{dn}={pr:.3f}  보정인가 {corr:4d}  보정률 {rate:4.1f}% {ci}')
print()
rat=(AV['audited']/241)/(GR['audited']/604)
cav=round(241*0.5); cgr=round(604*0.55)
print(f'  비율비 명목 {rat:.2f}  (구판 5.24)')
print(f'  비율비 보정 {(AV["audited"]/cav)/(GR["audited"]/cgr):.2f}  (구판 5.8)')
print()
print('[Fisher]')
o,p=fisher(AV['audited'],241-AV['audited'],RT['audited'],574-RT['audited'])
print(f'  항공 {AV["audited"]}/241 vs 도로 {RT["audited"]}/574 : p={p:.2e}  OR={o:.2f}   (구판 p=5.5e-07 OR=6.6)')
o,p=fisher(AV['audited'],241-AV['audited'],0,139)
print(f'  항공 vs 수평 0/139 : p={p:.2e}                  (구판 p=2.3e-05)')
o,p=fisher(AV['audited'],241-AV['audited'],D['crosscut']['audited'],169-D['crosscut']['audited'])
print(f'  항공 vs 교차 풀링 {D["crosscut"]["audited"]}/169 : p={p:.2e}')

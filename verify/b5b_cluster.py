# -*- coding: utf-8 -*-
"""설계효과·군집 계층 전체를 결속 41 에서 다시 낸다.

추정기 복구 근거 (verify/b5b_icc.py · verify/b5b_deff.py):
  · ANOVA 의 n0 항이 56.3 → 원고가 적은 '56' 과 일치. 이 항은 라벨과 무관하다.
  · deff 구간 추정기(유효표본 Wilson)가 구판 집계로 공개 구간 7개 중 6개를 소수점까지 재현.
  · 구판 34 의 항공 분배 5,304가지 중 ICC 0.074 가 재현된다(34가지가 0.074로 반올림).
따라서 철회가 아니라 재계산이 맞다."""
import json,math,sys,random
sys.path.insert(0,'graph'); sys.path.insert(0,'probe')
import paths3 as P3
from collections import Counter
from scipy import stats

A=P3.starts(); TP=set(json.load(open('labels/tpset.json',encoding='utf-8'))['tp'])
auth=Counter(k.split('::')[0] for k in A); bind=Counter(k.split('::')[0] for k in TP)
AV={'EU1139','EU947','EU945','US107','US89','USAC'}
GR={'JP道交法','KR도로교통법','KR도로교통법시행규칙','KR지능형로봇법','KR지능형로봇법시행령'}
SUBJ={**{d:'Aviation certification' for d in AV},
 'KR지능형로봇법':'Robot certification','KR지능형로봇법시행령':'Robot certification',
 'JP道交法':'Road traffic, drivers','KR도로교통법':'Road traffic, drivers',
 'KR도로교통법시행규칙':'Road traffic, drivers','LED':'Police conduct',
 'SMC1418':'Police conduct','CAGOV':'Police conduct',
 'EUAI':'Horizontal product law','MID':'Horizontal product law'}
def dom(i): return 'aviation' if i in AV else ('ground' if i in GR else 'crosscut')
inst=sorted(auth); n=[auth[i] for i in inst]; y=[bind.get(i,0) for i in inst]

def wilson(k,m,z=1.96):
    if m<=0: return (0.0,0.0)
    p=k/m; d=1+z*z/m; c=(p+z*z/(2*m))/d
    h=z/d*math.sqrt(p*(1-p)/m+z*z/(4*m*m)); return (max(0.0,c-h),min(1.0,c+h))
def deff_ci(k,m,D): return wilson(k/D,m/D)
def icc_anova(n,y):
    N=sum(n); p=sum(y)/N; K=len(n)
    msb=sum(ni*((yi/ni)-p)**2 for ni,yi in zip(n,y))/(K-1)
    msw=sum(yi*(1-yi/ni)+(ni-yi)*((yi/ni)**2) for ni,yi in zip(n,y))/(N-K)
    n0=(N-sum(ni*ni for ni in n)/N)/(K-1)
    return (msb-msw)/(msb+(n0-1)*msw), n0
ic,n0=icc_anova(n,y); D=1+(n0-1)*ic; N=sum(n)
print('='*66); print('군집 구조 (결속 41)'); print('='*66)
print(f'  ICC {ic:.4f}   n0 {n0:.1f}   설계효과 {D:.2f}   유효표본 {N/D:.0f} / 명목 {N}')
print(f'  (구판: ICC 0.074 · 설계효과 5.10 · 유효표본 199)')
print()
print('[표 8] 주제별 설계효과 95% 구간')
for s in ['Aviation certification','Robot certification','Road traffic, drivers','Police conduct','Horizontal product law']:
    a=sum(auth[i] for i in inst if SUBJ.get(i)==s); b=sum(bind.get(i,0) for i in inst if SUBJ.get(i)==s)
    lo,hi=wilson(b,a); dlo,dhi=deff_ci(b,a,D)
    print(f'  {s:24s} {b:2d}/{a:4d}  Wilson [{lo*100:.1f}, {hi*100:.1f}]  설계효과 [{dlo*100:.1f}, {dhi*100:.1f}]')
print()
print('[표 9] 도메인별')
for d in ['aviation','ground','crosscut']:
    a=sum(auth[i] for i in inst if dom(i)==d); b=sum(bind.get(i,0) for i in inst if dom(i)==d)
    dlo,dhi=deff_ci(b,a,D)
    print(f'  {d:10s} {b:2d}/{a:4d}  설계효과 [{dlo*100:.1f}, {dhi*100:.1f}]')
print()
# 기여 기관 (반환>0) 단위 검정
contrib=[i for i in inst if dom(i) in ('aviation','ground') and auth[i]>0]
av=[i for i in contrib if dom(i)=='aviation']; gr=[i for i in contrib if dom(i)=='ground']
ra=[bind.get(i,0)/auth[i] for i in av]; rg=[bind.get(i,0)/auth[i] for i in gr]
u,pmw=stats.mannwhitneyu(ra,rg,alternative='two-sided')
print(f'[기관단위] Mann-Whitney 항공 {len(av)} vs 지상 {len(gr)} : p = {pmw:.2f}   (구판 p = 0.40)')
# 순열검정: 기관을 단위로 라벨 교환
random.seed(20261015)
A_=sum(bind.get(i,0) for i in av); NA=sum(auth[i] for i in av)
G_=sum(bind.get(i,0) for i in gr); NG=sum(auth[i] for i in gr)
obs=abs(A_/NA-G_/NG); pool=av+gr; cnt=0; B=20000
for _ in range(B):
    sh=pool[:]; random.shuffle(sh); s1=sh[:len(av)]; s2=sh[len(av):]
    n1=sum(auth[i] for i in s1); n2=sum(auth[i] for i in s2)
    if n1==0 or n2==0: continue
    d1=sum(bind.get(i,0) for i in s1)/n1; d2=sum(bind.get(i,0) for i in s2)/n2
    if abs(d1-d2)>=obs-1e-12: cnt+=1
print(f'[기관단위] 순열검정 p = {cnt/B:.2f}   (구판 p = 0.11, 기관 교환 {B}회)')
# 설계효과 보정 Fisher
o,pf=stats.fisher_exact([[A_,NA-A_],[G_,NG-G_]])
oc,pc=stats.fisher_exact([[round(A_/D),round((NA-A_)/D)],[round(G_/D),round((NG-G_)/D)]])
print(f'[조항단위] Fisher p = {pf:.2e}  →  설계효과 보정 p = {pc:.3f}   (구판 보정 p = 0.022)')
# 비율비·h 의 군집 부트스트랩
def h(p1,p2): return abs(2*math.asin(math.sqrt(p1))-2*math.asin(math.sqrt(p2)))
rats=[];hs=[];dfs=[]
for _ in range(10000):
    s=[random.choice(contrib) for _ in contrib]
    sa=[i for i in s if dom(i)=='aviation']; sg=[i for i in s if dom(i)=='ground']
    if not sa or not sg: continue
    na=sum(auth[i] for i in sa); ng=sum(auth[i] for i in sg)
    pa=sum(bind.get(i,0) for i in sa)/na; pg=sum(bind.get(i,0) for i in sg)/ng
    if pg==0: continue
    rats.append(pa/pg); hs.append(h(pa,pg))
    nn=[auth[i] for i in s]; yy=[bind.get(i,0) for i in s]
    try:
        v,m0=icc_anova(nn,yy); dfs.append(1+(m0-1)*v)
    except ZeroDivisionError: pass
q=lambda a,p: sorted(a)[int(p*len(a))]
print(f'[군집 부트스트랩, 기여 기관 {len(contrib)}개 · 유효 추출 {len(rats)}]')
print(f'  비율비 [{q(rats,.025):.2f}, {q(rats,.975):.2f}]   (구판 [2.59, 10.58])')
print(f'  Cohen h [{q(hs,.025):.2f}, {q(hs,.975):.2f}]      (구판 [0.21, 0.51])')
print(f'  설계효과 [{q(dfs,.025):.2f}, {q(dfs,.975):.2f}]   (구판 [1.12, 11.04])')
# 하한이 1 에 닿는 설계효과
pa=A_/NA; pg=G_/NG
d=D
while d<40:
    lo1,hi1=deff_ci(A_,NA,d); lo2,hi2=deff_ci(G_,NG,d)
    if lo1<=hi2: break
    d+=0.01
print(f'[배제 한계] 하한이 지상 상한에 닿는 설계효과 {d:.2f}  (측정 {D:.2f}) → {(d/D-1)*100:.0f}% 여유   (구판 5.55 대 5.10, 9%)')

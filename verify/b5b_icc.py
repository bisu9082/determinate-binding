# -*- coding: utf-8 -*-
"""설계효과 계층 복구 시도. 철회할지 재계산할지는 측정으로 결정한다.

원고가 남긴 식별 정보:
  deff 5.10 · ICC 0.074 · 유효표본 199 · 명목 1,014 · 군집크기 56 · 평균 63 · 중위 34
  199 = 1014/5.10  ·  5.10 = 1 + (56-1)x0.0745  -> 식은 deff = 1 + (m-1)xICC
m(=56)은 라벨과 무관하고, ICC 만 라벨에 의존한다."""
import json,sys,math,itertools
sys.path.insert(0,'graph'); sys.path.insert(0,'probe')
import paths3 as P3
from collections import Counter,defaultdict

A=P3.starts()
TP=set(json.load(open('labels/tpset.json',encoding='utf-8'))['tp'])
auth=Counter(k.split('::')[0] for k in A)
bind=Counter(k.split('::')[0] for k in TP)
inst=sorted(auth)
n=[auth[i] for i in inst]; y=[bind.get(i,0) for i in inst]
N=sum(n); K=len(n)
print(f'기관 {K} · 인가 {N} · 결속 {sum(y)}')
print(f'산술평균 {N/K:.1f}  중위 {sorted(n)[K//2-1:K//2+1]}  Kish(sum n^2/sum n) {sum(x*x for x in n)/N:.1f}')

def icc_anova(n,y):
    """이진 결과의 군집 내 상관 (ANOVA 추정량, Fleiss/Donner 형태)."""
    N=sum(n); p=sum(y)/N; K=len(n)
    msb=sum(ni*((yi/ni)-p)**2 for ni,yi in zip(n,y))/(K-1)
    msw=sum(yi*(1-yi/ni)+(ni-yi)*((yi/ni)**2) for ni,yi in zip(n,y))
    msw=msw/(N-K)
    n0=(N-sum(ni*ni for ni in n)/N)/(K-1)
    return (msb-msw)/(msb+(n0-1)*msw), n0

ic,n0=icc_anova(n,y)
print(f'\nICC(41, 전 16기관) = {ic:.4f}   n0 = {n0:.1f}')
for m in (56,):
    print(f'  deff = 1 + ({m}-1)x{ic:.4f} = {1+(m-1)*ic:.2f}   유효표본 {N/(1+(m-1)*ic):.0f}')

# 구판 34 로 ICC 0.074 를 재현할 수 있는가 — 알려진 제약 안에서 전수 탐색
# 알려진 것: 항공 23 · 지상 11 · 교차 0 · JP 4 · KR-RTA 5 · KR-IRA 2 · KR-RTA-R 0
# 모르는 것: 항공 23 의 6기관 분배. 단 EU쪽 15, US쪽 8 (EU1139+EU947+EU945=15, US107+US89+USAC=8)
AV_EU=['EU1139','EU947','EU945']; AV_US=['US107','US89','USAC']
old_fixed={'JP道交法':4,'KR도로교통법':5,'KR지능형로봇법':2,'KR도로교통법시행규칙':0,
           'KR지능형로봇법시행령':0,'EUAI':0,'MID':0,'LED':0,'SMC1418':0,'CAGOV':0}
# 구판 인가 분모는 보수 이전(US107 35, US89 20)
auth_old=dict(auth); auth_old['US107']=35; auth_old['US89']=20
best=[]
def parts(total,caps):
    for c in itertools.product(*[range(0,min(total,cp)+1) for cp in caps]):
        if sum(c)==total: yield c
for eu in parts(15,[auth_old[k] for k in AV_EU]):
    for us in parts(8,[auth_old[k] for k in AV_US]):
        d=dict(old_fixed); d.update(dict(zip(AV_EU,eu))); d.update(dict(zip(AV_US,us)))
        no=[auth_old[i] for i in inst]; yo=[d.get(i,0) for i in inst]
        v,_=icc_anova(no,yo)
        best.append((abs(v-0.074),v,eu,us))
best.sort()
print(f'\n구판 34 재현 탐색: 가능한 분배 {len(best)}가지')
print(f'  ICC 범위 {min(b[1] for b in best):.4f} ~ {max(b[1] for b in best):.4f}')
print(f'  0.074 에 가장 가까운 분배의 ICC = {best[0][1]:.4f}  (EU {best[0][2]} · US {best[0][3]})')
hit=[b for b in best if abs(b[1]-0.074)<0.0005]
print(f'  ICC 가 0.074 로 반올림되는 분배 {len(hit)}가지')

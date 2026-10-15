# -*- coding: utf-8 -*-
"""부트스트랩 문장 복구 시도 — 내부 통계량을 원고의 것(조항단위 SE x sqrt(deff))으로 고쳐 재시도.
구판 분배는 점 식별되지 않으므로 공개값(1 포함 64% · deff [1.12, 11.04])이
재현 가능 범위에 들어오는지 본다."""
import json,math,random,sys,itertools
sys.path.insert(0,'graph'); sys.path.insert(0,'probe')
import paths3 as P3
from collections import Counter
auth=Counter(k.split('::')[0] for k in P3.starts())
auth_old=dict(auth); auth_old['US107']=35; auth_old['US89']=20
AV=['EU1139','EU947','EU945','US107','US89','USAC']
GR=['JP道交法','KR도로교통법','KR도로교통법시행규칙','KR지능형로봇법','KR지능형로봇법시행령']
CON=AV+GR; Z=1.96
def icc_anova(n,y):
    N=sum(n); p=sum(y)/N; K=len(n)
    if p in (0,1) or K<2: return None,None
    msb=sum(ni*((yi/ni)-p)**2 for ni,yi in zip(n,y))/(K-1)
    msw=sum(yi*(1-yi/ni)+(ni-yi)*((yi/ni)**2) for ni,yi in zip(n,y))/(N-K)
    n0=(N-sum(ni*ni for ni in n)/N)/(K-1)
    den=msb+(n0-1)*msw
    return ((msb-msw)/den if den else None),n0
def run(bd,au,B=6000,seed=11):
    random.seed(seed); inc=0; use=0; dfs=[]
    for _ in range(B):
        s=[random.choice(CON) for _ in CON]
        sa=[i for i in s if i in AV]; sg=[i for i in s if i in GR]
        if not sa or not sg: continue
        na=sum(au[i] for i in sa); ng=sum(au[i] for i in sg)
        k1=sum(bd.get(i,0) for i in sa); k2=sum(bd.get(i,0) for i in sg)
        if k1==0 or k2==0: continue
        nn=[au[i] for i in s]; yy=[bd.get(i,0) for i in s]
        ic,n0=icc_anova(nn,yy)
        if ic is None: continue
        D=max(1.0,1+(n0-1)*ic); dfs.append(D)
        r=(k1/na)/(k2/ng); se=math.sqrt(1/k1-1/na+1/k2-1/ng)*math.sqrt(D)
        use+=1
        if r*math.exp(-Z*se)<=1<=r*math.exp(Z*se): inc+=1
    q=lambda a,p: sorted(a)[int(p*len(a))]
    return inc/use, (q(dfs,.025),q(dfs,.975)), use/B
def parts(t,caps):
    for c in itertools.product(*[range(0,min(t,cp)+1) for cp in caps]):
        if sum(c)==t: yield c
fixed={'JP道交法':4,'KR도로교통법':5,'KR지능형로봇법':2,'KR도로교통법시행규칙':0,'KR지능형로봇법시행령':0}
ALL=[(e,u) for e in parts(15,[auth_old[k] for k in AV[:3]]) for u in parts(8,[auth_old[k] for k in AV[3:]])]
random.seed(3); S=random.sample(ALL,120)
fr=[];dl=[];dh=[]
for eu,us in S:
    bd=dict(fixed); bd.update(dict(zip(AV[:3],eu))); bd.update(dict(zip(AV[3:],us)))
    f,(a,b),keep=run(bd,auth_old,B=2500)
    fr.append(f); dl.append(a); dh.append(b)
print(f'구판 {len(S)}가지 표본')
print(f'  1 포함 비율 {min(fr)*100:.0f}% ~ {max(fr)*100:.0f}%   공개 64%   재현가능 {min(fr)<=0.64<=max(fr)}')
print(f'  deff 하한 {min(dl):.2f}~{max(dl):.2f} (공개 1.12)  상한 {min(dh):.2f}~{max(dh):.2f} (공개 11.04)')
bind=Counter(k.split('::')[0] for k in set(json.load(open('labels/tpset.json',encoding='utf-8'))['tp']))
f,(a,b),keep=run(bind,auth)
print(f'\n결속 41: 1 포함 {f*100:.0f}% · deff [{a:.2f}, {b:.2f}] · 유효추출 {keep*100:.0f}%')

# -*- coding: utf-8 -*-
"""부트스트랩 구현 대조. 구판 라벨의 기관별 분배는 점 식별되지 않으므로
알려진 제약을 만족하는 5,304가지 전부에 대해 돌려 공개 구간 [2.59, 10.58] 이
그 안에 들어오는지 본다. 들어오지 않으면 내 구현이 원고의 것과 다른 것이다."""
import json,math,random,sys,itertools
sys.path.insert(0,'graph'); sys.path.insert(0,'probe')
import paths3 as P3
from collections import Counter
A=P3.starts(); auth=Counter(k.split('::')[0] for k in A)
auth_old=dict(auth); auth_old['US107']=35; auth_old['US89']=20
AV=['EU1139','EU947','EU945','US107','US89','USAC']
GRc=['JP道交法','KR도로교통법','KR도로교통법시행규칙','KR지능형로봇법','KR지능형로봇법시행령']
contrib=AV+GRc
fixed={'JP道交法':4,'KR도로교통법':5,'KR지능형로봇법':2,'KR도로교통법시행규칙':0,'KR지능형로봇법시행령':0}
def boot(bd,seed,B=1500):
    random.seed(seed); rats=[]
    for _ in range(B):
        s=[random.choice(contrib) for _ in contrib]
        sa=[i for i in s if i in AV]; sg=[i for i in s if i in GRc]
        if not sa or not sg: continue
        na=sum(auth_old[i] for i in sa); ng=sum(auth_old[i] for i in sg)
        pa=sum(bd.get(i,0) for i in sa)/na; pg=sum(bd.get(i,0) for i in sg)/ng
        if pg==0: continue
        rats.append(pa/pg)
    if len(rats)<100: return None
    q=lambda p: sorted(rats)[int(p*len(rats))]
    return q(.025),q(.975),len(rats)/B
def parts(t,caps):
    for c in itertools.product(*[range(0,min(t,cp)+1) for cp in caps]):
        if sum(c)==t: yield c
ALL=[(eu,us) for eu in parts(15,[auth_old[k] for k in AV[:3]])
             for us in parts(8,[auth_old[k] for k in AV[3:]])]
random.seed(7); SAMP=random.sample(ALL,250)
los=[];his=[];hit=0;tot=0
if True:
    for eu,us in SAMP:
        bd=dict(fixed); bd.update(dict(zip(AV[:3],eu))); bd.update(dict(zip(AV[3:],us)))
        r=boot(bd,1); tot+=1
        if not r: continue
        lo,hi,frac=r; los.append(lo); his.append(hi)
        if lo>1: hit+=1
print(f'전체 {len(ALL)}가지 중 무작위 {tot}가지 검사')
print(f'  하한 범위 {min(los):.2f} ~ {max(los):.2f}   (공개 하한 2.59)')
print(f'  상한 범위 {min(his):.2f} ~ {max(his):.2f}   (공개 상한 10.58)')
print(f'  하한 > 1 (1 배제) 인 분배 {hit}/{len(los)} = {hit/len(los)*100:.0f}%')
print(f'  공개 구간이 재현 가능 범위 안에 있나: 하한 {min(los)<=2.59<=max(los)} · 상한 {min(his)<=10.58<=max(his)}')

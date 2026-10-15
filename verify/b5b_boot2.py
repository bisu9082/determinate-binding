# -*- coding: utf-8 -*-
"""부트스트랩 설계 후보 2종을 구판 공개 구간 [2.59, 10.58] 로 대조한다.
  (1) 풀링: 11개에서 11개를 복원추출 — 앞서 기각됨 (하한 최대 1.67)
  (2) 층화: 항공 6개에서 6개, 지상 5개에서 5개를 각각 복원추출
원고는 '한 도메인의 결속을 전부 잃는 추출은 버린다'고 적었다. 층화와 맞는 서술이다."""
import json,math,random,sys,itertools
sys.path.insert(0,'graph'); sys.path.insert(0,'probe')
import paths3 as P3
from collections import Counter
auth=Counter(k.split('::')[0] for k in P3.starts())
auth_old=dict(auth); auth_old['US107']=35; auth_old['US89']=20
AV=['EU1139','EU947','EU945','US107','US89','USAC']
GR=['JP道交法','KR도로교통법','KR도로교통법시행규칙','KR지능형로봇법','KR지능형로봇법시행령']
fixed={'JP道交法':4,'KR도로교통법':5,'KR지능형로봇법':2,'KR도로교통법시행규칙':0,'KR지능형로봇법시행령':0}
def h(p1,p2): return abs(2*math.asin(math.sqrt(p1))-2*math.asin(math.sqrt(p2)))
def boot_strat(bd,au,B=4000,seed=1):
    random.seed(seed); rats=[];hs=[];drop=0
    for _ in range(B):
        sa=[random.choice(AV) for _ in AV]; sg=[random.choice(GR) for _ in GR]
        na=sum(au[i] for i in sa); ng=sum(au[i] for i in sg)
        pa=sum(bd.get(i,0) for i in sa)/na; pg=sum(bd.get(i,0) for i in sg)/ng
        if pg==0 or pa==0: drop+=1; continue
        rats.append(pa/pg); hs.append(h(pa,pg))
    q=lambda a,p: sorted(a)[int(p*len(a))]
    return (q(rats,.025),q(rats,.975),q(hs,.025),q(hs,.975),drop/B)
def parts(t,caps):
    for c in itertools.product(*[range(0,min(t,cp)+1) for cp in caps]):
        if sum(c)==t: yield c
ALL=[(e,u) for e in parts(15,[auth_old[k] for k in AV[:3]])
           for u in parts(8,[auth_old[k] for k in AV[3:]])]
random.seed(7); SAMP=random.sample(ALL,220)
los=[];his=[];best=None
for eu,us in SAMP:
    bd=dict(fixed); bd.update(dict(zip(AV[:3],eu))); bd.update(dict(zip(AV[3:],us)))
    lo,hi,hl,hh,dr=boot_strat(bd,auth_old)
    los.append(lo); his.append(hi)
    err=abs(lo-2.59)+abs(hi-10.58)
    if best is None or err<best[0]: best=(err,lo,hi,hl,hh,dr,eu,us)
print('층화 부트스트랩, 구판 라벨')
print(f'  하한 범위 {min(los):.2f} ~ {max(los):.2f}   (공개 2.59)')
print(f'  상한 범위 {min(his):.2f} ~ {max(his):.2f}   (공개 10.58)')
print(f'  공개 구간 재현 가능: 하한 {min(los)<=2.59<=max(los)} · 상한 {min(his)<=10.58<=max(his)}')
print(f'  최적합 분배: 비율비 [{best[1]:.2f}, {best[2]:.2f}]  h [{best[3]:.2f}, {best[4]:.2f}]  버린추출 {best[5]*100:.0f}%')
print(f'    (공개 비율비 [2.59, 10.58] · h [0.21, 0.51])   EU {best[6]} US {best[7]}')
print()
bind=Counter(k.split('::')[0] for k in set(json.load(open('labels/tpset.json',encoding='utf-8'))['tp']))
lo,hi,hl,hh,dr=boot_strat(bind,auth)
print(f'결속 41, 같은 설계: 비율비 [{lo:.2f}, {hi:.2f}]  h [{hl:.2f}, {hh:.2f}]  버린추출 {dr*100:.0f}%')

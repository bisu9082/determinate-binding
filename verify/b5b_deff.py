# -*- coding: utf-8 -*-
"""설계효과 구간 추정기 대조. 구판 집계(항공 23/241 등)는 남아 있으므로
이 추정기는 점 단위로 대조할 수 있다."""
import math,json
def wilson(k,n,z=1.96):
    if n<=0: return (0.0,0.0)
    p=k/n; d=1+z*z/n; c=(p+z*z/(2*n))/d
    m=z/d*math.sqrt(p*(1-p)/n+z*z/(4*n*n))
    return (max(0.0,c-m),min(1.0,c+m))
def deff_ci(k,n,deff):
    """유효표본으로 축소한 Wilson. 비율은 유지하고 n 만 n/deff 로 줄인다."""
    return wilson(k/deff,n/deff)
D=5.10
print('구판 라벨 + 공개 deff 5.10 로 공개 구간을 재현하는가')
cases=[('항공 인증',23,241,'[4.0, 21.2]'),('로봇 인증',2,30,'[0.6, 47.0]'),
       ('도로교통',9,574,'[0.4, 5.9]'),('경찰 직무',0,30,'[0.0, 39.5]'),
       ('수평 제품법',0,139,'[0.0, 12.3]'),('지상(도메인)',11,604,'[0.5, 6.1]'),
       ('교차(도메인)',0,169,'[0.0, 10.4]')]
ok=0
for nm,k,n,pub in cases:
    lo,hi=deff_ci(k,n,D); got=f'[{lo*100:.1f}, {hi*100:.1f}]'
    m = 'OK' if got==pub else '불일치'
    ok+= got==pub
    print(f'  {nm:12s} {k:3d}/{n:4d}  내 계산 {got:14s} 공개 {pub:14s} {m}')
print(f'\n  {ok}/{len(cases)} 일치')

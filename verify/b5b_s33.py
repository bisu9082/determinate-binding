# -*- coding: utf-8 -*-
"""3.3절 통계 계층. 원고가 쓴 것은 군집-강건 SE 가 아니라 '조항 단위 SE' 였다.
로그비율 델타법 + 설계효과 배율. 전부 구판 값으로 대조한 뒤 41 에서 다시 낸다."""
import json,math,sys,random,itertools
sys.path.insert(0,'graph'); sys.path.insert(0,'probe')
import paths3 as P3
from collections import Counter
from scipy import stats
auth=Counter(k.split('::')[0] for k in P3.starts())
bind=Counter(k.split('::')[0] for k in set(json.load(open('labels/tpset.json',encoding='utf-8'))['tp']))
AV=['EU1139','EU947','EU945','US107','US89','USAC']
GR=['JP道交法','KR도로교통법','KR도로교통법시행규칙','KR지능형로봇법','KR지능형로봇법시행령']
Z=1.96
def se_logratio(k1,n1,k2,n2): return math.sqrt(1/k1-1/n1+1/k2-1/n2)
def ratio_ci(k1,n1,k2,n2,D=1.0):
    r=(k1/n1)/(k2/n2); s=se_logratio(k1,n1,k2,n2)*math.sqrt(D)
    return r,(r*math.exp(-Z*s),r*math.exp(Z*s))
def h(p1,p2): return abs(2*math.asin(math.sqrt(p1))-2*math.asin(math.sqrt(p2)))
def h_ci(k1,n1,k2,n2,D=1.0):
    v=h(k1/n1,k2/n2); s=math.sqrt(1/n1+1/n2)*math.sqrt(D)
    return v,(max(0,v-Z*s),v+Z*s)
def d_crit(k1,n1,k2,n2):
    r=(k1/n1)/(k2/n2); s=se_logratio(k1,n1,k2,n2)
    return (math.log(r)/(Z*s))**2
print('='*64); print('대조 — 구판 23/241 대 11/604'); print('='*64)
r,(a,b)=ratio_ci(23,241,11,604); print(f'  비율비 {r:.2f} [{a:.2f}, {b:.2f}]        공개 [2.59, 10.58]  {"OK" if (round(a,2),round(b,2))==(2.59,10.58) else "불일치"}')
r,(a,b)=ratio_ci(23,241,11,604,5.10); print(f'  설계효과 보정 [{a:.2f}, {b:.2f}]      공개 [1.07, 25.61]  {"OK" if (round(a,2),round(b,2))==(1.07,25.61) else "불일치"}')
v,(a,b)=h_ci(23,241,11,604); print(f'  h {v:.3f} [{a:.2f}, {b:.2f}]            공개 [0.21, 0.51]   {"OK" if (round(a,2),round(b,2))==(0.21,0.51) else "불일치"}')
v,(a,b)=h_ci(23,241,11,604,5.10); print(f'  h 보정 [{a:.2f}, {b:.2f}]             공개 [0.02, 0.70]   {"OK" if (round(a,2),round(b,2))==(0.02,0.70) else "근사"}')
print(f'  하한이 1 에 닿는 설계효과 {d_crit(23,241,11,604):.2f}   공개 5.55          {"OK" if abs(d_crit(23,241,11,604)-5.55)<0.01 else "불일치"}')
print()
print('='*64); print('결속 41 — 26/241 대 15/604 · 설계효과 4.68'); print('='*64)
D=4.68
r,(a,b)=ratio_ci(26,241,15,604); print(f'  비율비 {r:.2f} [{a:.2f}, {b:.2f}]')
r,(a,b)=ratio_ci(26,241,15,604,D); print(f'  설계효과 보정 [{a:.2f}, {b:.2f}]  → 1 배제 {"예" if a>1 else "아니오"}')
v,(a,b)=h_ci(26,241,15,604); print(f'  h {v:.3f} [{a:.2f}, {b:.2f}]')
v,(a,b)=h_ci(26,241,15,604,D); print(f'  h 보정 [{a:.2f}, {b:.2f}]')
dc=d_crit(26,241,15,604); print(f'  하한이 1 에 닿는 설계효과 {dc:.2f} 대 측정 {D:.2f} → {(dc/D-1)*100:.0f}% 여유  (구판 9%)')
print()
print('기관 하나를 빼면 배제가 사라지는가 (구판은 4개 기관)')
gone=[]
for drop in AV+GR:
    a_=sum(bind.get(i,0) for i in AV if i!=drop); na=sum(auth[i] for i in AV if i!=drop)
    g_=sum(bind.get(i,0) for i in GR if i!=drop); ng=sum(auth[i] for i in GR if i!=drop)
    if a_==0 or g_==0: gone.append((drop,'도메인 소실')); continue
    _,(lo,_)=ratio_ci(a_,na,g_,ng,D)
    if lo<=1: gone.append((drop,f'하한 {lo:.2f}'))
print(f'  배제가 사라지는 기관 {len(gone)}개: '+', '.join(f'{d}({w})' for d,w in gone) if gone else '  없음')
print()
print('기관별 구성 (본문 서술 확인용)')
av_s=sorted(((i,bind.get(i,0)) for i in AV),key=lambda x:-x[1])
gr_s=sorted(((i,bind.get(i,0)) for i in GR),key=lambda x:-x[1])
print(f'  항공 {sum(bind.get(i,0) for i in AV)}건: '+' · '.join(f'{i} {c}' for i,c in av_s))
print(f'  지상 {sum(bind.get(i,0) for i in GR)}건: '+' · '.join(f'{i} {c}' for i,c in gr_s))
print(f'  항공 상위 2기관 합 {av_s[0][1]+av_s[1][1]} / 0건 기관 {sum(1 for _,c in av_s if c==0)}개')
print(f'  지상 비영 기관 {sum(1 for _,c in gr_s if c>0)}/5')

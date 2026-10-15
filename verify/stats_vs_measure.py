# -*- coding: utf-8 -*-
"""양성 검사: 측정에서 낸 통계량이 원고에 실제로 적혀 있는지 본다.

body_vs_measure 는 '구판 수치가 없는지'를 보는 음성 검사다. 그것만으로는
B5-a 에서 실제로 일어난 일을 못 잡는다 — 분자를 23에서 26으로 고치면서
p = 5.5e-7 을 그대로 둔 것(F-14). 구판 값이 사라졌으니 음성 검사는 통과한다.
그래서 여기서는 반대로, 현행 측정값이 본문에 있어야 통과한다."""
import json,math,os,re,sys
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
sys.path.insert(0,'graph'); sys.path.insert(0,'probe')
import paths3 as P3
from collections import Counter
from scipy import stats
auth=Counter(k.split('::')[0] for k in P3.starts())
bind=Counter(k.split('::')[0] for k in set(json.load(open('labels/tpset.json',encoding='utf-8'))['tp']))
AV=['EU1139','EU947','EU945','US107','US89','USAC']
GR=['JP道交法','KR도로교통법','KR도로교통법시행규칙','KR지능형로봇법','KR지능형로봇법시행령']
TXT=''.join(open(f'tex/{x}_v23.tex',encoding='utf-8').read()
            for x in ('front','methods','results','discussion','appendix','back','main'))
TXT=re.sub(r'\s+',' ',TXT).replace(chr(92)+'%','%').replace('{,}',',')
Z=1.96
def wilson(k,n):
    p=k/n; d=1+Z*Z/n; c=(p+Z*Z/(2*n))/d
    h=Z/d*math.sqrt(p*(1-p)/n+Z*Z/(4*n*n)); return max(0,c-h),min(1,c+h)
def icc_anova(n,y):
    N=sum(n); p=sum(y)/N; K=len(n)
    msb=sum(ni*((yi/ni)-p)**2 for ni,yi in zip(n,y))/(K-1)
    msw=sum(yi*(1-yi/ni)+(ni-yi)*((yi/ni)**2) for ni,yi in zip(n,y))/(N-K)
    n0=(N-sum(ni*ni for ni in n)/N)/(K-1)
    return (msb-msw)/(msb+(n0-1)*msw), n0
inst=sorted(auth)
ic,n0=icc_anova([auth[i] for i in inst],[bind.get(i,0) for i in inst])
D=1+(n0-1)*ic; N=sum(auth.values())
A=sum(bind.get(i,0) for i in AV); NA=sum(auth[i] for i in AV)
G=sum(bind.get(i,0) for i in GR); NG=sum(auth[i] for i in GR)
se=math.sqrt(1/A-1/NA+1/G-1/NG); r=(A/NA)/(G/NG)
def h(p1,p2): return abs(2*math.asin(math.sqrt(p1))-2*math.asin(math.sqrt(p2)))
hv=h(A/NA,G/NG); hse=math.sqrt(1/NA+1/NG)
_,pf=stats.fisher_exact([[A,NA-A],[G,NG-G]])
_,pc=stats.fisher_exact([[round(A/D),round((NA-A)/D)],[round(G/D),round((NG-G)/D)]])
RT=['JP道交法','KR도로교통법','KR도로교통법시행규칙']
RTb=sum(bind.get(i,0) for i in RT); RTn=sum(auth[i] for i in RT)
orv,prt=stats.fisher_exact([[A,NA-A],[RTb,RTn-RTb]])
CL=json.load(open('classify/final.json',encoding='utf-8'))
SUP=sum(1 for r in CL['records'] if r['verdict']=='SUPPLY')
OPR=sum(1 for r in CL['records'] if r['verdict']=='OPERATE')
AVS=sum(1 for r in CL['records'] if r['verdict']=='SUPPLY' and r['provision'].split('::')[0] in AV)
AVO=sum(1 for r in CL['records'] if r['verdict']=='OPERATE' and r['provision'].split('::')[0] in AV)
GRO=sum(1 for r in CL['records'] if r['verdict']=='OPERATE' and r['provision'].split('::')[0] in GR)
NUM={26:'Twenty-six',35:'Thirty-five',6:'Six',41:'Forty-one'}
CH=[('공급 결속',f'{SUP:d}'),('운용 결속',f'{OPR:d}'),
    ('운용 결속(영문)',NUM.get(OPR,str(OPR))),('공급 결속(영문)',NUM.get(SUP,str(SUP))),
    ('항공 운용',f'{AVO:d}'),('항공 공급',f'{AVS:d}'),('지상 운용',f'{GRO:d}'),
    ('ICC',f'{ic:.3f}'),('설계효과',f'{D:.2f}'),('유효표본',f'{N/D:.0f}'),
    ('정밀도',f'{A+G:d}' if False else f'{(A+G)/91:.3f}'),
    ('항공 결속',f'{A:d}'),('지상 결속',f'{G:d}'),
    ('비율비',f'{r:.2f}'),("Cohen h",f'{hv:.3f}'),
    ('비율비 구간 하한',f'{r*math.exp(-Z*se):.2f}'),('비율비 구간 상한',f'{r*math.exp(Z*se):.2f}'),
    ('보정 비율비 하한',f'{r*math.exp(-Z*se*math.sqrt(D)):.2f}'),
    ('보정 비율비 상한',f'{r*math.exp(Z*se*math.sqrt(D)):.2f}'),
    ('임계 설계효과',f'{(math.log(r)/(Z*se))**2:.2f}'),
    ('설계효과 보정 Fisher p',f'{pc:.3f}'),
    ('항공vs도로 OR',f'{orv:.1f}'),
    ('항공 Wilson 하한',f'{wilson(A,NA)[0]*100:.1f}'),('항공 Wilson 상한',f'{wilson(A,NA)[1]*100:.1f}')]
miss=[(w,v) for w,v in CH if v not in TXT]
print(f"{'측정값':24s} {'값':>9s}  원고에 있나")
print('-'*54)
for w,v in CH: print(f'{w:24s} {v:>9s}  {"있음" if v in TXT else "없음  <-"}')
print(f'\n원고에 없는 측정값 {len(miss)}종')
if miss: print('수치를 고치면서 그 수치에 딸린 통계량을 안 고친 자리가 있다.')
sys.exit(1 if miss else 0)

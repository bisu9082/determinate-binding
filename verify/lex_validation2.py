# -*- coding: utf-8 -*-
"""어휘집 타당성 검증 v2 — 2026-10-14 재건.

9/20 판(verify/lex_validation.py)에 부록 A 의 변경 ②·⑨ 를 반영한다.
② 표본 중 수선으로 인가 모집단을 떠난 것을 뺀다.
⑨ 대칭화로 tier 1 을 떠난(tier 2 로 올라간) 것도 뺀다. 위험집단에 없으면 분모가 아니다.
그리고 층 가중을 적용한다 — 배분은 균등이고 층은 균등하지 않으므로 풀링은 틀린다.

라벨은 9/20 판의 것을 그대로 쓴다. 재라벨링이 아니라 모집단 정정이다."""
import json,math,re,sys,os
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
sys.path.insert(0,'graph'); sys.path.insert(0,'probe')
import paths3 as P3

src=open('verify/lex_validation.py',encoding='utf-8').read()
LAB=eval('{'+re.search(r'LABEL = \{(.*?)\n\}',src,re.S).group(1)+'\n}')
E=[tuple(e) for e in json.load(open('graph/edges3.json',encoding='utf-8'))]
R=P3.run(E,4)
T1={k for k,v in R.items() if v[0]==1}
def lang(k):
    d=k.split('::')[0]
    return 'JP' if d.startswith('JP') else ('KR' if d.startswith('KR') else 'EN')

dropped={k:('인가 모집단 이탈(변경 ①)' if k not in R else 'tier 1 이탈(변경 ⑨)')
         for k in LAB if k not in T1}
keep=[k for k in LAB if k in T1]

def wilson(k,n,z=1.96):
    if n==0: return (0.0,0.0)
    p=k/n; d=1+z*z/n; c=p+z*z/(2*n); h=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))
    return (max(0.0,(c-h)/d),min(1.0,(c+h)/d))

strata={}
for L in ('EN','KR','JP'):
    s=[k for k in keep if lang(k)==L]
    x=sum(LAB[k][0] for k in s)
    strata[L]={'n':len(s),'fn':x,'rate':x/len(s),'wilson':wilson(x,len(s)),
               'N_tier1':sum(1 for k in T1 if lang(k)==L)}
Ntot=sum(v['N_tier1'] for v in strata.values())
w={L:v['N_tier1']/Ntot for L,v in strata.items()}
p_w=sum(w[L]*strata[L]['rate'] for L in strata)
# 층 가중 추정의 분산 (층별 이항, 유한모집단 보정 없음) → 로짓 구간
var=sum(w[L]**2*strata[L]['rate']*(1-strata[L]['rate'])/strata[L]['n'] for L in strata)
se=math.sqrt(var)
if 0<p_w<1:
    lg=math.log(p_w/(1-p_w)); se_lg=se/(p_w*(1-p_w))
    lo,hi=[1/(1+math.exp(-(lg+z*1.96*se_lg))) for z in (-1,1)]
else: lo,hi=0.0,1.0
T2=sum(1 for v in R.values() if v[0]==2)
out={'_purpose':'어휘집 위음성률. 층 가중 추정. 2026-10-14 재건.',
 '_labels':'9/20 판 라벨 그대로. 모집단만 정정했다.',
 'dropped_from_sample':dropped,
 'strata':strata,'weights':w,'tier1_total':Ntot,
 'weighted':{'rate':p_w,'logit_ci':[lo,hi],'se':se},
 'pooled':{'n':len(keep),'fn':sum(LAB[k][0] for k in keep),
           'rate':sum(LAB[k][0] for k in keep)/len(keep),
           'wilson':wilson(sum(LAB[k][0] for k in keep),len(keep))},
 'projection':{'_how':'tier1 모집단에 가중 위음성률을 외삽한다',
   'missed_point':round(Ntot*p_w),
   'missed_ci':[round(Ntot*lo),round(Ntot*hi)],
   'returned_now':T2}}
json.dump(out,open('verify/lex_validation2.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print('표본에서 뺀 것:',dropped)
print(f"{'층':4s}{'n':>4s}{'위음성':>6s}{'율':>8s}   Wilson 95%        tier1 모집단  가중")
for L in ('EN','KR','JP'):
    v=strata[L]
    print(f"{L:4s}{v['n']:>4}{v['fn']:>6}{v['rate']*100:>7.1f}%"
          f"   [{v['wilson'][0]*100:>4.1f}, {v['wilson'][1]*100:>5.1f}]"
          f"      {v['N_tier1']:>6}   {w[L]*100:>5.1f}%")
print(f"\n층가중  {p_w*100:.1f}%  로짓 95% [{lo*100:.1f}, {hi*100:.1f}]")
print(f"풀링(참고) {out['pooled']['rate']*100:.1f}%")
print(f"tier1 {Ntot}건 외삽 → 놓친 결속 {out['projection']['missed_point']}건 "
      f"(CI {out['projection']['missed_ci'][0]}–{out['projection']['missed_ci'][1]})")

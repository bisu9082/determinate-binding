# -*- coding: utf-8 -*-
"""B5-b: 3.3절 군집·설계효과 계층을 결속 41 에서 다시 쓴다.

추정기는 전부 구판 값으로 대조했다 (verify/b5b_s33.py):
  로그비율 델타법 [2.59, 10.58] · 설계효과 배율 [1.07, 25.61] · h [0.21, 0.51]
  · 임계 설계효과 5.55 · 설계효과 Wilson 구간 7개 중 6개 · ANOVA n0 = 56
부트스트랩은 내부 통계량을 원고의 것으로 고친 뒤 공개값(64% · [1.12, 11.04])이
재현 범위에 들어옴을 확인했다 (verify/b5b_boot3.py)."""
import json,os,sys
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
PA=json.load(open('recover/paras.json',encoding='utf-8'))
TB=json.load(open('recover/tables.json',encoding='utf-8'))
E=[]
def p(old,new,n=1): E.append((old,new,n))

# 163: 명목 Wilson 과 설계효과 구간
p('are [6.4, 13.9], [1.0, 3.2] and [0.0, 2.2] per cent','are [7.5, 15.3], [1.5, 4.1] and [0.0, 2.2] per cent')
p('they widen to [4.0, 21.2], [0.5, 6.1] and [0.0, 10.4]','they widen to [4.9, 22.1], [0.9, 6.8] and [0.0, 9.6]')
# 164: 집중도와 ICC·설계효과
p('Of the 23 aviation bindings, 20 are in two instruments, 13 in Regulation (EU) 2018/1139 and 7 in 14 CFR Part 107',
  'Of the 26 aviation bindings, 24 are in two instruments, 17 in Regulation (EU) 2018/1139 and 7 in 14 CFR Part 107')
p('All 11 ground bindings are in three of the five ground instruments',
  'All 15 ground bindings are in four of the five ground instruments')
p('across the sixteen instruments is 0.074, which at an effective (Kish) cluster size of 56 provisions, against an arithmetic mean of 63 and a median of 34, gives a design effect of 5.10 and an effective sample size of 199 against a nominal 1,014',
  'across the sixteen instruments is 0.067, which at an effective (Kish) cluster size of 56 provisions, against an arithmetic mean of 63 and a median of 34, gives a design effect of 4.68 and an effective sample size of 217 against a nominal 1,014')
# 165: 기관 단위 검정 3종
p('is equalled or exceeded in 51 of them: p = 0.11','is equalled or exceeded in 41 of them: p = 0.09')
p('on the eleven instrumentlevel rates gives p = 0.40','on the eleven instrumentlevel rates gives p = 0.52')
p('applied to the provision-level table gives p = 0.022','applied to the provision-level table gives p = 0.018')
# 167: 효과크기 구간·임계 설계효과·부트스트랩
p("Cohen's h = 0.357 sits in the range","Cohen's h = 0.353 sits in the range")
p('the ratio runs [2.59, 10.58] and h runs [0.21, 0.51]; under the design effect of 5.10 they run [1.07, 25.61] and [0.02, 0.70]',
  'the ratio runs [2.34, 8.06] and h runs [0.20, 0.50]; under the design effect of 4.68 they run [1.14, 16.53] and [0.03, 0.68]')
p('The design effect at which the lower bound reaches 1 is 5.55 against the 5.10 measured, so a 9 per cent movement in the design effect removes the exclusion',
  'The design effect at which the lower bound reaches 1 is 5.65 against the 4.68 measured, so a 21 per cent movement in the design effect removes the exclusion')
p("the corrected interval includes 1 in 64 per cent of the 9,652 draws in which the ratio is defined (348 of 10,000 draws lose one domain's bindings entirely and are discarded), with the design effect itself running [1.12, 11.04]",
  "the corrected interval includes 1 in 53 per cent of the 9,864 draws in which the ratio is defined (136 of 10,000 draws lose one domain's bindings entirely and are discarded), with the design effect itself running [1.00, 8.23], where 955 draws return a negative variance-component estimate and are floored at 1")
# 170: Fisher 3종 + 설계효과 + 잔여 항공 결속
p('gives p = 5.5 $\\times$ 10$-$7 with an odds ratio of 6.6','gives p = 2.6 $\\times$ 10$-$6 with an odds ratio of 4.8')
p('it gives p = 2.3 $\\times$ 10$-$5 , and against the pooled cross-cutting denominator p = 3.5 $\\times$ 10$-$6 ',
  'it gives p = 6.7 $\\times$ 10$-$6 , and against the pooled cross-cutting denominator p = 9.3 $\\times$ 10$-$7 ')
p('the design effect of the instrument clustering is 5.10, and the three aviation bindings outside Regulation (EU) 2018/1139 and Part 107',
  'the design effect of the instrument clustering is 4.68, and the two aviation bindings outside Regulation (EU) 2018/1139 and Part 107')
# 174: 영 셀
p('which sits below the aviation rate of 9.5 per cent','which sits below the aviation rate of 10.8 per cent')
p('Under the design effect of 5.10 the bounds move to 12.3 and 10.4 per cent','Under the design effect of 4.68 the bounds move to 11.5 and 9.6 per cent')

# 표 8·9 설계효과 열
T=[]
def t(k,ri,ci,old,new): T.append((k,ri,ci,old,new))
t('8',1,5,'[4.0, 21.2]','[4.9, 22.1]'); t('8',2,5,'[0.6, 47.0]','[0.2, 41.5]')
t('8',3,5,'[0.4, 5.9]','[0.8, 6.9]');  t('8',4,5,'[0.0, 39.5]','[0.0, 37.5]')
t('8',5,5,'[0.0, 12.3]','[0.0, 11.5]')
t('9',1,5,'[4.0, 21.2]','[4.9, 22.1]'); t('9',2,5,'[0.5, 6.1]','[0.9, 6.8]')
t('9',3,5,'[0.0, 10.4]','[0.0, 9.6]')

bad=[]
for old,new,n in E:
    g=sum(s.count(old) for s in PA)
    if g!=n: bad.append(('para',n,g,old[:88]))
for k,ri,ci,old,new in T:
    cur=TB[k]['rows'][ri][ci]
    if cur!=old: bad.append((f'T{k}[{ri}][{ci}]',old,cur,''))
if bad:
    print('치환 불가 — 아무것도 적용하지 않았다')
    for a,b,c,d in bad: print(f'  {a}: 기대 {b} 실제 {c}  |{d}|')
    sys.exit(1)
for old,new,n in E: PA=[s.replace(old,new) for s in PA]
for k,ri,ci,old,new in T: TB[k]['rows'][ri][ci]=new
json.dump(PA,open('recover/paras.json','w',encoding='utf-8'),ensure_ascii=False,indent=0)
json.dump(TB,open('recover/tables.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print(f'본문 {len(E)}건 · 표 {len(T)}건 적용')

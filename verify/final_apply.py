# -*- coding: utf-8 -*-
"""투고 전 마무리. 두 체커가 놓친 잔존 구판 수치 + 공개하지 않고 있던 재정 사실 + 후기 항목.

두 체커가 놓친 이유를 적어 둔다. body_vs_measure 는 내가 적어 넣은 표현만 보는
음성 검사이고 '34 of 91' 과 '[0.281, 0.476]' 이 그 목록에 없었다. stats_vs_measure 는
현행값이 어딘가에 있으면 통과하는 양성 검사라 다른 곳의 구판값을 못 본다.
그래서 둘 다 통과한 채로 원고가 '41 are bindings' 와 '34 of 91 is a census' 를
동시에 적고 있었다."""
import json,os,sys,re
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
PA=json.load(open('recover/paras.json',encoding='utf-8'))
E=[]
def p(old,new,n=1): E.append((old,new,n))

# ── 잔존 구판 수치 ─────────────────────────────────────────────
p('because 34 of 91 is a census of the returned set and not a sample from it. The Wilson 95% interval of [0.281, 0.476] is',
  'because 41 of 91 is a census of the returned set and not a sample from it. The Wilson 95% interval of [0.352, 0.553] is')
p('recomputing the precision in each draw, gives [0.239, 0.500], which is a third wider',
  'recomputing the precision in each draw, gives [0.306, 0.518], which is a quarter wider')
p('bootstrap interval of [0.239, 0.500] (Section 2.7)','bootstrap interval of [0.306, 0.518] (Section 2.7)')
p('moves the nominal aviation rate from 9.5 per cent to 9.7 per cent, 23 of 236',
  'moves the nominal aviation rate from 10.8 per cent to 11.0 per cent, 26 of 236')
p('On the police route as a whole there are 12 audited bindings and 367 tier-1 provisions, so the projection is 46 missed bindings with an interval of 17 to 108 and recall is 0.21 [0.10, 0.41]',
  'On the police route as a whole there are 16 audited bindings and 367 tier-1 provisions, so the projection is 46 missed bindings with an interval of 17 to 108 and recall is 0.26 [0.13, 0.48]')
p('that implies a recall of 0.35 [0.19, 0.59] corpus-wide and, on the police route where the key negative claim lives, 0.21 [0.10, 0.41] (Section 3.4)',
  'that implies a recall of 0.40 [0.22, 0.64] corpus-wide and, on the police route where the key negative claim lives, 0.26 [0.13, 0.48] (Section 3.4)')
p('and the corpus-wide recall to [0.13, 0.74] (Section 2.6)','and the corpus-wide recall to [0.16, 0.77] (Section 2.6)')
p('What the measurement shows is that those 34 bindings attach to three objects',
  'What the measurement shows is that those 41 bindings attach to three objects')
p('market access account for 8 of the 34 audited bindings, assessed before sale',
  'market access account for 6 of the 41 audited bindings, assessed before sale')
p('the classification of Section 3.3 measures 26 of the 34 as conditioning an operating permission instead',
  'the classification of Section 3.3 measures 35 of the 41 as conditioning an operating permission instead')
p('and the Act returns 20 provisions of which 4 are bindings','and the Act returns 20 provisions of which 8 are bindings')

# ── 후기 항목 ─────────────────────────────────────────────────
# 저자 둘 다 화생방이다. 경찰청은 이 논문의 소속기관이 아니다.
p('The views expressed are those of the authors and do not represent the official position of the Korean National Police Agency or of the Chemical, Biological, Radiological and Nuclear Defense Research Institute.',
  'The views expressed are those of the authors and do not represent the official position of the Chemical, Biological, Radiological and Nuclear Defense Research Institute, of the Republic of Korea CBRN Defence Command, or of the Ministry of National Defense.')
# AI 공시: 쓰임이 넷으로 늘었다. 공시가 방패다.
p('A large language model was used in two places in this study and both are reported in the Methods rather than only here. It was the instrument that applied the labels in the binding audit of Section 2.7, in two passes by one investigator, which is why that section states the agreement',
  'A large language model was used in four places in this study and all four are reported in the Methods or the Results rather than only here. It was the instrument that applied the labels in the binding audit of Section 2.7, in two passes by one investigator, which is why that section states the agreement')
p('It was also the instrument that re-wrote the search terms in the reliability test of Section 3.8. It was additionally used to assist with language editing of the manuscript.',
  'It was also the instrument that made the blind third pass over the enriched audit records reported in Section 2.7, and the instrument that classified the bindings by the kind of permission they condition in Section 3.3, in two independent passes over the provision texts against a rubric from which the counts had been removed. It was also the instrument that re-wrote the search terms in the reliability test of Section 3.8. It was additionally used to assist with language editing of the manuscript.')
p('the lexicons and their validation sample with labels, the full binding audit with the labels',
  'the lexicons and their validation sample with labels, the full binding audit with the labels of all three passes and the adjudication record of each, the permission-type classification with both passes and the rubric they were given, the full binding audit with the labels')

bad=[(n,sum(s.count(old) for s in PA),old[:92]) for old,new,n in E if sum(s.count(old) for s in PA)!=n]
if bad:
    print('치환 불가 — 아무것도 적용하지 않았다')
    for b,c,o in bad: print(f'  기대 {b} 실제 {c}  |{o}|')
    sys.exit(1)
for old,new,n in E: PA=[s.replace(old,new) for s in PA]

# ── 재정 사실 공개: 2.7절 끝에 문단 신설 ───────────────────────
ANCHOR='Tuning the lexicon or the path bound against these labels would convert a measurement into a fit.'
idx=[i for i,s in enumerate(PA) if ANCHOR in s]
if len(idx)!=1: print('2.7절 닫는 문단을 못 찾았다',idx); sys.exit(1)
NEW=("The labels this paper adopts are not the labels its first release reported, and the "
 "difference is large enough to state here rather than in a limitation. The two passes "
 "described above resolved to 34 bindings, and that is the count the earlier version "
 "published. The audit records released with it carried every lexicon match and the path "
 "the predicate recorded, but not the text of the provision a path arrived at, so the rule "
 "that admits a binding reached through a named provision could not be applied from the "
 "record alone; a reader working from the released records could not reproduce the "
 "adjudication. We enriched the records with the cited text and had the audit repeated, "
 "blind, against a rubric from which the counts had been removed. That pass moves 10 of the "
 "91 records and gives 41. On the binding value the three passes stand at 43, 26 and 41, "
 "so the labelling is not stable to the procedure that produces it, and the adopted count "
 "is the third pass rather than an average of them. What the change does not move is the "
 "comparison the paper rests on: Cohen's h goes from 0.357 to 0.353 and the "
 "aviation-against-ground Fisher test from p = 1.5 $\\times$ 10$-$6 to p = 2.6 $\\times$ 10$-$6 . "
 "The direction of the change is against us in the headline rate, which rises from 3.4 to "
 "4.0 per cent, and in favour of us in the precision, which rises from 0.374 to 0.451. "
 "All three label sets are released.")
PA.insert(idx[0]+1,NEW)
json.dump(PA,open('recover/paras.json','w',encoding='utf-8'),ensure_ascii=False,indent=0)
print(f'본문 {len(E)}건 적용 · 재정 공개 문단 1개 신설 (위치 {idx[0]+1})')

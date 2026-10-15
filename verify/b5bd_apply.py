# -*- coding: utf-8 -*-
"""범주 B(허가 종류 분류)와 범주 D(변경별 델타)를 결속 41 에서 다시 쓴다.

B: classify/final.json — 두 판독 맹검(정순·역순, 독립 에이전트), 41/41 일치,
   경계 1건을 2.7절과 같은 방식으로 문언에 대고 재정. SUPPLY 6 / OPERATE 35.
D: 변경 ⑤·⑦ 의 공개 수치 10종이 구판 입력으로 전부 재현되어 추정기가 확정됐다
   (8.07 · 4.8e-08 · 2.0e-06 · 5.13 · 9.3% · 9.5% · 5.24 · 0.351 · 0.357 · 1.5e-06).
   재계산 불가가 아니었다. 등재를 해제한다."""
import json,os,sys
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
PA=json.load(open('recover/paras.json',encoding='utf-8'))
TB=json.load(open('recover/tables.json',encoding='utf-8'))
E=[]
def p(old,new,n=1): E.append((old,new,n))

# ── 범주 B ──────────────────────────────────────────────────────
p('Each of the 34 audited bindings was classified, in two passes over its own text',
  'Each of the 41 audited bindings was classified, in two passes over its own text')
p('The passes agreed on 33 of 34 and on the operating count exactly; as there, the figure measures repeatability of a procedure, not agreement between two readers.',
  'The passes agreed on all 41, including on the single provision each recorded as borderline; as there, the figure measures repeatability of a procedure, not agreement between two readers. The borderline record was resolved against the provision text by the procedure of Section 2.7.')
p('Twenty-six of the 34 bindings condition operating, not supplying. Within aviation the split is 16 operating to 7 supplying, and 9 of the 10 ground-side operating bindings are driving licences, the tenth being the Korean robot re-certification provision. Seven of the eight supply-side bindings are the classical ones, and all seven are in Regulation (EU) 2018/1139: type certification of a design, certification of parts and of non-installed equipment, the airworthiness certificate of an individual aircraft, certification of design and production organisations, the certificate for a flight simulation training device, and certification of ATM/ANS systems and constituents. The eighth supply-side binding is not aviation and not pre-market: Article 40-2(3) of the Korean Intelligent Robots Act bars use of a robot inside a development district before completion certification, which attaches to the article but conditions use rather than sale. The sixteen operating-side bindings are pilot and air traffic controller licences, aerodrome certificates, air operator certification, the UAS operational authorisation of Implementing Regulation (EU) 2019/947, and the United States small unmanned aircraft operating rules of 14 CFR Parts 107 and 89.',
  'Thirty-five of the 41 bindings condition operating, not supplying. Within aviation the split is 20 operating to 6 supplying, and every one of the 15 ground-side bindings conditions operating: 14 are driving licences and the fifteenth is the Korean robot change-certification provision. All six supply-side bindings are the classical ones and all six are in Regulation (EU) 2018/1139: type certification of a design, certification of parts and of non-installed equipment, the airworthiness certificate of an individual aircraft, certification of design and production organisations, and the certificate for a flight simulation training device. Two corrections to the earlier version of this paragraph belong here, because both were errors of identification rather than of counting. It listed certification of ATM/ANS systems and constituents as a seventh supply-side binding; the re-adjudication rejects Article 45(2) of the basic act, because the same paragraph permits the organisation to declare compliance instead of holding a certificate, and a branch that reaches the permission without the evaluation fails the rule. It also listed an eighth supply-side binding described as Article 40-2(3) of the Korean Intelligent Robots Act barring use of a robot inside a development district before completion certification. That description belongs to Article 37(4), which bars the project implementer from using land and facilities before the completion certificate and is not a binding under the audit; Article 40-2(3) is a duty to obtain change certification when altering certified matters, and because the certification it alters is the outdoor mobile robot operating-safety certification it conditions operating rather than supply. The twenty operating-side aviation bindings are pilot and air traffic controller licences, cabin crew attestations, training organisation and aero-medical centre approvals, instructor and examiner certificates, aerodrome certificates, air operator certification, the UAS operational authorisation of Implementing Regulation (EU) 2019/947, and the United States small unmanned aircraft operating rules of 14 CFR Parts 107 and 89.')
p('Eight of the 34 bindings attach to the machine as an article rather than to the mission. Seven are pre-market certification in the European basic act, assessed before sale by a body external to the buyer against thresholds fixed in advance; the eighth bars use of a robot inside a Korean development district before completion certification, which attaches to the article but is not a condition of sale. The other 26 condition operating it (Section 3.3).',
  'Six of the 41 bindings attach to the machine as an article rather than to the mission. All six are pre-market certification in the European basic act, assessed before sale by a body external to the buyer against thresholds fixed in advance. The other 35 condition operating it (Section 3.3).')

# ── 범주 D ──────────────────────────────────────────────────────
p('the audit of those ten finds four bindings and six false positives. All four are Japanese driving-licence provisions that condition the grant or the revocation of a licence on a named examination: Article 89(1), which requires the applicant to sit the driving licence examination, and Article 104-2-2(1), (2) and (4), which require the public safety commission to revoke a licence where the holder fails or does not sit the re-examination. The six rejected are discretionary (may decline to grant), procedural, or condition on attendance at a course rather than on an examination. The audited count moves from 30 to 34, precision from 0.366 to 0.374, and the ground rate from 7 of 604 to 11 of 604. The aviation-to-ground ratio falls from 8.07 to 5.13 and the Fisher test from p = 4.8 $\\times$ 10$-$8 to p = 2.0 $\\times$ 10$-$6 , so the contrast survives at a materially smaller effect size.',
  'the audit of those ten finds eight bindings and two false positives. All eight are Japanese driving-licence provisions that condition the grant, the eligibility or the revocation of a licence on a named examination: Article 89(1), which requires the applicant to sit the driving licence examination; Article 104-2-2(1), (2) and (4), which require the public safety commission to revoke a licence where the holder fails or does not sit the re-examination; Article 90(13) and Article 90-2(2), which turn on having passed the examination; and Article 96(4) and (5), which condition eligibility to sit one examination on holding a licence obtained through another. The earlier version of this paragraph reported four bindings and six rejections here, and the blind re-adjudication of the audit moves four of those six the other way. The audited count moves from 33 to 41, precision from 0.402 to 0.451, and the ground rate from 7 of 604 to 15 of 604. The aviation-to-ground ratio falls from 9.12 to 4.26 and the Fisher test from p = 2.0 $\\times$ 10$-$9 to p = 3.2 $\\times$ 10$-$6 , so the contrast survives at a materially smaller effect size.')
p("The returned count, the audited count and the precision are unchanged at 91, 34 and 0.374, because no removed caption was returned. The aviation denominator falls from 246 to 241, so the aviation rate rises from 9.3% to 9.5%, the aviation-toground ratio from 5.13 to 5.24, Cohen's h from 0.351 to 0.357 and the aviation-against-ground Fisher test from p = 2.0 $\\times$ 10$-$6 to p = 1.5 $\\times$ 10$-$6 .",
  "The returned count, the audited count and the precision are unchanged at 91, 41 and 0.451, because no removed caption was returned. The aviation denominator falls from 246 to 241, so the aviation rate rises from 10.6% to 10.8%, the aviation-toground ratio from 4.26 to 4.34, Cohen's h from 0.346 to 0.353 and the aviation-against-ground Fisher test from p = 3.2 $\\times$ 10$-$6 to p = 2.6 $\\times$ 10$-$6 .")

T=[]
# 표 6 캡션: Before 열이 구판 판정에서 나온 값임을 명시
Q1,Q2='“','”'
T.append(('6','caption',f'{Q1}Before{Q2} is the state at the first freeze that reported each quantity',
          f'{Q1}Before{Q2} is the state at the first freeze that reported each quantity, and for the rows that depend on labels it is that state as labelled then, because the pre-change returned sets were not re-labelled under the adjudication this paper adopts'))
# 'Appendix Appendix A' 중복이 원천 캡션에 남아 있다
T.append(('6','caption','Appendix Appendix A attributes','Appendix A attributes'))

bad=[]
for old,new,n in E:
    g=sum(s.count(old) for s in PA)
    if g!=n: bad.append(('para',n,g,old[:92]))
for k,w,old,new in [(a,b,c,d) for a,b,c,d in T]:
    if TB[k]['caption'].count(old)!=1: bad.append((f'T{k}.caption',1,TB[k]['caption'].count(old),old[:60]))
if bad:
    print('치환 불가 — 아무것도 적용하지 않았다')
    for a,b,c,d in bad: print(f'  {a}: 기대 {b} 실제 {c}  |{d}|')
    sys.exit(1)
for old,new,n in E: PA=[s.replace(old,new) for s in PA]
for k,w,old,new in T: TB[k]['caption']=TB[k]['caption'].replace(old,new)
json.dump(PA,open('recover/paras.json','w',encoding='utf-8'),ensure_ascii=False,indent=0)
json.dump(TB,open('recover/tables.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print(f'본문 {len(E)}건 · 표 캡션 {len(T)}건 적용')

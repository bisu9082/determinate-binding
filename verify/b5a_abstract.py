# -*- coding: utf-8 -*-
"""B5-a: 초록. 가장 많이 읽히는 곳이고, 원천(paras.json)에 있다."""
import json,os,sys
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
PA=json.load(open('recover/paras.json',encoding='utf-8'))
E=[('the predicate returns 91 and 34 survive the audit, a precision of 0.374',
    'the predicate returns 91 and 41 survive the audit, a precision of 0.451'),
   ('raising the aviation binding rate from 9.5% to 19.2%',
    'raising the aviation binding rate from 10.8% to 21.7%'),
   ('22 of the 23 audited bindings a civil unmanned aircraft carries cease to apply to a police one, 15 analytically and 7 by measurement',
    '25 of the 26 audited bindings a civil unmanned aircraft carries cease to apply to a police one, 18 analytically and 7 by measurement'),
   # hop0 -> hop4 증분: 반환 72->91(+19), 결속 37->41(+4), 따라서 위양성 +15. 불변.
   ('Following cross-references adds four bindings and fifteen false positives',
    'Following cross-references adds four bindings and fifteen false positives')]
bad=[(o[:80],sum(s.count(o) for s in PA)) for o,_ in E if sum(s.count(o) for s in PA)!=1]
if bad:
    print('치환 불가'); [print('  ',b,c) for b,c in bad]; sys.exit(1)
for o,n in E: PA=[s.replace(o,n) for s in PA]
json.dump(PA,open('recover/paras.json','w',encoding='utf-8'),ensure_ascii=False,indent=0)
print(f'초록 {len(E)}건 확인·적용')

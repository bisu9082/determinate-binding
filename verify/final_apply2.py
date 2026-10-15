# -*- coding: utf-8 -*-
"""구조적 주사(走査)가 찾아낸 잔존 구판 수치.

손으로 적은 목록이 아니라 '결속을 세는 어구'를 정규식으로 전수 추출해 측정과
대조하는 방식으로 찾았다. 손목록은 이미 네 번 샜다(F-10·F-11·F-14, 그리고 여기).
표 5 의 복원 행은 노드 4,594/4,826/5,508 과 반환 7/8/40 이 공개값과 정확히
일치해 추정기가 확정된 뒤 감사 열만 다시 셌다."""
import json,os,sys
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
PA=json.load(open('recover/paras.json',encoding='utf-8'))
TB=json.load(open('recover/tables.json',encoding='utf-8'))
E=[('On the civil route the predicate returns 54 provisions, of which 23 survive the audit.',
    'On the civil route the predicate returns 54 provisions, of which 26 survive the audit.'),
   ('Restoring the whole of Regulation 2018/1139 puts 14 audited bindings back in force on the police route, 13 of the 22 audited bindings the carve-out removes.',
    'Restoring the whole of Regulation 2018/1139 puts 18 audited bindings back in force on the police route, 17 of the 25 audited bindings the carve-out removes.'),
   ('the EU side contributes 15 audited bindings on the civil route and 0 on the police route',
    'the EU side contributes 18 audited bindings on the civil route and 0 on the police route'),
   ('the Korean robot instruments supply 30 authorising provisions and 2 audited bindings',
    'the Korean robot instruments supply 30 authorising provisions and 1 audited binding'),
   ('the Act now yields 4 audited bindings and the Korean Road Traffic Act yields 5',
    'the Act now yields 8 audited bindings and the Korean Road Traffic Act yields 5')]
bad=[(n,sum(s.count(o) for s in PA),o[:84]) for o,n in E if sum(s.count(o) for s in PA)!=1]
if bad:
    print('치환 불가'); [print(f'  실제 {b}  |{c}|') for a,b,c in bad]; sys.exit(1)
for o,n in E: PA=[s.replace(o,n) for s in PA]
cur=TB['5']['rows'][3][3]
if cur!='14': print(f'표5 복원 행 감사값이 14 가 아니다: {cur}'); sys.exit(1)
TB['5']['rows'][3][3]='18'
json.dump(PA,open('recover/paras.json','w',encoding='utf-8'),ensure_ascii=False,indent=0)
json.dump(TB,open('recover/tables.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print(f'본문 {len(E)}건 · 표 5 감사 열 1건 적용')

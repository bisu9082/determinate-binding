# -*- coding: utf-8 -*-
"""데이터 가용성: 실제 장치 수치 + GitHub 주소. 제노도는 쓰지 않는다(Ku 지시).

약속한 것과 실제가 달랐다. 523검사·12게이트 → 103검사·10게이트.
부록 B 는 같은 자리에서 '열한 게이트' 라고 적고 있었다 — 원고 안에서 이미 모순이었고
구판 검사 523개가 그것을 못 잡았다. 이제 게이트가 자기 수를 검사한다."""
import os,re,sys
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
URL='https://github.com/bisu9082/determinate-binding'
p='tex/back_v23.tex'; s=open(p,encoding='utf-8').read()
E=[
 # 같은 구절이 두 번 들어가 있었다(내 편집이 기존 구절 앞에 삽입되면서)
 ('the full binding audit with the labels of all three passes and the adjudication record of each, the permission-type classification with both passes and the rubric they were given, the full binding audit with the labels from both passes and the adjudication record for every provision a rule change moved,',
  'the full binding audit with the labels of all three passes and the adjudication record of each, the permission-type classification with both passes and the rubric they were given, the adjudication record for every provision a rule change moved,'),
 (("A consistency suite of 523 checks is released with them; it verifies that the numbers in "
   "the manuscript, the figures and the released outputs agree with one another. Twelve further "
   "gates are released beside it. They exist because the suite's pass count was not by itself "
   "informative,"),
  ("A consistency suite of 103 checks in nine gates is released with them, with a tenth that "
   "measures how weak one of the nine is; it verifies that the numbers in the manuscript, the "
   "tables, the figures and the typeset output agree with one another and with the measurement. "
   "The suite of the earlier version was lost with the working tree and is not recovered; what "
   "runs now was rebuilt to close the defect classes this project produced rather than to restore "
   "a pass count, and Appendix B states what that cost. They exist because a pass count was not "
   "by itself informative,")),
 ('We report coverage rather than pass counts because two of these gates were at one point repaired into a state in which they could not fail, and reported full passes while in it.',
  'We report coverage rather than pass counts because gates in this project were twice repaired into a state in which they could not fail and reported full passes while in it, and because three defects reached the typeset manuscript that no check on the source files could see.'),
]
m=re.search(r'No part of this material is withheld\. The archive will be deposited with a persistent identifier[^.]*\.',s)
if not m: print('기탁 문장을 못 찾았다'); sys.exit(1)
E.append((m.group(0),
 'No part of this material is withheld. The archive is at \\url{'+URL+'}; the commit this '
 'manuscript was built from is recorded in its CITATION.cff and in the manifest, and every file '
 'in it is pinned by SHA-256 in MANIFEST.sha256.'))
bad=[(o[:72],s.count(o)) for o,_ in E if s.count(o)!=1]
if bad:
    print('치환 불가'); [print('  ',a,b) for a,b in bad]; sys.exit(1)
for o,n in E: s=s.replace(o,n)
if '\\usepackage{url}' not in open('tex/main_v23.tex',encoding='utf-8').read():
    print('경고: url 패키지 없음')
open(p,'w',encoding='utf-8').write(s)
print(f'데이터 가용성 {len(E)}건 적용 · 주소 {URL}')

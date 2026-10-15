# -*- coding: utf-8 -*-
"""저자 확정 (2026-10-15 Ku 지시).

차장현(경찰청) → 신명식 → 박보연 → 한인애 → 강구(교신, 마지막).
표기는 reference_coauthors 정본을 따른다. Ku 가 교신이면 마지막 저자라는 상시 규칙.

중요: 1저자가 경찰청이므로 어제 뺀 면책의 경찰청을 되돌려야 한다.
저자 구성이 바뀌면 면책 대상 기관도 바뀐다 — 둘이 묶여 있다는 것을 게이트에 넣는다."""
import os,sys,re
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))

p='tex/main_v23.tex'; s=open(p,encoding='utf-8').read()
OLD='''\\author[cbrn]{Myeongsik Shin}
\\author[cbrn]{Ku Kang\\corref{cor}}
\\cortext[cor]{Corresponding author.}
\\ead{bisu9082@gmail.com}
\\address[cbrn]{Chemical, Biological, Radiological and Nuclear (CBRN) Defense Research Institute, Republic of Korea}'''
NEW='''%% 저자 확정 2026-10-15. ORCID 는 투고 시스템에 입력한다(elsarticle 본문에 넣지 않음).
%%   Janghyeon Cha  0009-0002-1419-1832  chajh6596@police.go.kr
%%   Myeongsik Shin 0009-0005-1189-4366  fhwm0448@snu.ac.kr
%%   Boyeon Park    0009-0001-1663-8207  kobir0601@gmail.com
%%   Inae Han       0009-0002-6336-4242  iahan0657@gmail.com
%%   Ku Kang        0000-0001-8739-218X  bisu9082@mnd.go.kr (교신)
\\author[knpa]{Janghyeon Cha}
\\author[cbrn]{Myeongsik Shin}
\\author[cbrn]{Boyeon Park}
\\author[cbrn]{Inae Han}
\\author[cbrn]{Ku Kang\\corref{cor}}
\\cortext[cor]{Corresponding author.}
\\ead{bisu9082@mnd.go.kr}
\\address[knpa]{Korean National Police Agency, Seoul, Republic of Korea}
\\address[cbrn]{Chemical, Biological, Radiological and Nuclear (CBRN) Defense Research Institute, Seoul, Republic of Korea}'''
if s.count(OLD)==1:
    s=s.replace(OLD,NEW)
elif '\\author[knpa]{Janghyeon Cha}' not in s:
    print('저자 블록을 못 찾았다'); sys.exit(1)
else:
    print('  저자 블록은 이미 적용됨')
# 복원 머리말이 낡았다. 도판·게이트는 이제 있다.
s=re.sub(r'%% 아직 복원하지 못한 것: 도판 4종 이미지\(측정 장치 재건 후 재생성 필요\),\n%% 검증 장치\(게이트 12종·523검사\), 근거 산출물 47종, 동결 기록 v18~v22\.\n%% RECOVERY_NOTE\.md 를 함께 볼 것\.',
 '%% 2026-10-15: 측정 장치·도판 4종·게이트(verify/gate.py, 99검사)를 모두 재건했다.\n'
 '%% 결속 정본은 labels/tpset.json (맹검 재정 41건).',s)
open(p,'w',encoding='utf-8').write(s)

# 후기: 면책 복원 + CRediT 5인
b='tex/back_v23.tex'; t=open(b,encoding='utf-8').read()
E=[('The views expressed are those of the authors and do not represent the official position of the Chemical, Biological, Radiological and Nuclear Defense Research Institute, of the Republic of Korea CBRN Defence Command, or of the Ministry of National Defense.',
    'The views expressed are those of the authors and do not represent the official position of the Korean National Police Agency, of the Chemical, Biological, Radiological and Nuclear Defense Research Institute, or of the Ministry of National Defense of the Republic of Korea.'),
   ('% [CONFIRM] 개별 기여 배분은 잠정이다. 저자 구성 확정 시 각 저자가 확인해야 한다.\n','')]
bad=[(o[:70],t.count(o)) for o,_ in E if t.count(o)!=1]
if bad: print('후기 치환 불가',bad); sys.exit(1)
for o,n in E: t=t.replace(o,n)
old_cr=re.search(r'\\textbf\{Myeongsik Shin:\}.*?\\section\*\{Declaration of competing',t,re.S)
if not old_cr: print('CRediT 블록을 못 찾았다'); sys.exit(1)
new_cr=('\\textbf{Janghyeon Cha:} Investigation, Resources, Writing -- review \\& editing. '
 '\\textbf{Myeongsik Shin:} Investigation, Data curation, Validation, Writing -- review \\& editing. '
 '\\textbf{Boyeon Park:} Investigation, Validation, Writing -- review \\& editing. '
 '\\textbf{Inae Han:} Investigation, Validation, Writing -- review \\& editing. '
 '\\textbf{Ku Kang:} Conceptualization, Methodology, Software, Formal analysis, Data curation, '
 'Writing -- original draft, Writing -- review \\& editing, Visualization, Supervision, '
 'Project administration.\n\n\\section*{Declaration of competing')
t=t[:old_cr.start()]+new_cr+t[old_cr.end():]
open(b,'w',encoding='utf-8').write(t)
print('저자 5인 · 소속 2곳 · CRediT · 면책 적용')

# -*- coding: utf-8 -*-
"""후기의 정본은 tex/back_v23.tex 다.

세 곳에 같은 글이 있었다: paras.json(조립이 본문으로 뽑아 중복 인쇄, 삭제됨),
recover/back.json(assemble 이 읽지 않는 죽은 산출물), tex/back_v23.tex(손으로
유지되며 조립이 덮어쓰지 않는 파일 = 실제 조판되는 것).
어느 것이 정본인지 확인하지 않고 두 번 고쳤다. 조판물을 그레이프해 확인했다."""
import os,sys
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
p='tex/back_v23.tex'; s=open(p,encoding='utf-8').read()
E=[('The views expressed are those of the authors and do not represent the official position of the Korean National Police Agency or of the Chemical, Biological, Radiological and Nuclear Defense Research Institute.',
    'The views expressed are those of the authors and do not represent the official position of the Chemical, Biological, Radiological and Nuclear Defense Research Institute, of the Republic of Korea CBRN Defence Command, or of the Ministry of National Defense.'),
   ('A large language model was used in two places in this study and both are reported in the Methods rather than only here.',
    'A large language model was used in four places in this study and all four are reported in the Methods or the Results rather than only here.'),
   ('It was also the instrument that re-wrote the search terms in the reliability test of Section 3.8.',
    'It was also the instrument that made the blind third pass over the enriched audit records reported in Section 2.7, and the instrument that classified the bindings by the kind of permission they condition in Section 3.3, in two independent passes over the provision texts against a rubric from which the counts had been removed. It was also the instrument that re-wrote the search terms in the reliability test of Section 3.8.'),
   ('the lexicons and their validation sample with labels, the full binding audit with the labels',
    'the lexicons and their validation sample with labels, the full binding audit with the labels of all three passes and the adjudication record of each, the permission-type classification with both passes and the rubric they were given, the full binding audit with the labels')]
bad=[(o[:78],s.count(o)) for o,_ in E if s.count(o)!=1]
if bad:
    print('치환 불가'); [print('  ',a,b) for a,b in bad]; sys.exit(1)
for o,n in E: s=s.replace(o,n)
open(p,'w',encoding='utf-8').write(s)
# 죽은 산출물에 표시를 남긴다
import json
B=json.load(open('recover/back.json',encoding='utf-8'))
B['_DEAD']='assemble_v23.py 는 이 파일을 읽지 않는다. 후기 정본은 tex/back_v23.tex 다.'
json.dump(B,open('recover/back.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print(f'후기 {len(E)}건 적용 (tex/back_v23.tex) · back.json 에 사망 표시')

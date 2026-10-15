# -*- coding: utf-8 -*-
"""후기(back matter)는 recover/back.json 이 정본이다. paras.json 에도 같은 글이
남아 있어 한쪽만 고치면 조판물은 그대로다(F-13 과 같은 함정). 양쪽을 맞춘다."""
import json,os,sys
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
B=json.load(open('recover/back.json',encoding='utf-8'))
E=[('The views expressed are those of the authors and do not represent the official position of the Korean National Police Agency or of the Chemical, Biological, Radiological and Nuclear Defense Research Institute.',
    'The views expressed are those of the authors and do not represent the official position of the Chemical, Biological, Radiological and Nuclear Defense Research Institute, of the Republic of Korea CBRN Defence Command, or of the Ministry of National Defense.'),
   ('A large language model was used in two places in this study and both are reported in the Methods rather than only here.',
    'A large language model was used in four places in this study and all four are reported in the Methods or the Results rather than only here.'),
   ('It was also the instrument that re-wrote the search terms in the reliability test of Section 3.8. It was additionally used to assist with language editing of the manuscript.',
    'It was also the instrument that made the blind third pass over the enriched audit records reported in Section 2.7, and the instrument that classified the bindings by the kind of permission they condition in Section 3.3, in two independent passes over the provision texts against a rubric from which the counts had been removed. It was also the instrument that re-wrote the search terms in the reliability test of Section 3.8. It was additionally used to assist with language editing of the manuscript.'),
   ('the lexicons and their validation sample with labels, the full binding audit with the labels',
    'the lexicons and their validation sample with labels, the full binding audit with the labels of all three passes and the adjudication record of each, the permission-type classification with both passes and the rubric they were given, the full binding audit with the labels')]
s=json.dumps(B,ensure_ascii=False)
bad=[(o[:80],s.count(o)) for o,_ in E if s.count(o)!=1]
if bad:
    print('치환 불가'); [print('  ',a,b) for a,b in bad]; sys.exit(1)
for o,n in E: s=s.replace(o,n)
json.dump(json.loads(s),open('recover/back.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print(f'후기 {len(E)}건 적용 (recover/back.json)')

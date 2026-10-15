# -*- coding: utf-8 -*-
"""B5-a 2차: 재계산 가능한 민감도·대안판정 수치. 전부 labels_final.json 에서 다시 센 값이다."""
import os,sys
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
P=chr(92)+'%'; R=chr(92)+'rightarrow'
E=[]
def ed(f,old,new,n=1): E.append((f,old,new,n))

# 부정문맥 가드 민감도: 40/88. EU947::art_5.1 은 41 정본에서도 결속이다(재확인).
ed('methods','drops two false positives and one binding, and leaves precision near unchanged at 0.374',
            'drops two false positives and one binding, and leaves precision near unchanged at 0.455')
# 조건(iii) 반대 방향. 소생 레코드는 12건, 전부 EU1139.
ed('methods','revives 19 of the records the adjudication rejects and gives 53 bindings instead of 34, a precision of 0.582 instead of 0.374',
            'revives 12 of the records the adjudication rejects and gives 53 bindings instead of 41, a precision of 0.582 instead of 0.451')
ed('methods',"n-to-ground ratio rises from 5.24 to 8.56 with Cohen's h from 0.357 to 0.567",
            "n-to-ground ratio rises from 4.34 to 6.35 with Cohen's h from 0.353 to 0.500")
ed('methods',f'in either direction (41 to 1 instead of 23 to 1)',f'in either direction (38 to 1 instead of 26 to 1)')
ed('methods',f'Includes (alternative) & 53 & 0.582 & 41/241 & 12/604 & 0/169 & 41 ${R}$ 1',
            f'Includes (alternative) & 53 & 0.582 & 38/241 & 15/604 & 0/169 & 38 ${R}$ 1')
ed('methods',f'Includes (alternative) 53 0.582 41/241 12/604 0/169 41 ${R}$ 1',
            f'Includes (alternative) 53 0.582 38/241 15/604 0/169 38 ${R}$ 1')
# 현행 비율비를 가리키는 서술
ed('results','the ratio reaches its current 5.24 only after','the ratio reaches its current 4.34 only after')

txt={}
for f in ('main','methods','results','discussion','appendix'):
    txt[f]=open(f'tex/{f}_v23.tex',encoding='utf-8').read()
bad=[(f,n,txt[f].count(o),o[:95]) for f,o,_,n in E if txt[f].count(o)!=n]
if bad:
    print('치환 불가 — 아무것도 적용하지 않았다')
    for f,e,g,o in bad: print(f'  {f}: 기대 {e} 실제 {g}  |{o}|')
    sys.exit(1)
for f,o,n_,_ in E: txt[f]=txt[f].replace(o,n_)
for f,s in txt.items(): open(f'tex/{f}_v23.tex','w',encoding='utf-8').write(s)
print(f'적용 {len(E)}건')

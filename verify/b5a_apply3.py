# -*- coding: utf-8 -*-
"""B5-a 3차: 결속 총계에 딸린 유도 수치. 전부 측정에서 다시 센 값이다."""
import os,sys
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
P=chr(92)+'%'
E=[]
def ed(f,old,new,n=1): E.append((f,old,new,n))

# --- 결속 총계를 세는 서술 ---
ed('results',f'Of the 34 audited bindings, 30 (88.2{P}) are visible in a single paragraph read alone',
            f'Of the 41 audited bindings, 37 (90.2{P}) are visible in a single paragraph read alone')
ed('results','The 34 audited bindings are not spread evenly','The 41 audited bindings are not spread evenly')
ed('results','We therefore repartitioned the same 34 audited bindings by subject matter',
            'We therefore repartitioned the same 41 audited bindings by subject matter')
ed('results','The same 34 audited bindings repartitioned by subject matter','The same 41 audited bindings repartitioned by subject matter')
ed('methods','supplies 32 of the 91 returns and 13 of the 34 bindings','supplies 32 of the 91 returns and 17 of the 41 bindings')
ed('results','The Japanese Road Traffic Act contributes 4 of the 34 bindings','The Japanese Road Traffic Act contributes 8 of the 41 bindings')
ed('results','Of the 11 ground bindings, 5 are in the Korean Road Traffic Act','Of the 15 ground bindings, 5 are in the Korean Road Traffic Act')
ed('discussion','Thirty of the 34 bindings are legible in a single paragraph read alone',
              'Thirty-seven of the 41 bindings are legible in a single paragraph read alone')

# --- 면제가 지우는 결속: 22/23 -> 25/26 ---
ed('results','The carve-out therefore removes 22 of the 23 audited technical bindings that a civil unmanned aircraft carries, 96',
            'The carve-out therefore removes 25 of the 26 audited technical bindings that a civil unmanned aircraft carries, 96')
ed('discussion','removes 22 of the 23 audited bindings that a civil unmanned aircraft carries',
              'removes 25 of the 26 audited bindings that a civil unmanned aircraft carries')
ed('results','Without this, the 22 reads as stronger than it is','Without this, the 25 reads as stronger than it is')
ed('results','and the 22 is a sum across two bodies of law','and the 25 is a sum across two bodies of law')

# --- 재현율 투영 (투영 누락 62 [23,145] 는 FN율에만 의존하므로 불변) ---
ed('results','34 audited bindings against 491 tier-1 provisions give a projection of 62 [23, 145] and recall 0.35 [0.19, 0.59]',
            '41 audited bindings against 491 tier-1 provisions give a projection of 62 [23, 145] and recall 0.40 [0.22, 0.64]')
ed('results','Audited 34 96 audited Audited + projected misses [57, 179]',
            'Audited 41 103 audited Audited + projected misses [64, 186]')

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

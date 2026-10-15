# -*- coding: utf-8 -*-
"""F-16: 후기가 PDF 에 두 번 나온다.

assemble 은 recover/back.json 의 구조화된 후기를 조판하고, 동시에 paras.json 에
남아 있는 같은 글을 본문 문단으로도 조판한다. 그 결과 CRediT·경쟁이익·AI 공시·
데이터 가용성·연구비·면책이 전부 두 번 인쇄된다.

정본은 back.json(절 이름으로 키가 잡혀 있다). paras.json 쪽 사본을 지운다.
경계는 'CRediT authorship contribution statement' 문단에서 시작해
'Appendix A.' 로 시작하는 문단 바로 앞까지로 단언한다."""
import json,os,sys,re
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
PA=json.load(open('recover/paras.json',encoding='utf-8'))
def n(s): return re.sub(r'\s+',' ',s).strip()
si=[i for i,s in enumerate(PA) if n(s)=='CRediT authorship contribution statement']
ei=[i for i,s in enumerate(PA) if n(s).startswith('Appendix A. The ten changes')]
if len(si)!=1 or len(ei)!=1 or not si[0]<ei[0]:
    print('경계 불확정',si,ei); sys.exit(1)
blk=list(range(si[0],ei[0]))
B=json.load(open('recover/back.json',encoding='utf-8'))
print(f'back.json 절 {len(B)}개: {", ".join(list(B))}')
print(f'삭제 대상 문단 {blk[0]}..{blk[-1]} ({len(blk)}개)')
for i in blk: print(f'   [{i:3d}] {n(PA[i])[:84]}')
if '--apply' not in sys.argv: print('\n드라이런. 적용은 --apply'); sys.exit(0)
json.dump([s for i,s in enumerate(PA) if i not in set(blk)],
          open('recover/paras.json','w',encoding='utf-8'),ensure_ascii=False,indent=0)
print(f'\n{len(blk)}개 삭제 ({len(PA)} → {len(PA)-len(blk)})')

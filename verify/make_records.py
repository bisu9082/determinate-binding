# -*- coding: utf-8 -*-
"""감사 기록 91건 생성 — §2.7 이 규정한 형식 그대로.

기록 하나에 들어가는 것: 조항 본문 / 발화한 모든 어휘 패턴과 실제로 일치한 문자열과
전후 85자 / 술어가 기록한 경로 / 평가어가 점화한 노드.

이 스크립트는 판정을 하지 않는다. 판정자가 볼 것을 만든다. 둘을 섞으면 판정이
자기 근거를 만들어 버린다."""
import json,re,sys,os
sys.path.insert(0,'probe'); sys.path.insert(0,'graph')
import lex2
os.makedirs('audit',exist_ok=True)
N=json.load(open('graph/nodes3.json',encoding='utf-8'))
P=json.load(open('graph/paths3.json',encoding='utf-8'))
CTX=85

def fires(text,pats,label):
    out=[]
    for p in pats:
        for m in re.finditer(p,text,re.I):
            a=max(0,m.start()-CTX); b=min(len(text),m.end()+CTX)
            out.append({'lexicon':label,'pattern':p,'matched':m.group(0),
                        'context':text[a:b]})
            break          # 패턴당 첫 일치만 (기록 비대 방지)
    return out

rE=re.compile('|'.join(lex2.EVAL),re.I)
recs=[]
for k,v in sorted(P.items()):
    if v['tier']!=2: continue
    txt=N[k]
    path=v['path']
    ign=None
    for nd in path:
        if rE.search(N.get(nd,'')):
            m=rE.search(N[nd]); ign={'node':nd,'matched':m.group(0),
                'context':N[nd][max(0,m.start()-CTX):m.end()+CTX]}
            break
    recs.append({
      'id':k,
      'doc':k.split('::')[0],
      'text':txt,
      'path':path,
      'path_len':len(path)-1,
      'evaluation_ignited_at':ign,
      'patterns':{
        'AUTH':fires(txt,lex2.AUTH,'AUTH'),
        'DET':fires(txt,lex2.DET,'DET'),
        'NONDET':fires(txt,lex2.NONDET,'NONDET'),
        'EVAL_own_text':fires(txt,lex2.EVAL,'EVAL'),
      },
    })
json.dump(recs,open('audit/records.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print(f'감사 기록 {len(recs)}건 생성 (목표 91)')
from collections import Counter
print('문서별:',dict(Counter(r['doc'] for r in recs)))
print('경로 길이별:',dict(Counter(r['path_len'] for r in recs)))
print('자기 본문에 평가어 있는 것:',sum(1 for r in recs if r['patterns']['EVAL_own_text']))

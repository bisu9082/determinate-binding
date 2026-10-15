# -*- coding: utf-8 -*-
"""안전제약 → 코퍼스 결속 탐색 1차 시험.
각 SC의 기능어(임무 분석에서 나온 것)로 조문 그래프를 검색한다. 저자가 만든 사전이 아니라
UCA 문장에서 추출한 기능어라는 점이 ⓐ(키워드 사전)와의 차이."""
import json,re,sys
sys.path.insert(0,'stpa'); sys.path.insert(0,'probe')
from uca_mg import UCA
N=json.load(open('graph/nodes3.json',encoding='utf-8'))
P=json.load(open('graph/paths3.json',encoding='utf-8'))
# SC별 기능어 — UCA/SC 문장에서 뽑은 명사구(수기 추출, 사전 아님)
FUNC={
 'SC-06-1':[r'calibrat\w*',r'교정',r'較正'], 'SC-06-2':[r'uncertaint\w*',r'repeat\w* (?:test|measur)',r'재검사',r'불확도'],
 'SC-06-3':[r'time window',r'within \d+ (?:minutes|hours)',r'기한'],
 'SC-04-1':[r'sampl\w+ (?:media|equipment|tool)',r'채취(?:기구|용기)',r'qualif\w+ for'],
 'SC-04-2':[r'contaminat\w*',r'오염',r'汚染'],
 'SC-08-1':[r'uncertaint\w*',r'measurement result',r'분석\s*결과'],
 'SC-08-2':[r'validat\w+ (?:scope|for)',r'provenance',r'적용\s*범위'],
 'SC-08-3':[r'without (?:undue )?delay',r'지체\s*없이',r'latency'],
 'SC-09-1':[r'performance (?:standard|requirement)',r'demonstrat\w+ (?:compliance|performance)',
            r'성능\s*(?:기준|시험)',r'적합성?\s*(?:평가|검사)',r'型式|認定'],
 'SC-09-2':[r'within \d+',r'이내에'], 'SC-09-3':[r'confirmat\w+'],
 'SC-09-4':[r'change of (?:circumstance|condition)',r'변경(?:된|되는) 경우',r'재승인|변경인증'],
 'SC-10-1':[r'chain of custody',r'보관\s*연속성',r'인계|인수'],
 'SC-10-2':[r'custody (?:record|log)',r'기록을 작성',r'log\w*'],
 'SC-11-1':[r'decontaminat\w*',r'제염'], 'SC-11-2':[r'release criterion|clearance',r'해제\s*기준'],
 'SC-01-1':[r'standard operating procedure|\bSOP\b',r'표준\s*작업|운영\s*절차'],
 'SC-01-2':[r'record the reason',r'사유를 기록'],
}
rows=[]
for u in UCA:
    sc=u[5].split(':')[0]
    pats=FUNC.get(sc,[])
    if not pats: rows.append((sc,0,0,[])); continue
    R=re.compile("|".join(pats),re.I)
    hit=[k for k,v in N.items() if R.search(v)]
    t2=[k for k in hit if P.get(k,{}).get('tier')==2]
    t1=[k for k in hit if P.get(k,{}).get('tier')==1]
    rows.append((sc,len(t2),len(t1),t2[:3]))
print(f"{'SC':10s}{'Tier2':>7s}{'Tier1':>7s}   예시")
print('-'*76)
for sc,a,b,ex in rows:
    print(f"{sc:10s}{a:>7}{b:>7}   {', '.join(x.split('::')[0]+':'+x.split('::')[1] for x in ex)[:52]}")
z=[r[0] for r in rows if r[1]==0]
print(f"\nTier2 결속 0인 안전제약 {len(z)}/{len(rows)}건:")
print("  "+", ".join(z))

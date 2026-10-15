# -*- coding: utf-8 -*-
"""M-G 안전제약 30건 × 코퍼스 결속. 기능어는 UCA/SC 문장에서 추출(수기, Methods에 명시)."""
import json,re,sys
from collections import defaultdict,deque,Counter
sys.path.insert(0,'stpa'); sys.path.insert(0,'probe')
from uca_mg import UCA
from carveout import N,build,tier_of
FUNC={
 'SC-01-1':[r'standard operating procedure|\bSOP\b',r'표준\s*(?:작업|운영)\s*절차'],
 'SC-01-2':[r'record the reason|사유를 기록|이유를 기재'],
 'SC-02-1':[r'withdraw\w*|철수|중지 명령',r'change of (?:circumstance|condition)|사정변경'],
 'SC-02-2':[r'disposition|처분|인계',r'sample|시료|검체'],
 'SC-02-3':[r'dose limit|선량한도|누적선량',r'threshold|임계|한도'],
 'SC-03-1':[r'decontaminat\w*|제염',r'resistan\w*|내성'],
 'SC-03-2':[r'dwell|체류|잔류 시간',r'tolerance|허용'],
 'SC-03-3':[r'egress|이탈 경로|반출',r'decontaminat\w*|제염'],
 'SC-04-1':[r'sampl\w+ (?:media|equipment|tool|container)',r'채취(?:기구|용기|장비)',r'qualif\w+ for'],
 'SC-04-2':[r'contaminat\w*|오염'],
 'SC-05-1':[r'lost link|loss of (?:the )?(?:command and control|C2) link|통신\s*두절',
            r'emergency stop|비상\s*정지|긴급\s*정지'],
 'SC-05-2':[r'manipulator|조작기|매니퓰레이터',r'sample (?:container|holder)|시료\s*용기'],
 'SC-05-3':[r'resum\w*|재개',r'explicit (?:human )?(?:instruction|command)|명시적\s*지시'],
 'SC-06-1':[r'calibrat\w*|교정|較正'],
 'SC-06-2':[r'uncertaint\w*|불확도',r'재검사|repeat\w* (?:test|measur)|confirmatory'],
 'SC-06-3':[r'time window|시간\s*범위|이내에 측정'],
 'SC-07-1':[r'safe state|안전\s*상태|fail-?safe',r'recover\w*|회수'],
 'SC-07-2':[r'sensor|센서|감지기',r'validat\w*|검증|유효성'],
 'SC-07-3':[r'dropout|두절\s*시간|link loss duration'],
 'SC-08-1':[r'uncertaint\w*|불확도',r'measurement result|분석\s*결과|측정\s*결과'],
 'SC-08-2':[r'validat\w+ (?:scope|for)|적용\s*범위',r'provenance|출처'],
 'SC-08-3':[r'without (?:undue )?delay|지체\s*없이|latency'],
 'SC-09-1':[r'performance (?:standard|requirement)|성능\s*(?:기준|시험)',
            r'demonstrat\w+ (?:compliance|performance)',r'적합성?\s*(?:평가|검사)',r'型式|認定'],
 'SC-09-2':[r'within \d+|이내에'],
 'SC-09-3':[r'confirmat\w*|확인\s*검사'],
 'SC-09-4':[r'change of (?:circumstance|condition)|변경(?:된|되는) 경우',r'재승인|변경인증'],
 'SC-10-1':[r'chain of custody|보관\s*연속성|인계|인수'],
 'SC-10-2':[r'custody (?:record|log)|기록을 작성|logs? of'],
 'SC-11-1':[r'decontaminat\w*|제염'],
 'SC-11-2':[r'release criterion|clearance|해제\s*기준'],
}
from scope import admissible
if __name__=='__main__':
    allowed=set(N); ADJ=build(allowed)
    print(f"{'안전제약':10s}{'매칭':>6s}{'인가항':>7s}{'T2':>4s}{'T1':>4s}  판정")
    print('-'*70)
    CLS=Counter(); rows=[]
    for u in UCA:
        sc=u[5].split(':')[0]
        pats=FUNC.get(sc)
        if not pats: continue
        R=re.compile("|".join(pats),re.I)
        hit=[k for k in sorted(allowed) if admissible(sc,k) and R.search(N[k])]
        tiers={k:tier_of(k,ADJ,allowed) for k in hit}
        auth=[k for k,t in tiers.items() if t is not None]
        t2=sum(1 for k in auth if tiers[k]==2); t1=sum(1 for k in auth if tiers[k]==1)
        if not hit: c='개념 부재'
        elif not auth: c='인가조항 아님'
        elif t2==0: c='영점'
        else: c=f'확정결속 {t2}'
        CLS[c.split()[0]]+=1; rows.append((sc,len(hit),len(auth),t2,t1,c))
        print(f"{sc:10s}{len(hit):>6}{len(auth):>7}{t2:>4}{t1:>4}  {c}")
    print('-'*70)
    for k,v in CLS.most_common(): print(f"  {k:12s}{v:>3}건")
    json.dump([dict(sc=r[0],hits=r[1],auth=r[2],t2=r[3],t1=r[4],cls=r[5]) for r in rows],
              open('stpa/match_mg.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)

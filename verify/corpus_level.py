# -*- coding: utf-8 -*-
"""기능어 등록부를 전혀 쓰지 않는 코퍼스 수준 측정.
보류집합 검증(κ=0.192)으로 제약 수준 매칭의 재현성이 무너졌으므로,
어휘집 + 그래프 + 면제규칙만으로 성립하는 것이 무엇인지 확정한다."""
import json,sys,collections
sys.path.insert(0,'stpa'); sys.path.insert(0,'graph'); sys.path.insert(0,'probe')
from scope import DOMAIN
import paths3 as P
from carveout import ap_nodes
N=P.N; E=P.E
full=P.run(E,4); iso=P.run([],4)
t=collections.Counter(v[0] for v in full.values())
print(f"[1] 인가항 {len(full)} · Tier2 {t[2]} · Tier1 {t[1]} · Tier0 {t[0]}")

d=collections.Counter(); tot=collections.Counter()
for k,v in full.items():
    dm=DOMAIN[k.split('::')[0]]; tot[dm]+=1
    if v[0]==2: d[dm]+=1
print("\n[2] 영역별 결속 전환율 (기능어 미사용)")
for dm in ('aviation','ground','crosscut'):
    print(f"    {dm:10s} 인가항 {tot[dm]:>4} · Tier2 {d[dm]:>3} · {d[dm]/tot[dm]*100:>5.1f}%")
# 비율차 효과크기 (Cohen's h)
import math
def h(p1,p2): return abs(2*math.asin(math.sqrt(p1))-2*math.asin(math.sqrt(p2)))
pa,pg=d['aviation']/tot['aviation'], d['ground']/tot['ground']
print(f"    항공 vs 지상: 비율비 {pa/pg:.2f}배 · Cohen's h = {h(pa,pg):.3f}")

only=[k for k in full if full[k][0]==2 and iso[k][0]<2]
print(f"\n[3] 경로 기여: 조문 고립 Tier2 {sum(1 for v in iso.values() if v[0]==2)} → hop4 {t[2]}")
print(f"    경로로만 성립 {len(only)}건 ({len(only)/t[2]*100:.1f}%) · 소실 0건")

apset,drop=ap_nodes()
apfull=P.run([e for e in E if e[0] in apset and e[1] in apset],4)
apfull={k:v for k,v in apfull.items() if k in apset}
av_ac=[k for k,v in full.items() if v[0]==2 and DOMAIN[k.split('::')[0]]=='aviation']
av_ap=[k for k,v in apfull.items() if v[0]==2 and DOMAIN[k.split('::')[0]]=='aviation']
print(f"\n[4] 면제의 코퍼스 수준 효과 (항공 영역)")
print(f"    민간경로 Tier2 {len(av_ac)} → 경찰경로 Tier2 {len(av_ap)} "
      f"({(1-len(av_ap)/len(av_ac))*100:.0f}% 소멸)")
print(f"    경찰경로 생존: {sorted(av_ap)}")
print(f"    삭제 노드 {len(drop)} / {len(N)}")
json.dump({'auth':len(full),'t2':t[2],'t1':t[1],'t0':t[0],
           'domain':{dm:[tot[dm],d[dm]] for dm in tot},
           'path_only':len(only),'iso_t2':sum(1 for v in iso.values() if v[0]==2),
           'av_ac_t2':len(av_ac),'av_ap_t2':len(av_ap),'av_ap_survivors':sorted(av_ap)},
          open('verify/corpus_level.json','w'),ensure_ascii=False,indent=1)

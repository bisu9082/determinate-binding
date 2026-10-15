# -*- coding: utf-8 -*-
"""구성타당도 점검: 유도된 안전제약 44건이 기존 22개 수기 통제항목을 재현하는가.
매핑은 의미 판단이므로 수기이며, 그 사실을 명시한다."""
MAP={
 'N01':['SCA-01-1','SC-01-1'], 'N02':['SC-03-1','SC-06-1'],
 'N03':['SC-09-1','SC-09-2','SC-09-3','SCA-01-2'], 'N04':['SC-08-1','SC-08-3'],
 'N05':['SC-09-4','SCA-01-2'], 'N06':['SC-06-1','SC-06-2','SC-08-1','SC-08-2','CC-09-1','CC-06-1','CC-04-1','CC-07-1'],
 'N07':['SC-08-2','SC-09-1'], 'N08':['SC-02-1','SCA-02-1','CC-02-1'],
 'N09':['SC-10-2','SC-01-2'], 'N10':['SC-07-1','SC-07-2','SC-07-3','SCA-06-1','SCA-06-2','CC-07-1'],
 'N11':['SC-05-1','SC-05-2','SC-05-3','SCA-05-1','SCA-05-2'],
 'N12':['SC-02-1','SC-02-2','SC-02-3','SC-03-2'],
 'N13':['SC-09-1','SCA-03-1','CC-A03-2'],
 'N14':['CC-05-1','CC-09-2','CC-A03-1','CC-A03-2'],
 'N15':['CC-05-2','CC-09-1','CC-06-1','CC-04-1','CC-10-1','CC-A04-1'],
 'N16':['SCA-03-1','SCA-03-2','SC-05-2'],
 'N17':['SC-10-1','SC-10-2','SC-11-1','SCA-07-1','SCA-07-2','CC-10-1'],
 'N18':['SC-04-1','SC-04-2','SC-06-1','SC-06-2','SC-06-3'],
 'N19':['SC-03-1','SC-03-3','SC-11-1','SC-11-2','SC-04-2'],
 'N20':['SCA-04-1','SCA-04-2','CC-A04-1'],
 'N21':['AC-1','AC-2','AC-5'], 'N22':['AC-2','AC-4','AC-7'],
}
NAMES={}
cov=[k for k,v in MAP.items() if v]; un=[k for k,v in MAP.items() if not v]
import json
mg={r['sc'] for r in json.load(open('stpa/match_mg.json',encoding='utf-8'))}
ma={r['sc'] for r in json.load(open('stpa/compare_ma.json',encoding='utf-8'))}
import sys; sys.path.insert(0,'stpa')
from scenarios import SCEN
from accountability import ELEMENTS
cc={s[4].split(':')[0] for s in SCEN}; ac={e[0] for e in ELEMENTS}
allsc=mg|ma|cc|ac
used={s for v in MAP.values() for s in v}
print(f"기존 22개 통제항목 중 유도가 재현한 것 {len(cov)}/22")
print(f"재현 실패 {len(un)}건:")
for k in un: print(f"   {k}  {NAMES[k]}")
print(f"\n유도 제약 {len(allsc)}건 = 안전제약 {len(mg|ma)} + 인과제약 {len(cc)} + 책무성 {len(ac)}")
print(f"기존 항목에 매핑된 제약 {len(used & allsc)}건 · 매핑 안 된 제약 {len(allsc-used)}건")
if allsc-used: print("   신규(기존 22개에 없던 제약):", sorted(allsc-used))

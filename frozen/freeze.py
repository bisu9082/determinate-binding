# -*- coding: utf-8 -*-
"""규칙 동결 — 판정에 영향을 주는 모든 파일의 SHA256을 기록한다. 이후 변경은 재동결을 요구한다."""
import hashlib,json,os,datetime
FILES=[
 'probe/lex2.py',            # 어휘집 v2 (EVAL/AUTH/DET/NONDET/PENALTY/DET_EXCLUDE)
 'graph/extract2.py',        # 조문 노드 추출
 'graph/chapters.py',        # EU 장/절 구조
 'graph/edges2.py',          # 참조 엣지
 'graph/edges3.py',          # 구조참조 + 장 포함엣지
 'graph/paths3.py',          # 경로 탐색·Tier 판정
 'stpa/structure.py',        # 제어구조
 'stpa/uca_mg.py',           # M-G UCA 30
 'stpa/uca_ma.py',           # M-A UCA 14
 'stpa/scenarios.py',        # 손실 시나리오 12
 'stpa/accountability.py',   # 책무성 7
 'stpa/scope.py',            # 적용범위 제한
 'stpa/carveout.py',         # 면제 = 노드 삭제
 'stpa/match_mg.py',         # M-G 기능어
 'stpa/compare.py',          # M-A 기능어
 'corpus/MANIFEST.json',     # 코퍼스 해시 목록
 'frozen/adjudicate.py',     # 판정 실행기 (4수준 분류 산출)
 'stpa/coverage.py',         # 구성타당도 대조
 'stpa/termproc.py',         # 기능어 추출 T1/T2 계측
 'verify/lex_validation.py', # 어휘집 타당성 라벨
]
import sys
VER = sys.argv[1] if len(sys.argv)>1 else 'v1'
REASON = sys.argv[2] if len(sys.argv)>2 else ''
rec={'ruleset_version':VER,'refreeze_reason':REASON,
     'frozen_at':datetime.datetime.now().isoformat(timespec='seconds'),'files':{}}
for f in FILES:
    b=open(f,'rb').read()
    rec['files'][f]={'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
agg=hashlib.sha256(''.join(rec['files'][f]['sha256'] for f in FILES).encode()).hexdigest()
rec['ruleset_sha256']=agg
json.dump(rec,open('frozen/RULESET_FROZEN.json','w'),indent=1)
print(f"동결 파일 {len(FILES)}개")
for f in FILES: print(f"  {rec['files'][f]['sha256'][:16]}  {rec['files'][f]['bytes']:>8,}B  {f}")
print(f"\n★ RULESET SHA256 = {agg}")
print(f"  버전 {VER} · 동결 시각 {rec['frozen_at']}")
if REASON: print(f"  재동결 사유: {REASON}")

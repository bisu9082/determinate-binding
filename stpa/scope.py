# -*- coding: utf-8 -*-
"""적용범위 제한 — 임무의 플랫폼이 결속될 수 있는 규제 영역을 한정한다.
항공 임무의 제약이 지상로봇 인증에 걸리는 교차매칭을 차단한다."""
# 문서 → 규제 영역
DOMAIN = {
 'US107':'aviation', 'USAC':'aviation', 'US89':'aviation',
 'EU1139':'aviation', 'EU947':'aviation', 'EU945':'aviation',
 'KR도로교통법':'ground', 'KR도로교통법시행규칙':'ground',
 'KR지능형로봇법':'ground', 'KR지능형로봇법시행령':'ground',
 'JP道交法':'ground',
 'LED':'crosscut', 'EUAI':'crosscut',          # 데이터·AI 규율: 플랫폼 불문
 'SMC1418':'crosscut', 'CAGOV':'crosscut',     # 경찰 장비 거버넌스: 플랫폼 불문
 'MID':'crosscut',                             # 법정계량(측정기기 지침): 플랫폼 불문 (2026-09-20 편입)
}
# 임무 → 허용 영역
MISSION_SCOPE = {'M-G':{'ground','crosscut'}, 'M-A':{'aviation','crosscut'}}
def scope_of(sc):
    """안전제약 id로 임무를 판별한다. SCA-* = M-A, 그 외 = M-G. CC-A*/AC-* 처리 포함."""
    if sc.startswith('SCA-') or sc.startswith('CC-A'): return MISSION_SCOPE['M-A']
    if sc.startswith('AC-'): return {'ground','aviation','crosscut'}   # 책무성은 플랫폼 불문
    return MISSION_SCOPE['M-G']
def admissible(sc, node_id):
    return DOMAIN.get(node_id.split('::')[0]) in scope_of(sc)
if __name__=='__main__':
    for m,s in MISSION_SCOPE.items():
        docs=[d for d,v in DOMAIN.items() if v in s]
        print(f"  {m}: {sorted(s)} → 문서 {len(docs)}개 {docs}")

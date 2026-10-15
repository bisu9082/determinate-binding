# -*- coding: utf-8 -*-
"""[지위] verify/gate.py GATE 3 가 이 검사를 포함한다. 여기는 단독 실행용 축약판이고,
연혁 등재 목록이 갈라지면 둘 다 틀린다. 등재는 양쪽에 같이 넣을 것.

본문이 적은 수치가 현행 측정과 어긋나는 곳을 전수로 센다.

B3 에서 결속 정본이 34 → 41 로 바뀌었다. 도판은 측정에서 다시 그렸으므로
본문만 구판 수치를 들고 있다. 그 어긋남을 조용히 두지 않고 기계로 드러낸다."""
import json,re,os,sys
# 연혁 표현 허용 목록. 각 항목은 "구판 수치를 적는 것이 맞는 자리"다.
# 허용 목록이 없으면 체커가 정당한 연혁까지 실패로 띄우고, 그러면 아무도 안 본다.
HISTORY=[
 # (앵커, 사유)
 ("Lexicon false-negative rate & 11.1% & 12.6%",
  "열개 변경 표의 before 열. 11.1%는 변경 전 실측값이다"),
 ("the precision, which rises from 0.374 to 0.451",
  "2.7절 재정 공개 문단. 구판을 구판으로 명시하는 자리다"),
 ("pooled false-negative rate from 11.1% to 11.4%",
  "변경별 델타 서술. 11.1%는 그 변경 직전 값이다"),
]
# 재계산 불가 — 변경을 하나씩 끈 상태의 감사 결속수가 필요하고,
# 끈 상태에서 반환되는 조항에는 라벨이 없다. 신규 판정 없이는 못 고친다.
BLOCKED=[
 # 2026-10-15: 네 건 모두 해소됐다. 변경 ⑤·⑦ 의 공개 수치 10종이 구판 입력으로
 # 전부 재현되어(verify/b5bd_apply.py 머리말) 재계산 불가가 아니었음이 밝혀졌다.
 # 면제가 남아 있으면 그 자리는 더 이상 검사받지 않는다. 그래서 비운다.
]

def cnt(txt,pat):
    # 앞이 숫자나 소수점이면 더 긴 수치의 일부다 (1.8% in 11.8%)
    out=[]
    for m in re.finditer(re.escape(pat),txt):
        if m.start()>0 and txt[m.start()-1] in '0123456789.': continue
        seg=txt[max(0,m.start()-90):m.end()+90]
        if any(a in seg for a,_ in HISTORY+BLOCKED): continue
        out.append(m)
    return len(out)
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
M=json.load(open('verify/fig_measures.json',encoding='utf-8'))
S=M['by_subject']; D=M['by_domain']; CO=M['carveout']; H=M['by_hop']
# F-10: 초록은 main_v23.tex 에 있다. 이 파일을 빼면 가장 많이 읽히는 곳을 못 센다.
TXT=''.join(open(f'tex/{x}_v23.tex',encoding='utf-8').read()
            for x in ('front','methods','results','discussion','appendix','back','main'))
TXT=re.sub(r'\s+',' ',TXT)
# 본문은 퍼센트를 \\% 로 쓴다. 정규화하지 않으면 9.5% 같은 표현을 한 건도 못 센다.
TXT=TXT.replace(chr(92)+'%','%').replace('{,}',',')
sub={s['subject']:s for s in S}; dom={d['domain']:d for d in D}
# (구판 표현, 현행 값, 설명)
CHECKS=[
 ('34 are bindings',          H['hop4']['audited'],'결속 총계'),
 ('0.374',                    round(H['hop4']['precision'],3),'정밀도'),
 ('3.4%',                     f"{H['hop4']['audited']/H['hop4']['auth']*100:.1f}%",'코퍼스 전체 결속률'),
 ('23 of the 23',             None,'(참고)'),
 ('the audited counts 23 and 1',
   f"the audited counts {CO['civil_route']['audited']} and {CO['police_route']['audited']}",'경로 비교'),
 ('15 are EU and 8 are US',
   f"{CO['civil_route']['eu']} are EU and {CO['civil_route']['us']} are US",'민간경로 내역'),
 ('9.5%',  f"{sub['Aviation certification']['rate']*100:.1f}%",'항공 인증 결속률'),
 ('1.8%',  f"{dom['ground']['rate']*100:.1f}%",'지상 결속률'),
 ('5.24',  round(sub['Aviation certification']['rate']/dom['ground']['rate'],2),'항공/지상 비율비'),
 ('11.1%', f"{M['lexicon_validation']['pooled']['rate']*100:.1f}%",'풀링 위음성률'),
 ('four bindings and six false', None,'(참고)'),
]
bad=[]
for old,new,why in CHECKS:
    if new is None: continue
    n=cnt(TXT,old)
    if n and str(old)!=str(new):
        bad.append((old,new,why,n))
print(f"{'본문 표현':34s}{'현행 측정':>12s}  설명 (등장 횟수)")
print('-'*76)
for old,new,why,n in bad:
    print(f'{old:34s}{str(new):>12s}  {why} ({n}회)')
print(f'\n어긋난 표현 {len(bad)}종 · 등장 {sum(x[3] for x in bad)}회')
if bad:
    print('본문이 구판(결속 34) 수치를 들고 있다. 고치거나 연혁으로 등재해야 한다.')
else:
    print('본문·표·도판이 모두 현행 측정(결속 41)과 일치한다.')

# 면제한 자리를 숨기지 않는다. 이 목록이 길어지는 것이 곧 부채다.
print(f'\n[연혁 등재 {len(HISTORY)}건] 구판 수치를 적는 것이 맞는 자리')
for a,why in HISTORY: print(f'  · {why}')
print(f'\n[재계산 불가 {len(BLOCKED)}건] 신규 판정 없이는 못 고친다')
for a,why in BLOCKED: print(f'  · {a[:52]:54s} {why}')
print('  상세: recover/b5a_blocked.md')
sys.exit(1 if bad else 0)

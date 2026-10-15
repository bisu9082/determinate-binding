# -*- coding: utf-8 -*-
"""F-12: 조판표의 평문 메아리 제거.

v23 복원은 v22 PDF 텍스트 레이어에서 문단을 떴다. 그 과정에서 조판된 표의 내용이
문단으로도 잡혔고, assemble 이 tables.json 으로 표를 다시 조판하므로 모든 표가
PDF 에 두 번 나온다(평문 메아리 + 진짜 표).

판정은 추측이 아니라 대조다. 메아리는 v22 당시의 셀 값으로 되어 있으므로,
B5-a 편집 이전 tables.json(git HEAD)의 셀 값과 정확히 맞춰 본다.
캡션 바로 뒤에서 연속으로 맞는 문단만 지우고, 처음 안 맞는 곳에서 멈춘다."""
import json,os,sys,re,subprocess
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
PA=json.load(open('recover/paras.json',encoding='utf-8'))
ORIG=json.loads(subprocess.run(['git','show','HEAD:recover/tables.json'],
                 capture_output=True,text=True,check=True).stdout)
DRY='--apply' not in sys.argv
def norm(s): return re.sub(r'\s+',' ',s.replace('$\\le$','≤').replace('$\\rightarrow$','→')).strip()

kill=[]; TRUNC=[]
for key,v in ORIG.items():
    rows=v['rows']
    ci=[i for i,x in enumerate(PA) if norm(x).startswith(f'Table {key}:')]
    if len(ci)!=1:
        print(f'  표 {key}: 캡션 {len(ci)}개 — 건너뜀'); continue
    c=ci[0]
    # 각 행(헤더 포함)의 셀을 모두 품은 문단이면 그 행의 메아리다.
    def row_of(n):
        for ri,r in enumerate(rows):
            cells=[norm(x) for x in r if x and x.strip()]
            if len(cells)<2: continue
            if all(x in n for x in cells): return ri
        return None
    # 표 1 은 PDF 에서 줄바꿈되어 한 문단이 여러 행에 걸친다. 숫자 3연을 본다.
    nums={ri:[norm(x) for x in r[-3:] if re.fullmatch(r'[\d,]+',norm(x))] for ri,r in enumerate(rows)}
    def wrapped(n):
        return any(len(ns)==3 and all(x in n for x in ns) for ns in nums.values())
    CODES=[norm(r[0]) for r in rows[1:] if norm(r[0])]
    def coded(n):
        return len(n)<230 and any(cd and cd in n for cd in CODES) and len(re.findall(r'\d',n))>=2
    STOP=re.compile(r'^(\(a\)|\d+\.\d+\.|Figure \d)')
    def frag(n):   # 줄바꿈된 헤더 조각
        return len(n.split())<=10 and not re.search(r'\d',n)
    # 캡션 문단 자체에 헤더 행이 이어 붙은 경우가 있다(표 1). 거기서 잘라낸다.
    hdr=' '.join(norm(x) for x in rows[0] if x and x.strip())
    if hdr and hdr in norm(PA[c]):
        TRUNC.append((c,hdr))
    j=c+1; block=[]; seen=set(); pend=[]
    while j<len(PA):
        n=norm(PA[j])
        if STOP.match(n): break
        ri=row_of(n)
        if ri is None and not wrapped(n) and not coded(n):
            if frag(n) and len(pend)<2: pend.append(j); j+=1; continue
            break
        if ri is not None: seen.add(ri)
        block+=pend; pend=[]; block.append(j); j+=1
    if block:
        kill+=block
        print(f'  표 {key}: 문단 {block[0]}..{block[-1]} ({len(block)}개) · 맞춘 행 {len(seen)}/{len(rows)}')
    else:
        print(f'  표 {key}: 메아리 없음')
print(f'\n총 {len(kill)}개 제거 (전체 {len(PA)})')
if DRY:
    for b in kill: print(f'  [{b:3d}] {norm(PA[b])[:112]}')
    print('드라이런. 적용은 --apply')
else:
    for ci_,hdr in TRUNC:
        t=PA[ci_]; k=re.sub(r'\s+',' ',t).find(hdr)
        # 원문은 줄바꿈을 품으므로 정규화 인덱스를 그대로 못 쓴다. 토큰으로 자른다.
        first=hdr.split()[0]
        idx=t.rfind('\n'+first)
        if idx<0: idx=t.rfind(' '+first)
        if idx>0: PA[ci_]=t[:idx].rstrip()
        else: print(f'  경고: 문단 {ci_} 절단 실패')
    ks=set(kill)
    json.dump([s for i,s in enumerate(PA) if i not in ks],
              open('recover/paras.json','w',encoding='utf-8'),ensure_ascii=False,indent=0)
    print(f'적용 완료 — 문단 {len(kill)}개 삭제, {len(TRUNC)}개 절단')

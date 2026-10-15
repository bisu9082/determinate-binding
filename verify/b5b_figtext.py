# -*- coding: utf-8 -*-
"""F-15: 구판 도판의 텍스트 레이어가 본문 문단으로 들어와 있다.

v22 PDF 에서 문단을 뜰 때 조판된 그림 4장의 글자가 함께 잡혔다. 2단 패널의 글이
뒤섞여 한 문단이 되었고("The sensing subsystem never classifies. The determination
is a human act taken Does any provision make..."), B4 에서 도판을 전부 다시 그렸으므로
이 글은 구판 수치를 지고 본문에 남은 잡음이다.

경계는 추측하지 않는다. 각 블록은 첫 패널 라벨 '(a) ...' 에서 시작해 진짜 캡션
'Figure N: ...' 바로 앞에서 끝난다. 시작과 끝 문단의 내용을 단언한다."""
import json,os,sys,re
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
PA=json.load(open('recover/paras.json',encoding='utf-8'))
def n(s): return re.sub(r'\s+',' ',s).strip()
BLOCKS=[('(a) Measurement and determination are separate acts','Figure 1:'),
        ('(a) Paths add returns, not bindings','Figure 2:'),
        ('(a) Bindings concentrate in aviation','Figure 3:'),
        ('(a) The form exists','Figure 4:')]
kill=[]
for start,endcap in BLOCKS:
    si=[i for i,s in enumerate(PA) if n(s).startswith(start)]
    ei=[i for i,s in enumerate(PA) if n(s).startswith(endcap)]
    if len(si)!=1 or len(ei)!=1:
        print(f'  경계 불확정: {start[:34]} 시작 {len(si)} 끝 {len(ei)}'); sys.exit(1)
    s,e=si[0],ei[0]
    if not s<e: print(f'  순서 이상: {s} {e}'); sys.exit(1)
    kill+=list(range(s,e))
    print(f'  {endcap:10s} 문단 {s}..{e-1} ({e-s}개) 삭제, 캡션 {e} 유지')
if '--apply' not in sys.argv:
    print(f'\n총 {len(kill)}개. 드라이런. 적용은 --apply'); sys.exit(0)
ks=set(kill)
json.dump([s for i,s in enumerate(PA) if i not in ks],
          open('recover/paras.json','w',encoding='utf-8'),ensure_ascii=False,indent=0)
print(f'\n{len(kill)}개 삭제 완료 ({len(PA)} → {len(PA)-len(kill)})')

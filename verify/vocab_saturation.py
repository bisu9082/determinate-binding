# -*- coding: utf-8 -*-
"""증거 어휘의 포화도. 부록 B 가 이 출력에 대고 쓰인다.

'원고의 모든 측정값이 공개 산출물에서 유도 가능하다' 는 검사는 값을 비교할 뿐
출처를 비교하지 않는다. 공개 산출물의 모든 수를 소수 1·2·3자리로 반올림하고
비율을 퍼센트로 바꾸어 어휘를 만들면, 날조된 값이 어떤 공개 수와 우연히 일치하는
것만으로 통과한다. 그 통과가 얼마나 쉬운지를 세어 둔다 — 어휘가 이미 들고 있는
소수값의 비율이 그 바(bar)의 낮이다.

자기참조 금지: 이 스크립트의 출력(vocab_saturation.json)은 어휘에서 제외한다.
제외하지 않으면 어휘가 자기 숫자로 불어나고 포화도가 저절로 올라간다."""
import json,os,re,sys,glob
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
SELF='verify/vocab_saturation.json'
SRC=[]
for pat in ('verify/*.json','labels/*.json','audit/*.json','classify/*.json',
            'frozen/*.json','graph/paths*.json','corpus/MANIFEST.json','stpa/*.json'):
    SRC+=[f for f in glob.glob(pat) if os.path.abspath(f)!=os.path.abspath(SELF)]
SRC=sorted(set(SRC))
NUM=re.compile(r'-?\d+(?:\.\d+)?')
vals=set()
for f in SRC:
    try: txt=open(f,encoding='utf-8').read()
    except Exception: continue
    for m in NUM.finditer(txt):
        try: v=float(m.group(0))
        except ValueError: continue
        vals.add(v)
        if 0.0<=v<=1.0: vals.add(v*100)     # 비율 → 퍼센트 (원고 문언: 이 방향만)
voc={1:set(),2:set(),3:set()}
for v in vals:
    for d in (1,2,3):
        r=round(v,d)
        if 0.0<=r<=1.0: voc[d].add(round(r,d))
out={'_purpose':'증거 어휘 포화도. 부록 B 가 이 출력에 대고 쓰인다.',
     '_sources':len(SRC),'_distinct_values':len(vals),
     '_note':'자기 출력은 어휘에서 제외한다.'}
for d,tot in ((1,10),(2,100),(3,1000)):
    held=sum(1 for i in range(tot) if round(i/tot,d) in voc[d])
    out[f'decimals_{d}']={'held':held,'possible':tot}
json.dump(out,open(SELF,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
for d,tot in ((1,10),(2,100),(3,1000)):
    h=out[f'decimals_{d}']['held']
    print(f'  소수 {d}자리: 가능한 {tot}개 중 어휘가 이미 {h}개를 들고 있다 ({h/tot*100:.0f}%)')
print(f'  (공개 산출물 {len(SRC)}개 · 구별되는 수 {len(vals):,}개)')

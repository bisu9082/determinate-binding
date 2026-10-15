# -*- coding: utf-8 -*-
"""조판본에서 표 10종의 행 데이터를 뽑아 되돌린다.

pdftotext -layout 은 열을 공백으로 유지하므로 2칸 이상 공백으로 나누면 셀이 나온다.
표 1 처럼 셀이 여러 줄로 접힌 표가 있으므로, 첫 열이 빈 줄은 앞 행의 이어짐으로 본다.
추측은 하지 않는다. 열 수가 어긋나는 행은 그대로 남기고 보고한다."""
import re,json

raw=open('recovery/v22.txt',encoding='utf-8').read()
raw='\n'.join(l for l in raw.replace('\f','\n').split('\n')
              if not re.fullmatch(r'\s*\d{1,3}\s*',l))
lines=raw.split('\n')
CAP=re.compile(r'^\s*Table (\d+):')

def cells(s): return re.split(r'\s{2,}',s.strip())
def indent(s): return len(s)-len(s.lstrip())

out={}
for i,l in enumerate(lines):
    m=CAP.match(l)
    if not m: continue
    n=int(m.group(1))
    j=i+1; cap=[l.strip()]
    while j<len(lines):
        s=lines[j]
        if not s.strip(): j+=1; continue
        if len(cells(s))>=3: break
        cap.append(s.strip()); j+=1
    rows=[]; cont=[]
    first_ind=None
    while j<len(lines):
        s=lines[j]
        if not s.strip():
            # 표가 쪽을 넘거나 행 사이에 빈 줄이 들어간다. 빈 줄 하나로 끊지 않고
            # 연속 두 줄이 비거나 다음 캡션/절 제목을 만나면 끝낸다.
            if rows and (j+1>=len(lines) or not lines[j+1].strip()): break
            j+=1; continue
        if rows and (CAP.match(s) or re.match(r'^\s*(Figure \d+:|\d+\.(\d+\.)? [A-Z])',s)): break
        c=cells(s)
        if first_ind is None and len(c)>=2: first_ind=indent(s)
        # 이어짐 판정: 들여쓰기가 첫 행보다 깊고 셀이 적으면 앞 행의 wrap.
        # 셀이 하나뿐인 깊은 들여쓰기 줄도 wrap 이다(표 1 의 인용 꼬리). 종전에는
        # 여기서 끊어 21행 표가 2행만 복원됐다.
        if rows and first_ind is not None and indent(s)>first_ind+4 \
           and len(c)<len(rows[-1]):
            cont.append((len(rows)-1,c)); j+=1; continue
        if len(c)<2: break
        rows.append(c); j+=1
    # wrap 을 앞 행의 해당 열에 붙인다 (텍스트 열은 보통 마지막 글자열 셀)
    # 셀 안에서 줄바꿈 하이픈이 살아 있으면 인용 치환이 안 된다("U.S. Gov- ernment").
    for ri,c in cont:
        tgt=rows[ri]
        k=max((x for x in range(len(tgt)) if not re.fullmatch(r'[\d,.%\[\]\s-]+',tgt[x])),
              default=len(tgt)-1)
        tgt[k]=tgt[k]+' '+' '.join(c)
    out[n]={'caption':' '.join(cap),'rows':rows}

# 합친 뒤 셀 단위로 줄바꿈 하이픈을 제거한다
for n in out:
    for r in out[n]['rows']:
        for k in range(len(r)):
            r[k]=re.sub(r'([A-Za-z])-\s+([a-z])',r'\1\2',r[k])
    out[n]['caption']=re.sub(r'([A-Za-z])-\s+([a-z])',r'\1\2',out[n]['caption'])

json.dump(out,open('recover/tables.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
bad=[]
for n in sorted(out):
    r=out[n]['rows']; w=sorted({len(x) for x in r})
    if len(w)>1: bad.append(n)
    print(f'Table {n:2d}: {len(r):2d}행 · 열수 {w}')
if bad: print('열수 불균일:',bad)

# -*- coding: utf-8 -*-
"""복원이 충실한지 기계로 보인다. 주장이 아니라 대조다.

v22 조판본(소실 직전의 유일한 증거)과 v23 복원본에서 각각 텍스트를 뽑아
단어 다중집합으로 대조한다. 순서 비교가 아니라 다중집합 비교인 이유는 플로트 위치와
참고문헌 정렬이 바뀌면 순서는 달라져도 손실은 없기 때문이다.

허용되는 차이는 아래 ALLOW 다섯 개뿐이고, 전부 사유가 있다. 하나라도 늘면 실패다."""
import re,subprocess,collections,sys,os
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))

OLD='recovery/policerobot_v22_20261012.pdf'
NEW='tex/main_v23.pdf'
# 원본 조판의 줄바꿈 하이픈이 만든 토막 4개와, v22 의 "Appendix Appendix" 버그를
# 고치며 하나 줄어든 Appendix. 전부 손실이 아니다.
ALLOW={'aviationto-ground':1,'aviation-toground':1,'post-market':1,
       'three-decimal':1,'Appendix':1}

def words(pdf,mode):
    t=subprocess.run(['pdftotext','-layout',pdf,'-'],capture_output=True,text=True).stdout
    i=t.rindex('\nReferences\n')
    t=t[:i] if mode=='body' else t[i:]
    t='\n'.join(l for l in t.replace('\f','\n').split('\n')
                if not re.fullmatch(r'\s*\d{1,3}\s*',l))
    t=re.sub(r'([A-Za-z])-\n\s*([a-z])',r'\1\2',t)
    t=re.sub(r'([A-Za-z])-\s+([a-z])',r'\1\2',t)
    for a,b in (('’',"'"),('‘',"'"),('“','"'),('”','"'),
                ('–','-'),('—','-'),('ﬁ','fi'),('ﬂ','fl'),(' ',' ')):
        t=t.replace(a,b)
    return collections.Counter(re.findall(r"[A-Za-z0-9][A-Za-z0-9'.,%/()\[\]-]*",t))

bad=[]
for mode in ('body','refs'):
    A=words(OLD,mode); B=words(NEW,mode); miss=A-B
    print(f'[{mode:5s}] 원본 {sum(A.values()):,}어 · 복원 {sum(B.values()):,}어 · '
          f'원본에만 {sum(miss.values())}개')
    for w,n in miss.items():
        if ALLOW.get(w,0)>=n: continue
        bad.append((mode,w,n)); print(f'   ✘ {n}  {w}')

# em-dash 는 절대 금지다. v22 에 0건이었고 복원본도 0건이어야 한다.
for lbl,p in (('원본',OLD),('복원본',NEW)):
    t=subprocess.run(['pdftotext',p,'-'],capture_output=True,text=True).stdout
    n=t.count('—')
    print(f'{lbl} em-dash {n}건')
    if lbl=='복원본' and n: bad.append(('em-dash','—',n))

print('\n복원 충실성:', '✔ 통과' if not bad else f'✘ 실패 {len(bad)}건')
sys.exit(1 if bad else 0)

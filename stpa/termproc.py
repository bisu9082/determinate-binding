# -*- coding: utf-8 -*-
"""기능어 추출 절차 — 인간 개입을 좁히고 측정한다.
단계 T1 기계: 안전제약 문장에서 내용어 추출(불용어·법률상투어 제거, 빈도 상위)
단계 T2 인간: T1 후보를 4개 관할 법률 어휘로 번역·등가어 추가  ← 유일한 인간 단계
T2에서 추가된 항목 비율을 보고하여 인간 개입의 크기를 수치로 남긴다."""
import re,sys,json
sys.path.insert(0,'stpa')
from uca_mg import UCA as U1
from uca_ma import UCA as U2
from match_mg import FUNC as F1
from compare import FUNC as F2
STOP=set("""a an the of to in for on at by with from that this those these which whose must shall may
be is are was were been being it its their his her as and or not no any all each every such other than
then when where while within without before after during upon under over into out about against
only also both either neither same own more most less least own can could would should will
have has had do does did done make makes made use used using stated defined given taken
point paragraph article section subparagraph item provision regulation directive act law rule
requirement requirements obligation obligations条""".split())
def cand(sc_sentence):
    w=[x.lower() for x in re.findall(r"[A-Za-z][A-Za-z\-']+",sc_sentence)]
    out=[]
    for x in w:
        if x in STOP or len(x)<4: continue
        if x not in out: out.append(x)
    return out
rows=[];T1tot=T2tot=0
for U,F in ((U1,F1),(U2,F2)):
    for u in U:
        sc=u[5].split(':')[0]
        if sc not in F: continue
        sent=u[5].split(':',1)[1]
        c=cand(sent)
        # 사용된 패턴에서 영문 리터럴만 뽑아 T1과 대조
        used=[]
        for p in F[sc]:
            for lit in re.findall(r"[A-Za-z][A-Za-z\- ]{3,}",p):
                lit=lit.strip().lower()
                if lit and lit not in used: used.append(lit)
        auto=[x for x in used if any(x.split()[0].startswith(y[:5]) or y.startswith(x.split()[0][:5]) for y in c)]
        human=[x for x in used if x not in auto]
        nonlat=[p for p in F[sc] if not re.search(r'[A-Za-z]',p)]
        T1tot+=len(auto); T2tot+=len(human)+len(nonlat)
        rows.append((sc,len(c),len(used),len(auto),len(human)+len(nonlat)))
print(f"{'SC':11s}{'T1후보':>7s}{'사용패턴':>8s}{'T1유래':>7s}{'T2인간':>7s}")
print('-'*44)
for r in rows: print(f"{r[0]:11s}{r[1]:>7}{r[2]:>8}{r[3]:>7}{r[4]:>7}")
print('-'*44)
print(f"{'합계':9s}{'':>7}{T1tot+T2tot:>8}{T1tot:>7}{T2tot:>7}")
print(f"\n기계 유래 {T1tot/(T1tot+T2tot)*100:.0f}% · 인간 추가 {T2tot/(T1tot+T2tot)*100:.0f}%")
print("인간 추가분의 성격: ① 한국어·일본어 법률 등가어 ② 영문 법률 상투구(예: 'declaration of compliance')")

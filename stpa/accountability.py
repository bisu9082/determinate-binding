# -*- coding: utf-8 -*-
"""책무성 계층 — N21·N22는 안전제약이 아니다. STPA로 유도되지 않는 것이 정상이며,
별도 출처를 가진 별도 계층으로 선언한다.
출처(2026-09-20 정정): 7요소는 단일 문헌의 목록이 아니라 두 출처의 합성이다.
  AC-1~AC-4 (Actor / Forum / Standard / Consequence)
      ← Bovens (2007) European Law Journal 13(4):447-468, doi:10.1111/j.1468-0386.2007.00378.x
        의 책무성 관계 구성요소(행위자-포럼-판단기준-귀결).
  AC-5 Timing / AC-6 Expertise / AC-7 Standing
      ← Metcalf, Moss, Watkins, Singh & Elish (2021) FAccT '21:735-746,
        doi:10.1145/3442188.3445935 — 영향평가가 실제 책무성을 만들려면
        (i) 사전(ex ante) 시점에 수행되고 (ii) 포럼이 기술증거를 읽을 전문성을 갖추며
        (iii) 영향을 받는 공중이 제기할 수 있어야 한다는 세 조건.
  ※ 이전 판 주석은 7요소 전체를 Metcalf et al.의 목록으로 적었다. 오귀속이므로 정정한다.
각 요소를 경찰로봇 인가 맥락에 사상하고, 코퍼스에서 결속 여부를 동일 규칙으로 판정한다."""
ELEMENTS = [
 ("AC-1","Actor",      "Who is answerable for the robot's use of force, sensing and evidence handling"),
 ("AC-2","Forum",      "Before whom that actor must answer, and with what standing"),
 ("AC-3","Standard",   "Against what stated standard the conduct is judged"),
 ("AC-4","Consequence","What follows from a finding against the actor"),
 ("AC-5","Timing",     "Whether the account is given before, during or only after deployment"),
 ("AC-6","Expertise",  "Whether the forum can read the technical evidence it is given"),
 ("AC-7","Standing",   "Whether the affected public can raise the matter at all"),
]
MAP={'N21':['AC-1','AC-2','AC-5'], 'N22':['AC-2','AC-4','AC-7']}
FUNC={
 'AC-1':[r'responsible (?:person|entity|body)|accountable',r'책임\s*(?:자|기관)'],
 'AC-2':[r'oversight (?:body|board|committee)|competent authority|supervisory authority',
         r'감독\s*(?:기관|위원회)|심의\s*위원회'],
 'AC-3':[r'standard|criteria|기준',r'guideline|지침'],
 'AC-4':[r'shall be (?:revoked|withdrawn|suspended|refused)|penalt|sanction',r'취소|정지|제재'],
 'AC-5':[r'prior to (?:deployment|use|acquisition)|before (?:deployment|use)|ex ante',
         r'사전\s*(?:승인|심의|신고)'],
 'AC-6':[r'technical expert|expertise|전문\s*(?:가|성)'],
 'AC-7':[r'complaint|redress|remedy|right to (?:lodge|object)',r'이의\s*신청|고충|구제'],
}
if __name__=='__main__':
    import json,re,sys
    from collections import Counter
    sys.path.insert(0,'stpa'); sys.path.insert(0,'probe')
    from carveout import N,build,tier_of
    allowed=set(N); ADJ=build(allowed)
    print(f"{'요소':6s}{'명칭':13s}{'매칭':>6s}{'인가항':>7s}{'T2':>4s}{'T1':>4s}  판정")
    print('-'*64)
    C=Counter()
    for code,name,_ in ELEMENTS:
        R=re.compile("|".join(FUNC[code]),re.I)
        hit=[k for k in allowed if R.search(N[k])]
        tiers={k:tier_of(k,ADJ,allowed) for k in hit}
        auth=[k for k,t in tiers.items() if t is not None]
        t2=sum(1 for k in auth if tiers[k]==2); t1=sum(1 for k in auth if tiers[k]==1)
        c='개념 부재' if not hit else ('인가조항 아님' if not auth else ('영점' if t2==0 else f'확정결속 {t2}'))
        C[c.split()[0]]+=1
        print(f"{code:6s}{name:13s}{len(hit):>6}{len(auth):>7}{t2:>4}{t1:>4}  {c}")
    print('-'*64)
    for k,v in C.most_common(): print(f"  {k:12s}{v:>3}건")

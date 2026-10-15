# -*- coding: utf-8 -*-
"""M-A 안전제약 × {AC, AP} 결속 비교. 동일 제약·동일 기능어, 노드 집합만 다르다."""
import re,json,sys
sys.path.insert(0,'stpa'); sys.path.insert(0,'probe')
from carveout import N,E,L,ap_nodes,build,tier_of
from uca_ma import UCA
FUNC={
 'SCA-03-1':[r'kinetic energy|impact energy|ft-?lb|joule',r'exposed rotating parts|rotor',
             r'Category [1-4] operation'],
 'SCA-03-2':[r'sustained flight',r'open-air assembl'],
 'SCA-01-1':[r'purpose of the (?:flight|operation)',r'payload',r'목적'],
 'SCA-01-2':[r'change of (?:purpose|circumstance)',r'변경(?:된|되는) 경우|변경인증',r're-?authoris|re-?authoriz'],
 'SCA-02-1':[r'remote identification',r'position accuracy|accuracy of the position',r'airspace authoris'],
 'SCA-02-2':[r'withdraw\w*|revok\w*|suspend\w*'],
 'SCA-04-1':[r'purpose limitation|specified.{0,20}purposes',r'retention period|storage period',
             r'보유\s*기간|목적\s*외', r'biometric'],
 'SCA-04-2':[r'cease (?:to )?(?:record|process)',r'no longer necessary'],
 'SCA-05-1':[r'sufficient (?:power|energy)|endurance',r'safe (?:landing|recovery)'],
 'SCA-05-2':[r'ground risk|population density|people on the ground'],
 'SCA-06-1':[r'geo-?awareness|geo-?fenc',r'lost link|loss of (?:the )?(?:command and control|C2) link'],
 'SCA-06-2':[r'geo-?awareness|geo-?fenc',r'update.{0,30}(?:data|information).{0,30}before (?:the )?flight'],
 'SCA-07-1':[r'chain of custody|보관\s*연속성',r'logging|logs? of',r'transfer of personal data'],
 'SCA-07-2':[r'further processing|derived',r'same purpose'],
}
from scope import admissible
if __name__=='__main__':
    apset,drop=ap_nodes(); acset=set(N)
    ADJ_AC, ADJ_AP = build(acset), build(apset)
    def worst(sc,allowed,ADJ):
        pats=FUNC.get(sc)
        if not pats: return None,0
        R=re.compile("|".join(pats),re.I)
        hits=[k for k in sorted(allowed) if admissible(sc,k) and R.search(N[k])]
        tiers=[t for t in (tier_of(k,ADJ,allowed) for k in hits) if t is not None]
        return (max(tiers) if tiers else (0 if hits else None)), len(hits)
    print(f"{'안전제약':11s}{'AC':>4s}{'AP':>4s}{'Δ':>3s}   {'AC매칭':>6s}{'AP매칭':>6s}  비고")
    print('-'*72)
    rows=[];lower=0
    for u in UCA:
        sc=u[5].split(':')[0]
        ta,na=worst(sc,acset,ADJ_AC); tp,np_=worst(sc,apset,ADJ_AP)
        f=lambda x: '·' if x is None else str(x)
        d='' if (ta is None or tp is None) else ('↓' if tp<ta else ('↑' if tp>ta else '='))
        if d=='↓': lower+=1
        if d=='↑': print("  !! 역전"); 
        rows.append((sc,ta,tp,d,na,np_))
        note='면제로 결속 상실' if d=='↓' else ('개념 부재' if ta is None else '')
        print(f"{sc:11s}{f(ta):>4}{f(tp):>4}{d:>3}   {na:>6}{np_:>6}  {note}")
    print(f"\nAC>AP {lower}건 · AP>AC 0건(역전) · 동일 {sum(1 for r in rows if r[3]=='=')}건")
    json.dump([{'sc':r[0],'AC':r[1],'AP':r[2]} for r in rows],open('stpa/compare_ma.json','w'),ensure_ascii=False,indent=1)

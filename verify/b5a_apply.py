# -*- coding: utf-8 -*-
"""B5-a 범주 A 치환. 모든 치환은 기대 등장횟수를 단언한다. 하나라도 어긋나면 전부 적용하지 않는다."""
import os,sys,json
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
P=chr(92)+'%'   # LaTeX 퍼센트
E=[]
def ed(f,old,new,n=1): E.append((f,old,new,n))

# ---------- 초록 (main_v23.tex) ----------
ed('main','the predicate returns 91 and 34 survive the audit, a precision of 0.374',
         'the predicate returns 91 and 41 survive the audit, a precision of 0.451')
ed('main',f'raising the aviation binding rate from 9.5{P} to 19.2{P}',
         f'raising the aviation binding rate from 10.8{P} to 21.7{P}')
ed('main','22 of the 23 audited bindings a civil unmanned aircraft carries cease to apply to a police one, 15 analytically and 7 by measurement',
         '25 of the 26 audited bindings a civil unmanned aircraft carries cease to apply to a police one, 18 analytically and 7 by measurement')

# ---------- methods ----------
ed('methods','lowers precision from 0.417 to 0.374','lowers precision from 0.514 to 0.451')
ed('methods','Precision is 0.374. It is not uniform: 23 of 54 in aviation (0.426), 11 of 34 on the ground (0.324)',
            'Precision is 0.451. It is not uniform: 26 of 54 in aviation (0.481), 15 of 34 on the ground (0.441)')
ed('methods','Thirty-four of the 91 provisions are bindings','Forty-one of the 91 provisions are bindings')
ed('methods',f'Excludes (adopted) & 34 & 0.374 & 23/241 & 11/604 & 0/169 & 23 ${chr(92)}rightarrow$ 1',
            f'Excludes (adopted) & 41 & 0.451 & 26/241 & 15/604 & 0/169 & 26 ${chr(92)}rightarrow$ 1')
ed('methods',f'Excludes (adopted) 34 0.374 23/241 11/604 0/169 23 ${chr(92)}rightarrow$ 1',
            f'Excludes (adopted) 41 0.451 26/241 15/604 0/169 26 ${chr(92)}rightarrow$ 1')
ed('methods','Precision of the predicate & 0.351 & 0.374 & favourable','Precision of the predicate & 0.351 & 0.451 & favourable')
ed('methods','Precision of the predicate 0.351 0.374 favourable','Precision of the predicate 0.351 0.451 favourable')
ed('methods','Aviation-to-ground ratio & 8.07 & 5.24 & against','Aviation-to-ground ratio & 8.07 & 4.34 & against')
ed('methods','Aviation-to-ground ratio 8.07 5.24 against','Aviation-to-ground ratio 8.07 4.34 against')
ed('methods','Audited bindings & 27 & 34 & against','Audited bindings & 27 & 41 & against')
ed('methods','Audited bindings 27 34 against','Audited bindings 27 41 against')
# 표 4 + 그 서술
ed('methods',f'raises the aviation rate from 9.5{P} to 19.2{P} and the ground rate from 1.8{P} to 3.3{P}',
            f'raises the aviation rate from 10.8{P} to 21.7{P} and the ground rate from 2.5{P} to 4.5{P}')
ed('methods','the aviationto-ground ratio goes from 5.2 to 5.8','the aviationto-ground ratio goes from 4.3 to 4.8')
ed('methods',f'Aviation & 23 & 241 & 9.5{P} & 12/24 = 0.500 & 120 & 19.2{P} [13.9, 30.4]',
            f'Aviation & 26 & 241 & 10.8{P} & 12/24 = 0.500 & 120 & 21.7{P} [15.7, 34.3]')
ed('methods',f'Ground & 11 & 604 & 1.8{P} & 22/40 = 0.550 & 332 & 3.3{P} [2.6, 4.6]',
            f'Ground & 15 & 604 & 2.5{P} & 22/40 = 0.550 & 332 & 4.5{P} [3.6, 6.2]')
ed('methods',f'Total & 34 & 1,014 & 3.4{P} & 39/79 = 0.494 & 501 & 6.8{P}',
            f'Total & 41 & 1,014 & 4.0{P} & 39/79 = 0.494 & 501 & 8.2{P} [6.7, 10.5]')
ed('methods',f'Aviation 23 241 9.5{P} 12/24 = 0.500 120 19.2{P} [13.9, 30.4]',
            f'Aviation 26 241 10.8{P} 12/24 = 0.500 120 21.7{P} [15.7, 34.3]')
ed('methods',f'Ground 11 604 1.8{P} 22/40 = 0.550 332 3.3{P} [2.6, 4.6]',
            f'Ground 15 604 2.5{P} 22/40 = 0.550 332 4.5{P} [3.6, 6.2]')
ed('methods',f'Total 34 1,014 3.4{P} 39/79 = 0.494 501 6.8{P}',
            f'Total 41 1,014 4.0{P} 39/79 = 0.494 501 8.2{P} [6.7, 10.5]')
ed('methods','The audit of Section 2.7 establishes that 34 of the 91 provisions the predicate returns are bindings',
            'The audit of Section 2.7 establishes that 41 of the 91 provisions the predicate returns are bindings')
ed('methods',f'Lexicon false-negative rate & 11.1{P} & 12.6{P} & against',
            f'Lexicon false-negative rate & 11.1{P} & 12.6{P} & against')  # 연혁(before)·현행(after) 모두 불변

# ---------- results ----------
ed('results','Section 2.7 then separates the 91: 34 are bindings and 57 are not, a precision of 0.374; this is a census of the returned set, with a Wilson 95'+P+' interval of [0.281, 0.476]',
            'Section 2.7 then separates the 91: 41 are bindings and 50 are not, a precision of 0.451; this is a census of the returned set, with a Wilson 95'+P+' interval of [0.352, 0.553]')
ed('results',f'at 3.4{P} of the 1,014 after audit against 9.0{P} before it',
            f'at 4.0{P} of the 1,014 after audit against 9.0{P} before it')
ed('results',f'raises the corpus-wide rate from 3.4{P} to 6.8{P}',f'raises the corpus-wide rate from 4.0{P} to 8.2{P}')
ed('results','to 0.374 at four hops','to 0.451 at four hops')
ed('results',f'hop $\\le$ 2 & 34 & 54 & 88 & 0.386',f'hop $\\le$ 2 & 41 & 47 & 88 & 0.466')
ed('results',f'hop $\\le$ 3 & 34 & 56 & 90 & 0.378',f'hop $\\le$ 3 & 41 & 49 & 90 & 0.456')
ed('results',f'hop $\\le$ 4 (adopted) & 34 & 57 & 91 & 0.374',f'hop $\\le$ 4 (adopted) & 41 & 50 & 91 & 0.451')
ed('results','hop $\\le$ 2 34 54 88 0.386','hop $\\le$ 2 41 47 88 0.466')
ed('results','hop $\\le$ 3 34 56 90 0.378','hop $\\le$ 3 41 49 90 0.456')
ed('results','hop $\\le$ 4 (adopted) 34 57 91 0.374','hop $\\le$ 4 (adopted) 41 50 91 0.451')
ed('results',f'Aviation instruments convert 9.5{P} of their authorising provisions into audited bindings',
            f'Aviation instruments convert 10.8{P} of their authorising provisions into audited bindings')
ed('results',f'road-traffic instruments convert 1.8{P}',f'road-traffic instruments convert 2.5{P}')
ed('results','ratio is 5.24, with Cohen'+chr(39)+'s h = 0.357',
            'ratio is 4.34, with Cohen'+chr(39)+'s h = 0.353')
ed('results',f'raises the two rates to 19.2{P} and 3.3{P} and the ratio to 5.8',
            f'raises the two rates to 21.7{P} and 4.5{P} and the ratio to 4.8')
ed('results',f'Aviation certification (6) & 241 & 23 & 9.5{P} & [6.4, 13.9]',
            f'Aviation certification (6) & 241 & 26 & 10.8{P} & [7.5, 15.3]')
ed('results',f'Aviation certification (6) 241 23 9.5{P} [6.4, 13.9]',
            f'Aviation certification (6) 241 26 10.8{P} [7.5, 15.3]')
ed('results',f'Aviation (6 instruments) & 241 & 54 & 23 & 9.5{P} & [4.0, 21.2] & 0.426',
            f'Aviation (6 instruments) & 241 & 54 & 26 & 10.8{P} & [4.0, 21.2] & 0.481')
ed('results',f'Aviation (6 instruments) 241 54 23 9.5{P} [4.0, 21.2] 0.426',
            f'Aviation (6 instruments) 241 54 26 10.8{P} [4.0, 21.2] 0.481')
ed('results',f'Ground (5 instruments) & 604 & 34 & 11 & 1.8{P} & [0.5, 6.1] & 0.324',
            f'Ground (5 instruments) & 604 & 34 & 15 & 2.5{P} & [0.5, 6.1] & 0.441')
ed('results',f'Ground (5 instruments) 604 34 11 1.8{P} [0.5, 6.1] 0.324',
            f'Ground (5 instruments) 604 34 15 2.5{P} [0.5, 6.1] 0.441')
ed('results',f'{chr(92)}multicolumn{{2}}{{@{{}}l}}{{Total}} & 1,014 & 91 & 34 & 3.4{P} & 0.374',
            f'{chr(92)}multicolumn{{2}}{{@{{}}l}}{{Total}} & 1,014 & 91 & 41 & 4.0{P} & 0.451')
ed('results',f'Total 1,014 91 34 3.4{P} 0.374',f'Total 1,014 91 41 4.0{P} 0.451')
ed('results',f'The pooled ground rate of 1.8{P}',f'The pooled ground rate of 2.5{P}')
ed('results','Precision is 0.374 [0.281, 0.476] over the returned set','Precision is 0.451 [0.352, 0.553] over the returned set')
ed('results','the returned counts are 54 and 7, the audited counts 23 and 1. Of the 23 civil-route bindings, 15 are EU and 8 are US',
            'the returned counts are 54 and 7, the audited counts 26 and 1. Of the 26 civil-route bindings, 18 are EU and 8 are US')
ed('results','23 of 241 against 9 of 574, and a provision-level Fisher exact test on that table gives',
            '26 of 241 against 14 of 574, and a provision-level Fisher exact test on that table gives')
ed('results','23 of 241 against 0 of 139','26 of 241 against 0 of 139')

# ---------- discussion ----------
ed('discussion','the predicate returns 91 and the audit confirms 34','the predicate returns 91 and the audit confirms 41')
ed('discussion','Precision is 0.374 with a Wilson 95'+P+' interval of [0.281, 0.476], and it is not uniform: 0.426 in aviatio',
            'Precision is 0.451 with a Wilson 95'+P+' interval of [0.352, 0.553], and it is not uniform: 0.481 in aviatio')
ed('discussion','The predicate returns 91 provisions and 34 survive, a precision of 0.374 [0.281, 0.476]',
            'The predicate returns 91 provisions and 41 survive, a precision of 0.451 [0.352, 0.553]')
ed('discussion','precision falls from 0.417 to 0.374','precision falls from 0.514 to 0.451')
ed('discussion','At a precision of 0.374','At a precision of 0.451')
ed('discussion',f'aviation at 9.5{P} and the ground corpus at 1.8{P}',f'aviation at 10.8{P} and the ground corpus at 2.5{P}')
ed('discussion',f'Aviation certification converts 9.5{P} of its authorising provisions into audited bindings against 1.6{P} for road-traffic l',
            f'Aviation certification converts 10.8{P} of its authorising provisions into audited bindings against 2.4{P} for road-traffic l')
ed('discussion','aviation certification against road-traffic law, 23 of 241 against 9 of 574',
            'aviation certification against road-traffic law, 26 of 241 against 14 of 574')

# ---------- 검증 후 일괄 적용 ----------
txt={}
for f in ('main','methods','results','discussion','appendix','back','front'):
    p=f'tex/{f}_v23.tex'
    if os.path.exists(p): txt[f]=open(p,encoding='utf-8').read()
bad=[]
for f,old,new,n in E:
    got=txt[f].count(old)
    if got!=n: bad.append((f,n,got,old[:95]))
if bad:
    print('치환 불가 — 아무것도 적용하지 않았다')
    for f,exp,got,o in bad: print(f'  {f}: 기대 {exp} 실제 {got}  |{o}|')
    sys.exit(1)
for f,old,new,n in E:
    txt[f]=txt[f].replace(old,new)
for f,s in txt.items(): open(f'tex/{f}_v23.tex','w',encoding='utf-8').write(s)
print(f'적용 {len(E)}건 (등장 {sum(x[3] for x in E)}회)')

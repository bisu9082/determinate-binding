# -*- coding: utf-8 -*-
"""B5-a 재번호 — 원천 계층에 적용한다.

tex/*_v23.tex 는 recover/assemble_v23.py 가 recover/paras.json +
recover/tables.json 에서 만드는 산출물이다. .tex 를 고치면 다음 조립에서
조용히 되돌아간다. 그래서 원천을 고친다.

모든 치환은 기대 등장횟수를 단언한다. 하나라도 어긋나면 전부 적용하지 않는다.
수치는 verify/b5a_derive.py 가 낸 값이고, 그 추정기들은 먼저 구판 라벨(34)로
공개 수치를 재현하는지 대조했다."""
import json,os,sys
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
PA=json.load(open('recover/paras.json',encoding='utf-8'))
TB=json.load(open('recover/tables.json',encoding='utf-8'))

PROSE=[]
def p(old,new,n=1): PROSE.append((old,new,n))

# ── 감사 총계와 정밀도 ────────────────────────────────────────────
p('Thirty-four of the 91 provisions are bindings. Precision is 0.374. It is not uniform: 23 of 54 in aviation (0.426), 11 of 34 on the ground (0.324)',
  'Forty-one of the 91 provisions are bindings. Precision is 0.451. It is not uniform: 26 of 54 in aviation (0.481), 15 of 34 on the ground (0.441)')
p('The audit of Section 2.7 establishes that 34 of the 91 provisions the predicate returns are bindings',
  'The audit of Section 2.7 establishes that 41 of the 91 provisions the predicate returns are bindings')
p('Section 2.7 then separates the 91: 34 are bindings and 57 are not, a precision of 0.374; this is a census of the returned set, with a Wilson 95% interval of [0.281, 0.476]',
  'Section 2.7 then separates the 91: 41 are bindings and 50 are not, a precision of 0.451; this is a census of the returned set, with a Wilson 95% interval of [0.352, 0.553]')
p('Precision is 0.374 [0.281, 0.476] over the returned set','Precision is 0.451 [0.352, 0.553] over the returned set')
p('the predicate returns 91 and the audit confirms 34','the predicate returns 91 and the audit confirms 41')
p('Precision is 0.374 with a Wilson 95% interval of [0.281, 0.476], and it is not uniform: 0.426 in aviatio',
  'Precision is 0.451 with a Wilson 95% interval of [0.352, 0.553], and it is not uniform: 0.481 in aviatio')
p('The predicate returns 91 provisions and 34 survive, a precision of 0.374 [0.281, 0.476]',
  'The predicate returns 91 provisions and 41 survive, a precision of 0.451 [0.352, 0.553]')
p('At a precision of 0.374','At a precision of 0.451')
p('to 0.374 at four hops','to 0.451 at four hops')
p('lowers precision from 0.417 to 0.374','lowers precision from 0.514 to 0.451')
p('precision falls from 0.417 to 0.374','precision falls from 0.514 to 0.451')

# ── 비율·요율 ────────────────────────────────────────────────────
p('at 3.4% of the 1,014 after audit against 9.0% before it','at 4.0% of the 1,014 after audit against 9.0% before it')
p('raises the corpus-wide rate from 3.4% to 6.8%','raises the corpus-wide rate from 4.0% to 8.2%')
p('Aviation instruments convert 9.5% of their authorising provisions into audited bindings',
  'Aviation instruments convert 10.8% of their authorising provisions into audited bindings')
p('road-traffic instruments convert 1.8%','road-traffic instruments convert 2.5%')
p('The pooled ground rate of 1.8%','The pooled ground rate of 2.5%')
p('aviation at 9.5% and the ground corpus at 1.8%','aviation at 10.8% and the ground corpus at 2.5%')
p('Aviation certification converts 9.5% of its authorising provisions into audited bindings against 1.6% for road-traffic l',
  'Aviation certification converts 10.8% of its authorising provisions into audited bindings against 2.4% for road-traffic l')
p("ratio is 5.24, with Cohen's h = 0.357","ratio is 4.34, with Cohen's h = 0.353")
p('raises the two rates to 19.2% and 3.3% and the ratio to 5.8','raises the two rates to 21.7% and 4.5% and the ratio to 4.8')
p('raises the aviation rate from 9.5% to 19.2% and the ground rate from 1.8% to 3.3%',
  'raises the aviation rate from 10.8% to 21.7% and the ground rate from 2.5% to 4.5%')
p('the aviationto-ground ratio goes from 5.2 to 5.8','the aviationto-ground ratio goes from 4.3 to 4.8')
p('the ratio reaches its current 5.24 only after','the ratio reaches its current 4.34 only after')

# ── Fisher ──────────────────────────────────────────────────────
p('23 of 241 against 9 of 574, and a provision-level Fisher exact test on that table gives',
  '26 of 241 against 14 of 574, and a provision-level Fisher exact test on that table gives')
p('23 of 241 against 0 of 139','26 of 241 against 0 of 139')
p('aviation certification against road-traffic law, 23 of 241 against 9 of 574',
  'aviation certification against road-traffic law, 26 of 241 against 14 of 574')

# ── 민감도·대안 판정 ────────────────────────────────────────────
p('drops two false positives and one binding, and leaves precision near unchanged at 0.374',
  'drops two false positives and one binding, and leaves precision near unchanged at 0.455')
p('revives 19 of the records the adjudication rejects and gives 53 bindings instead of 34, a precision of 0.582 instead of 0.374',
  'revives 12 of the records the adjudication rejects and gives 53 bindings instead of 41, a precision of 0.582 instead of 0.451')
p("n-to-ground ratio rises from 5.24 to 8.56 with Cohen's h from 0.357 to 0.567",
  "n-to-ground ratio rises from 4.34 to 6.35 with Cohen's h from 0.353 to 0.500")
p('in either direction (41 to 1 instead of 23 to 1)','in either direction (38 to 1 instead of 26 to 1)')

# ── 결속 총계에 딸린 서술 ───────────────────────────────────────
p('Of the 34 audited bindings, 30 (88.2%) are visible in a single paragraph read alone',
  'Of the 41 audited bindings, 37 (90.2%) are visible in a single paragraph read alone')
p('The 34 audited bindings are not spread evenly','The 41 audited bindings are not spread evenly')
p('We therefore repartitioned the same 34 audited bindings by subject matter',
  'We therefore repartitioned the same 41 audited bindings by subject matter')
p('supplies 32 of the 91 returns and 13 of the 34 bindings','supplies 32 of the 91 returns and 17 of the 41 bindings')
p('The Japanese Road Traffic Act contributes 4 of the 34 bindings','The Japanese Road Traffic Act contributes 8 of the 41 bindings')
p('Of the 11 ground bindings, 5 are in the Korean Road Traffic Act','Of the 15 ground bindings, 5 are in the Korean Road Traffic Act')
p('Thirty of the 34 bindings are legible in a single paragraph read alone',
  'Thirty-seven of the 41 bindings are legible in a single paragraph read alone')

# ── 면제가 지우는 결속 ──────────────────────────────────────────
p('the returned counts are 54 and 7, the audited counts 23 and 1. Of the 23 civil-route bindings, 15 are EU and 8 are US',
  'the returned counts are 54 and 7, the audited counts 26 and 1. Of the 26 civil-route bindings, 18 are EU and 8 are US')
p('The carve-out therefore removes 22 of the 23 audited technical bindings that a civil unmanned aircraft carries, 96',
  'The carve-out therefore removes 25 of the 26 audited technical bindings that a civil unmanned aircraft carries, 96')
p('removes 22 of the 23 audited bindings that a civil unmanned aircraft carries',
  'removes 25 of the 26 audited bindings that a civil unmanned aircraft carries')
p('Without this, the 22 reads as stronger than it is','Without this, the 25 reads as stronger than it is')
p('and the 22 is a sum across two bodies of law','and the 25 is a sum across two bodies of law')

# ── 재현율 투영 (투영 누락 62 [23,145] 는 FN율에만 의존하므로 불변) ──
p('34 audited bindings against 491 tier-1 provisions give a projection of 62 [23, 145] and recall 0.35 [0.19, 0.59]',
  '41 audited bindings against 491 tier-1 provisions give a projection of 62 [23, 145] and recall 0.40 [0.22, 0.64]')

# ── 표 ───────────────────────────────────────────────────────────
TBL=[]
def t(key,row_i,col_i,old,new): TBL.append((key,row_i,col_i,old,new))
def cap(key,old,new): TBL.append((key,'caption',None,old,new))
# 표 1: 문단 노드 보수가 항공 분모를 246->241 로 줄였는데 기관별 열이 갱신되지 않았다.
t('1',4,4,'35','33')          # US107
t('1',5,4,'20','17')          # US89
cap('1','34 of the 91 survive the audit','41 of the 91 survive the audit')
# 표 3
t('3',1,1,'34','41'); t('3',1,2,'0.374','0.451'); t('3',1,3,'23/241','26/241')
t('3',1,4,'11/604','15/604'); t('3',1,6,'23 → 1','26 → 1')
t('3',2,3,'41/241','38/241'); t('3',2,4,'12/604','15/604'); t('3',2,6,'41 → 1','38 → 1')
# 표 4
t('4',1,1,'23','26'); t('4',1,3,'9.5%','10.8%'); t('4',1,6,'19.2% [13.9, 30.4]','21.7% [15.7, 34.3]')
t('4',2,1,'11','15'); t('4',2,3,'1.8%','2.5%'); t('4',2,6,'3.3% [2.6, 4.6]','4.5% [3.6, 6.2]')
t('4',4,1,'34','41'); t('4',4,3,'3.4%','4.0%'); t('4',4,6,'6.8%','8.2% [6.7, 10.5]')
# 표 6 (열개 변경, after 열만)
t('6',5,2,'34','41'); t('6',6,2,'0.374','0.451'); t('6',7,2,'5.24','4.34')
# 표 7
t('7',1,1,'30','37'); t('7',1,2,'42','35'); t('7',1,4,'0.417','0.514')
t('7',2,1,'30','37'); t('7',2,2,'46','39'); t('7',2,4,'0.395','0.487')
t('7',3,1,'34','41'); t('7',3,2,'54','47'); t('7',3,4,'0.386','0.466')
t('7',4,1,'34','41'); t('7',4,2,'56','49'); t('7',4,4,'0.378','0.456')
t('7',5,1,'34','41'); t('7',5,2,'57','50'); t('7',5,4,'0.374','0.451')
# 표 8 (주제별)
cap('8','The same 34 audited bindings','The same 41 audited bindings')
t('8',1,2,'23','26'); t('8',1,3,'9.5%','10.8%'); t('8',1,4,'[6.4, 13.9]','[7.5, 15.3]')
t('8',2,2,'2','1');  t('8',2,3,'6.7%','3.3%');  t('8',2,4,'[1.8, 21.3]','[0.6, 16.7]')
t('8',3,2,'9','14'); t('8',3,3,'1.6%','2.4%');  t('8',3,4,'[0.8, 3.0]','[1.5, 4.1]')
# 표 9 (도메인별)
t('9',1,3,'23','26'); t('9',1,4,'9.5%','10.8%'); t('9',1,6,'0.426','0.481')
t('9',2,3,'11','15'); t('9',2,4,'1.8%','2.5%');  t('9',2,6,'0.324','0.441')
t('9',4,3,'34','41'); t('9',4,4,'3.4%','4.0%');  t('9',4,5,'0.374','0.451')

# ── 검증 ────────────────────────────────────────────────────────
bad=[]
for old,new,n in PROSE:
    got=sum(s.count(old) for s in PA)
    if got!=n: bad.append(('para',n,got,old[:92]))
for key,ri,ci,old,new in TBL:
    if ri=='caption':
        got=TB[key]['caption'].count(old)
        if got!=1: bad.append((f'T{key}.caption',1,got,old[:60]))
    else:
        cur=TB[key]['rows'][ri][ci]
        if cur!=old: bad.append((f'T{key}[{ri}][{ci}]','=='+old,cur,''))
if bad:
    print('치환 불가 — 아무것도 적용하지 않았다')
    for a,b,c,d in bad: print(f'  {a}: 기대 {b} 실제 {c}  |{d}|')
    sys.exit(1)

for old,new,n in PROSE:
    PA=[s.replace(old,new) for s in PA]
for key,ri,ci,old,new in TBL:
    if ri=='caption': TB[key]['caption']=TB[key]['caption'].replace(old,new)
    else: TB[key]['rows'][ri][ci]=new
json.dump(PA,open('recover/paras.json','w',encoding='utf-8'),ensure_ascii=False,indent=0)
json.dump(TB,open('recover/tables.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print(f'본문 {len(PROSE)}건 · 표 {len(TBL)}건 적용 (원천 계층)')

# -*- coding: utf-8 -*-
"""도판이 쓰는 측정값 전부를 한 곳에서 낸다. 도판 스크립트는 수치를 들고 있지 않고
이 산출물을 읽는다(원고의 fig_hardcode 게이트가 요구하는 구조).

결속 정본은 labels/tpset.json (2026-10-14 맹검 재정, B3)."""
import json,os,sys,math,re
from collections import Counter,defaultdict
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
sys.path.insert(0,'graph'); sys.path.insert(0,'probe')
import paths3 as P3

TP=set(json.load(open('labels/tpset.json',encoding='utf-8'))['tp'])
N=json.load(open('graph/nodes3.json',encoding='utf-8'))
E=[tuple(e) for e in json.load(open('graph/edges3.json',encoding='utf-8'))]

def wilson(k,n,z=1.96):
    if n==0: return (0.0,0.0)
    p=k/n; d=1+z*z/n; c=p+z*z/(2*n); h=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))
    return ((c-h)/d,(c+h)/d)

AV={'EU1139','EU947','EU945','US107','US89','USAC'}
GR={'JP道交法','KR도로교통법','KR도로교통법시행규칙','KR지능형로봇법','KR지능형로봇법시행령'}
CC={'EUAI','MID','LED','SMC1418','CAGOV'}
def dom(k):
    d=k.split('::')[0]
    return 'aviation' if d in AV else ('ground' if d in GR else 'crosscut')
SUBJ={**{d:'Aviation certification' for d in AV},
      'KR지능형로봇법':'Robot certification','KR지능형로봇법시행령':'Robot certification',
      'JP道交法':'Road traffic, drivers','KR도로교통법':'Road traffic, drivers',
      'KR도로교통법시행규칙':'Road traffic, drivers',
      'LED':'Police conduct','SMC1418':'Police conduct','CAGOV':'Police conduct',
      'EUAI':'Horizontal product law','MID':'Horizontal product law'}

out={'_purpose':'도판 측정값. 결속 정본은 labels/tpset.json (맹검 재정 41건).',
     '_binding_source':'labels/tpset.json'}

# ── Fig1(b) tier 분포 · Fig2(a) hop별 반환·결속 ──────────────────
hops=[('no_edges',[],4),('hop1',E,1),('hop2',E,2),('hop3',E,3),
      ('hop4',E,4),('hop5',E,5)]
byhop={}
for lab,edg,h in hops:
    r=P3.run(edg,h)
    c=Counter(v[0] for v in r.values())
    ret={k for k,v in r.items() if v[0]==2}
    aud=ret&TP
    byhop[lab]={'auth':len(r),'t2':c[2],'t1':c[1],'t0':c[0],
                'returned':len(ret),'audited':len(aud),
                'precision':(len(aud)/len(ret) if ret else 0.0)}
out['by_hop']=byhop
out['tiers_adopted']={k:byhop['hop4'][k] for k in ('t2','t1','t0','auth')}

# ── Fig3(a) 주제별 결속률 ───────────────────────────────────────
R4=P3.run(E,4)
auth_by_subj=Counter(SUBJ[k.split('::')[0]] for k in R4)
tp_by_subj=Counter(SUBJ[k.split('::')[0]] for k in TP)
ret_by_subj=Counter(SUBJ[k.split('::')[0]] for k,v in R4.items() if v[0]==2)
ORDER=['Aviation certification','Robot certification','Road traffic, drivers',
       'Police conduct','Horizontal product law']
INST={'Aviation certification':6,'Robot certification':2,'Road traffic, drivers':3,
      'Police conduct':3,'Horizontal product law':2}
out['by_subject']=[{'subject':s,'instruments':INST[s],'auth':auth_by_subj[s],
    'returned':ret_by_subj[s],'audited':tp_by_subj[s],
    'rate':tp_by_subj[s]/auth_by_subj[s] if auth_by_subj[s] else 0.0,
    'wilson':wilson(tp_by_subj[s],auth_by_subj[s])} for s in ORDER]

# ── Fig2(b) 도메인 구성 · Fig3 도메인별 ─────────────────────────
auth_by_dom=Counter(dom(k) for k in R4)
out['by_domain']=[{'domain':d,'instruments':n,'auth':auth_by_dom[d],
    'returned':sum(1 for k,v in R4.items() if v[0]==2 and dom(k)==d),
    'audited':sum(1 for k in TP if dom(k)==d),
    'rate':sum(1 for k in TP if dom(k)==d)/auth_by_dom[d] if auth_by_dom[d] else 0.0,
    'wilson':wilson(sum(1 for k in TP if dom(k)==d),auth_by_dom[d])}
    for d,n in (('aviation',6),('ground',5),('crosscut',5))]

# ── Fig1(c)·Fig3(b) 면제 = 노드 삭제 ────────────────────────────
import importlib.util as _iu
_sp=_iu.spec_from_file_location('co','stpa/carveout.py')
# carveout 은 import 시 출력하므로 노드 집합만 다시 계산한다
CFR_C=[f"107.{n}" for n in (52,53,56,57,59,61,63,64,65,67,69,71,73,74,77,79)]
CFR_D=[f"107.{n}" for n in (100,105,110,115,120,125,130,135,140,145,150,155,160,165)]
def deleted(k):
    if k.split('::')[0] in ('EU1139','EU947','EU945'): return True
    return any(k.startswith(f"US107::{s}") for s in CFR_C+CFR_D)
keep={k for k in N if not deleted(k)}
Ek=[e for e in E if e[0] in keep and e[1] in keep]
import types
# paths3 의 L/N 을 경찰경로 집합으로 바꿔 재실행
_L0=dict(P3.L); _N0=dict(P3.N)
P3.N={k:v for k,v in N.items() if k in keep}
P3.L={k:v for k,v in _L0.items() if k in keep}
Rp=P3.run(Ek,4)
ret_p={k for k,v in Rp.items() if v[0]==2}
aud_p=ret_p&TP
P3.N=_N0; P3.L=_L0
civ_ret={k for k,v in R4.items() if v[0]==2 and dom(k)=='aviation'}
civ_aud=civ_ret&TP
out['carveout']={'nodes_total':len(N),'nodes_deleted':len(N)-len(keep),
  'nodes_retained':len(keep),
  'civil_route':{'returned':len(civ_ret),'audited':len(civ_aud),
     'eu':sum(1 for k in civ_aud if k.split('::')[0].startswith('EU')),
     'us':sum(1 for k in civ_aud if k.split('::')[0].startswith('US'))},
  # Fig3(b) 는 '같은 기체' 를 두 경로에서 재정한 비교다. 지상·교차 규범은 면제가
  # 건드리지 않으므로 경로 비교는 항공 기관으로 한정한다. 한정하지 않으면 삭제와
  # 무관한 지상 결속이 경찰 경로 쪽에 섞여 비교가 성립하지 않는다.
  'police_route':{'returned':sum(1 for k in ret_p if k.split('::')[0] in AV),
     'audited':sum(1 for k in aud_p if k.split('::')[0] in AV),
     'survivors':sorted(k for k in aud_p if k.split('::')[0] in AV)},
  'police_route_whole_corpus':{'returned':len(ret_p),'audited':len(aud_p),
     '_note':'면제가 건드리지 않는 지상·교차를 포함한 값. 경로 비교에는 쓰지 않는다.'},
  'part89_returned_on_police':sorted(k for k in ret_p if k.startswith('US89')),
  'retained_aviation_nodes':sum(1 for k in keep if k.split('::')[0] in AV),
  'retained_aviation_auth':sum(1 for k in Rp if k.split('::')[0] in AV)}

# ── Fig2(c) 어휘 검증 위음성률 ──────────────────────────────────
try:
    out['lexicon_validation']=json.load(open('verify/lex_validation2.json',encoding='utf-8'))
except Exception as e:
    out['lexicon_validation']={'_status':f'[수집 불가: {e}]'}

json.dump(out,open('verify/fig_measures.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print('결속 정본',len(TP),'건')
print('hop4: 반환',byhop['hop4']['returned'],'· 결속',byhop['hop4']['audited'],
      f"· 정밀도 {byhop['hop4']['precision']:.3f}")
print('hop별 결속:',{k:v['audited'] for k,v in byhop.items()})
print('면제: 삭제',out['carveout']['nodes_deleted'],'· 민간',out['carveout']['civil_route'],
      '· 경찰',{k:v for k,v in out['carveout']['police_route'].items() if k!='survivors'})
print('경찰 생존자:',out['carveout']['police_route']['survivors'])
print('Part89 경찰경로 반환:',len(out['carveout']['part89_returned_on_police']))

# ── 재현성 구멍 메움 (2026-10-15) ────────────────────────────────
# _corpus_files 와 mid_chain 은 산출물 JSON 에만 있었고 이 스크립트가 만들지
# 않았다. 릴리스 트리에서 문서대로 재실행하면 두 키가 사라지고 FigM·FigS 가
# 죽는다. 원고는 "re-runs bit-identically" 라고 적고 있으므로 구멍을 메운다.
import hashlib as _hl
_man=json.load(open('corpus/MANIFEST.json',encoding='utf-8'))
def _is_input(e):
    """그래프에 투입되는 파일만 센다. 비교 대조본(원본 판)은 투입되지 않고,
    텍스트 변환본이 있는 PDF 는 그 .txt 쪽이 투입된다."""
    if '그래프 미투입' in (e.get('role') or ''): return False
    f=e['file']
    if f.endswith('.pdf') and any(x['file']==f[:-4]+'.txt' for x in _man): return False
    return True
_inp=[e for e in _man if _is_input(e)]
_ok=sum(1 for e in _inp
        if os.path.exists(os.path.join('corpus',e['file']))
        and _hl.sha256(open(os.path.join('corpus',e['file']),'rb').read()).hexdigest()==e['sha256'])
out['_corpus_files']=_ok
out['_corpus_files_input']=len(_inp)
out['_corpus_files_manifest']=len(_man)

# MID 결속 사슬. 제2조제1항이 열거하는 계측기 범주와 제7조제2항의 시장출시 의무.
_mid_duty=None
for _k,_v in N.items():
    if not _k.startswith('MID::'): continue
    _t=re.sub(r'\s+',' ',_v).strip()
    if 'made available on the market and/or put into use only if' in _t and _mid_duty is None:
        _mid_duty=_t
_flat=re.sub(r'\s+',' ',N.get('MID::art_2.1',''))
_cats=[]; _prev=_flat.find('concerning')
_prev=_prev+len('concerning') if _prev>=0 else 0
for _m in re.finditer(r'\((MI-\d{3})\)',_flat):
    _nm=re.sub(r'^and\s+','',re.sub(r'^[,;]\s*','',_flat[_prev:_m.start()].strip())).strip(' ,;')
    _cats.append({'code':_m.group(1),'name':_nm}); _prev=_m.end()
_mid_ret=sorted(k for k in R4 if k.startswith('MID::') and R4[k][0]==2)
out['mid_chain']={'duty':_mid_duty,'scope_article':'MID::art_2.1','categories':_cats,
                  'annex_requirement':'Annex I requires that the error of measurement not '
                                      'exceed the instrument-specific maximum permissible error.',
                  'returned':_mid_ret,'audited':sorted(set(_mid_ret)&TP),
                  '_note':'제2조제1항 열거 10범주. 어느 것도 법집행용 계측기가 아니다.'}
json.dump(out,open('verify/fig_measures.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print(f"  코퍼스 해시 일치 {_ok}/{len(_inp)} · MID 범주 {len(_cats)}종 · MID 반환 {len(_mid_ret)}")

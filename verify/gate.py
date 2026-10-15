# -*- coding: utf-8 -*-
"""원고 게이트. 구판 523개 검사는 작업트리와 함께 소실됐고, 그것을 복원하지 않고
이번 라운드에서 실제로 발생한 결함 계열을 설계로 막는 검사를 새로 세운다.

설계 원칙 네 가지.

 1. 기대값의 출처는 검사 대상이 아니다 (F-2).
    도판 신선도 검사가 build 스크립트가 쓴 해시를 기대값으로 삼아 실패할 수
    없었던 사고가 있었다. 모든 기대값은 측정(labels/tpset.json, graph/*)이나
    동결 기록에서만 온다. 조립·빌드 산출물에서 오지 않는다.

 2. 음성 검사와 양성 검사를 같이 둔다 (F-14).
    '구판 수치가 없다' 만으로는 분자를 고치고 p 값을 안 고친 것을 못 잡는다.
    '현행 측정값이 원고에 있다' 도 같이 본다.

 3. 사본이 둘이면 둘을 비교한다 (F-13 · F-16).
    tex/*_v23.tex 는 조립 산출물이라 고쳐도 되돌아간다. 후기는 세 곳에 있었고
    실제로 조판되는 것은 하나였다. 같은 글의 사본이 갈라지는지 본다.

 4. 조판물 자체를 읽는다 (F-12 · F-15).
    표가 두 번 인쇄되고 도판 글자가 본문 산문으로 조판되는 것은 원천만 봐서는
    안 잡힌다. PDF 텍스트를 직접 센다.

사용: python3 -I verify/gate.py  →  종료코드 0 통과 / 1 실패
"""
import json,math,os,re,subprocess,sys,hashlib
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
sys.path.insert(0,'graph'); sys.path.insert(0,'probe')
R=[]   # (게이트, 이름, 통과?, 메모)
def chk(g,name,ok,memo=''): R.append((g,name,bool(ok),memo))

# ── 측정 (기대값의 유일한 출처) ────────────────────────────────
import paths3 as P3
from collections import Counter
from scipy import stats
AUTH=P3.starts(); TP=set(json.load(open('labels/tpset.json',encoding='utf-8'))['tp'])
FIN=json.load(open('audit/labels_final.json',encoding='utf-8'))
CL=json.load(open('classify/final.json',encoding='utf-8'))
M=json.load(open('verify/fig_measures.json',encoding='utf-8'))
AV={'EU1139','EU947','EU945','US107','US89','USAC'}
GR={'JP道交法','KR도로교통법','KR도로교통법시행규칙','KR지능형로봇법','KR지능형로봇법시행령'}
iof=lambda k:k.split('::')[0]
auth=Counter(iof(k) for k in AUTH); bind=Counter(iof(k) for k in TP)
NA=sum(auth[i] for i in AV); NG=sum(auth[i] for i in GR)
A=sum(bind.get(i,0) for i in AV); G=sum(bind.get(i,0) for i in GR)
PDF='tex/main_v23.pdf'
TXT=''.join(open(f'tex/{x}_v23.tex',encoding='utf-8').read()
            for x in ('front','methods','results','discussion','appendix','back','main'))
FLAT=re.sub(r'\s+',' ',TXT).replace(chr(92)+'%','%').replace('{,}',',')
PT=subprocess.run(['pdftotext','-layout',PDF,'-'],capture_output=True,text=True).stdout
PA=json.load(open('recover/paras.json',encoding='utf-8'))
TB=json.load(open('recover/tables.json',encoding='utf-8'))
LOG=open('tex/main_v23.log',encoding='utf-8',errors='replace').read()

# ── G1 무결성: 라벨과 측정의 내부 정합 ─────────────────────────
chk(1,'결속 집합 = 감사 결속 라벨',TP=={r['id'] for r in FIN if r['label']=='binding'})
chk(1,'감사 기록 = 반환 수 91',len(FIN)==91,f'{len(FIN)}')
chk(1,'인가 총계 1,014',len(AUTH)==1014,f'{len(AUTH)}')
chk(1,'도메인 결속 합 = 총계',A+G+sum(bind.get(i,0) for i in bind if i not in AV|GR)==len(TP))
chk(1,'분류 기록 = 결속 수',len(CL['records'])==len(TP))
chk(1,'분류 대상 = 결속 집합',{r['provision'] for r in CL['records']}==TP)
chk(1,'분류 값은 두 가지뿐',{r['verdict'] for r in CL['records']}<={'SUPPLY','OPERATE'})
chk(1,'fig_measures 가 같은 라벨에서 나왔다',M['by_hop']['hop4']['audited']==len(TP))

# ── G2 표: 열 합과 Total 행 ───────────────────────────────────
def num(x):
    x=x.replace(',','').replace('%','').strip()
    try: return float(x)
    except: return None
for k,v in TB.items():
    rows=v['rows']; hdr=rows[0]; cap=v['caption']
    tot=[r for r in rows[1:] if r[0].strip().lower().startswith('total')]
    if not tot: continue
    t=tot[0]; body=[r for r in rows[1:] if r is not t]
    # Total 행은 셀 수가 적을 수 있다(1열에 설명이 들어간다). 오른쪽으로 맞춘다.
    off=len(hdr)-len(t)
    for ci in range(1,len(hdr)):
        ti=ci-off
        if ti<1 or ti>=len(t): continue
        tv=num(t[ti])
        if tv is None: continue
        vals=[num(r[ci]) for r in body if ci<len(r)]
        if not vals or any(x is None for x in vals): continue
        if not all(float(x).is_integer() for x in vals+[tv]): continue
        s_=sum(vals)
        if abs(s_-tv)<0.5:
            chk(2,f'표{k} {hdr[ci]} 열합 대 Total행',True); continue
        # 캡션이 비가산성을 명시하고 그 두 수치를 적고 있으면 면제. 아니면 실패.
        ok = ('do not add' in cap) and (f'{s_:.0f}' in cap.replace(',','')) and (f'{tv:.0f}' in cap.replace(',',''))
        chk(2,f'표{k} {hdr[ci]} 열합 대 Total행',ok,
            f'합 {s_:.0f} 대 {tv:.0f}'+(' (캡션이 명시, 면제)' if ok else ' (캡션에 설명 없음)'))

CODEMAP={'EU1139':'EU1139','EU947':'EU947','EU945':'EU945','US107':'US107','US89':'US89',
 'USAC':'USAC','JP-RTA':'JP道交法','KR-RTA':'KR도로교통법','KR-RTA-R':'KR도로교통법시행규칙',
 'KR-IRA':'KR지능형로봇법','KR-IRA-D':'KR지능형로봇법시행령','EUAI':'EUAI','MID':'MID',
 'LED':'LED','SMC1418':'SMC1418','CAGOV':'CAGOV'}
miss=[]
for row in TB['1']['rows'][1:]:
    if len(row)<6 or row[0] not in CODEMAP: continue
    want=auth.get(CODEMAP[row[0]]); got=num(row[4])
    if got is None or want is None or abs(got-want)>0.5: miss.append(f'{row[0]} 표{got} 실측{want}')
chk(2,'표 1 인가 열 = 그래프 실측',not miss,'; '.join(miss[:4]))
chk(2,'표 1 인가 열합 = 1,014',
    abs(sum(num(r[4]) for r in TB['1']['rows'][1:] if len(r)>=6 and r[0] in CODEMAP)-1014)<0.5,
    f"합 {sum(num(r[4]) for r in TB['1']['rows'][1:] if len(r)>=6 and r[0] in CODEMAP):.0f}")

# ── G3 음성: 구판 수치가 원고에 없다 ──────────────────────────
OLD=[('0.374','정밀도'),('5.24','비율비'),('34 are bindings','결속 총계'),('34 of 91','정밀도 분자'),
     ('[0.281, 0.476]','정밀도 Wilson'),('[0.239, 0.500]','정밀도 부트스트랩'),
     ('9.5%','항공률'),('3.4%','코퍼스률'),('22 of 23','면제 제거'),('0.21 [0.10, 0.41]','경찰경로 재현율'),
     ('[0.13, 0.74]','군집 보정 재현율'),('design effect of 5.10','설계효과'),('ICC','')]
HIST=['Lexicon false-negative rate & 11.1% & 12.6%','pooled false-negative rate from 11.1% to 11.4%',
      'returned 11 provisions and the audit rejected all 11',
      'the precision, which rises from 0.374 to 0.451',   # 재정 공개 문단: 구판을 구판으로 명시
      'resolved to 34 bindings, and that is the count the earlier version published']
def cnt(pat):
    out=0
    for m in re.finditer(re.escape(pat),FLAT):
        if m.start()>0 and FLAT[m.start()-1] in '0123456789.': continue
        seg=FLAT[max(0,m.start()-110):m.end()+110]
        if any(h in seg for h in HIST): continue
        out+=1
    return out
for pat,why in OLD:
    if pat=='ICC': continue
    chk(3,f'구판 "{pat}" 부재 ({why})',cnt(pat)==0,f'{cnt(pat)}회')

# ── G4 양성: 현행 측정값이 원고에 있다 ────────────────────────
def wilson(k,n,z=1.96):
    p=k/n; d=1+z*z/n; c=(p+z*z/(2*n))/d
    h=z/d*math.sqrt(p*(1-p)/n+z*z/(4*n*n)); return max(0,c-h),min(1,c+h)
def icc_anova(n,y):
    N=sum(n); p=sum(y)/N; K=len(n)
    msb=sum(ni*((yi/ni)-p)**2 for ni,yi in zip(n,y))/(K-1)
    msw=sum(yi*(1-yi/ni)+(ni-yi)*((yi/ni)**2) for ni,yi in zip(n,y))/(N-K)
    n0=(N-sum(ni*ni for ni in n)/N)/(K-1)
    return (msb-msw)/(msb+(n0-1)*msw), n0
inst=sorted(auth); ic,n0=icc_anova([auth[i] for i in inst],[bind.get(i,0) for i in inst])
D=1+(n0-1)*ic; se=math.sqrt(1/A-1/NA+1/G-1/NG); r=(A/NA)/(G/NG)
def h(p1,p2): return abs(2*math.asin(math.sqrt(p1))-2*math.asin(math.sqrt(p2)))
_,pc=stats.fisher_exact([[round(A/D),round((NA-A)/D)],[round(G/D),round((NG-G)/D)]])
SUP=sum(1 for x in CL['records'] if x['verdict']=='SUPPLY'); OPR=len(TP)-SUP
NUM={6:'Six',35:'Thirty-five',41:'Forty-one'}
POS=[(f'{len(TP)}','결속 총계'),(f'{len(TP)/91:.3f}','정밀도'),
     (f'[{wilson(len(TP),91)[0]:.3f}, {wilson(len(TP),91)[1]:.3f}]','정밀도 Wilson'),
     (f'{A/NA*100:.1f}%','항공률'),(f'{G/NG*100:.1f}%','지상률'),(f'{len(TP)/1014*100:.1f}%','코퍼스률'),
     (f'{r:.2f}','비율비'),(f'{h(A/NA,G/NG):.3f}','Cohen h'),(f'{ic:.3f}','ICC'),(f'{D:.2f}','설계효과'),
     (f'{1014/D:.0f}','유효표본'),(f'{pc:.3f}','설계효과 보정 Fisher p'),
     (f'{SUP}','공급 결속'),(f'{OPR}','운용 결속'),
     (NUM.get(OPR,str(OPR)),'운용 결속 영문'),(NUM.get(SUP,str(SUP)),'공급 결속 영문')]
for v,why in POS: chk(4,f'현행 "{v}" 존재 ({why})',v in FLAT)

# ── G5 조판물: 중복 인쇄 ──────────────────────────────────────
PTF=re.sub(r'\s+',' ',PT)
for k,v in TB.items():
    row=next((r for r in v['rows'][1:] if sum(1 for c in r if num(c) is not None)>=2),None)
    if not row: continue
    key=re.sub(r'\s+',' ',' '.join(c for c in row if c.strip()))
    chk(5,f'표{k} 평문 메아리 없음',PTF.count(key)<=1,f'행 전체 등장 {PTF.count(key)}회')
for sec in ('CRediT authorship contribution statement','Declaration of competing interest',
            'Data availability','Funding','Disclaimer'):
    chk(5,f'후기 "{sec}" 1회',PT.count(sec)==1,f'{PT.count(sec)}회')
for frag in ('(a) Measurement and determination are separate acts','(a) Paths add returns',
             '(a) Bindings concentrate in aviation','(a) The form exists','ICC = 0.074, design effect'):
    chk(5,f'구판 도판 글자 "{frag[:30]}" 부재',frag not in PT)

# ── G6 사본 분기 ──────────────────────────────────────────────
DUP=[('Disclaimer 본문','The views expressed are those of the authors',['tex/back_v23.tex'],'recover/paras.json'),
     ('AI 공시','A large language model was used in',['tex/back_v23.tex'],'recover/paras.json')]
for nm,anchor,live,dead in DUP:
    inlive=sum(open(f,encoding='utf-8').read().count(anchor) for f in live)
    indead=sum(s.count(anchor) for s in PA) if dead.endswith('paras.json') else 0
    chk(6,f'{nm} 사본 1곳만',inlive==1 and indead==0,f'정본 {inlive} · paras {indead}')
# recover/back.json 은 조립기가 읽지 않는 죽은 사본이었다. 2026-10-15 삭제했다.
# 죽은 파일에 표시를 다는 것보다 없애는 쪽이 낫다. 되살아나면 실패한다.
chk(6,'죽은 후기 사본이 없다',not os.path.exists('recover/back.json'))

# ── G7 도판: 수치 하드코딩 금지 · 측정에서 생성 ────────────────
MEASURED=[str(len(TP)),f'{A/NA*100:.1f}',f'{G/NG*100:.1f}',f'{len(TP)/91:.3f}',str(A),str(G),
          str(M['carveout']['nodes_deleted']),str(M['carveout']['retained_aviation_nodes'])]
for f in ('fig_concept','fig_method','fig_results','fig_scope'):
    src=open(f'fig2026/{f}.py',encoding='utf-8').read()
    body='\n'.join(l for l in re.sub(r'#.*','',src).split('\n')
        if not re.search(r'bound_left|set_[xy]lim|ticks=|fontsize|linewidth|figsize|dpi=|'
                         r'zorder|alpha=|pad=|markersize|set_[xy]ticks|annotate\(|bbox|wspace|hspace',l))
    hard=[v for v in MEASURED if re.search(r'(?<![\w.])'+re.escape(v)+r'(?![\w.])',body)]
    chk(7,f'{f}.py 에 측정값 하드코딩 없음',not hard,f'박힌 값 {hard}')
    chk(7,f'{f}.py 가 fig_measures 를 읽는다','fig_measures' in src)
    chk(7,f'{f}.py 가 tpset 을 직접 읽지 않는다','tpset' not in src)

# ── G8 빌드 ──────────────────────────────────────────────────
chk(8,'LaTeX 오류 0',LOG.count('\n!')==0,f"{LOG.count(chr(10)+'!')}")
chk(8,'미정의 인용 0',len(re.findall(r'Citation.*undefined',LOG))==0)
chk(8,'미정의 참조 0',len(re.findall(r'Reference.*undefined',LOG))==0)
chk(8,'누락 그림 0',len(re.findall(r'File.*not found',LOG))==0)
chk(8,'em-dash 0',PT.count('—')==0,f"{PT.count(chr(0x2014))}")
chk(8,'Appendix 중복 표기 0',PT.count('Appendix Appendix')==0)
PENDING=[]   # 2026-10-15 저자 확정으로 CRediT 등재 해제
ph=[m.group(0) for m in re.finditer(r'%?\s*\[CONFIRM\][^\n]*|TODO[^\n]*|FIXME[^\n]*|\[확인 필요\][^\n]*|\[수집 불가\][^\n]*|\[복원 필요\][^\n]*',TXT)]
unreg=[x for x in ph if not any(a.strip('% ') in x for a,_ in PENDING)]
chk(8,'등재되지 않은 플레이스홀더 0',not unreg,'; '.join(x[:60] for x in unreg[:3]))
chk(8,'도판 플레이스홀더 상자 0','figure file lost' not in PT)
chk(8,'도판 4장 조판됨',sum(PT.count(f'Figure {i}:') for i in (1,2,3,4))==4,
    f"{sum(PT.count(f'Figure {i}:') for i in (1,2,3,4))}")
chk(8,'texttt 깨짐 없음','extttREPRO' not in PT and 'extttv' not in PT)

# ── G9 공개 의무 ──────────────────────────────────────────────
BK=open('tex/back_v23.tex',encoding='utf-8').read()
chk(9,'AI 공시가 네 쓰임을 적는다','four places' in BK)
chk(9,'AI 공시가 맹검 3차 판독을 적는다','blind third pass' in BK)
chk(9,'AI 공시가 분류를 적는다','classified the bindings' in BK)
chk(9,'데이터 가용성이 세 라벨셋을 적는다','all three passes' in BK)
MAIN=open('tex/main_v23.tex',encoding='utf-8').read()
AFFIL={'Korean National Police Agency':'knpa','Defense Research Institute':'cbrn'}
# 면책이 가려야 할 기관 = 저자 소속으로 적힌 기관. 저자가 바뀌면 면책도 바뀐다.
for inst,lab in AFFIL.items():
    used=f'\\address[{lab}]' in MAIN
    chk(9,f'면책이 저자 소속 "{inst[:28]}" 을 가린다',(inst in BK)==used,
        f'소속표기 {used} · 면책언급 {inst in BK}')
chk(9,'저자 수 = 소속 지정 수',MAIN.count('\\author[')==5,f"{MAIN.count(chr(92)+'author[')}")
chk(9,'교신저자 1명',MAIN.count('\\corref{cor}')==1)
chk(9,'CRediT 가 저자 5인을 모두 적는다',
    all(f'\\textbf{{{n}:}}' in BK for n in ('Janghyeon Cha','Myeongsik Shin','Boyeon Park','Inae Han','Ku Kang')))
chk(9,'재정 사실이 본문에 있다','three passes stand at 43, 26 and 41' in FLAT)
chk(9,'라벨 불안정이 본문에 있다','not stable to the procedure' in FLAT)

# ── G10 장치가 자기 자신을 정확히 서술하는가 ──────────────────
V=json.load(open('verify/vocab_saturation.json',encoding='utf-8'))
for d,tot in ((1,10),(2,100),(3,1000)):
    held=V[f'decimals_{d}']['held']
    want=f'{held} of the {tot:,} '.replace('10 of the 10 ','10 of the 10 ')
    chk(10,f'어휘 포화 소수{d}자리 {held} 가 본문에 있다',
        re.search(rf'{held} of the {tot:,}'.replace(',',',?')+r'\s+\w+-decimal',FLAT) is not None,
        f'{held}/{tot}')
# 부록 B 와 데이터 가용성이 서로 다른 게이트 수를 적고 있었다(11 대 12).
# 두 자리를 각각 집어 서로 맞는지 본다. 다른 문장의 "three gates"(소실된 것들)는
# 그 수를 말하는 자리가 아니므로 건드리지 않는다.
_b=re.search(r'\b(\w+) gates run over the consistency suite',FLAT)
_d=re.search(r'suite of \d+ checks in (\w+) gates',FLAT)
chk(10,'부록 B 와 데이터 가용성의 게이트 수가 일치',
    bool(_b and _d) and _b.group(1).lower()==_d.group(1).lower(),
    f"부록B {_b.group(1) if _b else None} · 가용성 {_d.group(1) if _d else None}")
chk(10,'저장소 주소가 본문에 있다','github.com/bisu9082/determinate-binding' in FLAT)
chk(10,'제노도/DOI 기탁 약속이 남아 있지 않다',
    'deposited with a persistent identifier' not in FLAT and 'Zenodo' not in FLAT)

# ── G11 공개 아카이브 ────────────────────────────────────────
REL='release/determinate-binding'
SKIP11=False
ARCHIVE_CHECKS=([f'아카이브에 {d}/' for d in ('corpus','graph','probe','frozen','stpa','labels',
    'audit','classify','verify','fig2026','tex','recover')]
 +[f'아카이브에 {f}' for f in ('README.md','LICENSE','CITATION.cff','MANIFEST.sha256',
    'requirements.txt','REPRODUCIBILITY.md')]
 +['매니페스트가 전 파일을 덮는다','아카이브에 조판본 PDF 없음']
 +[f'CITATION.cff 에 {n}' for n in ('Janghyeon','Myeongsik','Boyeon','Inae','Ku')]
 +['CITATION.cff 커밋 핀이 본문 약속과 일치','README 가 결속 41 을 적는다']
 +[f'REPRODUCIBILITY 어휘 포화 소수{d}자리' for d in (1,2,3)])
if os.path.isdir(REL):
    need=[('corpus','16개 법령'),('graph','조항 그래프'),('probe','어휘집'),
          ('frozen','동결 규칙과 해시 사슬'),('stpa','STPA 제어구조·제약등록부'),
          ('labels','결속 정본'),('audit','감사 3회 판독'),('classify','허가 종류 분류'),
          ('verify','측정·검사 스크립트'),('fig2026','도판 코드'),('tex','원고 원본'),
          ('recover','원고 원천(조립 입력)')]
    for d,why in need:
        chk(11,f'아카이브에 {d}/ ({why})',os.path.isdir(os.path.join(REL,d)))
    for f in ('README.md','LICENSE','CITATION.cff','MANIFEST.sha256',
              'requirements.txt','REPRODUCIBILITY.md'):
        chk(11,f'아카이브에 {f}',os.path.exists(os.path.join(REL,f)))
    man=open(os.path.join(REL,'MANIFEST.sha256'),encoding='utf-8').read().splitlines()
    rows=[l for l in man if l and not l.startswith('#')]
    nfile=sum(len([f for f in fs if f!='MANIFEST.sha256'])
              for _,ds,fs in os.walk(REL) if '.git' not in _)
    chk(11,'매니페스트가 전 파일을 덮는다',len(rows)==nfile,f'매니페스트 {len(rows)} · 파일 {nfile}')
    chk(11,'아카이브에 조판본 PDF 없음',not os.path.exists(os.path.join(REL,'tex','main_v23.pdf')))
    cff=open(os.path.join(REL,'CITATION.cff'),encoding='utf-8').read()
    for n in ('Janghyeon','Myeongsik','Boyeon','Inae','Ku'):
        chk(11,f'CITATION.cff 에 {n}',n in cff)
    cff=open(os.path.join(REL,'CITATION.cff'),encoding='utf-8').read()
    # 원고가 "커밋이 CITATION.cff 에 기록돼 있다"고 적는다. 적었으면 있어야 한다.
    promises='commit this manuscript was built from is recorded in its CITATION.cff' in FLAT
    has=bool(re.search(r'^commit:\s*[0-9a-f]{40}\s*$',cff,re.M))
    chk(11,'CITATION.cff 커밋 핀이 본문 약속과 일치',promises==has,
        f'약속 {promises} · 실제 {has}')
    chk(11,'README 가 결속 41 을 적는다','41' in open(os.path.join(REL,'README.md'),encoding='utf-8').read())
    rp=open('REPRODUCIBILITY.md',encoding='utf-8').read()
    for d,tot in ((1,10),(2,100),(3,1000)):
        chk(11,f'REPRODUCIBILITY 어휘 포화 소수{d}자리',f"**{V[f'decimals_{d}']['held']}**" in rp)
else:
    # 아카이브 안에서 돌리면 release/ 가 없다. 실패가 아니라 건너뜀이다.
    # 다만 총수에는 센다 — 원고가 적는 수는 장치의 크기이지 이번 실행의 크기가 아니다.
    SKIP11=True
    for _n in ARCHIVE_CHECKS: R.append((11,_n,None,'건너뜀'))

# ── G10(이어서) 수 대조는 모든 게이트가 끝난 뒤에 센다 ─────────
# 하위 구간을 세면 게이트가 하나 더 생겨도 안 걸린다. 전체를 본다.
# 이번 라운드에 실제로 어긋나 있었다: 523검사·12게이트를 약속했고 같은 원고의
# 부록 B 는 11게이트라고 적고 있었다. 둘 다 존재하지 않는 수였다.
WORD=['','one','two','three','four','five','six','seven','eight','nine','ten','eleven','twelve']
_N=len(R)+2; _G=len({g for g,_,_,_ in R})
chk(10,'본문이 적은 검사 수 = 실제',f'{_N} checks' in FLAT,f'실제 {_N}')
chk(10,'본문이 적은 게이트 수 = 실제',f'{WORD[_G]} gates' in FLAT,f'실제 {_G} ({WORD[_G]})')

# ── 출력 ──────────────────────────────────────────────────────
G={}
for g,nm,ok,memo in R: G.setdefault(g,[]).append((nm,ok,memo))
NAMES={1:'무결성',2:'표 산술',3:'음성 (구판 부재)',4:'양성 (현행 존재)',5:'조판물 중복',
       6:'사본 분기',7:'도판 생성',8:'빌드',9:'공개 의무',10:'자기 서술',11:'공개 아카이브'}
fail=0
for g in sorted(G):
    bad=[x for x in G[g] if x[1] is False]
    skp=[x for x in G[g] if x[1] is None]
    fail+=len(bad)
    print(f"GATE {g} {NAMES[g]:16s} {len(G[g])-len(bad)-len(skp):3d}/{len(G[g]):3d} "
          f"{'통과' if not bad else '실패'}{' (건너뜀 '+str(len(skp))+')' if skp else ''}")
    for nm,ok,memo in bad: print(f'    x {nm}  {memo}')
print(f'\n검사 {len(R)}개 · 실패 {fail}개'+(' · GATE 11 건너뜀(아카이브 내부 실행)' if SKIP11 else ''))
if PENDING:
    print(f'\n[미결 등재 {len(PENDING)}건] 게이트가 통과시키되 매 실행 출력한다')
    for a,why in PENDING: print(f'  · {why}')
sys.exit(1 if fail else 0)

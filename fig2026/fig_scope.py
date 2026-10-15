# -*- coding: utf-8 -*-
"""FigS — 센싱 성능을 걸 법형식, 그 열거된 적용범위, 그리고 수의 강건성.
수치·문언은 verify/fig_measures.json 에서만 읽는다."""
import json,os,sys
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
sys.path.insert(0,'fig2026')
from style2 import *
from matplotlib.patches import FancyBboxPatch,FancyArrowPatch
import numpy as np

M=json.load(open('verify/fig_measures.json',encoding='utf-8'))
CH=M['mid_chain']; H=M['by_hop']; LV=M['lexicon_validation']

fig=plt.figure(figsize=(21,7.4))
gs=fig.add_gridspec(1,3,width_ratios=[1.12,0.94,1.20],wspace=0.42,
                    left=0.02,right=0.985,top=0.87,bottom=0.09)
def blank(ax):
    ax.set_xticks([]); ax.set_yticks([]); ax.set_xlim(0,1); ax.set_ylim(0,1)
    for sp in ax.spines.values(): sp.set_visible(False)
    ax.set_facecolor('white')

# ── (a) 결속 사슬 ──────────────────────────────────────────────
ax=fig.add_subplot(gs[0,0]); blank(ax)
steps=[('Art. 7(2) duty',
        'Member States shall take all appropriate measures\n'
        'to ensure that measuring instruments are made\n'
        'available on the market and/or put into use\n'
        'only if they satisfy this Directive',C_PALE),
       ('Annex I requirement',
        'the error of measurement shall not exceed the\n'
        'instrument-specific maximum permissible error',C2)]
y0=0.955
for i,(t,body,fc) in enumerate(steps):
    h=0.255 if i==0 else 0.175
    y=y0-i*0.37-h
    ax.add_patch(FancyBboxPatch((0.03,y),0.94,h,
        boxstyle='round,pad=0.010,rounding_size=0.02',fc=fc,ec=INK,lw=1.2,zorder=3))
    ax.text(0.05,y+h-0.030,t,ha='left',va='top',fontsize=FS_ANNOT,
            fontweight='bold',color='white' if i else INK,zorder=4)
    ax.text(0.05,y+h-0.085,body,ha='left',va='top',fontsize=FS_FOOT,
            color='white' if i else '#333333',zorder=4,linespacing=1.45)
    if i==0:
        ax.add_patch(FancyArrowPatch((0.5,y-0.012),(0.5,y-0.095),arrowstyle='-|>',
            mutation_scale=18,lw=1.6,color=INK,zorder=4))
ax.text(0.03,0.30,'This is the structure the predicate searches for.',
        ha='left',va='top',fontsize=FS_ANNOT,color=INK)
ax.text(0.03,0.225,'“all appropriate measures” is the same form the predicate treats as\n'
        'a hedge elsewhere and did not catch here.',
        ha='left',va='top',fontsize=FS_FOOT,color='#444444',style='italic')
ax.text(0.03,0.085,f"The Directive returns {len(CH['returned'])} provision and the audit confirms "
        f"{len(CH['audited'])}.\nThe corpus therefore holds no verified positive control: this is\n"
        f"the legal form, not a confirmed instance of it.",
        ha='left',va='top',fontsize=FS_FOOT,color=C1)
panel(ax,'a')

# ── (b) 열거된 적용범위 ─────────────────────────────────────────
ax=fig.add_subplot(gs[0,1]); blank(ax)
cats=CH['categories']
ax.text(0.02,0.975,f'Article 2(1) enumerates {len(cats)} instrument categories',
        ha='left',va='top',fontsize=FS_AXIS-2,color=INK)
for i,c in enumerate(cats):
    y=0.885-i*0.0665
    ax.add_patch(FancyBboxPatch((0.03,y-0.045),0.94,0.050,
        boxstyle='round,pad=0.004,rounding_size=0.012',fc=C_PALE,ec='#BBB09A',lw=0.8,zorder=3))
    ax.text(0.055,y-0.020,c['code'],ha='left',va='center',fontsize=FS_FOOT,
            color='#6B5B45',fontweight='bold',zorder=4)
    nm=c['name']
    if len(nm)>52: nm=nm[:49].rsplit(' ',1)[0]+'…'
    ax.text(0.215,y-0.020,nm,ha='left',va='center',fontsize=FS_FOOT,color=INK,zorder=4)
ax.add_patch(FancyBboxPatch((0.03,0.045),0.94,0.145,
    boxstyle='round,pad=0.010,rounding_size=0.02',fc='white',ec=C1,lw=1.6,ls='--',zorder=3))
ax.text(0.50,0.117,'None is a law-enforcement measuring instrument, a CBRN\n'
        'detector, an airborne sensing payload, or any instrument whose\n'
        'reading supports a police determination.',
        ha='center',va='center',fontsize=FS_FOOT,color=INK,zorder=4,linespacing=1.45)
panel(ax,'b')

# ── (c) 규칙 변형별 수 ──────────────────────────────────────────
ax=fig.add_subplot(gs[0,2]); tidy(ax,grid='x')
up=[('Provision read alone','no_edges'),('hop ≤ 2','hop2'),
    ('hop ≤ 4 (adopted)','hop4'),('hop ≤ 5','hop5')]
rows=[(lab,H[k]['returned'],C2,'returned') for lab,k in up]
rows+=[(lab,H[k]['audited'],C1,'audited') for lab,k in up]
proj=LV['projection']
rows+=[('Projected for lexicon\nfalse negatives',
        proj['missed_point']+H['hop4']['audited'],C3,'projected')]
y=np.arange(len(rows))[::-1]
vals=[r[1] for r in rows]; cols=[r[2] for r in rows]
ax.barh(y,vals,color=cols,edgecolor=INK,lw=0.8,height=0.60,zorder=3)
# 외삽 행만 구간을 붙인다
pi=len(rows)-1
lo=proj['missed_ci'][0]+H['hop4']['audited']; hi=proj['missed_ci'][1]+H['hop4']['audited']
ax.errorbar([vals[pi]],[y[pi]],xerr=[[vals[pi]-lo],[hi-vals[pi]]],fmt='none',
            ecolor=INK,elinewidth=1.3,capsize=5,capthick=1.3,zorder=4)
for i,(yy,v) in enumerate(zip(y,vals)):
    if i==pi:   # 외삽 행은 구간선이 지나가므로 숫자를 막대 위로 올린다
        ax.text(v,yy+0.36,str(v),ha='center',va='bottom',fontsize=FS_ANNOT,
                color=INK,zorder=5)
    else:
        ax.text(v+4,yy,str(v),ha='left',va='center',fontsize=FS_ANNOT,color=INK,zorder=5)
ax.text(hi+7,y[pi],f'[{lo}, {hi}]',ha='left',va='center',fontsize=FS_FOOT,
        color='#444444',zorder=5)
ax.set_yticks(y); ax.set_yticklabels([r[0] for r in rows],fontsize=FS_TICK-1)
ax.set_xlim(0,255); ax.set_xticks([0,50,100,150,200])
ax.spines['bottom'].set_bounds(0,200)
ax.set_xlabel('Authorising provisions',fontsize=FS_AXIS)
from matplotlib.patches import Patch
ax.legend(handles=[Patch(fc=C2,ec=INK,label='Returned coordinates'),
                   Patch(fc=C1,ec=INK,label='Audited coordinates'),
                   Patch(fc=C3,ec=INK,label='Audited, projected')],
          loc='upper right',bbox_to_anchor=(1.0,1.0),frameon=True,
          framealpha=0.95,fontsize=FS_LEG)
ax.axhline(y[3]-0.5,color='#AAAAAA',lw=1.0,ls=':')
ax.text(0.0,-0.175,'The two blocks are not added: the lexicon projection estimates missed bindings\n'
        'and therefore applies to the audited count, not to what the predicate returns.\n'
        'The interval is the Wilson interval of the false-negative rate carried onto that projection.',
        transform=ax.transAxes,ha='left',va='top',fontsize=FS_FOOT,
        color='#444444',style='italic')
panel(ax,'c')

for ext in ('png','pdf'):
    fig.savefig(f'fig2026/FigS.{ext}',dpi=200,bbox_inches='tight',facecolor='white')
print('fig2026/FigS.png · FigS.pdf 저장')

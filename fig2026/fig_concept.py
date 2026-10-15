# -*- coding: utf-8 -*-
"""FigC — 무엇을 측정하는가. 수치는 verify/fig_measures.json 에서만 읽는다."""
import json,os,sys
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
sys.path.insert(0,'fig2026')
from style2 import *
from matplotlib.patches import FancyBboxPatch,FancyArrowPatch
import numpy as np

M=json.load(open('verify/fig_measures.json',encoding='utf-8'))
T=M['tiers_adopted']; CO=M['carveout']

fig=plt.figure(figsize=(21,6.6))
gs=fig.add_gridspec(1,3,width_ratios=[1.38,0.92,1.12],wspace=0.20,
                    left=0.02,right=0.985,top=0.86,bottom=0.10)

def blank(ax):
    ax.set_xticks([]); ax.set_yticks([]); ax.set_xlim(0,1); ax.set_ylim(0,1)
    for sp in ax.spines.values(): sp.set_visible(False)
    ax.set_facecolor('white')

def rbox(ax,x,y,w,h,txt,fc,tc=INK,fs=None,bold=False):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.012,rounding_size=0.02',
        fc=fc,ec=INK,lw=1.2,zorder=3))
    ax.text(x+w/2,y+h/2,txt,ha='center',va='center',fontsize=fs or FS_ANNOT,
            color=tc,zorder=4,fontweight='bold' if bold else 'normal',linespacing=1.45)

def arrow(ax,x1,y1,x2,y2,style='-|>',ls='-',col=INK):
    ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2),arrowstyle=style,ls=ls,
        mutation_scale=17,lw=1.5,color=col,zorder=2,shrinkA=2,shrinkB=2))

# ── (a) 측정과 판단은 분리된 행위다 ─────────────────────────────
ax=fig.add_subplot(gs[0,0]); blank(ax)
# 상자 폭을 글자가 넘지 않도록 잡는다. 종전 0.205 에서 'incident commander' 가 잘렸다.
W,H=0.200,0.205
ys=0.59
XS=[0.010,0.258,0.506,0.754]
rbox(ax,XS[0],ys,W,H,'Sensing\nsubsystem\nmeasures only',C_PALE,fs=FS_FOOT+1)
rbox(ax,XS[1],ys,W,H,'Analyst\nadvises\na criterion',C_PALE,fs=FS_FOOT+1)
rbox(ax,XS[2],ys,W,H,'Incident\ncommander\ndetermines',C2,tc='white',bold=True,fs=FS_FOOT+1)
rbox(ax,XS[3],ys,W,H,'Persons\nbeneath\nconsequence',C_NEUTRAL,fs=FS_FOOT+1)
for x in XS[:3]:
    arrow(ax,x+W+0.016,ys+H/2,x+W+0.040,ys+H/2)
ax.text(0.5,0.47,'The determination is a human act taken on an advised criterion.\n'
        'The sensing subsystem never classifies.',ha='center',va='top',
        fontsize=FS_FOOT,color='#444444',style='italic')
ax.add_patch(FancyBboxPatch((0.015,0.085),0.955,0.235,
    boxstyle='round,pad=0.012,rounding_size=0.02',fc='white',ec=C1,lw=1.6,ls='--',zorder=3))
ax.text(0.4925,0.2025,'What this paper measures: does any provision make that\n'
        'authorisation depend on a named evaluation of the measurement it rests on?',
        ha='center',va='center',fontsize=FS_ANNOT,color=INK,zorder=4,linespacing=1.5)
panel(ax,'a')

# ── (b) 인가항이 설 수 있는 세 단 ───────────────────────────────
ax=fig.add_subplot(gs[0,1]); tidy(ax)
names=['Tier 2\ndeterminate\nbinding','Tier 1\nindeterminate\nbinding','Tier 0\nno evaluation\nreached']
vals=[T['t2'],T['t1'],T['t0']]
cols=[C1,C2,C_NEUTRAL]
x=np.arange(3)
ax.bar(x,vals,color=cols,edgecolor=INK,lw=0.9,width=0.64,zorder=3)
for xx,v in zip(x,vals):
    ax.text(xx,v+14,f'{v:,}',ha='center',va='bottom',fontsize=FS_ANNOT,
            fontweight='bold',color=INK)
ax.set_xticks(x); ax.set_xticklabels(names,fontsize=FS_TICK-1)
ax.set_ylabel(f"Authorising provisions (of {T['auth']:,})",fontsize=FS_AXIS)
ax.set_ylim(0,max(vals)*1.30); bound_left(ax,0,500,ticks=[0,100,200,300,400,500])
ax.text(0.5,0.985,'The determinate operator must sit on the\n'
        'authorising provision itself; it is not\naccumulated along the path.',
        transform=ax.transAxes,ha='center',va='top',fontsize=FS_FOOT,
        color='#444444',style='italic',bbox=box(ec='none'))
panel(ax,'b')

# ── (c) 면제 = 그래프의 노드 삭제 ───────────────────────────────
ax=fig.add_subplot(gs[0,2]); blank(ax)
tot=CO['nodes_total']; dele=CO['nodes_deleted']; keep=CO['nodes_retained']
bx,bw=0.06,0.88; by,bh=0.60,0.17
fr=dele/tot
ax.add_patch(FancyBboxPatch((bx,by),bw,bh,boxstyle='round,pad=0.006,rounding_size=0.015',
    fc=C_PALE,ec=INK,lw=1.2,zorder=3))
ax.add_patch(FancyBboxPatch((bx,by),bw*fr,bh,boxstyle='round,pad=0.006,rounding_size=0.015',
    fc=C1,ec=INK,lw=1.2,zorder=4))
ax.text(bx+bw*fr/2,by+bh/2,f'{dele:,}\ndeleted',ha='center',va='center',
        fontsize=FS_FOOT,color='white',fontweight='bold',zorder=5,linespacing=1.3)
ax.text(bx+bw*fr+(bw*(1-fr))/2,by+bh/2,f'{keep:,} retained',ha='center',va='center',
        fontsize=FS_ANNOT,color=INK,zorder=5)
ax.text(bx,by+bh+0.045,f'Provision graph: {tot:,} nodes',ha='left',va='bottom',
        fontsize=FS_AXIS-2,color=INK)
ax.text(bx,0.52,'Deleted by the police and public-aircraft carve-out',
        ha='left',va='top',fontsize=FS_ANNOT,color=INK)
lines=['Reg. (EU) 2018/1139 Art. 2(3)(a) and the acts resting on it',
       '14 CFR Part 107 Subparts C and D, per AC 00-1.1B']
for i,t in enumerate(lines):
    ax.text(bx+0.025,0.44-i*0.075,'•  '+t,ha='left',va='top',
            fontsize=FS_FOOT,color='#444444')
ax.text(bx,0.235,'Mission, lexicons and rule are held constant, so the two\n'
        'routes are compared under one rule.',ha='left',va='top',
        fontsize=FS_FOOT,color='#444444',style='italic')
ax.text(bx,0.085,f"What is left in force on the police route: "
        f"{CO['retained_aviation_nodes']} aviation nodes\n"
        f"holding {CO['retained_aviation_auth']} authorising provisions, among which "
        f"{CO['police_route']['audited']} binds.",
        ha='left',va='top',fontsize=FS_FOOT,color=INK)
panel(ax,'c')

for ext in ('png','pdf'):
    fig.savefig(f'fig2026/FigC.{ext}',dpi=200,bbox_inches='tight',facecolor='white')
print('fig2026/FigC.png · FigC.pdf 저장')

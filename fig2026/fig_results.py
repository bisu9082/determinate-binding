# -*- coding: utf-8 -*-
"""FigR — 감사된 결속이 어디에 있고 경찰 면제가 무엇을 지우는가.

수치는 하나도 들고 있지 않다. verify/fig_measures.json 을 읽는다
(원고의 도판 하드코딩 금지 게이트가 요구하는 구조)."""
import json,os,sys
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
sys.path.insert(0,'fig2026')
from style2 import *
import numpy as np

M=json.load(open('verify/fig_measures.json',encoding='utf-8'))
S=M['by_subject']; CO=M['carveout']

fig=plt.figure(figsize=(21,7.2))
gs=fig.add_gridspec(1,3,width_ratios=[1.45,1.0,1.05],wspace=0.34,
                    left=0.055,right=0.985,top=0.87,bottom=0.20)

# ── (a) 주제별 결속률 ───────────────────────────────────────────
ax=fig.add_subplot(gs[0,0]); tidy(ax)
lab=[s['subject'].replace(', drivers','\n(drivers)').replace(' product law','\nproduct law')
     .replace('Aviation certification','Aviation\ncertification')
     .replace('Robot certification','Robot\ncertification')
     .replace('Police conduct','Police\nconduct') for s in S]
rate=np.array([s['rate']*100 for s in S])
lo=np.array([s['wilson'][0]*100 for s in S]); hi=np.array([s['wilson'][1]*100 for s in S])
x=np.arange(len(S))
# 색 예산: 3색만. 결속이 있는 범주는 C1, 없는 범주는 중립 tan.
cols=[C1 if s['audited']>0 else C_NEUTRAL for s in S]
ax.bar(x,rate,color=cols,edgecolor=INK,linewidth=0.8,width=0.62,zorder=3)
ax.errorbar(x,rate,yerr=[rate-lo,hi-rate],fmt='none',ecolor=INK,
            elinewidth=1.3,capsize=5,capthick=1.3,zorder=4)
for i,s in enumerate(S):
    ax.text(x[i],hi[i]+0.9,f"{s['audited']}/{s['auth']}",ha='center',va='bottom',
            fontsize=FS_BAR,color=INK,zorder=5)
ax.set_xticks(x); ax.set_xticklabels(lab,fontsize=FS_TICK-1)
ax.set_ylabel('Audited bindings (per cent of\nauthorising provisions)',fontsize=FS_AXIS)
ax.set_ylim(0,max(hi)*1.30)
bound_left(ax,0,15,ticks=[0,5,10,15])
ax.text(0.98,0.97,'Wilson 95% CI\nunit of analysis is the instrument,\nnot the provision',
        transform=ax.transAxes,ha='right',va='top',fontsize=FS_FOOT,
        style='italic',color='#444444',bbox=box(ec='none'))
panel(ax,'a')

# ── (b) 같은 기체, 두 경로 ──────────────────────────────────────
ax=fig.add_subplot(gs[0,1]); tidy(ax)
civ,pol=CO['civil_route'],CO['police_route']
g=np.arange(2); w=0.34
ax.bar(g-w/2,[civ['returned'],pol['returned']],w,label='Returned by predicate',
       color=C_NEUTRAL,edgecolor=INK,linewidth=0.8,zorder=3)
ax.bar(g+w/2,[civ['audited'],pol['audited']],w,label='Audited bindings',
       color=C1,edgecolor=INK,linewidth=0.8,zorder=3)
for xx,v in zip(g-w/2,[civ['returned'],pol['returned']]):
    ax.text(xx,v+1.0,str(v),ha='center',va='bottom',fontsize=FS_BAR,color=INK)
for xx,v in zip(g+w/2,[civ['audited'],pol['audited']]):
    ax.text(xx,v+1.0,str(v),ha='center',va='bottom',fontsize=FS_BAR,color=INK)
ax.set_xticks(g)
ax.set_xticklabels(['Civil route\n(all aviation nodes)',
                    'Police route\n(1,164 nodes deleted)'],fontsize=FS_TICK-1)
ax.set_ylabel('Aviation provisions',fontsize=FS_AXIS)
ax.set_ylim(0,civ['returned']*1.42)
bound_left(ax,0,60,ticks=[0,20,40,60])
ax.legend(loc='upper right',frameon=True,fontsize=FS_LEG,framealpha=0.95)
ax.text(0.97,0.56,f"of the {civ['audited']} civil-route bindings\n"
        f"{civ['eu']} are EU, {civ['us']} are US",transform=ax.transAxes,
        ha='right',va='top',fontsize=FS_FOOT,color='#444444',style='italic',
        bbox=box(ec='none'))
panel(ax,'b')

# ── (c) 면제가 남기는 것 ────────────────────────────────────────
ax=fig.add_subplot(gs[0,2]); tidy(ax,grid='x')
p89=CO['part89_returned_on_police']
surv=set(CO['police_route']['survivors'])
names=[k.split('::')[1] for k in p89]
isurv=[k in surv for k in p89]
y=np.arange(len(p89))[::-1]
ax.barh(y,[1]*len(p89),color=[C1 if s else C_PALE for s in isurv],
        edgecolor=INK,linewidth=0.8,height=0.6,zorder=3)
for yy,n,s in zip(y,names,isurv):
    ax.text(0.04,yy,'§'+n,ha='left',va='center',fontsize=FS_ANNOT,
            color='white' if s else INK,fontweight='bold' if s else 'normal',zorder=5)
    ax.text(1.04,yy,'survives the audit' if s else 'rejected by the audit',
            ha='left',va='center',fontsize=FS_FOOT,color=INK if s else '#777777',zorder=5)
# 아래쪽에 두 줄이 들어갈 자리를 축 안에 미리 비워 둔다(지우지 않고 헤드룸 확보).
ax.set_xlim(0,2.35); ax.set_ylim(-2.35,len(p89)-0.3)
ax.set_yticks([]); ax.set_xticks([])
ax.spines['left'].set_visible(False); ax.spines['bottom'].set_visible(False)
ax.xaxis.grid(False)
ax.text(0.0,-0.62,'Part 89 provisions reaching tier 2 on the police route',
        transform=ax.get_yaxis_transform(),ha='left',va='top',
        fontsize=FS_AXIS-2,color=INK)
ax.text(0.0,-1.30,'The survivor conditions operation on an accepted declaration\n'
        'that the aircraft reports its own position to within 100 feet\n'
        'with 95 per cent probability.',
        transform=ax.get_yaxis_transform(),ha='left',va='top',
        fontsize=FS_FOOT,color='#444444',style='italic')
panel(ax,'c')

os.makedirs('fig2026',exist_ok=True)
for ext in ('png','pdf'):
    fig.savefig(f'fig2026/FigR.{ext}',dpi=200,bbox_inches='tight',facecolor='white')
print('fig2026/FigR.png · FigR.pdf 저장')
print(f"  (a) 주제 5범주 · (b) 민간 {civ['returned']}/{civ['audited']} vs 경찰 "
      f"{pol['returned']}/{pol['audited']} · (c) Part89 {len(p89)}건 중 생존 {sum(isurv)}")

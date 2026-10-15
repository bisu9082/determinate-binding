# -*- coding: utf-8 -*-
"""FigM — 측정에 대한 점검. 수치는 verify/fig_measures.json 에서만 읽는다."""
import json,os,sys
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
sys.path.insert(0,'fig2026')
from style2 import *
import numpy as np

M=json.load(open('verify/fig_measures.json',encoding='utf-8'))
H=M['by_hop']; D=M['by_domain']; LV=M['lexicon_validation']

fig=plt.figure(figsize=(21,11.5))
gs=fig.add_gridspec(2,2,hspace=0.46,wspace=0.26,
                    left=0.058,right=0.985,top=0.93,bottom=0.075)

# ── (a) hop 경계별 반환과 결속 ──────────────────────────────────
ax=fig.add_subplot(gs[0,0]); tidy(ax)
order=['no_edges','hop1','hop2','hop3','hop4','hop5']
xs=np.arange(len(order))
ret=[H[k]['returned'] for k in order]; aud=[H[k]['audited'] for k in order]
ax.plot(xs,ret,'-o',color=C2,lw=2.2,ms=9,mec='white',mew=1.4,
        label='Returned by predicate',zorder=4)
ax.plot(xs,aud,'--s',color=C1,lw=2.2,ms=9,mec='white',mew=1.4,
        dashes=(5,3),label='Audited bindings',zorder=4)
for i,(r,a) in enumerate(zip(ret,aud)):
    ax.text(xs[i],r+2.6,str(r),ha='center',va='bottom',fontsize=FS_BAR,color=C2)
    ax.text(xs[i],a-3.4,str(a),ha='center',va='top',fontsize=FS_BAR,color=C1)
ax.set_xticks(xs)
ax.set_xticklabels(['none\n(read alone)','1','2','3','4\n(adopted)','5'],fontsize=FS_TICK-1)
ax.set_xlabel('Maximum path length (hops)',fontsize=FS_AXIS)
ax.set_ylabel('Authorising provisions',fontsize=FS_AXIS)
ax.set_ylim(20,118); bound_left(ax,30,100,ticks=[30,50,70,90])
d_ret=ret[4]-ret[0]; d_aud=aud[4]-aud[0]
ax.text(0.50,0.985,f'none $\\rightarrow$ 4 hops adds {d_ret} returns and {d_aud} bindings;\n'
        f'the other {d_ret-d_aud} are false positives',
        transform=ax.transAxes,ha='center',va='top',fontsize=FS_FOOT,
        color='#444444',style='italic',bbox=box(ec='none'))
ax.legend(loc='center left',bbox_to_anchor=(0.02,0.42),frameon=True,
          framealpha=0.95,fontsize=FS_LEG)
panel(ax,'a')

# ── (b) 도메인 구성 ────────────────────────────────────────────
ax=fig.add_subplot(gs[0,1]); tidy(ax)
names=[f"{d['domain'].capitalize()}\n({d['instruments']})" for d in D]
auth=[d['auth'] for d in D]; retd=[d['returned'] for d in D]; audd=[d['audited'] for d in D]
x=np.arange(len(D)); w=0.26
ax.bar(x-w,auth,w,label='Authorising',color=C_NEUTRAL,edgecolor=INK,lw=0.8,zorder=3)
ax.bar(x  ,retd,w,label='Returned',color=C2,edgecolor=INK,lw=0.8,zorder=3)
ax.bar(x+w,audd,w,label='Audited bindings',color=C1,edgecolor=INK,lw=0.8,zorder=3)
for xx,v in list(zip(x-w,auth))+list(zip(x,retd))+list(zip(x+w,audd)):
    ax.text(xx,(v*1.18+0.25) if v>0 else 1.05,f'{v:,}',ha='center',va='bottom',
            fontsize=FS_BAR,color=INK if v>0 else '#777777')
ax.set_yscale('log'); ax.set_ylim(0.6,2600)
ax.set_yticks([1,10,100,1000]); ax.set_yticklabels(['1','10','100','1,000'])
ax.yaxis.set_minor_locator(NullLocator())
ax.spines['left'].set_bounds(1,1000)
ax.set_xticks(x); ax.set_xticklabels(names,fontsize=FS_TICK)
ax.set_ylabel('Provisions (log scale)',fontsize=FS_AXIS)
ax.legend(loc='upper right',ncol=1,frameon=True,framealpha=0.95,fontsize=FS_LEG)
ax.text(0.015,0.985,'instrument count in parentheses',transform=ax.transAxes,
        ha='left',va='top',fontsize=FS_FOOT,color='#444444',style='italic')
panel(ax,'b')

# ── (c) 어휘 검증 위음성률 ──────────────────────────────────────
ax=fig.add_subplot(gs[1,0]); tidy(ax,grid='x')
ST=LV['strata']; W=LV['weighted']
rows=[('English',ST['EN']),('Korean',ST['KR']),('Japanese',ST['JP'])]
y=np.arange(len(rows)+1)[::-1]
vals=[r[1]['rate']*100 for r in rows]+[W['rate']*100]
los =[r[1]['wilson'][0]*100 for r in rows]+[W['logit_ci'][0]*100]
his =[r[1]['wilson'][1]*100 for r in rows]+[W['logit_ci'][1]*100]
labs=[f"{r[0]}\nn = {r[1]['n']}" for r in rows]+['Stratum-weighted\nestimate']
cols=[C3,C3,C3,C1]
ax.barh(y,vals,color=cols,edgecolor=INK,lw=0.8,height=0.56,zorder=3)
ax.errorbar(vals,y,xerr=[np.array(vals)-np.array(los),np.array(his)-np.array(vals)],
            fmt='none',ecolor=INK,elinewidth=1.3,capsize=5,capthick=1.3,zorder=4)
for yy,v,h in zip(y,vals,his):
    ax.text(h+1.6,yy,f'{v:.1f}%',ha='left',va='center',fontsize=FS_ANNOT,color=INK)
ax.set_yticks(y); ax.set_yticklabels(labs,fontsize=FS_TICK)
ax.set_xlim(0,58); ax.set_xticks([0,10,20,30,40,50])
ax.spines['bottom'].set_bounds(0,50)
ax.set_xlabel('False-negative rate among provisions scored indeterminate (per cent)',
              fontsize=FS_AXIS-1)
ax.text(0.0,-0.235,'Wilson 95% CI on the strata, logit interval on the weighted estimate. '
        'The bottom bar is weighted by each\nstratum\u2019s share of the tier-1 population, '
        'not pooled: allocation was equal and the strata are not.',
        transform=ax.transAxes,ha='left',va='top',fontsize=FS_FOOT,
        color='#444444',style='italic')
panel(ax,'c')

# ── (d) 무엇이 재현되고 무엇이 안 되는가 ────────────────────────
ax=fig.add_subplot(gs[1,1]); ax.set_facecolor('white')
ax.set_xticks([]); ax.set_yticks([])
for sp in ax.spines.values(): sp.set_visible(False)
items=[(True ,'Corpus against recorded SHA-256',f"{M['_corpus_files']} of {M['_corpus_files']} files"),
       (True ,'Graph and tier counts from the frozen rules',
              f"{H['hop4']['auth']:,} authorising, {H['hop4']['t2']} returned"),
       (True ,'Carve-out as node deletion',
              f"{M['carveout']['nodes_deleted']:,} of {M['carveout']['nodes_total']:,} nodes"),
       (True ,'Domain rates and the surviving binding','reproduced'),
       (False,'Adjudication labels from the published audit record',
              'rule 8-A needs the cited provision; the record omits it'),
       (False,'Constraint-class step (blind re-writing)','outcome agreement 5 of 12')]
for i,(ok,what,note) in enumerate(items):
    yy=0.95-i*0.150
    ax.text(0.015,yy,'✓' if ok else '✕',fontsize=20,fontweight='bold',
            color=C3 if ok else C1,ha='left',va='center',transform=ax.transAxes)
    ax.text(0.075,yy+0.028,what,fontsize=FS_ANNOT+1,color=INK,
            ha='left',va='center',transform=ax.transAxes)
    ax.text(0.075,yy-0.038,note,fontsize=FS_FOOT,color='#555555',style='italic',
            ha='left',va='center',transform=ax.transAxes)
ax.set_xlim(0,1); ax.set_ylim(0,1)
ax.text(0.015,-0.02,'No constraint-level count is reported, because the step that '
        'would produce one does not reproduce.',transform=ax.transAxes,
        ha='left',va='top',fontsize=FS_FOOT,color='#444444',style='italic')
panel(ax,'d')

for ext in ('png','pdf'):
    fig.savefig(f'fig2026/FigM.{ext}',dpi=200,bbox_inches='tight',facecolor='white')
print('fig2026/FigM.png · FigM.pdf 저장')

# -*- coding: utf-8 -*-
"""도판 공통 스타일. 2026-10-14 재건.

Ku 의 도판 규칙을 그대로 코드로 옮긴다.
· 색: 색맹 안전 검증을 통과한 3색만 쓴다 (#C94F4A / #E8943A / #3A6EA8).
  teal #4AACB0 과 dusty blue #5B8DB8 는 ΔE 9.4 로 같이 쓰지 않는다.
  4범주 이상이면 색을 늘리지 않고 패널을 쪼개거나 선 스타일을 2차 인코딩으로 쓴다.
· 패널 라벼는 축 좌상단 모서리에 포인트 단위 고정 오프셋으로 붙인다(비율 금지).
· 도판 안에 'Figure N' 문자열을 쓰지 않는다. 패널 구분은 (a)(b)(c) 뿐.
· 텍스트는 지우지 않고 헤드룸을 확보해 그 안에 넣는다.
· matplotlib 텍스트에 \\% 를 쓰지 않는다(리터럴로 렌더된다).
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import NullLocator

plt.rcParams.update({
 'pdf.fonttype':42,'ps.fonttype':42,'font.family':'sans-serif',
 'font.sans-serif':['DejaVu Sans'],
 'axes.labelsize':16,'xtick.labelsize':14,'ytick.labelsize':14,
 'legend.fontsize':12,'font.size':14,'axes.linewidth':1.1,
 'axes.spines.top':False,'axes.spines.right':False,
 'figure.facecolor':'white','axes.facecolor':'white',
 'axes.axisbelow':True,
})
FS_PANEL,FS_AXIS,FS_TICK,FS_BAR,FS_LEG,FS_ANNOT,FS_FOOT = 28,16,14,11,12,12,11

# 색맹 안전 검증 통과 3색 + 중립 2색
C1='#C94F4A'   # warm red   — 강조 / 결속
C2='#E8943A'   # amber      — 2번째
C3='#3A6EA8'   # deep blue  — 3번째
C_NEUTRAL='#C9A882'   # warm tan  — 중립 배경 범주
C_PALE='#EADFCB'      # 연한 크림 — 잔여/배경
INK='#1A1A1A'
GRID=dict(color='#DDDDDD',ls='--',lw=0.6)

def panel(ax,letter,fs=FS_PANEL,dy=6):
    """축 좌상단 모서리에 포인트 고정 오프셋으로 붙인다. 패널 높이와 무관."""
    ax.annotate(f'({letter})',xy=(0.0,1.0),xycoords='axes fraction',
                xytext=(0,dy),textcoords='offset points',
                fontsize=fs,fontweight='bold',va='bottom',ha='left',
                color=INK,annotation_clip=False)

def tidy(ax,grid='y'):
    ax.set_facecolor('white')
    if grid in ('y','both'): ax.yaxis.grid(True,**GRID)
    if grid in ('x','both'): ax.xaxis.grid(True,**GRID)
    ax.tick_params(labelsize=FS_TICK)

def bound_left(ax,lo,hi,ticks=None):
    """헤드룸을 만들되 축선과 눈금은 데이터 범위까지만 둔다."""
    if ticks is not None: ax.set_yticks(ticks)
    ax.spines['left'].set_bounds(lo,hi)
    ax.yaxis.set_minor_locator(NullLocator())

def box(fc='white',ec='#333333'):
    return dict(fc=fc,ec=ec,boxstyle='round,pad=0.30',alpha=0.93)

# -*- coding: utf-8 -*-
"""부록 B 와 데이터 가용성을 실제 장치에 맞춘다.

부록 B 는 존재하지 않는 장치를 서술하고 있었다. 거기 적힌 네 게이트 가운데
셋(봉인 적용범위, 검사 분류, 신선도)은 작업트리와 함께 소실됐고, 넷째(증거 어휘)는
스크립트가 사라져 9/63/128 을 재현할 수 없다. 어휘 게이트는 원고의 가장 날카로운
자기비판이므로 버리지 않고 원고 문언대로 다시 구현해 다시 쟀다. 결과는 공개값보다
나쁘다 — 소수 1자리에서 어휘가 포화되어 그 자리에서는 게이트가 실패할 수 없다.
방향이 우리에게 불리하므로 그대로 적는다.

데이터 가용성은 523검사·12게이트를 약속하고 있었다. 실제는 103검사·10게이트다."""
import json,os,re,sys
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
V=json.load(open('verify/vocab_saturation.json',encoding='utf-8'))
d1,d2,d3=(V[f'decimals_{d}']['held'] for d in (1,2,3))
PA=json.load(open('recover/paras.json',encoding='utf-8'))

B267=('Nine gates run over the consistency suite, and a tenth measures how weak one of them is. '
 'The suite and the gates can establish that the numbers in this paper agree with the released '
 'outputs and with each other; they cannot establish that the outputs are correct, and the '
 'distinction matters enough to state the coverage of each gate rather than its pass count. The '
 'repository file REPRODUCIBILITY.md lists every gate with the inputs that break it, the inputs '
 'that do not, and the measured size of the gap where one has been measured. Four statements '
 'about coverage belong here, because earlier versions of this paper implied more than the '
 'apparatus delivers and because the apparatus itself has since been rebuilt.')

B268=('The first concerns provenance. The gate that requires every measured quantity in the '
 'manuscript to be present in a released output compares values, not provenance. Its vocabulary '
 'is built by rounding every number in every released output to one, two and three decimal places '
 'and converting proportions to percentages, so a fabricated value that happens to coincide with '
 'any released number at the precision the manuscript prints it will pass. We measured the size of '
 'this by generating every decimal between zero and one at each precision and counting how many '
 'the vocabulary already holds: '
 f'{d1} of the 10 one-decimal values, {d2} of the 100 two-decimal values, and {d3} of the 1,000 '
 'three-decimal values. At one decimal place the vocabulary is saturated and the gate cannot fail. '
 'At two places a number has to clear a bar that about half the possible values do not clear, and '
 'at three places the bar is real. These three counts are a re-measurement. The script that '
 'produced the figures an earlier version printed was lost with the working tree, and the '
 'reimplementation written from the sentence above does not reproduce them; the released counts '
 'are the ones this paper now stands on, they are written by verify/vocab\\_saturation.json, and a '
 'released check fails if this paragraph and that output disagree. The direction of the correction '
 'is against us at one decimal place, where the earlier figure implied a bar that does not exist. '
 'A zero count from the provenance gate means no manuscript number failed to coincide with a '
 'released one; it does not mean every manuscript number came from the output a reader would '
 'expect it to come from.')

B269=('The second concerns what replaced the apparatus this appendix used to describe. The '
 'consistency suite of the earlier version, and three gates beside it, were lost with the working '
 'tree and are not recovered. What runs now was built to close the defect classes this project '
 'actually produced rather than to restore a pass count, and its first design rule is that no '
 'check may take its expected value from the thing it checks. The gate that was previously '
 'reported as true but uninformative is the reason for that rule: the runner recompiled the '
 'typeset files immediately before checking that they were current, so inside the run the check '
 'could not fail. Expected values now come from the measurement or from the freeze record and '
 'never from what the build writes.')

B270=('The third concerns negative checks. A check that a superseded number is absent passes as '
 'soon as that number is gone, which is not the same as the manuscript being right. Twice in this '
 'project a count was corrected while a statistic computed from it was left alone, and the absence '
 'check passed over it. The suite therefore pairs every negative check with a positive one that '
 'requires the current measured value to be present in the manuscript, and the figures that carry '
 'the counts are regenerated from the measurement rather than written by hand.')

B271=('The fourth concerns what no check in this apparatus reads. Three defects in this manuscript '
 'were visible only in the typeset output and not in any source file: every table was printed '
 'twice, the text layer of four superseded figures was set as body prose, and the four figures '
 'were replaced by empty placeholder boxes by the assembler on every build. The suite now reads '
 'the typeset PDF directly for all three. That it had to be taught to do so is the general point '
 'of this appendix: an apparatus tests what it was pointed at, and a pass count says nothing about '
 'where it was pointed.')

E=[(267,B267),(268,B268),(269,B269),(270,B270),(271,B271)]
anchors={267:'Eleven gates run beside the consistency suite',
         268:'The gate that requires every measured quantity',
         269:'the manuscript prints it will pass',
         270:'The gate that counts what the seal does not cover',
         271:'The gate that classifies every check by what it compares'}
for i,_ in E:
    if anchors[i] not in PA[i]: print(f'부록 B 문단 {i} 앵커 불일치'); sys.exit(1)
if 'One freshness check remains true but uninformative' not in PA[272]:
    print('문단 272 앵커 불일치'); sys.exit(1)
for i,txt in E: PA[i]=txt
PA.pop(272)   # 신선도 문단은 B269 에 흡수됐다
json.dump(PA,open('recover/paras.json','w',encoding='utf-8'),ensure_ascii=False,indent=0)
print(f'부록 B 5문단 교체 · 1문단 흡수 (어휘 포화 {d1}/{d2}/{d3})')

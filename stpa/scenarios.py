# -*- coding: utf-8 -*-
"""STPA 4단계 — 손실 시나리오. 'UCA가 왜 발생하는가'에서 인과제약(CC)이 나온다.
여기서 조작자 자격(N14)·인간기계 적합성(N15)이 유도된다. UCA 단계에서는 원리상 나올 수 없었다.

인과요인 분류 (Leveson):
 A 제어 알고리즘 부적절      B 프로세스 모델 결함
 C 피드백 결손·지연·오류     D 제어경로 실패
 E 피제어 프로세스 실패      F 조정·중복 제어 충돌
"""
SCEN = [
# ── UCA-05-N (통신 두절 시 정지 불가) ──
("LS-05-1","UCA-05-N","B",
 "The operator's process model holds that the stop control always reaches the platform, because in "
 "training the link never failed. The operator therefore does not pre-position an independent stop.",
 "CC-05-1: Operator qualification must be demonstrated against the degraded conditions the mission "
 "actually presents, not only against nominal conditions.", ["N14"]),
("LS-05-2","UCA-05-N","D",
 "The independent stop exists but is a control the operator cannot actuate while wearing the "
 "respiratory and hand protection the zone requires.",
 "CC-05-2: Every control that must remain available in the contaminated zone must be actuatable in "
 "the protective equipment prescribed for that zone, and this must be verified with the equipment on.",
 ["N15"]),
# ── UCA-09-P (미검증 계측 위에 판정) ──
("LS-09-1","UCA-09-P","B",
 "The commander's process model treats the number displayed as a measurement of contamination, when "
 "the instrument reports a raw signal that has not been referenced to any standard for this analyte.",
 "CC-09-1: What an instrument reports and what a decision needs must be distinguished on the display "
 "itself; where they differ the difference must be stated, not left to the reader's model.", ["N06","N15"]),
("LS-09-2","UCA-09-P","A",
 "The SOP fixes a threshold but not the instrument class it was derived for, so the commander applies "
 "a criterion validated on a laboratory instrument to a field sensor.",
 "CC-09-2: Qualification to make the determination must include the instrument classes the criterion "
 "was validated on, and must be refreshed when the fielded instrument changes.", ["N14"]),
# ── UCA-06-P (교정 만료 상태 측정) ──
("LS-06-1","UCA-06-P","C",
 "Calibration status is held in a maintenance record the operator does not see during the mission; "
 "no feedback path carries it to the point of use.",
 "CC-06-1: Calibration validity must be carried in the same feedback path as the reading it qualifies.",
 ["N06","N15"]),
# ── UCA-04-P (부적격 채취매체) ──
("LS-04-1","UCA-04-P","C",
 "Media types are distinguishable by colour and label, but the operator sees them only through the "
 "platform camera at the resolution and colour fidelity the link allows.",
 "CC-04-1: Any distinction the operator must make remotely has to be verifiable through the actual "
 "sensing and link path, not through direct inspection.", ["N15","N06"]),
# ── UCA-10-T (회수 후 지연 이관) ──
("LS-10-1","UCA-10-T","E",
 "Custody transfer requires a written entry at recovery, but the recovering personnel are in "
 "protective equipment and the entry is deferred until doffing, creating the unrecorded interval.",
 "CC-10-1: The custody entry required at recovery must be completable in the protective posture that "
 "recovery is conducted in.", ["N15","N17"]),
# ── UCA-A03-P (미실증 기체로 사람 위 비행) ──
("LS-A03-1","UCA-A03-P","B",
 "The remote pilot's process model does not separate 'the aircraft is airworthy' from 'the aircraft is "
 "in a category that permits flight over people', because the police route certifies the first to itself "
 "and never states the second.",
 "CC-A03-1: Pilot qualification must include the distinction between airworthiness and operating-category "
 "eligibility, and must state which of the two the fielded route actually establishes.", ["N14"]),
("LS-A03-2","UCA-A03-P","A",
 "The self-certification permitted on the police route has no stated content, so the operator has no "
 "criterion against which to refuse a platform.",
 "CC-A03-2: Where an operator may self-certify, the content of that certification must be stated well "
 "enough that a refusal is possible.", ["N14","N13"]),
# ── UCA-A04-P (목적제한 없는 촬영) ──
("LS-A04-1","UCA-A04-P","C",
 "The payload's field of view exceeds what the operator's display shows, so material outside the "
 "authorized subject is recorded without the operator being aware of it.",
 "CC-A04-1: The recorded field must not exceed the field the operator is shown.", ["N15","N20"]),
# ── UCA-02-N (조건 변화 후 철수 미명령) ──
("LS-02-1","UCA-02-N","C",
 "The condition that should trigger withdrawal (wind shift) is observable to the meteorological cell "
 "but not on any feedback path that reaches the commander during the mission.",
 "CC-02-1: Each stated withdrawal trigger must be bound to a feedback path that reaches the deciding "
 "authority within the mission.", ["N08"]),
# ── UCA-07-N (안전상태 미진입) ──
("LS-07-1","UCA-07-N","E",
 "The triggering sensor drifts within its unvalidated range and the autonomy has no way to detect that "
 "its own trigger input is out of trust.",
 "CC-07-1: A protective behaviour must be able to detect loss of trust in its own trigger input.",
 ["N06","N10"]),
]
if __name__=='__main__':
    from collections import Counter
    print(f"손실 시나리오 {len(SCEN)}건 · 인과제약 {len({s[4].split(':')[0] for s in SCEN})}건")
    print("인과요인 분류:",dict(Counter(s[2] for s in SCEN)))
    cov=Counter(n for s in SCEN for n in s[5])
    print("기존 통제항목 도달:",dict(cov))
    print()
    for s in SCEN:
        print(f"  {s[0]:9s}[{s[2]}] ←{s[1]:12s} → {s[4].split(':')[0]}  {', '.join(s[5])}")
        print(f"      {s[4].split(':',1)[1].strip()[:112]}")

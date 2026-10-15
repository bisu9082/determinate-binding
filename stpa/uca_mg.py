# -*- coding: utf-8 -*-
"""M-G (CBRN 현장 시료채취) UCA — 증거·측정 연쇄 중심.
유형 N=미제공 / P=제공 / T=시점·순서 / D=지속·조기중단.  각 UCA → 안전제약(SC) → 통제항목 후보."""
UCA = [
# CA6 측정 개시/중단/재측정  (C2 → P2)
("UCA-06-P","CA6","P","A measurement is commanded while the sensor's calibration has lapsed or its "
    "operating envelope (temperature, humidity, interferent load) is exceeded.", ["H3"],
    "SC-06-1: A measurement may be relied upon only while the instrument's calibration is valid and "
    "its stated operating envelope is met, and the instrument must make both observable to the operator."),
("UCA-06-N","CA6","N","No repeat measurement is commanded after a reading that falls in the "
    "instrument's stated uncertainty band around a decision threshold.", ["H3"],
    "SC-06-2: A reading within the declared uncertainty band of a decision threshold must trigger a "
    "defined repeat or confirmatory procedure before it is reported."),
("UCA-06-T","CA6","T","The measurement is taken before the sampling disturbance has settled, or after "
    "the volatile analyte has dispersed.", ["H3","H5"],
    "SC-06-3: The admissible time window between disturbance and measurement must be stated for each "
    "analyte class and enforced by the procedure."),
# CA4 시료 채취 동작 (C2 → P1)
("UCA-04-P","CA4","P","Sampling is commanded with a container, tool or surface that is not qualified "
    "for the analyte, cross-contaminating the sample.", ["H5"],
    "SC-04-1: Sampling media and tooling must be qualified for the analyte class, and the qualification "
    "must be identifiable from the sample record."),
("UCA-04-D","CA4","D","Sampling continues past the point at which the platform's own contamination "
    "begins to load the sample.", ["H5"],
    "SC-04-2: A platform contamination limit must be defined beyond which further sampling is not valid."),
# CA8 분석 결과 및 기준 조언 제출 (C4 → C1)
("UCA-08-N","CA8","N","The analytical result is submitted without the criterion it should be read "
    "against, or without its uncertainty.", ["H3"],
    "SC-08-1: An analytical result must be transmitted together with the criterion applied and the "
    "uncertainty of the measurement; a bare value is not a reportable result."),
("UCA-08-P","CA8","P","A criterion is advised that was validated for a different matrix, platform or "
    "analyte than the one measured.", ["H3"],
    "SC-08-2: The provenance and validated scope of any advised criterion must accompany the advice."),
("UCA-08-T","CA8","T","The result reaches the commander after the decision it was meant to inform has "
    "already been taken.", ["H3","H7"],
    "SC-08-3: The latency budget from measurement to result must be stated and must be shorter than the "
    "decision cycle it serves."),
# CA9 오염 여부 판정 (C1 → ALL)   ※ 지휘관 판정. 기준은 사전 SOP에 고정되어야 한다.
("UCA-09-P","CA9","P","A determination is made on a measurement whose instrument was never shown to "
    "meet any performance standard for the analyte and setting.", ["H3","H1"],
    "SC-09-1: A determination that carries consequences for persons must rest on an instrument whose "
    "performance for that analyte and setting has been demonstrated against a stated standard."),
("UCA-09-N","CA9","N","No determination is made and the scene is left in an indeterminate state while "
    "persons remain exposed.", ["H1","H7"],
    "SC-09-2: A maximum time to determination must be defined, after which a default protective posture applies."),
("UCA-09-T","CA9","T","The determination is made before the confirmatory procedure required by SC-06-2 "
    "has completed.", ["H3"],
    "SC-09-3: The determination must not precede completion of the confirmatory procedure that the "
    "reading triggered."),
("UCA-09-D","CA9","D","The determination is not revisited after conditions that grounded it change "
    "(wind shift, new release, decontamination completed).", ["H7"],
    "SC-09-4: Defined changes of condition must re-open the determination."),
# CA10 보관연속성 이관 (C2 → C5)  ※ Ku: 회수 즉시
("UCA-10-T","CA10","T","Transfer to custody happens after the platform has been moved, cleaned or "
    "re-tasked, leaving an unrecorded interval.", ["H5"],
    "SC-10-1: Custody transfer must occur at recovery, before any decontamination, movement or re-tasking "
    "of the platform, and the interval must be recorded."),
("UCA-10-N","CA10","N","No transfer record is produced because the robot, not a person, held the sample "
    "for the whole interval.", ["H5"],
    "SC-10-2: The period during which a machine holds a sample must itself be a recorded custody link, "
    "with the holder identified as the platform and its state logged."),
# CA11 제염 명령 (C1 → C2)
("UCA-11-T","CA11","T","Decontamination is ordered before the sample and its record have been transferred.", ["H5"],
    "SC-11-1: Decontamination must not precede custody transfer."),
("UCA-11-N","CA11","N","No decontamination is ordered and the platform re-enters a clean area or a "
    "subsequent mission.", ["H1","H5"],
    "SC-11-2: A release criterion must be defined and met before the platform re-enters a clean area, "
    "and the release must be verifiable."),
# CA1 채취 명령 (C1 → C2)  ※ Ku: 사전 SOP에 정립
("UCA-01-P","CA1","P","Sampling is ordered at a location or in a manner the SOP does not cover, so no "
    "pre-established criterion exists for reading the result.", ["H3","H7"],
    "SC-01-1: The sampling plan must map each ordered sample to a pre-established procedure and criterion; "
    "an unmapped sample must be flagged as such in the record."),
("UCA-01-N","CA1","N","No sampling is ordered where the SOP requires it, so the determination rests on "
    "observation alone.", ["H3"],
    "SC-01-2: Omission of an SOP-required sample must be recorded with its reason."),
]

# ===== 잔여 제어행위 4개 (CA2·CA3·CA5·CA7) — M-G 완결 =====
UCA += [
# CA2 임무 범위 변경 / 철수 명령 (C1 → C2)
("UCA-02-N","CA2","N","No withdrawal is ordered after a condition that grounded the deployment changes "
   "(wind shift, secondary release, arrival of uninvolved persons).", ["H7","H1"],
   "SC-02-1: The conditions that trigger withdrawal must be defined in advance and must be observable "
   "from the feedback the operator actually receives."),
("UCA-02-P","CA2","P","Withdrawal is ordered without instruction on the sample and record already held, "
   "so they are left on scene or carried out unrecorded.", ["H5"],
   "SC-02-2: A withdrawal order must carry a disposition for any sample and record already held."),
("UCA-02-T","CA2","T","Withdrawal is ordered only after an accumulated-dose or contamination limit has "
   "already been reached.", ["H1","H2"],
   "SC-02-3: Withdrawal thresholds must act on the projected time to reach a limit, not on the limit "
   "having been reached."),
# CA3 오염구역 진입 / 이탈 (C2 → P1)
("UCA-03-P","CA3","P","Entry is commanded with a platform whose resistance to, and decontaminability "
   "for, the suspected agent class has never been established.", ["H5","H1"],
   "SC-03-1: Entry may be commanded only with a platform established as decontaminable for the agent "
   "class in question, and the establishing evidence must be identifiable."),
("UCA-03-N","CA3","N","No egress is commanded and the platform dwells in the zone beyond its "
   "established tolerance.", ["H5"],
   "SC-03-2: A dwell limit referenced to the platform's established tolerance must be defined and enforced."),
("UCA-03-T","CA3","T","Egress occurs before the decontamination point and route are established, "
   "carrying contamination into the clean area.", ["H1","H5"],
   "SC-03-3: The egress route and the decontamination point must be fixed before entry is commanded."),
# CA5 정지 / 긴급이탈 (C2 → P1)
("UCA-05-N","CA5","N","Stop cannot be commanded because the authority to stop depends on the same link "
   "that has failed.", ["H2"],
   "SC-05-1: Stop authority must hold independently of the command link, and that independence must be "
   "demonstrated rather than asserted."),
("UCA-05-T","CA5","T","Stop is commanded while the manipulator holds an open sample container.", ["H5"],
   "SC-05-2: Stop behaviour must define the state of any sample held at the moment it executes."),
("UCA-05-D","CA5","D","Motion resumes automatically after the stop condition clears, without an "
   "explicit human instruction.", ["H2"],
   "SC-05-3: Release from a stop must require an explicit human instruction."),
# CA7 성능저하 안전상태 (C3 → P1)
("UCA-07-P","CA7","P","The safe state is entered as a halt in the middle of the contaminated zone, "
   "where the platform cannot be recovered without exposing personnel.", ["H1","H5"],
   "SC-07-1: A degraded-mode safe state must be defined so that recovery remains possible without "
   "exposing personnel."),
("UCA-07-N","CA7","N","The safe state is not entered although a dose or contamination limit has been "
   "exceeded, because the sensor that would trigger it was never validated for that quantity.", ["H1","H3"],
   "SC-07-2: Any sensor whose reading triggers a protective behaviour must be validated for the quantity "
   "and range in which that trigger sits."),
("UCA-07-T","CA7","T","The safe state is entered on a transient link dropout that would have recovered "
   "within the mission's tolerance.", ["H7"],
   "SC-07-3: The dropout duration that triggers the safe state must be stated and matched to the mission."),
]

if __name__=='__main__':
    from collections import Counter
    print(f"M-G UCA {len(UCA)}건 · 안전제약 {len({u[5].split(':')[0] for u in UCA})}건")
    print("유형:",dict(Counter(u[2] for u in UCA)))
    print("제어행위별:",dict(Counter(u[1] for u in UCA)))
    print("\n=== 유도된 안전제약 (→ 통제항목 후보) ===")
    for u in UCA: print(f"  {u[5].split(':')[0]:9s} {u[5].split(':',1)[1].strip()[:110]}")

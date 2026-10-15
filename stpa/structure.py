# -*- coding: utf-8 -*-
"""설계 ⓒ — 임무 STPA에서 통제항목을 유도한다.
22개 항목을 저자가 나열하는 대신, 2개 완전 STPA의 안전제약(Safety Constraint)이 항목 목록이 된다."""

LOSSES = [
 ("L1","Death or injury to a member of the public"),
 ("L2","Death or injury to a police officer or operator"),
 ("L3","Unlawful interference with a protected right (privacy, assembly, movement)"),
 ("L4","Loss or corruption of evidence, rendering it inadmissible or misleading"),
 ("L5","Damage to property or critical infrastructure"),
 ("L6","Loss of public trust in the deploying agency"),
]
HAZARDS = [
 ("H1","The robot applies or transmits physical force to a person outside the authorized envelope", ["L1","L2","L6"]),
 ("H2","The robot operates without a human authority able to interrupt it in the available time", ["L1","L2","L5","L6"]),
 ("H3","The robot's reported state diverges from its actual state during an authorization decision", ["L1","L2","L4","L5"]),
 ("H4","The robot collects, retains or transfers data outside the authorized purpose", ["L3","L6"]),
 ("H5","Material handled by the robot loses identity or integrity", ["L4"]),
 ("H6","The robot occupies a position or trajectory incompatible with surrounding traffic or persons", ["L1","L2","L5"]),
 ("H7","The robot continues a mission after the conditions that justified the authorization have changed", ["L1","L3","L6"]),
]

# ---- 임무 1: 지상 (G 경로) — CBRN/위험물질 현장 시료채취 ----
# Ku 교정(2026-09-19): 센서는 측정만, 분석관은 결과 산출 + 기준 '조언'만,
#   오염 여부 판정과 채취 '명령'은 현장지휘관, 그 판단기준은 사전 SOP에 정립되어 있어야 함.
#   보관연속성 이관은 로봇 회수 즉시.
M_G = dict(
 id="M-G", title="Ground robot sampling at a CBRN / hazardous-material scene under an incident commander",
 pathway="G",
 controllers=[
  ("C1","Incident commander",
      "orders sampling, determines whether contamination is present, directs decontamination; "
      "the criteria for that determination are to be fixed in advance by SOP, not improvised on scene"),
  ("C2","Robot operator",
      "executes movement, sampling and measurement commands; holds stop authority"),
  ("C3","On-board autonomy",
      "path following, obstacle avoidance, degraded-mode safe state"),
  ("C4","Analyst",
      "produces analytical results from the measurement data and MAY ADVISE on the applicable "
      "criteria or thresholds; DOES NOT make the contamination determination"),
  ("C5","Evidence custodian",
      "receives the sample and its record immediately on robot recovery"),
 ],
 processes=[("P1","Robot platform (mobility, manipulator, sampler)"),
            ("P2","Detection and measurement subsystem — MEASURES ONLY, does not classify"),
            ("P3","Collected sample and its record"),
            ("P4","Contaminated zone and the persons in or near it")],
 control_actions=[
  ("CA1","C1","C2","Order a sample to be taken at a stated location (per SOP)"),
  ("CA2","C1","C2","Revise the mission envelope or order withdrawal"),
  ("CA3","C2","P1","Command entry into or egress from the contaminated zone"),
  ("CA4","C2","P1","Command the sampling action"),
  ("CA5","C2","P1","Command stop / emergency disengagement"),
  ("CA6","C2","P2","Start, stop or repeat a measurement"),
  ("CA7","C3","P1","Enter degraded-mode safe state (link loss, dose limit, power)"),
  ("CA8","C4","C1","Submit the analytical result and advise the applicable criterion"),
  ("CA9","C1","ALL","Determine whether contamination is present and direct what follows"),
  ("CA10","C2","C5","Transfer the sample and record to custody on recovery"),
  ("CA11","C1","C2","Order decontamination of the platform and the sample container"),
 ],
 feedback=[("F1","P1","C2","Position, attitude, manipulator state, power, dose accumulated"),
           ("F2","P2","C2","Raw measurement value, sensor health, calibration validity"),
           ("F3","P2","C4","Measurement data for analysis"),
           ("F4","C4","C1","Analytical result + advised criterion"),
           ("F5","C2","C1","Mission state, sampling completed, container sealed"),
           ("F6","P3","C5","Seal state, transfer record, chain entries")],
 # 이 임무의 구조적 요점: 측정(P2) → 분석(C4) → 판정(C1) 이 설계상 분리되어 있다.
 # 지휘관의 판정은 확정적이되, 그 판정이 딛고 선 측정의 타당성을 어떤 법규도 조건화하지 않으면
 # 확정적 결정이 미검증 측정 위에 놓인다. 이것이 본 논문의 인터페이스 공백 명제다.
 key_chain=("F2","F3","F4","CA9"),
)

# ---- 임무 2: 항공 (AC/AP 대조 경로) ----
M_A = dict(
 id="M-A", title="Police sUAS searching and tracking over an urban area, flown either on the civil route or as a public aircraft operation",
 pathway="AC|AP",
 controllers=[
  ("C1","Incident commander", "authorizes the flight and its purpose"),
  ("C2","Remote pilot in command", "holds final authority over the operation"),
  ("C3","On-board autonomy / flight controller", "stabilization, return-to-home, geofence"),
  ("C4","Airspace authority (ATC / COA conditions)", "grants and constrains access to airspace"),
  ("C5","Evidence custodian", "receives imagery and derived records"),
 ],
 processes=[("P1","Unmanned aircraft"),("P2","Imaging and sensing payload"),
            ("P3","Airspace and persons beneath the flight path"),("P4","Imagery and derived records")],
 control_actions=[
  ("CA1","C1","C2","Authorize the flight for a stated purpose and area"),
  ("CA2","C4","C2","Grant, condition or withdraw airspace access"),
  ("CA3","C2","P1","Command flight over or near people"),
  ("CA4","C2","P2","Command imaging of a person, dwelling or vehicle"),
  ("CA5","C2","P1","Command return-to-home / land / terminate flight"),
  ("CA6","C3","P1","Execute geofence or lost-link behaviour"),
  ("CA7","C2","C5","Transfer imagery and derived records to custody"),
 ],
 feedback=[("F1","P1","C2","Position, altitude, energy state, link quality"),
           ("F2","P2","C2","Field of view, recording status, retention state"),
           ("F3","P3","C2","Persons beneath, other aircraft, ground risk"),
           ("F4","C2","C1","Purpose compliance, observed conditions"),
           ("F5","C2","C4","Conformance with airspace conditions")],
)
MISSIONS=[M_G,M_A]
if __name__=='__main__':
    for m in MISSIONS:
        print(f"\n=== {m['id']} · {m['pathway']} ===\n  {m['title']}")
        print(f"  제어자 {len(m['controllers'])} · 피제어 {len(m['processes'])} · 제어행위 {len(m['control_actions'])} · 피드백 {len(m['feedback'])}")
        for cid,src,dst,txt in m['control_actions']:
            print(f"    {cid}  {src}→{dst}  {txt}")
    print(f"\n손실 {len(LOSSES)} · 위험 {len(HAZARDS)}")
    print(f"제어행위 총 {sum(len(m['control_actions']) for m in MISSIONS)}개 → UCA 4유형 적용 시 최대 {sum(len(m['control_actions']) for m in MISSIONS)*4}개")

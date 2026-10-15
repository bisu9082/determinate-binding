# -*- coding: utf-8 -*-
"""M-A (도심 수색·추적 sUAS) UCA. 동일 임무·동일 제어구조를 AC(민간경로)·AP(경찰경로)로 각각 통과시킨다."""
UCA = [
# CA3 사람 위/근처 비행 (C2 → P1)
("UCA-A03-P","CA3","P","Flight over people is commanded with an aircraft whose impact energy and "
   "exposed-rotor characteristics have never been shown to meet a stated limit.", ["H1","H6"],
   "SCA-03-1: Flight over people may be conducted only with an aircraft demonstrated against a stated "
   "kinetic-energy limit and a stated rotor-exposure condition."),
("UCA-A03-D","CA3","D","Sustained flight over an assembly continues after the condition that justified "
   "the exposure has ended.", ["H1","H7"],
   "SCA-03-2: Sustained exposure of an assembly must be bounded by the condition that justified it."),
# CA1 임무 인가 (C1 → C2)
("UCA-A01-P","CA1","P","The flight is authorized for a purpose the platform's sensing cannot actually "
   "serve, so the operator improvises sensing outside the stated purpose.", ["H4","H7"],
   "SCA-01-1: The authorized purpose must be matched to a stated sensing capability; a purpose the "
   "payload cannot serve must not be authorized."),
("UCA-A01-N","CA1","N","No re-authorization is sought when the purpose changes in flight.", ["H4","H7"],
   "SCA-01-2: A change of purpose in flight must require re-authorization before the new sensing begins."),
# CA2 공역 접근 부여·조건·철회 (C4 → C2)
("UCA-A02-P","CA2","P","Airspace access is granted on conditions the operator's equipment cannot "
   "verify it is meeting (position accuracy, remote identification).", ["H6","H3"],
   "SCA-02-1: Any airspace condition imposed must be observable by the equipment carried, and the "
   "equipment's ability to meet it must be demonstrated before access is granted."),
("UCA-A02-N","CA2","N","Access is not withdrawn when the conditions it rested on cease to hold.", ["H6","H7"],
   "SCA-02-2: Withdrawal criteria for airspace access must be stated and monitored."),
# CA4 인물·주거·차량 촬영 (C2 → P2)
("UCA-A04-P","CA4","P","Imaging of a dwelling or an identifiable person is commanded without the "
   "purpose limitation and retention rule that the authorization assumed.", ["H4"],
   "SCA-04-1: Imaging that can identify a person or the interior of a dwelling must be bound to a stated "
   "purpose, retention period and access rule at the moment it is commanded."),
("UCA-A04-D","CA4","D","Recording continues after the subject of the authorization has left the frame.", ["H4"],
   "SCA-04-2: Recording must stop when the authorized subject is no longer the object of observation."),
# CA5 복귀·착륙·비행종료 (C2 → P1)
("UCA-A05-N","CA5","N","Termination is not commanded when the energy state no longer permits a safe "
   "recovery over the population beneath.", ["H1","H6"],
   "SCA-05-1: A recovery margin referenced to the population beneath must be defined and enforced."),
("UCA-A05-T","CA5","T","Termination is commanded over the densest point of the ground population.", ["H1"],
   "SCA-05-2: Termination behaviour must account for the ground risk distribution, not only the aircraft."),
# CA6 지오펜스·링크상실 거동 (C3 → P1)
("UCA-A06-P","CA6","P","Lost-link behaviour executes a return path over an area the authorization "
   "excluded.", ["H4","H6"],
   "SCA-06-1: Automatic behaviours must be constrained by the same spatial limits as commanded flight, "
   "and that constraint must be verifiable before flight."),
("UCA-A06-N","CA6","N","Geofence does not engage because its data were never validated against the "
   "authorized area.", ["H6","H7"],
   "SCA-06-2: Geofence data must be validated against the authorization before flight."),
# CA7 영상·파생기록 이관 (C2 → C5)
("UCA-A07-T","CA7","T","Imagery is transferred to custody after copies have already propagated to other "
   "systems.", ["H4"],
   "SCA-07-1: Custody of imagery must attach before any derived copy leaves the capture system."),
("UCA-A07-N","CA7","N","Derived products (tracks, identifications) are not placed under the same custody "
   "as the imagery they came from.", ["H4"],
   "SCA-07-2: Derived products must inherit the custody and retention rule of their source."),
]
if __name__=='__main__':
    from collections import Counter
    print(f"M-A UCA {len(UCA)}건 · 안전제약 {len({u[5].split(':')[0] for u in UCA})}건")
    print("유형:",dict(Counter(u[2] for u in UCA)),"· 제어행위별:",dict(Counter(u[1] for u in UCA)))
    for u in UCA: print(f"  {u[5].split(':')[0]:10s} {u[5].split(':',1)[1].strip()[:104]}")

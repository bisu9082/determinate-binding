# -*- coding: utf-8 -*-
"""어휘집 v2 — 교정 이력: lex_v0(최초) → lex(v1, NLF 시장출시 보정) → lex2(v2, 아래 5건).
D-6 확정연산자 일반형 / D-7 인가어휘 보강 / AUTH 과포괄 축소 / 벌칙 본문어휘 / EVAL 정밀화."""

# ① 지명된 기술적 평가 (Nasirov 2026 converter 어휘군 + 코퍼스 표제어)
EVAL = [r"certificat\w*", r"\bcertif\w*", r"conformity assessment", r"conformity",
        r"\btest(?:s|ed|ing)?\b", r"inspection", r"\baudit\w*", r"impact assessment",
        r"verificat\w*", r"accredit\w*", r"type[- ]approval", r"airworthiness",
        r"notified bod(?:y|ies)", r"declaration of conformity", r"assessment",
        r"declaration of compliance", r"demonstrat\w+ (?:compliance|that)",
        r"인증", r"검사", r"시험", r"적합성평가", r"성능평가", r"형식승인",
        r"適合性?(?:評価|検査)", r"検査", r"型式(?:認定|承認)", r"認定",
        # 변경 ⑨ 대칭화: 한국어 쪽이 이미 담고 있던 개념의 일본어 対応語
        r"試験",            # ← 시험
        r"認証",            # ← 인증
        r"性能評価"]        # ← 성능평가
# ⚠ 제외 확정: 교육/훈련/협의 — 평가가 아니라 절차. 심사도 제외(인사·행정심사 혼입).

# ② 지명된 인가 결과 — 활동어(운행·통행)가 아니라 인가 처분어만
AUTH = [r"authoris(?:ation|ed)|authoriz(?:ation|ed)", r"\bpermit(?:ted)?\b",
        r"licen[cs]\w*", r"registrat\w*|registered", r"approval|approved",
        r"placed? on the market", r"made available on the market",
        r"\beligible for\b", r"may (?:be )?operate", r"shall be issued",
        r"procure\w*|acquisition", r"exempt\w*", r"certificate (?:is|shall be) required",
        r"(?:허가|승인|인증|등록|면허|신고)\s*(?:를|을)?\s*(?:받|취득|필요)",
        r"(?:허가|승인|인증|등록|면허)(?:증|서)?(?=[을를이가은는에의로와과도만,.)\]\s]|$)",
        r"(?:許可|認可|登録|免許)\s*(?:を)?\s*(?:受け|取得)", r"(?:許可|認可|登録|免許)証?"]

# ③-A 확정 연산자
DET = [r"shall not\b[^.]{0,120}\bunless", r"may not\b[^.]{0,120}\b(unless|without)",
       r"\bno\s+\w[\w\s\-]{0,40}?\bmay\b[^.]{0,140}\b(unless|without)",   # D-6 일반형
       r"no person may", r"shall not be (placed|made available|issued|granted)",
       r"only if\b", r"only where\b", r"only upon\b", r"only when\b",
       r"shall only be\b[^.]{0,140}\bif\b",
       r"(?:shall|may) only\b[^.]{0,140}\b(if|when|where|unless)\b",
       r"only be (placed|made available|issued|granted|used|operated)\b[^.]{0,140}\bif\b",
       r"shall be (revoked|withdrawn|refused|denied|suspended)",
       r"shall cease to (be valid|apply)", r"\bis required to\b", r"shall be required",
       r"prohibited unless", r"conditional upon",
       r"shall be subject to\b[^.]{0,80}\b(certificat|conformity|test|approval)",
       r"shall be issued\b[^.]{0,120}\bwhen\b",
       # D-8 일반형: 의무동사의 목적어가 인가 산출물인 경우
       r"\bmust\b[^.]{0,200}\b(eligible|declaration of compliance|certificat\w*|licen[cs]\w*|approval|authoris\w*|authoriz\w*|type[- ]approval)",
       r"shall\b[^.]{0,200}\b(hold|obtain|be in possession of)\b[^.]{0,80}\b(certificat\w*|licen[cs]\w*|approval|authoris\w*)",
       r"(?:인증|검사|시험|형식승인)\s*을?\s*받은[^.]{0,60}(?:사용|운행|판매|설치)하여야",
       r"받은 것을 말한다", r"받지 아니하고는", r"취소하여야 한다", r"받은 경우에만", r"받은 자만",
       r"(?:인증|검사|시험|허가|승인|등록)\s*(?:을|를)\s*받아야 한다",
       r"아니면[^.]{0,60}아니 된다", r"하여서는 아니 된다",
       # D-10 (2026-09-20): 시험·검사 합격을 인가의 조건으로 거는 한국어 구문.
       #   미보강 시 KR도로교통법 제85조제1항(면허=시험 합격 조건)을 놓쳤다.
       r"합격하여야 한다", r"합격한 (?:사람|자)", r"합격하지 (?:못|아니)한",
       r"받은 (?:사람|자)(?:만|가 아니면)", r"받지 아니하면[^.]{0,60}없다",
       r"거쳐야 한다",
       r"でなければ[^。]{0,60}してはならない", r"受けなければならない",
       # D-11 (2026-09-20): 일본어 한정·합격 조건 구문. 미보강 시 道交法 第90条第1項
       #   (시험 합격자에게 면허를 부여하여야 한다)을 놓쳤다.
       r"合格した者", r"場合に限る", r"に限り", r"受けている者に限",
       r"なければ[^。]{0,60}できない",
       # 변경 ⑨ 대칭화: 한국어 쪽이 이미 담고 있던 확정 구문의 일본어 対応語
       r"取り消さなければならない",      # ← 취소하여야 한다
       r"合格しなければならない",        # ← 합격하여야 한다
       r"経なければならない"]            # ← 거쳐야 한다

# ③-B 비확정 연산자
# 변경 ③ (부록 A): 맨모달 may 의 부정 선읽기가 only if / only when / only where 를
#   헤지로 취급해, 영어가 제공하는 가장 강한 조건 구문을 통째로 눌렀다.
#   "a person may operate ... only if" 의 only if 는 허가에 걸린 헤지가 아니라
#   허가를 조건 짓는 확정연산자다. 선읽기에 이 셋을 넣어 취소를 막는다.
#   unless 와 without 은 그대로 둔다.
NONDET = [r"\bshould\b", r"\bmay\b(?![^.]{0,120}\b(unless|without|only if|only when|only where)\b)", r"due regard",
          r"as appropriate", r"to the extent (practicable|possible)",
          r"shall (consider|take into account)", r"encourag\w*", r"best practice",
          r"where (appropriate|necessary)", r"may require",
          r"할 수 있다", r"고려하여야", r"노력하여야",
          r"努めなければならない", r"することができる",
          # 변경 ⑨ 대칭화: 헤지 어휘집도 같이 대칭화한다. 그래서 이 수선은
          #   반환을 더하기만 하지 않고 빼기도 한다.
          # ← 고려하여야 / shall consider · take into account.
          #   다른 두 언어가 어간 수준으로 담은 개념이므로 일본어도 어간으로 담는다.
          #   좁은 형태(考慮しなければならない)로 두면 道交法 제102조제4항의
          #   「その他の事情を考慮するものとする」를 놓친다. 그 조항은 같은 문장에서
          #   「命ずることができる」로 재량을 쓰므로 인가가 확정적으로 조건 지어지지
          #   않는다. 대칭화가 반환을 빼는 쪽으로 작동하는 한 건이다.
          r"考慮"]

# ④ 벌칙·제재 조항 — 경로 출발점에서 제외 (본문 어휘 기준, 캡션 비의존)
PENALTY = [r"罰金|科料|懲役|拘留|過料",
           r"징역|벌금|구류|과료|과태료를 부과",
           r"shall be (fined|punished)|criminal penalt|administrative fine",
           # 변경 ④ (부록 A): 벌칙 조항은 경로 출발이 금지되는데 패턴 목록에
           #   한국어·일본어 형태만 있었다. 그래서 거짓·은폐 진술에 민사벌을
           #   매기는 14 CFR Part 89 세 항이 인가 분모에 들어왔다. 미국 형태를
           #   넣는다. 제외는 여전히 불완전하다 — §2.8 분모 감사가 패턴이 잡지
           #   못하는 한국어·일본어 벌칙 조항 세 건을 더 뽑았고, 사후 수선하지
           #   않고 그대로 보고한다.
           r"civil penalt(?:y|ies)",
           r"subject to a civil penalty",
           r"(?:false|fraudulent|incorrect) (?:statement|entry|record|report)"
           r"[^.]{0,200}(?:civil penalt|punishab|fine)",
           r"(?:fraudulent|intentionally false)[^.]{0,120}(?:statement|entry|reproduction)",
           # §89.5 는 (a) 허위 기재 · (b) 부작위에 의한 은폐 · (c) 그것이 제재의
           #   근거가 된다는 조항 세 항으로 돼 있다. (b) 는 'penalty' 라는 말을
           #   쓰지 않으므로 은폐 형태를 따로 적는다.
           r"knowingly conceal or cause to be concealed",
           r"by omission[^.]{0,60}conceal"]

# ④-2 D-9 배제형: '첨부/제출 요건'은 평가 결과를 인가에 거는 것이 아니다.
#     DET에 걸렸더라도 이 패턴이 같은 단위에 있으면 확정으로 보지 않는다.
DET_EXCLUDE = [r"must be (included|accompanied|submitted|attached|provided) with",
               r"shall be (included|accompanied|submitted|attached) with",
               r"must accompany", r"shall accompany"]

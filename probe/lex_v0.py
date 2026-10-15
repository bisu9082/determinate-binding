# -*- coding: utf-8 -*-
"""사전등록용 어휘집 v0 — 결과를 보기 전에 고정한다."""
# ① 지명된 기술적 평가 (Nasirov 2026 converter 어휘군 + 코퍼스 표제어)
EVAL = [r"certificat\w*", r"certif\w*", r"conformity assessment", r"conformity",
        r"\btest\w*", r"inspection", r"\baudit\w*", r"impact assessment",
        r"evaluat\w*", r"verificat\w*", r"accredit\w*", r"type[- ]approval",
        r"airworthiness", r"notified body|notified bodies", r"declaration of conformity",
        r"인증", r"시험", r"검사", r"심사", r"適合", r"検査", r"認定", r"型式"]
# ② 지명된 인가 결과
AUTH = [r"authoris\w*|authoriz\w*", r"\bpermit\w*", r"licen[cs]\w*", r"registrat\w*",
        r"approval|approved", r"placed? on the market", r"made available on the market",
        r"may operate|shall operate|operation of", r"procure\w*|acquisition",
        r"deploy\w*", r"exempt\w*",
        r"운행", r"통행", r"허가", r"승인", r"등록", r"판매", r"通行", r"運行", r"許可"]
# ③-A 확정적 연산자
DET = [r"shall not\b[^.]{0,120}\bunless", r"may not\b[^.]{0,120}\b(unless|without)",
       r"no person may", r"shall not be (placed|made available|issued|granted)",
       r"only if\b", r"only where\b", r"only upon\b", r"only when\b",
       r"shall be (revoked|withdrawn|refused|denied|suspended)",
       r"shall cease to (be valid|apply)", r"is required to", r"shall be required",
       r"prohibited unless", r"subject to\b[^.]{0,60}\bcertificat",
       r"받은 것을 말한다", r"받지 아니하고는", r"취소하여야 한다", r"받아야 한다",
       r"하여서는 아니 된다", r"가입하여야 한다",
       r"でなければ[^。]{0,60}してはならない", r"受けなければならない"]
# ③-B 비확정적 연산자
NONDET = [r"\bshould\b", r"\bmay\b(?![^.]{0,120}\b(unless|without)\b)", r"due regard",
          r"as appropriate", r"to the extent (practicable|possible)",
          r"shall (consider|take into account)", r"encourag\w*", r"best practice",
          r"where (appropriate|necessary)", r"may require",
          r"할 수 있다", r"고려하여야", r"노력하여야",
          r"努めなければならない", r"することができる"]

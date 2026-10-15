# -*- coding: utf-8 -*-
"""M-G 기능어 등록부 v2 — 패싯 연언 구조. 명세: stpa/facetspec.md (F-1~F-4).
각 제약 = {패싯명: [동의어 정규식, ...]} · 패싯 내부 OR · 패싯 사이 AND.
패싯 내부 동의어는 영/한/일 이형을 넓게 싣는다(F-3). 좁힘은 연언으로만 한다."""

# ---- 재사용 패싯 (동의어를 한 곳에서 관리) ----
INSTRUMENT = [r'instrument\b', r'detector', r'\bsensor', r'measur\w+ (?:device|equipment|instrument|system)',
              r'monitoring equipment', r'measuring (?:instrument|equipment|device)',
              r'계측(?:기|기기|장비|장치)', r'측정\s*(?:기기|장비|장치|기)', r'센서', r'감지기', r'검지기',
              r'測定(?:器|機器|装置)', r'検知器', r'センサ']
SAMPLE     = [r'\bsample', r'specimen', r'\bswab', r'evidence item',
              r'시료', r'검체', r'채취물', r'試料', r'検体']
MEASUREMENT= [r'measurement', r'\breading\b', r'analytical result', r'test result',
              r'측정\s*(?:값|결과)', r'판독\s*값', r'분석\s*결과', r'計測', r'測定(?:値|結果)']
EVALUATION = [r'certificat\w*', r'conformity assessment', r'type[- ]approval', r'verification',
              r'\btest(?:s|ed|ing)?\b', r'inspection', r'accredit\w*', r'\baudit\w*',
              r'demonstrat\w+ (?:compliance|performance|conformity)', r'performance (?:standard|requirement)',
              r'인증', r'검정', r'검사', r'시험', r'적합성\s*평가', r'성능\s*(?:기준|시험)', r'형식승인',
              r'型式(?:認定|承認|検定)', r'適合性?(?:評価|検査)', r'検定']
PLATFORM   = [r'robot', r'unmanned', r'\bUA\b', r'aircraft', r'vehicle', r'machine',
              r'로봇', r'무인', r'자동차', r'차량', r'ロボット', r'無人', r'自動車']
OPERATOR   = [r'operator', r'remote pilot', r'\bpilot\b', r'person in charge',
              r'조작자', r'운전자', r'운용자', r'操縦者', r'運転者']
LINK       = [r'command and control link', r'\bC2 link\b', r'lost link', r'loss of .{0,30}link',
              r'communication', r'통신', r'무선', r'通信']
RECORD     = [r'\brecord\b', r'\blog\b', r'logs? of', r'logging', r'documentation',
              r'기록', r'대장', r'記録', r'台帳']
AUTHZ      = [r'authoris\w*|authoriz\w*', r'\bpermit', r'licen[cs]\w*', r'approval', r'registrat\w*',
              r'허가', r'승인', r'인가', r'면허', r'등록', r'許可', r'認可', r'免許', r'登録']

FACETS = {
# ── CA6 측정 (계측기·측정값) ─────────────────────────────────────────
'SC-06-1': {'subject': INSTRUMENT,
            'predicate': [r'calibrat\w*', r'교정', r'較正', r'校正',
                          r'operating (?:envelope|range|condition)', r'사용\s*조건', r'測定範囲']},
'SC-06-2': {'subject': MEASUREMENT,
            'predicate': [r'uncertaint\w*', r'불확도', r'不確かさ',
                          r'repeat\w* (?:test|measur)', r'confirmatory', r'재검사', r'再検査']},
'SC-06-3': {'subject': MEASUREMENT,
            'predicate': [r'time window', r'within .{0,20}(?:minutes|hours) of (?:the )?(?:sampling|collection)',
                          r'시간\s*범위', r'이내에\s*측정', r'測定.{0,10}時間']},
# ── CA4 시료채취 ─────────────────────────────────────────────────────
'SC-04-1': {'subject': [r'sampl\w+ (?:media|equipment|tool|container|device)', r'collection (?:device|container)',
                        r'채취(?:기구|용기|장비)', r'採取(?:器具|容器)'] + SAMPLE,
            'predicate': [r'qualif\w+ for', r'suitab\w+ for', r'fit for', r'적격', r'적합', r'適合']},
'SC-04-2': {'subject': PLATFORM,
            'predicate': [r'contaminat\w*', r'오염', r'汚染'],
            'qualifier': [r'\blimit', r'threshold', r'한도', r'한계', r'限度', r'基準値']},
# ── CA8 분석결과 제출 ────────────────────────────────────────────────
'SC-08-1': {'subject': MEASUREMENT,
            'predicate': [r'uncertaint\w*', r'불확도', r'不確かさ',
                          r'criteri\w+ applied', r'적용\s*기준', r'適用.{0,6}基準']},
'SC-08-2': {'subject': [r'criteri\w+', r'threshold', r'기준', r'임계', r'基準', r'閾値'],
            'predicate': [r'validat\w+ (?:scope|range|for)', r'provenance', r'\bsource of\b',
                          r'적용\s*범위', r'출처', r'適用範囲', r'出典']},
'SC-08-3': {'subject': MEASUREMENT,
            'predicate': [r'without (?:undue )?delay', r'latency', r'지체\s*없이', r'遅滞なく',
                          r'time.{0,15}(?:budget|limit)', r'소요\s*시간']},
# ── CA9 판정 ─────────────────────────────────────────────────────────
'SC-09-1': {'subject': INSTRUMENT + MEASUREMENT,
            'predicate': EVALUATION,
            'qualifier': [r'performance', r'accura\w*', r'sensitiv\w*', r'detection limit',
                          r'성능', r'정확도', r'검출\s*한계', r'性能', r'精度', r'検出限界']},
'SC-09-2': {'subject': [r'determination', r'decision', r'판정', r'결정', r'判定', r'決定'],
            'predicate': [r'within \d+', r'이내에', r'以内に', r'no later than', r'까지']},
'SC-09-3': {'subject': MEASUREMENT,
            'predicate': [r'confirmat\w*', r'확인\s*(?:검사|시험)', r'確認(?:検査|試験)', r'再検査']},
'SC-09-4': {'subject': [r'certificat\w*', r'authoris\w*|authoriz\w*', r'approval', r'인증', r'승인', r'認定', r'認可'],
            'predicate': [r'change of (?:circumstance|condition)', r'변경(?:된|되는) 경우', r'변경인증',
                          r'재승인', r'変更.{0,6}(?:認定|許可)']},
# ── CA2 철수 ─────────────────────────────────────────────────────────
'SC-02-1': {'subject': [r'withdraw\w*', r'abort', r'철수', r'중지\s*명령', r'撤収', r'中止'],
            'predicate': [r'condition\w* (?:that|which) trigger', r'criteri\w+ for',
                          r'observ\w+ (?:from|by)', r'기준', r'요건', r'基準']},
# F-4 적용(2026-09-20 감사): 'dispos\w+ of'가 "keep at the disposal of"(제공 의무)를 잡고,
# RECORD를 subject에 OR로 넣으면 AI Act 문서보관 조항이 들어온다. 둘 다 제거한다.
'SC-02-2': {'subject': SAMPLE,
            'predicate': [r'disposition of', r'dispose[ds]? of', r'hand(?:ed|ing)? over',
                          r'인계', r'인수', r'引渡']},
'SC-02-3': {'subject': [r'dose limit', r'선량한도', r'누적선량', r'線量限度',
                        r'threshold', r'임계', r'한도', r'閾値', r'限度'],
            'predicate': [r'project\w+ (?:time|value)', r'anticipat\w+', r'predicted',
                          r'예상', r'도달\s*시간', r'予測']},
# ── CA3 진입·체류 ────────────────────────────────────────────────────
'SC-03-1': {'subject': PLATFORM,
            'predicate': [r'decontaminat\w*', r'제염', r'除染'],
            'qualifier': [r'resistan\w*', r'tolerance', r'내성', r'내구', r'耐性']},
'SC-03-2': {'subject': PLATFORM,
            'predicate': [r'dwell', r'체류', r'잔류\s*시간', r'滞留'],
            'qualifier': [r'tolerance', r'\blimit', r'허용', r'한도', r'許容', r'限度']},
'SC-03-3': {'subject': [r'egress', r'exit route', r'이탈\s*경로', r'반출', r'退出'],
            'predicate': [r'decontaminat\w*', r'제염', r'除染']},
# ── CA5 정지 ─────────────────────────────────────────────────────────
'SC-05-1': {'subject': [r'emergency stop', r'비상\s*정지', r'긴급\s*정지', r'非常停止'],
            'predicate': LINK},
'SC-05-2': {'subject': SAMPLE + [r'manipulator', r'조작기', r'매니퓰레이터', r'マニピュレータ'],
            'predicate': [r'emergency stop', r'비상\s*정지', r'stop (?:command|function)', r'停止']},
'SC-05-3': {'subject': [r'resum\w*', r'restart', r'재개', r'재기동', r'再開'],
            'predicate': [r'explicit (?:human )?(?:instruction|command)', r'명시적\s*지시',
                          r'human (?:intervention|operator)', r'人の(?:指示|操作)']},
# ── CA7 열화모드 ─────────────────────────────────────────────────────
'SC-07-1': {'subject': [r'safe state', r'fail-?safe', r'안전\s*상태', r'安全(?:状態|側)'],
            'predicate': [r'recover\w*', r'retriev\w*', r'회수', r'복구', r'回収', r'復旧']},
'SC-07-2': {'subject': INSTRUMENT,
            'predicate': [r'validat\w*', r'verif\w*', r'검증', r'유효성', r'検証', r'妥当性']},
'SC-07-3': {'subject': LINK,
            'predicate': [r'dropout', r'duration', r'두절\s*시간', r'지속\s*시간', r'継続時間', r'時間']},
# ── CA1 채취명령 ─────────────────────────────────────────────────────
'SC-01-1': {'subject': SAMPLE,
            'predicate': [r'standard operating procedure', r'\bSOP\b', r'표준\s*(?:작업|운영)\s*절차',
                          r'작업\s*절차서', r'標準(?:作業|運用)手順']},
'SC-01-2': {'subject': SAMPLE,
            'predicate': [r'record the reason', r'사유를 기록', r'이유를 기재', r'理由を記録']},
# ── CA10 보관이관 ────────────────────────────────────────────────────
'SC-10-1': {'subject': SAMPLE,
            'predicate': [r'chain of custody', r'보관\s*연속성', r'인계', r'인수', r'保管の連続性', r'引継']},
'SC-10-2': {'subject': SAMPLE,
            'predicate': RECORD,
            'qualifier': [r'custody', r'holder', r'보관', r'소지', r'保管', r'所持']},
# ── CA11 제염 ────────────────────────────────────────────────────────
'SC-11-1': {'subject': SAMPLE,
            'predicate': [r'decontaminat\w*', r'제염', r'除染']},
'SC-11-2': {'subject': PLATFORM,
            'predicate': [r'release criterion', r'clearance', r'해제\s*기준', r'반출\s*기준', r'解除基準']},
}

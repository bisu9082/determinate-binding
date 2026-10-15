# -*- coding: utf-8 -*-
"""M-A 기능어 등록부 v2 — 패싯 연언 구조. 명세: stpa/facetspec.md."""
from facets_mg import EVALUATION, RECORD, AUTHZ, OPERATOR, LINK

AIRCRAFT = [r'unmanned aircraft', r'\bUAS?\b', r'aircraft', r'drone', r'무인\s*항공', r'항공기', r'無人航空']
IMAGERY  = [r'imagery', r'image\b', r'video', r'recording', r'footage', r'personal data', r'biometric',
            r'영상', r'화상', r'개인정보', r'생체정보', r'映像', r'個人データ']
PERSONS  = [r'people', r'persons?', r'human being', r'assembl\w+', r'crowd', r'bystander',
            r'injury to a human', r'on the ground',
            r'사람', r'보행자', r'군중', r'인체', r'人(?:体|身)', r'歩行者', r'群衆']
AIRSPACE = [r'airspace', r'공역', r'空域', r'flight (?:area|zone)', r'operating (?:area|volume)']

FACETS = {
'SCA-03-1': {'subject': AIRCRAFT,
             'predicate': [r'kinetic energy', r'impact energy', r'ft-?lb', r'joule',
                           r'exposed rotating parts', r'rotor', r'운동\s*에너지', r'운동에너지'],
             'qualifier': PERSONS + [r'over (?:human beings|people)']},
'SCA-03-2': {'subject': PERSONS,
             'predicate': [r'sustained flight', r'sustained .{0,20}(?:over|above)',
                           r'open-air assembl', r'지속\s*비행']},
'SCA-01-1': {'subject': [r'payload', r'sensor', r'camera', r'탑재체', r'센서', r'카메라', r'搭載'],
             'predicate': [r'purpose of the (?:flight|operation)', r'stated purpose', r'intended purpose',
                           r'운용\s*목적', r'사용\s*목적', r'利用目的']},
'SCA-01-2': {'subject': [r'purpose', r'목적', r'目的'],
             'predicate': [r'change of (?:purpose|circumstance)', r're-?authoris', r're-?authoriz',
                           r'변경(?:된|되는) 경우', r'재승인', r'변경인증', r'変更.{0,6}(?:認定|許可)']},
'SCA-02-1': {'subject': AIRSPACE + AIRCRAFT,
             'predicate': [r'remote identification', r'position accuracy', r'accuracy of the position',
                           r'원격\s*식별', r'위치\s*정확도'],
             'qualifier': EVALUATION + [r'demonstrat\w+', r'capab\w+ of']},
'SCA-02-2': {'subject': AIRSPACE,
             'predicate': [r'withdraw\w*', r'revok\w*', r'suspend\w*', r'철회', r'취소', r'정지', r'取消']},
'SCA-04-1': {'subject': IMAGERY,
             'predicate': [r'purpose limitation', r'specified.{0,20}purposes', r'retention period',
                           r'storage period', r'보유\s*기간', r'목적\s*외', r'保存期間'],
             'qualifier': [r'access', r'disclos\w*', r'접근', r'열람', r'제공', r'アクセス']},
'SCA-04-2': {'subject': IMAGERY,
             'predicate': [r'cease (?:to )?(?:record|process)', r'no longer necessary',
                           r'중단', r'필요\s*없게', r'中止', r'不要となった']},
'SCA-05-1': {'subject': AIRCRAFT,
             'predicate': [r'sufficient (?:power|energy)', r'endurance', r'safe (?:landing|recovery)',
                           r'잔여\s*(?:전력|연료)', r'안전\s*착륙', r'安全.{0,4}着陸'],
             'qualifier': PERSONS + [r'ground risk', r'population', r'지상\s*위험', r'인구']},
'SCA-05-2': {'subject': [r'terminat\w+', r'flight termination', r'비행\s*종료', r'강제\s*착륙', r'飛行終了'],
             'predicate': [r'ground risk', r'population density', r'people on the ground',
                           r'지상\s*위험', r'인구\s*밀도', r'地上.{0,6}リスク']},
'SCA-06-1': {'subject': [r'geo-?awareness', r'geo-?fenc', r'지오\s*펜', r'공간\s*제한', r'ジオフェン'],
             'predicate': [r'lost link', r'loss of (?:the )?(?:command and control|C2) link',
                           r'automatic', r'autonomous', r'통신\s*두절', r'자동', r'自動']},
'SCA-06-2': {'subject': [r'geo-?awareness', r'geo-?fenc', r'지오\s*펜', r'공간\s*제한', r'ジオフェン'],
             'predicate': [r'update.{0,30}(?:data|information).{0,30}before (?:the )?flight',
                           r'before (?:the )?flight', r'비행\s*전', r'飛行前'] + EVALUATION},
'SCA-07-1': {'subject': IMAGERY,
             'predicate': [r'chain of custody', r'보관\s*연속성', r'保管の連続性'] + RECORD},
'SCA-07-2': {'subject': [r'further processing', r'derived', r'2차\s*가공', r'파생', r'二次利用'],
             'predicate': [r'same purpose', r'purpose limitation', r'retention',
                           r'동일\s*목적', r'목적\s*범위', r'同一の目的']},
}

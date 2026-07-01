import requests

BASE = 'http://localhost:5000'
SUBJECT = '275'
EXAM_TYPE = 'Annual'
YEAR = '2025-2026'

# Combined rolls 201-448
MARKS = {
    # Batch 1 (201-409)
    201: (26, 14, 20, False),
    202: (22, 13, 15, False),
    203: (25, 10, 15, False),
    204: (33, 11, 20, False),
    205: (31, 14, 20, False),
    206: (24, 14, 20, False),
    207: (22, 8, 15, False),
    208: (24, 9, 17, False),
    209: (20, 10, 15, False),
    210: (22, 13, 15, False),
    211: (38, 14, 20, False),
    212: (23, 12, 15, False),
    213: (24, 14, 20, False),
    214: (23, 11, 16, False),
    215: (24, 14, 20, False),
    216: ('', '', '', True),
    217: ('', '', '', True),
    218: (21, 16, 15, False),
    219: ('', '', '', True),
    220: (21, 12, 15, False),
    221: (23, 13, 15, False),
    222: (29, 15, 20, False),
    223: (27, 14, 20, False),
    224: (30, 14, 20, False),
    225: (29, 14, 20, False),
    226: (24, 12, 15, False),
    227: (20, 11, 15, False),
    228: ('', '', '', True),
    229: (27, 9, 15, False),
    230: (19, 12, 15, False),
    231: (17, 13, 15, False),
    232: (24, 12, 15, False),
    233: (25, 12, 15, False),
    234: (21, 9, 15, False),
    235: (24, 8, 15, False),
    236: (26, 10, 15, False),
    237: (20, 14, 16, False),
    238: (17, 12, 15, False),
    239: (25, 9, 16, False),
    240: (26, 10, 15, False),
    241: (31, 12, 20, False),
    242: (19, 13, 15, False),
    243: (27, 11, 20, False),
    244: (17, 10, 15, False),
    245: (10, 4, 10, False),
    246: (10, 6, 10, False),
    247: (17, 9, 15, False),
    248: (9, 9, 10, False),
    249: (15, 6, 10, False),
    250: (12, 8, 10, False),
    251: (20, 10, 15, False),
    252: (17, 9, 15, False),
    253: (20, 12, 15, False),
    254: (22, 9, 15, False),
    255: (19, 9, 15, False),
    256: (18, 9, 15, False),
    257: (17, 8, 15, False),
    258: (12, 5, 20, False),
    259: (9, 8, 10, False),
    260: (22, 8, 15, False),
    261: (17, 9, 15, False),
    262: (22, 13, 15, False),
    263: (11, 11, 10, False),
    264: (23, 11, 16, False),
    265: (18, 9, 15, False),
    266: (25, 10, 15, False),
    267: (12, 8, 10, False),
    268: (18, 8, 15, False),
    269: (21, 9, 15, False),
    270: (9, 9, 10, False),
    271: (23, 11, 16, False),
    272: (20, 12, 15, False),
    273: (20, 8, 15, False),
    274: (17, 10, 15, False),
    275: (25, 11, 15, False),
    276: (18, 8, 15, False),
    277: (17, 5, 10, False),
    278: ('', '', '', True),
    279: (13, 8, 10, False),
    280: ('', '', '', True),
    281: (22, 8, 15, False),
    282: (29, 11, 20, False),
    283: (17, 10, 15, False),
    284: (5, 8, 10, False),
    285: (19, 14, 15, False),
    286: (22, 8, 15, False),
    287: (17, 8, 15, False),
    288: (9, 11, 10, False),
    289: (25, 8, 15, False),
    290: (26, 8, 16, False),
    291: (31, 13, 20, False),
    292: (25, 11, 15, False),
    293: (21, 16, 15, False),
    294: (17, 11, 15, False),
    295: (19, 9, 15, False),
    296: (17, 8, 15, False),
    297: (29, 10, 21, False),
    298: (43, 13, 25, False),
    299: (29, 11, 20, False),
    300: (17, 8, 15, False),
    301: (23, 8, 15, False),
    302: (4, 4, 10, False),
    303: (31, 19, 20, False),
    304: (9, 8, 10, False),
    305: (17, 9, 15, False),
    306: (24, 3, 10, False),
    307: (18, 8, 15, False),
    308: (17, 9, 15, False),
    309: (29, 9, 15, False),
    310: (17, 9, 15, False),
    311: (18, 12, 15, False),
    312: (19, 12, 15, False),
    313: (18, 10, 15, False),
    314: (13, 11, 10, False),
    315: (20, 12, 15, False),
    316: (22, 8, 15, False),
    317: (23, 5, 10, False),
    318: (27, 11, 15, False),
    319: (17, 11, 15, False),
    320: (19, 8, 15, False),
    321: (17, 11, 15, False),
    322: ('', '', '', True),
    323: (17, 8, 15, False),
    324: (11, 10, 10, False),
    325: (17, 11, 15, False),
    326: (18, 8, 15, False),
    327: (9, 9, 10, False),
    328: (20, 8, 15, False),
    329: (22, 8, 15, False),
    330: (25, 9, 16, False),
    331: (22, 10, 15, False),
    332: (7, 5, 10, False),
    333: ('', '', '', True),
    334: (5, 8, 10, False),
    335: (7, 9, 10, False),
    336: (19, 4, 10, False),
    337: (24, 9, 15, False),
    338: (27, 8, 15, False),
    339: (13, 9, 10, False),
    340: ('', '', '', True),
    341: (10, 8, 10, False),
    342: (17, 9, 15, False),
    343: (13, 8, 10, False),
    344: (29, 4, 10, False),
    345: (20, 5, 10, False),
    346: ('', '', '', True),
    347: (4, 6, 10, False),
    348: (17, 8, 15, False),
    349: (18, 12, 15, False),
    350: (22, 15, 15, False),
    351: (17, 10, 15, False),
    352: (27, 9, 15, False),
    353: (13, 8, 10, False),
    354: (17, 5, 10, False),
    355: ('', '', '', True),
    356: (28, 11, 21, False),
    357: (23, 9, 15, False),
    358: (19, 9, 15, False),
    359: (19, 12, 15, False),
    360: (17, 8, 15, False),
    361: (23, 12, 15, False),
    362: (19, 8, 15, False),
    363: ('', '', '', True),
    364: (17, 14, 15, False),
    365: (17, 6, 10, False),
    366: (20, 6, 10, False),
    367: (10, 6, 10, False),
    368: (32, 8, 20, False),
    369: (27, 9, 15, False),
    370: (22, 9, 15, False),
    371: (20, 10, 15, False),
    372: (24, 8, 15, False),
    373: (24, 8, 15, False),
    374: (20, 12, 15, False),
    375: (31, 12, 20, False),
    376: (29, 10, 21, False),
    377: (31, 9, 20, False),
    378: (27, 11, 20, False),
    379: ('', '', '', True),
    380: (17, 9, 15, False),
    381: (21, 8, 15, False),
    382: (22, 10, 15, False),
    383: (23, 6, 10, False),
    384: (24, 9, 15, False),
    385: (22, 10, 15, False),
    386: (19, 6, 10, False),
    387: (22, 6, 10, False),
    388: (17, 9, 15, False),
    389: (10, 6, 10, False),
    390: (5, 8, 10, False),
    391: (20, 8, 15, False),
    392: (10, 8, 10, False),
    393: (29, 8, 15, False),
    394: ('', '', '', True),
    395: (42, 11, 20, False),
    396: (25, 8, 15, False),
    397: (19, 8, 15, False),
    398: (19, 9, 15, False),
    399: (21, 9, 15, False),
    400: (28, 11, 21, False),
    401: (15, 6, 10, False),
    402: (18, 6, 10, False),
    403: (17, 8, 15, False),
    404: (17, 9, 15, False),
    405: (5, 6, 10, False),
    406: (2, 8, 10, False),
    407: (28, 13, 20, False),
    408: (22, 9, 15, False),
    409: (9, 11, 10, False),

    # Batch 2 (410-450)
    410: (33, 9, 20, False),
    411: ('', '', '', True),
    412: (21, 8, 15, False),
    413: (23, 8, 15, False),
    414: (24, 12, 15, False),
    415: (18, 12, 15, False),
    416: (20, 6, 10, False),
    417: (30, 13, 20, False),
    418: ('', '', '', True),
    419: (17, 6, 10, False),
    420: ('', '', '', True),
    421: (19, 8, 15, False),
    422: (19, 11, 15, False),
    423: (17, 8, 15, False),
    424: (17, 8, 15, False),
    425: (14, 8, 10, False),
    426: (20, 12, 15, False),
    427: (23, 15, 15, False),
    428: ('', '', '', True),
    429: (21, 10, 15, False),
    430: ('', '', '', True),
    431: (20, 6, 10, False),
    432: (31, 13, 20, False),
    433: (17, 6, 10, False),
    434: (6, 12, 10, False),
    435: (9, 11, 10, False),
    436: (8, 13, 10, False),
    437: (17, 14, 15, False),
    438: (17, 12, 15, False),
    439: (17, 8, 15, False),
    440: (4, 9, 10, False),
    441: ('', '', '', True),
    442: (20, 8, 15, False),
    443: (21, 9, 15, False),
    444: (25, 8, 15, False),
    445: (24, 10, 16, False),
    446: (20, 11, 15, False),
    447: (24, 13, 15, False),
    448: (8, 6, 10, False)
}

def main():
    sess = requests.Session()

    # Login
    r = sess.post(BASE + '/api/login', json={'uid': 'admin', 'pw': '1234'})
    if not r.json().get('ok'):
        print('Login failed:', r.json())
        return
    print('Login OK')

    # Get all students
    r = sess.get(BASE + '/api/students')
    students = r.json().get('data', [])
    print(f'Fetched {len(students)} students')

    # Build roll->id map (Humanities group only, rolls 201-448)
    roll_to_id = {}
    for s in students:
        roll = s.get('roll', '')
        if s.get('group', '').lower() == 'humanities':
            roll_to_id[roll] = s['id']

    # Build entries
    entries = []
    missing = []
    for roll_num, (cq, mcq, prac, absent) in MARKS.items():
        roll_str = str(roll_num)
        sid = roll_to_id.get(roll_str)
        if not sid:
            missing.append(roll_str)
            continue
        entries.append({
            'studentId': sid,
            'cq': cq,
            'mcq': mcq,
            'prac': prac,
            'absent': absent
        })

    print(f'Prepared {len(entries)} entries.')
    if missing:
        print(f'Missing rolls (not in DB): {missing}')

    # POST batch-subject
    payload = {
        'subjectCode': SUBJECT,
        'examType': EXAM_TYPE,
        'year': YEAR,
        'entries': entries
    }
    r = sess.post(BASE + '/api/marks/batch-subject', json=payload)
    resp = r.json()
    if resp.get('ok'):
        print(f'SUCCESS: {resp.get("message")}')
    else:
        print(f'FAILED ({r.status_code}):', resp)
        return

if __name__ == '__main__':
    main()

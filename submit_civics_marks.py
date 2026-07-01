import requests

BASE = 'http://localhost:5000'
SUBJECT = '269'
EXAM_TYPE = 'Annual'
YEAR = '2025-2026'

# roll -> (cq, mcq, absent)
MARKS = {
    201: (37, 17, False),
    202: (29, 17, False),
    203: (28, 16, False),
    204: (43, 19, False),
    205: (34, 13, False),
    206: (32, 13, False),
    207: (27, 13, False),
    208: (28, 12, False),
    209: (33, 12, False),
    210: (28, 16, False),
    211: (36, 15, False),
    212: (25, 15, False),
    213: (29, 12, False),
    214: (29, 13, False),
    215: (24, 13, False),
    216: ('', '', True),
    217: ('', '', True),
    218: (31, 11, False),
    219: ('', '', True),
    220: (29, 16, False),
    221: (28, 15, False),
    222: (31, 17, False),
    223: (24, 14, False),
    224: ('', '', True),
    225: (40, 17, False),
    226: (38, 19, False),
    227: (29, 17, False),
    228: ('', '', True),
    229: (31, 16, False),
    230: (27, 10, False),
    231: (34, 11, False),
    232: (32, 15, False),
    233: (36, 18, False),
    234: (23, 13, False),
    235: (24, 16, False),
    236: (26, 17, False),
    237: (23, 15, False),
    238: (35, 10, False),
    239: (29, 18, False),
    240: (36, 15, False),
    241: (48, 15, False),
    242: (27, 14, False),
    243: (29, 15, False),
    244: (37, 14, False),
    245: (18, 14, False),
    246: (18, 11, False),
    247: (29, 21, False),
    248: (14, 15, False),
    249: (27, 17, False),
    250: (25, 19, False),
    251: (28, 10, False),
    252: (23, 13, False),
    253: (24, 16, False),
    254: (30, 16, False),
    255: (26, 11, False),
    256: (26, 14, False),
    257: (24, 16, False),
    258: (25, 15, False),
    259: (31, 19, False),
    260: (38, 18, False),
    261: (26, 14, False),
    262: (26, 14, False),
    263: (23, 15, False),
    264: (26, 15, False),
    265: (25, 15, False),
    266: (23, 19, False),
    267: (27, 14, False),
    268: (28, 17, False),
    269: (30, 16, False),
    270: (23, 13, False),
    271: (40, 16, False),
    272: (32, 11, False),
    273: (24, 16, False),
    274: (15, 15, False),
    275: ('', '', True),
    276: (34, 12, False),
    277: (23, 15, False),
    278: (16, 15, False),
    279: (23, 19, False),
    280: ('', '', True),
    281: (24, 17, False),
    282: (33, 20, False),
    283: (31, 13, False),
    284: (23, 10, False),
    285: (27, 18, False),
    286: (18, 12, False),
    287: (25, 16, False),
    288: (23, 11, False),
    289: (30, 14, False),
    290: (26, 17, False),
    291: (26, 19, False),
    292: (34, 20, False),
    293: (29, 17, False),
    294: (19, 16, False),
    295: (27, 16, False),
    296: (26, 16, False),
    297: (29, 16, False),
    298: (45, 19, False),
    299: (33, 12, False),
    300: (31, 15, False),
    301: (11, 13, False),
    302: (12, 14, False),
    303: (31, 20, False),
    304: (18, 14, False),
    305: (33, 13, False),
    306: (39, 18, False),
    307: (30, 16, False),
    308: (36, 14, False),
    309: (27, 15, False),
    310: (30, 13, False),
    311: (34, 14, False),
    312: (28, 14, False),
    313: (39, 17, False),
    314: (30, 15, False),
    315: (31, 13, False),
    316: (23, 14, False),
    317: (17, 16, False),
    318: (18, 16, False),
    319: (24, 16, False),
    320: (17, 14, False),
    321: (13, 14, False),
    322: ('', '', True),
    323: (27, 11, False),
    324: (12, 12, False),
    325: (23, 13, False),
    326: (27, 15, False),
    327: (30, 18, False),
    328: (39, 11, False),
    329: (37, 17, False),
    330: (26, 14, False),
    331: (27, 14, False),
    332: (26, 19, False),
    333: ('', '', True),
    334: (23, 12, False),
    335: (34, 13, False),
    336: (34, 14, False),
    337: (32, 18, False),
    338: (35, 18, False),
    339: (25, 11, False),
    340: ('', '', True),
    341: (17, 14, False),
    342: (27, 13, False),
    343: (23, 13, False),
    344: (23, 18, False),
    345: (26, 15, False),
    346: ('', '', True),
    347: (16, 13, False),
    348: (30, 10, False),
    349: (31, 14, False),
    350: (46, 21, False),
    351: (32, 18, False),
    352: (33, 17, False),
    353: (19, 11, False),
    354: (31, 10, False),
    355: ('', '', True),
    356: (40, 12, False),
    357: (30, 11, False),
    358: (45, 19, False),
    359: (35, 15, False),
    360: (14, 13, False),
    361: (50, 23, False),
    362: (35, 15, False),
    363: ('', '', True),
    364: (30, 12, False),
    365: (23, 15, False),
    366: (40, 18, False),
    367: (3, 18, False),
    368: (31, 14, False),
    369: (33, 14, False),
    370: (30, 14, False),
    371: (24, 17, False),
    372: (28, 19, False),
    373: (35, 11, False),
    374: (41, 17, False),
    375: (39, 21, False),
    376: (43, 13, False),
    377: (41, 15, False),
    378: (32, 21, False),
    379: ('', '', True),
    380: (27, 14, False),
    381: (26, 20, False),
    382: (31, 19, False),
    383: (17, 14, False),
    384: (33, 11, False),
    385: (44, 16, False),
    386: (23, 15, False),
    387: (34, 14, False),
    388: (25, 16, False),
    389: (35, 15, False),
    390: (9, 17, False),
    391: (32, 15, False),
    392: (7, 12, False),
    393: (32, 18, False),
    394: ('', '', True),
    395: (45, 27, False),
    396: (30, 10, False),
    397: (25, 15, False),
    398: (37, 16, False),
    399: (36, 15, False),
    400: (38, 15, False),
    401: ('', '', True),
    402: (31, 16, False),
    403: (31, 17, False),
    404: (30, 16, False),
    405: (51, 12, False),
    406: (31, 13, False),
    407: (48, 16, False),
    408: (31, 19, False),
    409: (50, 15, False)
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

    # Build roll->id map (Humanities group only, rolls 201-409)
    roll_to_id = {}
    for s in students:
        roll = s.get('roll', '')
        if s.get('group', '').lower() == 'humanities':
            roll_to_id[roll] = s['id']

    # Build entries
    entries = []
    missing = []
    for roll_num, (cq, mcq, absent) in MARKS.items():
        roll_str = str(roll_num)
        sid = roll_to_id.get(roll_str)
        if not sid:
            missing.append(roll_str)
            continue
        entries.append({
            'studentId': sid,
            'cq': cq,
            'mcq': mcq,
            'prac': '',   # Civics has no practical
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

    # Spot checks
    print('\n--- Verification Spot Checks ---')
    checks = [201, 216, 274, 321, 367, 409]
    for roll_num in checks:
        roll_str = str(roll_num)
        sid = roll_to_id.get(roll_str)
        if not sid:
            print(f'Roll {roll_str} not in DB')
            continue
        rv = sess.get(BASE + f'/api/marks/{sid}')
        if rv.ok:
            data = rv.json().get('data', {})
            marks_sub = (data.get(EXAM_TYPE) or {}).get(SUBJECT)
            if marks_sub:
                print(f'Roll {roll_str}: cq={marks_sub.get("cq")}, mcq={marks_sub.get("mcq")}, absent={marks_sub.get("absent")}')
            else:
                print(f'Roll {roll_str}: no civics marks found')

if __name__ == '__main__':
    main()

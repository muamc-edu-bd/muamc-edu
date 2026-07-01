"""
ICT (275) Annual Marks submission via localhost:5000 API
Session: 2025-2026 | Exam: Annual
Roll 720 MCQ = 13 (corrected)
Roll 732 skipped
"""

import requests

BASE      = 'http://localhost:5000'
SUBJECT   = '275'
EXAM_TYPE = 'Annual'
YEAR      = '2025-2026'

# roll -> (cq, mcq, prac, absent)
MARKS = {
    '701': (13,  8, 10, False),
    '702': (28, 10, 20, False),
    '703': (21, 10, 15, False),
    '704': ( 9, 11, 10, False),
    '705': (28,  8, 15, False),
    '706': (32, 13, 20, False),
    '707': (21, 10, 15, False),
    '708': (12, 13, 10, False),
    '709': (13, 10, 10, False),
    '710': (14,  9, 10, False),
    '711': ( 7,  6, 10, False),
    '712': (20, 15, 15, False),
    '713': ( 0,  0,  0, True ),  # AB
    '714': (14,  6, 10, False),
    '715': ( 8, 10, 10, False),
    '716': (17, 12, 15, False),
    '717': ( 0,  0,  0, True ),  # AB
    '718': (17, 13, 15, False),
    '719': ( 6,  5, 10, False),
    '720': (36, 13, 21, False),  # MCQ corrected to 13
    '721': (17, 12, 15, False),
    '722': ( 7,  8, 10, False),
    '723': (13, 13, 10, False),
    '724': ( 8, 13, 10, False),
    '725': (10, 12, 10, False),
    '726': (17, 11, 15, False),
    '727': (17, 11, 15, False),
    '728': ( 0,  0,  0, True ),  # AB
    '729': (17, 14, 15, False),
    '730': (21, 14, 15, False),
    '731': ( 0,  0,  0, True ),  # AB
    # 732 skipped
}

# Correct student IDs from PostgreSQL (via /api/students)
ROLL_TO_ID = {
    '701': 'e6266e8ac6674431',
    '702': '75ec7be0f4aa4aca',
    '703': 'a96877c499ce48f7',
    '704': '3c31ee000b13492c',
    '705': '03cde60825ec4268',
    '706': 'fcf59c1a6ae14542',
    '707': '8f2a450404744e2d',
    '708': '2af7b48e24804f62',
    '709': '17041b2d381a4376',
    '710': 'b7177ca4e04a4680',
    '711': 'e2a13e7fb5a74982',
    '712': '6086dc226801422b',
    '713': '59e8eeb60319479e',
    '714': '45bceaa786314a2e',
    '715': '78d0ebf7ed1441d7',
    '716': 'b611091e79064afc',
    '717': '731030bc5235426b',
    '718': '8e59a2120e8e46f1',
    '719': 'cb10c4d5fbc34416',
    '720': '5a6c70c4f8e04480',
    '721': '3acf8e8ac6964282',
    '722': '585a1b57c9154b19',
    '723': '1b698eb5e57a45aa',
    '724': 'f412f3ae09864313',
    '725': 'f78a1c6cd6a64ce9',
    '726': '0f7ee5bdcd18478e',
    '727': 'a48e2d19f78d4808',
    '728': '0ffea2cba31049cf',
    '729': 'ff639f5ae18f48fe',
    '730': '6482acf0840c47c1',
    '731': '34fe24d4afea4ed0',
}

def main():
    sess = requests.Session()

    # Login
    r = sess.post(BASE + '/api/login', json={'uid': 'admin', 'pw': '1234'})
    if not r.json().get('ok'):
        print('Login failed:', r.json())
        return
    print('Login OK')

    # Build entries
    entries = []
    for roll, (cq, mcq, prac, absent) in MARKS.items():
        sid = ROLL_TO_ID.get(roll)
        if not sid:
            print(f'  SKIP roll {roll} - no ID')
            continue
        entries.append({
            'studentId': sid,
            'cq':     '' if absent else cq,
            'mcq':    '' if absent else mcq,
            'prac':   '' if absent else prac,
            'absent': absent,
        })

    print(f'Submitting {len(entries)} entries...')

    payload = {
        'subjectCode': SUBJECT,
        'examType':    EXAM_TYPE,
        'year':        YEAR,
        'entries':     entries,
    }

    r = sess.post(BASE + '/api/marks/batch-subject', json=payload)
    resp = r.json()
    if resp.get('ok'):
        print('SUCCESS:', resp.get('message'))
    else:
        print('FAILED:', resp)
        return

    # Verify a sample
    print('\n--- Verification (roll 701, 713 AB, 720 corrected) ---')
    for check_roll in ['701', '713', '720']:
        sid = ROLL_TO_ID[check_roll]
        rv = sess.get(BASE + f'/api/marks/{sid}')
        if rv.ok:
            m = rv.json()
            ict = (m.get(EXAM_TYPE) or {}).get(SUBJECT, {})
            print(f'Roll {check_roll}: {ict}')

if __name__ == '__main__':
    main()

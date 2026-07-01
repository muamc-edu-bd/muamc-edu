import requests

BASE = 'http://localhost:5000'
SUBJECT = '178'
EXAM_TYPE = 'Annual'
YEAR = '2025-2026'

# roll -> (cq, mcq, prac, absent)
MARKS = {
    1: (28, 9, 24, False),
    2: (21, 10, 21, False),
    3: (41, 11, 25, False),
    4: (11, 14, 11, False),
    5: (14, 14, 11, False),
    6: (19, 9, '', False),
    7: (23, 11, 19, False),
    8: (23, 13, 24, False),
    9: (26, 13, 21, False),
    10: (24, 9, 20, False),
    11: (26, 12, 14, False),
    12: (9, 8, 19, False),
    13: (9, '', '', False),
    14: (9, 11, 22, False),
    15: (17, 8, 19, False),
    16: (12, 9, 12, False),
    17: (14, 10, 19, False),
    18: (26, 13, 23, False),
    19: (11, 7, 20, False),
    20: ('', '', '', True),
    21: (9, 7, 20, False),
    22: (24, 8, 24, False),
    23: (22, 11, 19, False),
    24: (10, 10, '', False),
    25: (14, 11, 23, False),
    26: (4, 8, 22, False),
    27: (20, 7, 11, False),
    28: (28, 13, 18, False),
    29: (30, 12, 20, False),
    30: (8, 5, 5, False),
    31: (23, 12, 21, False),
    32: (36, 12, 20, False),
    33: (7, 8, 16, False),
    34: (7, 11, '', False),
    35: (7, 6, 19, False),
    36: (0, 9, 21, False),
    37: (20, 9, 22, False),
    38: (24, 12, 22, False),
    39: (13, 10, 23, False),
    40: (17, 9, 14, False),
    41: (7, 11, 21, False),
    42: (17, 12, 13, False),
    43: (6, 10, 18, False),
    44: (36, 15, 18, False),
    45: (7, 5, 12, False),
    46: (17, 11, 22, False),
    47: (23, 11, 20, False),
    48: (21, 13, 17, False),
    49: (18, 10, 21, False),
    50: (17, 10, 23, False),
    51: (13, 11, 11, False),
    52: (24, 10, 12, False),
    53: (23, 16, 17, False),
    54: (19, 14, 16, False),
    55: (21, 11, 12, False),
    56: (4, 6, '', False),
    57: (14, 7, 18, False),
    58: (24, 14, 23, False),
    59: (19, 8, 14, False),
    60: ('', '', '', True),
    61: (24, 11, 24, False),
    62: (20, 9, '', False),
    63: (21, 10, 17, False),
    64: (10, 9, 9, False),
    65: (17, 14, 20, False),
    66: (19, 11, 13, False),
    67: (11, 10, 15, False),
    68: (11, 10, 17, False),
    69: (27, 9, 17, False),
    70: (26, 11, 13, False),
    71: (23, 10, 19, False),
    72: (7, 7, 10, False),
    73: (10, 6, 15, False),
    74: (4, 12, 8, False),
    75: (9, 11, 10, False),
    76: (22, 7, 11, False),
    77: (8, 13, 17, False),
    78: (19, 14, 18, False),
    79: (4, 12, '', False),
    80: (30, 14, 16, False),
    81: (14, 8, 19, False),
    82: (9, 10, 20, False),
    83: (8, 13, 21, False),
    84: (19, 10, 22, False),
    85: (18, 11, 13, False),
    86: (17, 9, 18, False),
    87: (26, 10, 22, False),
    88: (10, 12, 16, False),
    89: (10, 9, 6, False),
    90: (25, 13, 24, False),
    91: (20, 11, 18, False),
    92: (20, 11, 17, False),
    93: (25, 8, 15, False),
    94: (13, 11, 21, False),
    95: (23, 14, 11, False),
    96: (13, 10, 20, False),
    97: (14, 11, 17, False),
    98: (11, 11, 17, False),
    99: (17, 12, 18, False),
    100: (23, 10, 23, False),
    101: (20, 8, 13, False),
    102: (30, 12, 24, False),
    103: (13, 10, 23, False),
    104: (20, 10, 21, False),
    105: (17, 14, 14, False),
    106: (18, 13, 21, False),
    107: (14, 12, 12, False),
    108: (9, 12, 17, False),
    109: (5, 10, 16, False),
    110: (14, 7, 14, False),
    111: ('', '', 12, False),
    112: (23, 16, 23, False),
    113: ('', '', '', True),
    114: (29, 8, 18, False),
    115: (22, 10, 18, False),
    116: (27, 10, 17, False),
    117: (11, 10, 21, False),
    118: (23, 8, 20, False),
    119: (21, 9, '', False),
    120: (20, 10, 20, False),
    121: (17, 8, 12, False),
    122: (21, 12, 14, False),
    123: (14, 9, 13, False),
    124: ('', '', '', True),
    125: (18, 10, 23, False),
    126: (18, 13, 10, False),
    127: (14, 11, 23, False),
    128: (13, 7, 18, False),
    129: (14, 12, 11, False),
    130: (17, 8, 13, False),
    131: (22, 13, 17, False),
    132: (21, 9, 19, False),
    133: ('', '', '', True),
    134: (14, 5, 15, False),
    135: (18, 8, 22, False),
    136: (27, 11, 21, False),
    137: (32, 9, 23, False),
    138: (20, 9, 13, False),
    139: (9, 10, 14, False),
    140: (9, 11, 12, False),
    141: (8, 10, '', False),
    142: (28, 10, 16, False),
    143: (20, 11, 21, False),
    144: (30, 9, 13, False),
    145: (31, 8, 10, False),
    146: (27, 8, 18, False)
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

    # Build roll->id map (Science group only, rolls 1-146)
    roll_to_id = {}
    for s in students:
        roll = s.get('roll', '')
        if s.get('group', '').lower() == 'science':
            roll_to_id[roll] = s['id']

    # Build entries
    entries = []
    missing = []
    for roll_num, (cq, mcq, prac, absent) in MARKS.items():
        # Pad to 2 digits for single-digit rolls to match DB format (e.g. '01')
        roll_str = str(roll_num).zfill(2) if roll_num < 10 else str(roll_num)
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

    # Spot checks
    print('\n--- Verification Spot Checks ---')
    checks = [1, 20, 56, 111, 146]
    for roll_num in checks:
        roll_str = str(roll_num).zfill(2) if roll_num < 10 else str(roll_num)
        sid = roll_to_id.get(roll_str)
        if not sid:
            print(f'Roll {roll_str} not in DB')
            continue
        rv = sess.get(BASE + f'/api/marks/{sid}')
        if rv.ok:
            data = rv.json().get('data', {})
            marks_sub = (data.get(EXAM_TYPE) or {}).get(SUBJECT)
            if marks_sub:
                print(f'Roll {roll_str}: cq={marks_sub.get("cq")}, mcq={marks_sub.get("mcq")}, prac={marks_sub.get("prac")}, absent={marks_sub.get("absent")}')
            else:
                print(f'Roll {roll_str}: no biology marks found')

if __name__ == '__main__':
    main()

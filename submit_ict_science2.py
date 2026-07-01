"""
ICT (275) Annual Marks - Science (বিজ্ঞান) Division
Rolls 36-78 (new) + fix missing rolls 1-9 (leading-zero rollfix)
Exam: Annual | Year: 2025-2026
"""
import requests

BASE      = 'http://localhost:5000'
SUBJECT   = '275'
EXAM_TYPE = 'Annual'
YEAR      = '2025-2026'

# Previously entered rolls 1-35 marks (for fixing rolls 1-9 which were missed)
MARKS_1_9 = {
    1:  (20, 15, 15, False),
    2:  (18, 12, 15, False),
    3:  (44, 15, 25, False),
    4:  (24, 13, 15, False),
    5:  (25, 15, 20, False),
    6:  (20, 13, 17, False),
    7:  (35, 12, 20, False),
    8:  (32, 16, 22, False),
    9:  (41, 17, 25, False),
}

# New marks: rolls 36-78
MARKS_36_78 = {
    36: (10, 11, 10, False),
    37: (25,  9, 15, False),
    38: (26, 12, 15, False),
    39: (18, 14, 15, False),
    40: (28, 13, 20, False),
    41: (21, 11, 15, False),
    42: (24, 12, 15, False),
    43: (23, 11, 16, False),
    44: (29, 19, 22, False),
    45: (17,  9, 15, False),
    46: (18, 10, 15, False),
    47: (34,  9, 17, False),
    48: (31, 11, 20, False),
    49: (24, 15, 21, False),
    50: (34, 15, 21, False),
    51: (31, 15, 20, False),
    52: (32, 14, 20, False),
    53: (26, 13, 21, False),
    54: (26, 18, 20, False),
    55: (30, 14, 20, False),
    56: (17,  9, 15, False),
    57: (26, 11, 15, False),
    58: (29,  9, 15, False),
    59: (17,  3, 10, False),
    60: ( 0,  0,  0, True ),   # AB
    61: (42, 17, 25, False),
    62: (18, 14, 15, False),
    63: (33, 13, 20, False),
    64: (17, 10, 15, False),
    65: (26, 15, 20, False),
    66: (22, 14, 15, False),
    67: (22, 11, 17, False),
    68: (28, 12, 20, False),
    69: (34, 12, 20, False),
    70: (23,  8, 15, False),
    71: (27, 10, 15, False),
    72: (19,  9, 15, False),
    73: (21, 10, 15, False),
    74: (17, 10, 15, False),
    75: (17, 12, 15, False),
    76: (27, 13, 20, False),
    77: (24,  8, 15, False),
    78: (26,  8, 16, False),
}

def main():
    sess = requests.Session()

    # Login
    r = sess.post(BASE + '/api/login', json={'uid': 'admin', 'pw': '1234'})
    if not r.json().get('ok'):
        print('Login failed:', r.json()); return
    print('Login OK')

    # Get all students
    r = sess.get(BASE + '/api/students')
    students = r.json().get('data', [])
    print(f'Fetched {len(students)} students')

    # Build roll_int -> (id, stored_roll_str) map for Science group
    roll_int_to_sid = {}
    for s in students:
        roll_str = s.get('roll', '')
        if not roll_str.isdigit():
            continue
        roll_int = int(roll_str)
        if 1 <= roll_int <= 78 and s.get('group', '').lower() == 'science':
            roll_int_to_sid[roll_int] = s['id']

    print(f'Found {len(roll_int_to_sid)} Science students (rolls 1-78)')

    # Combine both mark sets
    all_marks = {}
    all_marks.update(MARKS_1_9)
    all_marks.update(MARKS_36_78)

    entries = []
    missing = []
    for roll_int, (cq, mcq, prac, absent) in all_marks.items():
        sid = roll_int_to_sid.get(roll_int)
        if not sid:
            missing.append(roll_int)
            continue
        entries.append({
            'studentId': sid,
            'cq':     '' if absent else cq,
            'mcq':    '' if absent else mcq,
            'prac':   '' if absent else prac,
            'absent': absent,
        })

    print(f'Prepared {len(entries)} entries. Missing rolls: {sorted(missing)}')

    # POST batch-subject
    payload = {
        'subjectCode': SUBJECT,
        'examType':    EXAM_TYPE,
        'year':        YEAR,
        'entries':     entries,
    }
    r = sess.post(BASE + '/api/marks/batch-subject', json=payload)
    resp = r.json()
    if resp.get('ok'):
        print(f'SUCCESS: {resp.get("message")}')
    else:
        print(f'FAILED ({r.status_code}):', resp)
        return

    # Spot check
    print('\n--- Spot check ---')
    for chk in [1, 3, 9, 36, 60, 78]:
        sid = roll_int_to_sid.get(chk)
        if not sid:
            print(f'Roll {chk}: not in DB'); continue
        rv = sess.get(BASE + f'/api/marks/{sid}')
        if rv.ok:
            data = rv.json().get('data', {})
            ict  = (data.get(EXAM_TYPE) or {}).get(SUBJECT)
            if ict:
                tag = 'AB' if ict.get('absent') else f"CQ={ict['cq']}, MCQ={ict['mcq']}, Prac={ict['prac']}"
                print(f'Roll {chk:>2}: {tag}')
            else:
                print(f'Roll {chk:>2}: no ICT data')

if __name__ == '__main__':
    main()

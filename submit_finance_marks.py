import requests

BASE = 'http://localhost:5000'
SUBJECT = '292'
EXAM_TYPE = 'Annual'
YEAR = '2025-2026'

# roll -> (cq, mcq, absent)
MARKS = {
    701: (37, 23, False),
    702: (54, 23, False),
    703: (25, 16, False),
    704: (13, 19, False),
    705: (38, 15, False),
    706: (44, 16, False),
    707: (35, 20, False),
    708: (41, 23, False),
    709: (23, 16, False),
    710: (23, 19, False),
    711: (23, 15, False),
    712: (39, 17, False),
    713: (5, '', False),
    714: (5, 7, False),
    715: (13, 9, False),
    716: (6, 16, False),
    717: ('', '', True),
    718: (37, 19, False),
    719: (16, 14, False),
    720: (52, 24, False),
    721: (13, 16, False),
    722: (16, 16, False),
    723: (15, 14, False),
    724: (8, 5, False),
    725: (7, 16, False),
    726: (13, 14, False),
    727: (14, 10, False),
    728: ('', '', True),  # NIPA RANI DAS (absent, marks belong to 729)
    729: (7, 3, False),   # MST MAHABUBA HASAN MAISA (marks from row 28)
    730: (6, 15, False),
    731: ('', '', True)
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

    # Build roll->id map (Business group only, rolls 701-731)
    roll_to_id = {}
    for s in students:
        roll = s.get('roll', '')
        if s.get('group', '').lower() == 'business':
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
            'prac': '',   # Finance has no practical
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
    checks = [701, 713, 717, 728, 729, 730]
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
                print(f'Roll {roll_str}: no finance marks found')

if __name__ == '__main__':
    main()

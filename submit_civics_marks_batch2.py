import requests

BASE = 'http://localhost:5000'
SUBJECT = '269'
EXAM_TYPE = 'Annual'
YEAR = '2025-2026'

# roll -> (cq, mcq, absent)
MARKS = {
    410: (39, 21, False),
    411: ('', '', True),
    412: (35, 10, False),
    413: (33, 10, False),
    414: (38, 13, False),
    415: (25, 11, False),
    416: (24, 16, False),
    417: (38, 17, False),
    418: ('', '', True),
    419: (39, 17, False),
    420: ('', '', True),
    421: (26, 16, False),
    422: (29, 21, False),
    423: (42, 18, False),
    424: (32, 16, False),
    425: (36, 18, False),
    426: (24, 10, False),
    427: (23, 10, False),
    428: ('', '', True),
    429: (23, 13, False),
    430: ('', '', True),
    431: (25, 13, False),
    432: (33, 17, False),
    433: (33, 12, False),
    434: (23, 13, False),
    435: (17, 14, False),
    436: (36, 16, False),
    437: (30, 18, False),
    438: (39, 18, False),
    439: (43, 14, False),
    440: (32, 12, False),
    441: ('', '', True),
    442: (31, 13, False),
    443: (23, 11, False),
    444: (23, 18, False),
    445: (28, 18, False),
    446: (30, 18, False),
    447: (33, 20, False),
    448: (37, 11, False)
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

    # Build roll->id map (Humanities group only, rolls 410-448)
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

if __name__ == '__main__':
    main()

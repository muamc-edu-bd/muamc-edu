"""
ICT (275) Annual Marks - Science (বিজ্ঞান) Division
Rolls 1-35 | Exam: Annual | Year: 2025-2026
"""
import requests

BASE      = 'http://localhost:5000'
SUBJECT   = '275'
EXAM_TYPE = 'Annual'
YEAR      = '2025-2026'

# roll -> (cq, mcq, prac, absent)
# Read from Science ICT mark sheet
MARKS = {
    '1':  (20, 15, 15, False),
    '2':  (18, 12, 15, False),
    '3':  (44, 15, 25, False),
    '4':  (24, 13, 15, False),
    '5':  (25, 15, 20, False),
    '6':  (20, 13, 17, False),
    '7':  (35, 12, 20, False),
    '8':  (32, 16, 22, False),
    '9':  (41, 17, 25, False),
    '10': (27, 13, 20, False),
    '11': (27, 16, 20, False),
    '12': (22, 11, 17, False),
    '13': (17,  9, 15, False),
    '14': (22, 13, 15, False),
    '15': (21, 12, 17, False),
    '16': (27, 12, 21, False),   # prac: 21 (corrected in sheet)
    '17': (20, 13, 17, False),
    '18': (34, 13, 20, False),
    '19': (17, 11, 15, False),
    '20': ( 0,  0,  0, True ),   # AB
    '21': (29, 11, 20, False),
    '22': (38, 16, 20, False),
    '23': (29, 14, 20, False),
    '24': (42, 16, 25, False),
    '25': (20, 13, 17, False),
    '26': ( 8,  3, 10, False),
    '27': (31, 10, 20, False),
    '28': (22, 10, 15, False),
    '29': (33, 15, 22, False),
    '30': ( 6,  9, 10, False),
    '31': (26, 10, 15, False),
    '32': (38, 15, 20, False),
    '33': (17, 12, 15, False),
    '34': (33, 14, 20, False),
    '35': (26, 12, 15, False),
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

    # Build roll->id map (only Science group, rolls 1-35)
    roll_to_id = {}
    for s in students:
        roll = s.get('roll', '')
        if roll.isdigit() and 1 <= int(roll) <= 35:
            # Prefer Science group students, but accept any if only one match per roll
            if roll not in roll_to_id:
                roll_to_id[roll] = s['id']
            elif s.get('group', '').lower() == 'science':
                roll_to_id[roll] = s['id']  # prefer Science

    # Show what we found
    print('Roll-to-ID map (1-35):')
    for roll in sorted(roll_to_id.keys(), key=int):
        sid = roll_to_id[roll]
        stu = next((s for s in students if s['id'] == sid), {})
        print(f'  Roll {roll}: id={sid}, group={stu.get("group")}, cls={stu.get("cls")}')

    # Build entries
    entries = []
    missing = []
    for roll, (cq, mcq, prac, absent) in MARKS.items():
        sid = roll_to_id.get(roll)
        if not sid:
            missing.append(roll)
            continue
        entries.append({
            'studentId': sid,
            'cq':     '' if absent else cq,
            'mcq':    '' if absent else mcq,
            'prac':   '' if absent else prac,
            'absent': absent,
        })

    print(f'\nPrepared {len(entries)} entries. Missing rolls: {missing}')

    # POST
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
    for chk in ['1', '20', '26', '35']:
        sid = roll_to_id.get(chk)
        if not sid:
            print(f'Roll {chk}: not found'); continue
        rv = sess.get(BASE + f'/api/marks/{sid}')
        if rv.ok:
            data = rv.json().get('data', {})
            ict  = (data.get(EXAM_TYPE) or {}).get(SUBJECT)
            if ict:
                tag = 'AB' if ict.get('absent') else f"CQ={ict['cq']}, MCQ={ict['mcq']}, Prac={ict['prac']}"
                print(f'Roll {chk}: {tag}')
            else:
                print(f'Roll {chk}: no ICT data')


if __name__ == '__main__':
    main()

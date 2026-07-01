"""
ICT (275) Annual Marks - Rolls 410-450
Exam: Annual | Year: 2025-2026
"""
import requests

BASE      = 'http://localhost:5000'
SUBJECT   = '275'
EXAM_TYPE = 'Annual'
YEAR      = '2025-2026'

# roll -> (cq, mcq, prac, absent)
MARKS = {
    '410': (33,  9, 20, False),
    '411': ( 0,  0,  0, True ),  # AB
    '412': (21,  8, 15, False),
    '413': (23,  8, 15, False),
    '414': (24, 12, 15, False),
    '415': (18, 12, 15, False),
    '416': (20,  6, 10, False),
    '417': (30, 13, 20, False),
    '418': ( 0,  0,  0, True ),  # AB
    '419': (17,  6, 10, False),
    '420': ( 0,  0,  0, True ),  # AB
    '421': (19,  8, 15, False),
    '422': (19, 11, 15, False),
    '423': (17,  8, 15, False),
    '424': (17,  8, 15, False),
    '425': (14,  8, 10, False),
    '426': (20, 12, 15, False),
    '427': (23, 15, 15, False),
    # 428: blank – skipped
    '429': (21, 10, 15, False),
    '430': ( 0,  0,  0, True ),  # AB
    '431': (20,  6, 10, False),
    '432': (31, 13, 20, False),
    '433': (17,  6, 10, False),
    '434': ( 6, 12, 10, False),
    '435': ( 9, 11, 10, False),
    '436': ( 8, 13, 10, False),
    '437': (17, 14, 15, False),
    '438': (17, 12, 15, False),
    '439': (17,  8, 15, False),
    '440': ( 4,  9, 10, False),
    '441': ( 0,  0,  0, True ),  # AB
    '442': (20,  8, 15, False),
    '443': (21,  9, 15, False),
    '444': (25,  8, 15, False),
    '445': (24, 10, 16, False),
    '446': (20, 11, 15, False),
    '447': (24, 13, 15, False),
    '448': ( 8,  6, 10, False),
    '449': (21, 10, 15, False),
    '450': (23,  6, 10, False),
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

    roll_to_id = {s['roll']: s['id'] for s in students}

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

    print(f'Prepared {len(entries)} entries. Missing rolls: {missing}')

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
    for chk in ['410', '411', '420', '432', '441', '450']:
        sid = roll_to_id.get(chk)
        if not sid:
            print(f'Roll {chk}: not in DB'); continue
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

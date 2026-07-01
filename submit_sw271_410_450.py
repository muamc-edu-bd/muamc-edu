"""
Social Work / সমাজকর্ম (Subject Code: 271)
Rolls 410-450 | Annual | 2025-2026 | No Practical
Blank rows treated as ABSENT (absent=True)
"""
import requests

BASE      = 'http://localhost:5000'
SUBJECT   = '271'
EXAM_TYPE = 'Annual'
YEAR      = '2025-2026'

# roll -> (cq, mcq, absent)
# Blank rows = absent=True, cq/mcq ignored
MARKS = {
    '410': (0,  0,  True ),   # AB
    '411': (0,  0,  True ),   # AB
    '412': (0,  0,  True ),   # AB
    '413': (30, 17, False),   # total 47
    '414': (16, 11, False),   # total 27 (red)
    '415': (0,  0,  True ),   # AB
    '416': (0,  0,  True ),   # AB
    '417': (0,  0,  True ),   # AB
    '418': (0,  0,  True ),   # AB
    '419': (0,  0,  True ),   # AB
    '420': (20, 19, False),   # total 39 (red)
    '421': (27, 19, False),   # total 46
    '422': (30, 19, False),   # total 49
    '423': (29, 19, False),   # total 48
    '424': (24, 10, False),   # total 34
    '425': (0,  0,  True ),   # AB
    '426': (0,  0,  True ),   # AB
    '427': (0,  0,  True ),   # AB
    '428': (0,  0,  True ),   # AB
    '429': (0,  0,  True ),   # AB
    '430': (0,  0,  True ),   # AB
    '431': (36, 19, False),   # total 55
    '432': (0,  0,  True ),   # AB
    '433': (0,  0,  True ),   # AB
    '434': (0,  0,  True ),   # AB
    '435': (0,  0,  True ),   # AB
    '436': (26, 17, False),   # total 43
    '437': (30, 17, False),   # total 47
    '438': (0,  0,  True ),   # AB
    '439': (0,  0,  True ),   # AB
    '440': (0,  0,  True ),   # AB
    '441': (27, 14, False),   # total 41
    '442': (0,  0,  True ),   # AB
    '443': (0,  0,  True ),   # AB
    '444': (33, 20, False),   # total 53
    '445': (25, 16, False),   # total 41
    '446': (24,  5, False),   # total 29 (red)
    '447': (32, 15, False),   # total 47
    '448': (24, 12, False),   # total 36
    '449': (0,  0,  True ),   # AB
    '450': (0,  0,  True ),   # AB
}


def main():
    sess = requests.Session()

    r = sess.post(BASE + '/api/login', json={'uid': 'admin', 'pw': '1234'})
    if not r.json().get('ok'):
        print('Login failed:', r.json()); return
    print('Login OK')

    r = sess.get(BASE + '/api/students')
    students = r.json().get('data', [])
    print(f'Fetched {len(students)} students')
    roll_to_id = {s['roll']: s['id'] for s in students}

    entries = []
    missing = []
    for roll, (cq, mcq, absent) in MARKS.items():
        sid = roll_to_id.get(roll)
        if not sid:
            missing.append(roll); continue
        entries.append({
            'studentId': sid,
            'cq':    '' if absent else cq,
            'mcq':   '' if absent else mcq,
            'prac':  '',          # no practical
            'absent': absent,
        })

    print(f'Prepared {len(entries)} entries  (absent={sum(1 for _,(_,_,a) in MARKS.items() if a)}).')
    if missing:
        print(f'Not in DB: {missing}')

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
        print(f'FAILED ({r.status_code}):', resp); return

    # Spot check
    print('\n--- Spot check ---')
    for chk in ['410', '413', '414', '420', '431', '441', '444', '446']:
        sid = roll_to_id.get(chk)
        if not sid:
            print(f'  Roll {chk}: not in DB'); continue
        rv = sess.get(BASE + f'/api/marks/{sid}')
        if rv.ok:
            data = rv.json().get('data', {})
            sw = (data.get(EXAM_TYPE) or {}).get(SUBJECT)
            if sw:
                if sw.get('absent'):
                    print(f'  Roll {chk}: AB')
                else:
                    print(f'  Roll {chk}: CQ={sw["cq"]}, MCQ={sw["mcq"]}')
            else:
                print(f'  Roll {chk}: no data')

if __name__ == '__main__':
    main()

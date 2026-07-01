"""
Fix: Delete Social Work marks from subject 272 (wrong)
      and re-enter under subject 271 (correct)
Humanities Division | Rolls 201-409 | Annual | 2025-2026
No Practical
"""
import requests

BASE      = 'http://localhost:5000'
EXAM_TYPE = 'Annual'
YEAR      = '2025-2026'
OLD_CODE  = '272'   # wrong — will be deleted
NEW_CODE  = '271'   # correct

# Same marks as before
MARKS = {
    '201': (30, 20), '202': (27, 14),
    '211': (28, 11), '212': (28, 13),
    '220': (17, 11), '223': (26, 15), '229': (27, 14),
    '232': (13, 18), '233': (28, 11),
    '238': (20, 10), '241': (44, 18), '250': (16, 16),
    '254': (33, 17),
    '263': (17, 13), '264': (27, 13), '269': (33, 18),
    '271': (33, 17), '273': (24, 15), '274': (24, 15),
    '275': (32, 16), '277': (34, 18),
    '281': (25, 21), '284': (10, 10),
    '286': (27, 18), '287': (28, 15),
    '293': (24, 14), '295': (34, 14), '297': (37, 16),
    '299': (32, 18), '300': (25, 11),
    '311': (30, 17), '312': (28, 19), '314': (28, 15),
    '317': (34, 16), '318': (36, 16), '321': (20, 16),
    '325': (24, 10), '326': (24, 17), '327': (30, 16),
    '328': (16, 10), '329': (28, 23), '330': (26, 18),
    '337': (32, 15), '338': (29, 23), '339': (19, 10),
    '342': (27, 11), '343': (15, 10), '348': (16, 13),
    '356': (35, 18), '357': (26, 17), '358': (27, 22),
    '361': (26, 19), '362': (28, 13), '364': (25, 15),
    '365': (16, 17),
    '366': (35, 16), '371': (20, 14), '372': (24, 11),
    '376': (32, 18), '379': (20, 16), '380': (16, 17),
    '381': (25, 17), '382': (31, 18), '383': (18, 14),
    '384': (24, 16),
    '392': (10, 14), '393': (31, 20), '395': (39, 22),
    '398': (20, 14), '399': (24, 15), '400': (32, 18),
    '402': (27, 18), '406': (30, 10),
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

    # ── STEP 1: Delete all 272 entries ──────────────────────────────────────
    print('\nStep 1: Deleting subject 272 entries...')
    delete_entries = []
    for roll in MARKS:
        sid = roll_to_id.get(roll)
        if sid:
            delete_entries.append({
                'studentId': sid,
                'cq': '', 'mcq': '', 'prac': '',   # empty = delete
                'absent': False,
            })

    r = sess.post(BASE + '/api/marks/batch-subject', json={
        'subjectCode': OLD_CODE,
        'examType':    EXAM_TYPE,
        'year':        YEAR,
        'entries':     delete_entries,
    })
    resp = r.json()
    if resp.get('ok'):
        print(f'  Deleted {len(delete_entries)} entries from subject {OLD_CODE}')
    else:
        print(f'  Delete FAILED:', resp)

    # ── STEP 2: Insert under correct code 271 ───────────────────────────────
    print('\nStep 2: Inserting under subject 271...')
    entries = []
    missing = []
    for roll, (cq, mcq) in MARKS.items():
        sid = roll_to_id.get(roll)
        if not sid:
            missing.append(roll); continue
        entries.append({
            'studentId': sid,
            'cq':  cq,
            'mcq': mcq,
            'prac': '',
            'absent': False,
        })

    print(f'  Prepared {len(entries)} entries. Missing: {missing}')

    r = sess.post(BASE + '/api/marks/batch-subject', json={
        'subjectCode': NEW_CODE,
        'examType':    EXAM_TYPE,
        'year':        YEAR,
        'entries':     entries,
    })
    resp = r.json()
    if resp.get('ok'):
        print(f'  SUCCESS: {resp.get("message")}')
    else:
        print(f'  FAILED:', resp); return

    # ── STEP 3: Verify ────────────────────────────────────────────────────────
    print('\nStep 3: Verification ---')
    for chk in ['201', '271', '366', '406']:
        sid = roll_to_id.get(chk)
        if not sid:
            print(f'  Roll {chk}: not in DB'); continue
        rv = sess.get(BASE + f'/api/marks/{sid}')
        if rv.ok:
            data = rv.json().get('data', {})
            sw272 = (data.get(EXAM_TYPE) or {}).get(OLD_CODE)
            sw271 = (data.get(EXAM_TYPE) or {}).get(NEW_CODE)
            print(f'  Roll {chk}:  271→ {sw271}  |  272→ {sw272}')

if __name__ == '__main__':
    main()

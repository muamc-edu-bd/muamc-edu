"""
Social Work / সমাজকর্ম (Subject Code: 272)
Humanities Division | Rolls 201-409
Exam: Annual | Year: 2025-2026
No Practical (prac=0 for all)
"""
import requests

BASE      = 'http://localhost:5000'
SUBJECT   = '272'
EXAM_TYPE = 'Annual'
YEAR      = '2025-2026'

# roll -> (cq, mcq) — no practical for this subject
# Blank rows in mark sheet are simply omitted (not entered)
# Verified: CQ + MCQ = Total shown on sheet
MARKS = {
    # ── Image 2: Serials 1-35 (Rolls 201-235) ───────────────────────────────
    '201': (30, 20),   # total 50
    '202': (27, 14),   # total 41
    # 203-210: blank
    '211': (28, 11),   # total 39
    '212': (28, 13),   # total 41
    # 213-219: blank
    '220': (17, 11),   # total 28
    # 221-222: blank
    '223': (26, 15),   # total 41
    # 224-228: blank
    '229': (27, 14),   # total 41
    # 230-231: blank
    '232': (13, 18),   # total 31 (red)
    '233': (28, 11),   # total 39
    # 234-235: blank

    # ── Image 4: Serials 36-78 (Rolls 236-278) ───────────────────────────────
    # 236-237: blank
    '238': (20, 10),   # total 30 (red)
    # 239-240: blank
    '241': (44, 18),   # total 62
    # 242-249: blank
    '250': (16, 16),   # total 32 (red)
    # 251-253: blank
    '254': (33, 17),   # total 50
    # 255-262: blank
    '263': (17, 13),   # total 30 (red)
    '264': (27, 13),   # total 40
    # 265-268: blank
    '269': (33, 18),   # total 51
    # 270: blank
    '271': (33, 17),   # total 50
    # 272: blank
    '273': (24, 15),   # total 39
    '274': (24, 15),   # total 39
    '275': (32, 16),   # total 48
    # 276: blank
    '277': (34, 18),   # total 52
    # 278: blank

    # ── Image 5: Serials 79-121 (Rolls 279-321) ─────────────────────────────
    # 279-280: blank
    '281': (25, 21),   # total 46
    # 282-283: blank
    '284': (10, 10),   # total 20 (red)
    # 285: blank
    '286': (27, 18),   # total 45
    '287': (28, 15),   # total 43
    # 288-292: blank
    '293': (24, 14),   # total 38
    # 294: blank
    '295': (34, 14),   # total 48
    # 296: blank
    '297': (37, 16),   # total 53
    # 298: blank
    '299': (32, 18),   # total 50
    '300': (25, 11),   # total 36
    # 301-310: blank
    '311': (30, 17),   # total 47
    '312': (28, 19),   # total 47
    # 313: blank
    '314': (28, 15),   # total 43
    # 315-316: blank
    '317': (34, 16),   # total 50
    '318': (36, 16),   # total 52
    # 319-320: blank
    '321': (20, 16),   # total 36 (red)

    # ── Image 3: Serials 122-165 (Rolls 322-365) ────────────────────────────
    # 322-324: blank
    '325': (24, 10),   # total 34
    '326': (24, 17),   # total 41
    '327': (30, 16),   # total 46
    '328': (16, 10),   # total 26 (red)
    '329': (28, 23),   # total 51
    '330': (26, 18),   # total 44
    # 331-336: blank
    '337': (32, 15),   # total 47
    '338': (29, 23),   # total 52
    '339': (19, 10),   # total 29 (red)
    # 340-341: blank
    '342': (27, 11),   # total 38
    '343': (15, 10),   # total 25 (red)
    # 344-347: blank
    '348': (16, 13),   # total 29 (red)
    # 349-355: blank
    '356': (35, 18),   # total 53
    '357': (26, 17),   # total 43
    '358': (27, 22),   # total 49
    # 359-360: blank / incomplete
    '361': (26, 19),   # total 45
    '362': (28, 13),   # total 41
    # 363: blank
    '364': (25, 15),   # total 40
    '365': (16, 17),   # total 33 (red)

    # ── Image 1: Serials 166-209 (Rolls 366-409) ────────────────────────────
    '366': (35, 16),   # total 51
    # 367-370: blank
    '371': (20, 14),   # total 34 (red)
    '372': (24, 11),   # total 35
    # 373-375: blank
    '376': (32, 18),   # total 50
    # 377-378: blank
    '379': (20, 16),   # total 36 (red)
    '380': (16, 17),   # total 33 (red)
    '381': (25, 17),   # total 42
    '382': (31, 18),   # total 49
    '383': (18, 14),   # total 32 (red)
    '384': (24, 16),   # total 40
    # 385-391: blank
    '392': (10, 14),   # total 24 (red)
    '393': (31, 20),   # total 51
    # 394: blank
    '395': (39, 22),   # total 61
    # 396-397: blank
    '398': (20, 14),   # total 34 (red)
    '399': (24, 15),   # total 39
    '400': (32, 18),   # total 50
    # 401: blank
    '402': (27, 18),   # total 45
    # 403-405: blank
    '406': (30, 10),   # total 40
    # 407-409: blank
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
    for roll, (cq, mcq) in MARKS.items():
        sid = roll_to_id.get(roll)
        if not sid:
            missing.append(roll)
            continue
        entries.append({
            'studentId': sid,
            'cq':   cq,
            'mcq':  mcq,
            'prac': '',       # No practical for Social Work
            'absent': False,
        })

    print(f'Prepared {len(entries)} entries.')
    if missing:
        print(f'Missing rolls (not in DB): {missing}')

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
    print('\n--- Spot check (CQ+MCQ, no prac) ---')
    for chk in ['201', '232', '271', '321', '366', '395', '406']:
        sid = roll_to_id.get(chk)
        if not sid:
            print(f'Roll {chk}: not in DB'); continue
        rv = sess.get(BASE + f'/api/marks/{sid}')
        if rv.ok:
            data = rv.json().get('data', {})
            sw = (data.get(EXAM_TYPE) or {}).get(SUBJECT)
            if sw:
                print(f'Roll {chk}: CQ={sw["cq"]}, MCQ={sw["mcq"]}, Prac={sw["prac"]}')
            else:
                print(f'Roll {chk}: no data found')

if __name__ == '__main__':
    main()

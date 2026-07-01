"""
ICT (275) Annual Marks - Batch 2
Rolls 79-152 (Business), 201-235 (Humanities), 236-278 (Business continued)
Exam: Annual | Year: 2025-2026
"""
import requests

BASE      = 'http://localhost:5000'
SUBJECT   = '275'
EXAM_TYPE = 'Annual'
YEAR      = '2025-2026'

# All marks from the 4 mark-sheet images
# Format: roll -> (cq, mcq, prac, absent)
MARKS = {
    # ── Rolls 79–121 (Image 1) ──────────────────────────────────────────────
    '79':  (23,  9, 15, False),
    '80':  (22, 10, 15, False),
    '81':  (24, 12, 15, False),
    '82':  (17,  6, 10, False),
    '83':  (29,  8, 15, False),
    '84':  (28,  8, 15, False),
    '85':  (28, 12, 20, False),
    '86':  (21, 12, 15, False),
    '87':  (22,  9, 15, False),
    '88':  (17,  8, 15, False),
    '89':  (28, 12, 20, False),
    '90':  (24, 15, 21, False),
    '91':  (28, 10, 20, False),
    '92':  (27, 10, 20, False),
    '93':  (36, 10, 20, False),
    '94':  (21,  5, 10, False),
    '95':  (19,  8, 15, False),
    '96':  (22, 12, 16, False),
    '97':  (22, 13, 15, False),
    '98':  (26, 14, 20, False),
    '99':  (12, 15, 10, False),
    '100': (29, 12, 20, False),
    '101': (26, 13, 21, False),
    '102': (28,  8, 15, False),
    '103': (23,  8, 15, False),
    '104': (30, 10, 20, False),
    '105': (24, 11, 15, False),
    '106': (22, 11, 15, False),
    '107': (21,  9, 15, False),
    '108': (12, 11, 10, False),
    '109': (17,  9, 15, False),
    '110': (24,  9, 15, False),
    '111': (25,  8, 15, False),
    '112': (40, 11, 20, False),
    '113': ( 0,  0,  0, True ),  # AB
    '114': (24,  9, 15, False),
    '115': (30, 11, 20, False),
    '116': (32, 10, 20, False),
    '117': (31,  8, 21, False),
    '118': (25,  8, 15, False),
    '119': (28,  8, 15, False),
    '120': (29,  8, 15, False),
    '121': (26,  8, 16, False),

    # ── Rolls 122–151 (Image 2) – 152 is blank ─────────────────────────────
    '122': (27,  9, 15, False),
    '123': (25, 13, 20, False),
    '124': ( 0,  0,  0, True ),  # AB
    '125': (28, 10, 15, False),
    '126': (28,  8, 15, False),
    '127': (24, 11, 15, False),
    '128': (25, 11, 15, False),
    '129': (25,  6, 10, False),
    '130': (29, 10, 21, False),
    '131': (22,  9, 15, False),
    '132': (28, 10, 20, False),
    '133': ( 0,  0,  0, True ),  # AB
    '134': (29, 10, 21, False),
    '135': (26, 12, 20, False),
    '136': (33,  9, 20, False),
    '137': (28, 10, 20, False),
    '138': (29,  8, 15, False),
    '139': (24, 10, 16, False),
    '140': (20, 11, 15, False),
    '141': (13, 10, 10, False),
    '142': (38, 16, 20, False),
    '143': (29, 12, 20, False),
    '144': (29, 10, 21, False),
    '145': (27, 10, 15, False),
    '146': ( 0,  0,  0, True ),  # AB
    '147': (26, 12, 20, False),
    '148': (22,  9, 15, False),
    '149': (21, 11, 15, False),
    '150': (17, 12, 15, False),
    '151': (27, 11, 20, False),
    # 152: blank – skipped

    # ── Rolls 201–235 (Image 4 – Humanities/মানবিক) ────────────────────────
    '201': (26, 14, 20, False),
    '202': (22, 13, 15, False),
    '203': (25, 10, 15, False),
    '204': (33, 11, 20, False),
    '205': (31, 14, 20, False),
    '206': (24, 14, 20, False),
    '207': (22,  8, 15, False),
    '208': (24,  9, 17, False),
    '209': (20, 10, 15, False),
    '210': (22, 13, 15, False),
    '211': (38, 14, 20, False),
    '212': (23, 12, 15, False),
    '213': (24, 14, 20, False),
    '214': (23, 11, 16, False),
    '215': (24, 14, 20, False),
    '216': ( 0,  0,  0, True ),  # AB
    '217': ( 0,  0,  0, True ),  # AB
    '218': (21, 16, 15, False),
    '219': ( 0,  0,  0, True ),  # AB
    '220': (21, 12, 15, False),
    '221': (23, 13, 15, False),
    '222': (29, 15, 20, False),
    '223': (27, 14, 20, False),
    '224': (30, 14, 20, False),
    '225': (29, 14, 20, False),
    '226': (24, 12, 15, False),
    '227': (20, 11, 15, False),
    '228': ( 0,  0,  0, True ),  # AB
    '229': (27,  9, 15, False),
    '230': (19, 12, 15, False),
    '231': (17, 13, 15, False),
    '232': (24, 12, 15, False),
    '233': (25, 12, 15, False),
    '234': (21,  9, 15, False),
    '235': (24,  8, 15, False),

    # ── Rolls 236–278 (Image 3 – continuation) ─────────────────────────────
    '236': (26, 10, 15, False),
    '237': (20, 14, 16, False),
    '238': (17, 12, 15, False),
    '239': (25,  9, 16, False),
    '240': (26, 10, 15, False),
    '241': (31, 12, 20, False),
    '242': (19, 13, 15, False),
    '243': (27, 11, 20, False),
    '244': (17, 10, 15, False),
    '245': (10,  8, 10, False),
    '246': (10,  6, 10, False),
    '247': (17,  9, 15, False),
    '248': ( 9,  9, 10, False),
    '249': (15,  6, 10, False),
    '250': (12,  8, 10, False),
    '251': (20, 10, 15, False),
    '252': (17,  9, 15, False),
    '253': (20, 12, 15, False),
    '254': (22,  9, 15, False),
    '255': (19,  9, 15, False),
    '256': (18,  9, 15, False),
    '257': (17,  8, 15, False),
    '258': (12,  5, 20, False),
    '259': ( 9,  8, 10, False),
    '260': (22,  8, 15, False),
    '261': (17,  9, 15, False),
    '262': (22, 13, 15, False),
    '263': (11, 11, 10, False),
    '264': (23, 11, 16, False),
    '265': (18,  9, 15, False),
    '266': (25, 10, 15, False),
    '267': (12,  8, 10, False),
    '268': (18,  8, 15, False),
    '269': (21,  9, 15, False),
    '270': ( 9,  9, 10, False),
    '271': (23, 11, 16, False),
    '272': (20, 12, 15, False),
    '273': (20,  8, 15, False),
    '274': (17, 10, 15, False),
    '275': (25, 11, 15, False),
    '276': (18,  8, 15, False),
    '277': (17,  5, 10, False),
    '278': (11,  9, 10, False),
}


def main():
    sess = requests.Session()

    # 1. Login
    r = sess.post(BASE + '/api/login', json={'uid': 'admin', 'pw': '1234'})
    if not r.json().get('ok'):
        print('Login failed:', r.json()); return
    print('Login OK')

    # 2. Get all students
    r = sess.get(BASE + '/api/students')
    students = r.json().get('data', [])
    print(f'Fetched {len(students)} students')

    roll_to_id = {s['roll']: s['id'] for s in students}

    # 3. Build entries
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

    # 4. POST batch-subject
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

    # 5. Quick spot-check
    print('\n--- Spot check ---')
    for check_roll in ['79', '113', '201', '236', '278']:
        sid = roll_to_id.get(check_roll)
        if not sid:
            print(f'Roll {check_roll}: not in DB'); continue
        rv = sess.get(BASE + f'/api/marks/{sid}')
        if rv.ok:
            data = rv.json().get('data', {})
            ict  = (data.get(EXAM_TYPE) or {}).get(SUBJECT, None)
            if ict:
                tag = 'AB' if ict.get('absent') else f"CQ={ict['cq']}, MCQ={ict['mcq']}, Prac={ict['prac']}"
                print(f'Roll {check_roll}: {tag}')
            else:
                print(f'Roll {check_roll}: no ICT data found')


if __name__ == '__main__':
    main()

"""
ICT (Subject Code: 275) Annual Exam Marks Entry Script
Source: মইনউদ্দিন আদর্শ মহিলা কলেজ, সিলেট — বার্ষিক পরীক্ষা-২০২৬, একাদশ শ্রেণি
Columns: সৃজনশীল (CQ), বহুনির্বাচনী (MCQ), ব্যবহারিক (Practical)
Exam Type: Annual | Year/Session: 2025-2026
AB = অনুপস্থিত (Absent) — stored as cq=mcq=prac=0
"""

import sqlite3
from datetime import datetime

# ── Marks data from the mark sheet ────────────────────────────────────────────
# Format: roll → (cq, mcq, prac, absent)
MARKS_DATA = {
    '701': (13,  8, 10, False),
    '702': (28, 10, 20, False),
    '703': (21, 10, 15, False),
    '704': ( 9, 11, 10, False),
    '705': (28,  8, 15, False),
    '706': (32, 13, 20, False),
    '707': (21, 10, 15, False),
    '708': (12, 13, 10, False),
    '709': (13, 10, 10, False),
    '710': (14,  9, 10, False),
    '711': ( 7,  6, 10, False),
    '712': (20, 15, 15, False),
    '713': ( 0,  0,  0, True ),   # AB (Absent)
    '714': (14,  6, 10, False),
    '715': ( 8, 10, 10, False),
    '716': (17, 12, 15, False),
    '717': ( 0,  0,  0, True ),   # AB (Absent)
    '718': (17, 13, 15, False),
    '719': ( 6,  5, 10, False),
    '720': (36, 19, 21, False),
    '721': (17, 12, 15, False),
    '722': ( 7,  8, 10, False),
    '723': (13, 13, 10, False),
    '724': ( 8, 13, 10, False),
    '725': (10, 12, 10, False),
    '726': (17, 11, 15, False),
    '727': (17, 11, 15, False),
    '728': ( 0,  0,  0, True ),   # AB (Absent)
    '729': (17, 14, 15, False),
    '730': (21, 14, 15, False),
    '731': ( 0,  0,  0, True ),   # AB (Absent)
    # Roll 732 does not exist in the database — skipped
}

SUBJECT_CODE = '275'
EXAM_TYPE    = 'Annual'
YEAR         = '2025-2026'

def main():
    conn = sqlite3.connect('hsc_academy.db')
    cur  = conn.cursor()

    # Check actual columns in marks table
    cur.execute('PRAGMA table_info(marks)')
    cols = {row[1] for row in cur.fetchall()}
    has_absent = 'absent' in cols

    # Build roll → student_id map
    cur.execute('SELECT id, roll FROM students WHERE CAST(roll AS INTEGER) BETWEEN 701 AND 732')
    roll_to_id = {roll: sid for sid, roll in cur.fetchall()}

    from datetime import timezone
    now = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
    inserted = 0
    skipped  = []

    for roll, (cq, mcq, prac, absent) in MARKS_DATA.items():
        sid = roll_to_id.get(roll)
        if not sid:
            skipped.append(roll)
            continue

        # Delete any existing record for same student/exam/subject
        cur.execute(
            'DELETE FROM marks WHERE student_id=? AND exam_type=? AND subject_code=?',
            (sid, EXAM_TYPE, SUBJECT_CODE)
        )

        if has_absent:
            cur.execute(
                '''INSERT INTO marks
                   (student_id, exam_type, year, subject_code, cq, mcq, prac, absent,
                    selected_optional, created_at, updated_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (sid, EXAM_TYPE, YEAR, SUBJECT_CODE,
                 cq, mcq, prac, 1 if absent else 0,
                 '', now, now)
            )
        else:
            # absent column missing in DB — store absent students as 0 marks
            cur.execute(
                '''INSERT INTO marks
                   (student_id, exam_type, year, subject_code, cq, mcq, prac,
                    selected_optional, created_at, updated_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (sid, EXAM_TYPE, YEAR, SUBJECT_CODE,
                 cq, mcq, prac,
                 '', now, now)
            )

        inserted += 1
        status = 'ABSENT (AB)' if absent else f'CQ={cq}, MCQ={mcq}, Prac={prac}'
        print(f'  Roll {roll} → {status}')

    conn.commit()
    conn.close()

    print(f'\n✅ Inserted/updated {inserted} records.')
    if skipped:
        print(f'⚠️  Skipped (not in DB): {skipped}')

if __name__ == '__main__':
    main()

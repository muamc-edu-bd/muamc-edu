import sqlite3

conn = sqlite3.connect('hsc_academy.db')
c = conn.cursor()

c.execute("select roll, name, [group], optional_subjects from students where optional_subjects like '%178%' or optional_subjects like '%179%'")
rows = c.fetchall()
print(f"Students with Biology (178/179) optional subject: {len(rows)}")
for r in rows:
    print(r)

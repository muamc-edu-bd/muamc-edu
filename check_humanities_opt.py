import sqlite3

conn = sqlite3.connect('hsc_academy.db')
c = conn.cursor()

c.execute("select roll, name, [group], optional_subjects from students where [group] = 'Humanities' and optional_subjects != ''")
rows = c.fetchall()
print(f"Humanities students with optional subjects: {len(rows)}")
for r in rows:
    print(r)

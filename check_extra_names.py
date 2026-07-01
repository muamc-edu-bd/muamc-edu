import sqlite3

conn = sqlite3.connect('hsc_academy.db')
c = conn.cursor()

c.execute("select roll, name, [group], optional_subjects from students")
all_students = c.fetchall()

print("--- Searching for any name containing SAIDA, ANY, EMA, JANNAT, MARIA ---")
for roll, name, group, opt in all_students:
    lname = name.lower()
    if 'saida' in lname or 'any' in lname or 'ema' in lname or 'jannat' in lname or 'maria' in lname:
        print(f"roll={roll}, name={name}, group={group}, opt={opt}")

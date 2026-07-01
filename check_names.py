import sqlite3

conn = sqlite3.connect('hsc_academy.db')
c = conn.cursor()

# Get all students and print those matching parts of the names
c.execute("select roll, name, [group] from students")
all_students = c.fetchall()

targets = ["MARIA JANNAT", "FAHMIDA", "SAIDA JAHAN ANY", "JANNAT RAHMAN EMA"]
for target in targets:
    print(f"\n--- Search for target: {target} ---")
    parts = target.split()
    for roll, name, group in all_students:
        # Check if all parts of target are in name
        if all(part.lower() in name.lower() for part in parts):
            print(f"Match: roll={roll}, name={name}, group={group}")
        elif len(parts) > 1 and parts[-1].lower() in name.lower() and parts[0].lower() in name.lower():
            print(f"Partial Match: roll={roll}, name={name}, group={group}")

import sqlite3

conn = sqlite3.connect('hsc_academy.db')
c = conn.cursor()

c.execute("select roll, name, [group] from students")
all_stu = c.fetchall()

def search(words):
    print(f"\nSearch for: {words}")
    for roll, name, group in all_stu:
        name_lower = name.lower()
        if all(w.lower() in name_lower for w in words):
            print(f"  Exact Match: roll={roll}, name={name}, group={group}")
        elif any(w.lower() in name_lower for w in words):
            # Check how many words match
            matched = [w for w in words if w.lower() in name_lower]
            if len(matched) >= len(words) - 1 and len(words) > 1:
                print(f"  Partial Match ({matched}): roll={roll}, name={name}, group={group}")

search(["maria", "jannat"])
search(["nusrat", "jahan", "mim"])
search(["fahmida", "akter"])
search(["fahmida", "akther"])
search(["saida", "jahan", "any"])
search(["jannat", "rahman", "ema"])
search(["saida"])
search(["any"])
search(["ema"])

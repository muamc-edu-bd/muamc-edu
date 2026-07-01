import requests
sess = requests.Session()
sess.post('http://localhost:5000/api/login', json={'uid':'admin','pw':'1234'})
r2 = sess.get('http://localhost:5000/api/students')
students = r2.json()['data']
print('Total students:', len(students))
relevant = [s for s in students if s.get('roll','').isdigit() and 701 <= int(s['roll']) <= 732]
relevant.sort(key=lambda s: int(s['roll']))
for s in relevant:
    print(f"Roll {s['roll']}: id={s['id']}, group={s['group']}, cls={s['cls']}")

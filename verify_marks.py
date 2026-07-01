import requests

BASE = 'http://localhost:5000'
sess = requests.Session()
sess.post(BASE + '/api/login', json={'uid': 'admin', 'pw': '1234'})

ROLL_TO_ID = {
    '701': 'e6266e8ac6674431', '702': '75ec7be0f4aa4aca', '703': 'a96877c499ce48f7',
    '704': '3c31ee000b13492c', '705': '03cde60825ec4268', '706': 'fcf59c1a6ae14542',
    '707': '8f2a450404744e2d', '708': '2af7b48e24804f62', '709': '17041b2d381a4376',
    '710': 'b7177ca4e04a4680', '711': 'e2a13e7fb5a74982', '712': '6086dc226801422b',
    '713': '59e8eeb60319479e', '714': '45bceaa786314a2e', '715': '78d0ebf7ed1441d7',
    '716': 'b611091e79064afc', '717': '731030bc5235426b', '718': '8e59a2120e8e46f1',
    '719': 'cb10c4d5fbc34416', '720': '5a6c70c4f8e04480', '721': '3acf8e8ac6964282',
    '722': '585a1b57c9154b19', '723': '1b698eb5e57a45aa', '724': 'f412f3ae09864313',
    '725': 'f78a1c6cd6a64ce9', '726': '0f7ee5bdcd18478e', '727': 'a48e2d19f78d4808',
    '728': '0ffea2cba31049cf', '729': 'ff639f5ae18f48fe', '730': '6482acf0840c47c1',
    '731': '34fe24d4afea4ed0',
}

print(f"{'Roll':<5} | {'CQ':<4} | {'MCQ':<4} | {'Prac':<5} | {'Absent'}")
print("-" * 40)
for roll in sorted(ROLL_TO_ID.keys(), key=int):
    sid = ROLL_TO_ID[roll]
    r = sess.get(BASE + f'/api/marks/{sid}')
    if r.ok:
        data = r.json().get('data', {})
        ict = (data.get('Annual') or {}).get('275', None)
        if ict:
            ab = 'AB' if ict.get('absent') else ''
            print(f"{roll:<5} | {ict['cq']:<4} | {ict['mcq']:<4} | {ict['prac']:<5} | {ab}")
        else:
            print(f"{roll:<5} | NO ICT DATA")
    else:
        print(f"{roll:<5} | ERROR {r.status_code}")

import os, json

'''
hierarchy:
Team (abbr)
    week
        stats
'''

week_lookup = {
    "0906": 1, "0909": 1, "0910": 1,
    "0913": 2, "0916": 2, "0917": 2,
    "0920": 3, "0923": 3, "0924": 3,
    "0927": 4, "0930": 4, "1001": 4,
    "1004": 5, "1007": 5, "1008": 5,
    "1011": 6, "1014": 6, "1015": 6,
    "1018": 7, "1021": 7, "1022": 7,
    "1025": 8, "1028": 8, "1029": 8,
}


dir = './data/playbyplay'

for filename in os.listdir(dir):
    file = dir + "/" + filename

    wk_lkup = filename[4:8]
    week = week_lookup[wk_lkup]

    with open(file) as f:
        data = json.load(f)
        key = next(iter(data))
        print(data[key]['home'])

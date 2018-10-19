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

results = {}

for filename in os.listdir(dir):
    file = dir + "/" + filename

    wk_lkup = filename[4:8]
    week = str(week_lookup[wk_lkup])

    with open(file) as f:
        data = json.load(f)
        key = next(iter(data))

        home_team = data[key]['home']['abbr']
        home_stats = data[key]['home']['stats']
        if home_team not in results:
            results[home_team] = {}
        results[home_team][week] = home_stats

        away_team = data[key]['away']['abbr']
        away_stats = data[key]['away']['stats']
        if away_team not in results:
            results[away_team] = {}
        results[away_team][week] = away_stats

with open('./data/PlayerStatsByTeamWeek.json', 'w+') as fp:
    json.dump(results, fp)

print(results)
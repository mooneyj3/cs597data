import os, json

'''
author Jonny Mooneyham

hierarchy1:
Team (abbr)
    week
        stats

ideal hierarchy:
Team
    Player
        Name
        Week
            category
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

# source dir for data
dir = './data/playbyplay'

def simple_data_extraction ():
    # init empty array
    results = {}

    # iterate through all the data files
    for filename in os.listdir(dir):
        # set teh filename we want to open
        file = dir + "/" + filename

        # identify which week we are looking at
        wk_lkup = filename[4:8]
        week = str(week_lookup[wk_lkup])

        # open the file to process the data
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

'''
ideal hierarchy:
Team
    Player
        Name
        Week
            category
                stats
'''

def simple_to_ideal ():
    input_file = 'data/PlayerStatsByTeamWeek.json'

    results = {}

    with open(input_file) as fp:
        data = json.load(fp)

        # iterate through teams in json
        for team in data.keys():

            # add the team to the results
            results[team] = {}

            # iterate through each week
            for week in data[team]:
                for play_category in data[team][week]:

                    # skip play_category for "team"
                    if play_category == "team":
                        continue

                    # now iterate through each player
                    for player in data[team][week][play_category]:

                        # add player if they are not already there
                        if player not in results[team]:
                            results[team][player] = {}
                            results[team][player]['name'] = data[team][week][play_category][player]['name']

                        if week not in results[team][player]:
                            results[team][player][week] = {}

                        # results[team][player][week][play_category] = {}
                        results[team][player][week][play_category] = data[team][week][play_category][player]
                        del results[team][player][week][play_category]['name']


    for team in results:
        with open('./data/team_stats/' + team + '_team_stats_' + '.json', 'w+') as fp:
            dump_team = {team: results[team]}
            json.dump(dump_team, fp)
            print(results[team])

    # with open('./data/team_stats/ImprovedTeamStats.json', 'w+') as fp:
    #     json.dump(results, fp)
    #
    # with open('./data/team_stats/ImprovedTeamStats.json') as fp:
    #     data = json.load(fp)
    #     print(data)

    # print(results)

# simple_data_extraction ()
simple_to_ideal()
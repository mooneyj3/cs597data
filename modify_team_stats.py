import json
import csv

input_file = "data/team_stats/DET_team_stats_.json"
output_file = "data/team_stats/aa_testing.csv"

def find_categories ():
    categories = {}

    with open(input_file) as fp:
        data = json.load(fp)

    data = data[list(data.keys())[0]]

    for player in data.keys():
        for week in data[player].keys():
            data_player = data[player][week]
            if week == "name":
                continue
            for play_type in data_player.keys():
                data_week = data_player[play_type]

                if play_type not in categories:
                    categories[play_type] = []

                for subcat in data_week:
                    strVal = play_type + "-" + subcat
                    if strVal not in categories[play_type]:
                        categories[play_type].append(strVal)

    return categories, data


def convert_to_csv():
    cats, data = find_categories()

    # convert cats to array
    play_types = []
    for key in cats:
        play_types = play_types + cats[key]


    with open(output_file, 'w+', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar="|")

        # header row
        header_row = ["player-name", "week", "play-type"] + play_types
        writer.writerow(header_row)

        # now get the data
        arr_len = len(header_row)

        for player in data:
            curr_player = data[player]
            # player_name = currPlayer['name']
            for week in curr_player:
                if week == 'name' : continue

                # row_entry = [None] * arr_len
                # row_entry[0] = curr_player['name']
                # row_entry[1] = week

                curr_week = curr_player[week]

                for play_category in curr_week:

                    row_entry = [None] * arr_len
                    row_entry[0] = curr_player['name']
                    row_entry[1] = week
                    row_entry[2] = play_category

                    curr_play_category = curr_week[play_category]

                    for play_sub_category in curr_play_category:
                        play_stat = play_category + "-" + play_sub_category
                        num_stat = curr_play_category[play_sub_category]
                        stat_idx = header_row.index(play_stat)
                        row_entry[stat_idx] = num_stat

                    writer.writerow(row_entry)





















    # with open(output_file, 'w+') as f:
    #     w = csv.DictWriter(f, data.keys())
    #     w.writeheader()
    #     w.writerow(data)






convert_to_csv()


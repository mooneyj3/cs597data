
"""
This code fetches play-by-play json data
"""

# 2018100701/2018100701_gtd.json

# target:  http://www.nfl.com/liveupdate/game-center/2018100701/2018100701_gtd.json

# naive implementation
# focus on year: 2018
# increment months from 09 - 12
# increment days from 01 - 31
# increment

import urllib
import urllib.request
import urllib.error

game_center_base_url = 'http://www.nfl.com/liveupdate/game-center/'
suffix = '_gtd.json'

output_dir = '/home/mooneyj3/cs597_dv/repos/cs597data/data/playbyplay/'

year = "2018"
months = range(9, 10 + 1)
days = range(1, 31 + 1)

counter_max = 16

for m in months:
    month_str = str(m).zfill(2)

    for d in days:
        day_str = str(d).zfill(2)

        for i in range(counter_max):
            game_str = str(i).zfill(2)

            game_id = year + month_str + day_str + game_str

            file_name = game_id + suffix

            dest_file = output_dir + file_name

            web_address = game_center_base_url + game_id + "/" + game_id + suffix

            try:
                urllib.request.urlretrieve(web_address, dest_file)
            except urllib.error.HTTPError as e:
                break

            print(game_id)






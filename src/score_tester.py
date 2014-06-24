import sys
import os
import time
from datetime import date
from datetime import datetime
import urllib2
import json
import socket
import string


d = date.today()
today = d.timetuple()
year = today[0]
month = today[1]
day = today[2]

master_scoreboard_url = "http://mlb.mlb.com/gdcross/components/game/mlb/year_%s/month_%s/day_%s/master_scoreboard.json" % (year, str(month).zfill(2), day)
print master_scoreboard_url

response_scoreboard = urllib2.urlopen(master_scoreboard_url)
scoreboard_data = json.load(response_scoreboard) 
scoreboard_data = json.dumps(scoreboard_data, sort_keys=True, indent=4, separators=(',', ': ')) # pretty printed json file object data
loaded_schedule_json = json.loads(scoreboard_data)

schedule_list = loaded_schedule_json["data"]["games"]["game"]

pitcher = ""
pitcher_era = ""

for game in schedule_list:
    if game["away_team_name"] == "Giants":
        pitcher = "%s %s" % (game["away_probable_pitcher"]["first_name"], game["away_probable_pitcher"]["last_name"])
        pitcher_era = game["away_probable_pitcher"]["era"]
    else:
        pitcher = "%s %s" % (game["home_probable_pitcher"]["first_name"], game["home_probable_pitcher"]["last_name"])
        pitcher_era = game["home_probable_pitcher"]["era"]
# print loaded_schedule_json

print "%s with a %s ERA" % (pitcher, pitcher_era)
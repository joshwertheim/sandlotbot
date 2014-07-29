import sys
import os
import time
from datetime import date
from datetime import datetime
import urllib2
import json
import socket
import string

from pprint import pprint

starting_lineup_feed = ""
team_id = "137" # SF Giants current team ID - liable to change next season...
lineup = {}
players = list()

year = ""
month = ""
day = ""

# curl http://sanfrancisco.giants.mlb.com/gen/lineups/2014/07/22.json | python -mjson.tool > Downloads/lineups_team.json

home = True

def get_todays_date():
    global year
    global month
    global day

    d = date.today()
    today = d.timetuple()
    year = today[0]
    month = today[1]
    day = today[2]

def parse_lineup_feed():
    global starting_lineup_feed
    global team_id
    global lineup

    get_todays_date()
    starting_lineup_feed = "http://sanfrancisco.giants.mlb.com/gen/lineups/%s/%s/%s.json" % (year, str(month).zfill(2), str(day).zfill(2))

    response = urllib2.urlopen(starting_lineup_feed)
    lineup_data = json.load(response) 
    lineup_data = json.dumps(lineup_data, sort_keys=True, indent=4, separators=(',', ': ')) # pretty printed json file object data
    loaded_lineup_data = json.loads(lineup_data)

    lineups_dict  = loaded_lineup_data["list"]

    for entry in lineups_dict:
        # print "%s" % entry
        # print "%s" % entry["team_id"]
        if entry["team_id"] == team_id:
            lineup = entry
            break

    global players

    pos = 1
    
    for player in lineup["players"]:
        name_pos = "%d. %s (%s)" % (pos, player.get("last_name"), player.get("position"))
        players.append(name_pos)
        pos += 1


parse_lineup_feed()

players = ", ".join(players)

print players

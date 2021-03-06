# usage
# python sandlotbot

import sys
import os
import time
from datetime import date
import datetime
import urllib2
import json
import socket
import string

import threading

from feed import Feed
from irc import IRCClient, Bot
from player_stats import PlayerStatsParser

class NewsItem(object):
    """Creates a NewsItem instance with two properties"""
    blurb = ""
    article = ""

    def __init__(self, blurb, article):
        self.blurb = blurb
        self.article = article

class ScoreWatcher(object):
    """docstring for ScoreWatcher"""
    def __init__(self):
        self.running = True
        self.last_msg = ''

    def terminate(self):
        self.running = False

    def run(self):
        while self.running:
            self.get_current_score()
            time.sleep(5)

    def get_current_score(self):
        global client
        global current_game_status
        send = client.sock.send
        dest = IRCClient.INIT_CHANNEL

        get_scoreboard_info()
        if current_game_status != "" and self.last_msg != current_game_status and "Final" not in self.last_msg:    
            msg = current_game_status
            self.last_msg = msg
            client.send_message(dest, msg)

client = ""
user = ""

# Basic setup function for starting IRC and logging into bot account
def setup():
    global client
    global user

    client = IRCClient()
    user = Bot(client)
    user.identify()


starting_lineup_feed = ""
team_id = "137" # SF Giants current team ID - liable to change next season...
lineup = {}
players = list()

return_addr = ""
today_game = ""

year = ""
month = ""
day = ""

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

def get_tomorrows_date():
    global year
    global month
    global day

    d = date.today() + datetime.timedelta(days=1)
    today = d.timetuple()
    year = today[0]
    month = today[1]
    day = today[2]

def print_today():
    
    full_date = "%s/%s/%s/" % (year, str(month).zfill(2), str(day).zfill(2))

    # print "%d %d %d" % (today[0], today[1], today[2])

    global today_game

    schedule_url = "http://sanfrancisco.giants.mlb.com/gen/schedule/sf/%s_%s.json" % (year, month)

    feed = Feed(schedule_url)
    feed.load_and_prepare()
    succeeded, loaded_schedule_json = feed.get_representation

    response_schedule = urllib2.urlopen(schedule_url)
    schedule_data = json.load(response_schedule) 
    schedule_data = json.dumps(schedule_data, sort_keys=True, indent=4, separators=(',', ': ')) # pretty printed json file object data
    loaded_schedule_json = json.loads(schedule_data)

    start_time = ""

    for entry in loaded_schedule_json:
        try:
            if full_date in entry["game_id"]:
                versus = entry["away"]["full"] + " @ " + entry["home"]["full"]

                if entry["away"]["full"] == "Giants":
                    start_time = entry["away"]["start_time_local"]
                    home = False
                else:
                    start_time = entry["home"]["start_time_local"]

                start_time = start_time[11:]
                start_time = start_time[:5]
                t = time.strptime(start_time, "%H:%M")
                
                new_start_time = time.strftime("%I:%M %p", t)

                # print versus + " starting at " + new_start_time

                today_game = versus + " starting at " + new_start_time
        except:
            continue

giants_pitcher_name = ""
giants_pitcher_era = ""

end_game_message = ""

current_game_status = ""
current_game_inning = ""


def parse_lineup_feed():
    global starting_lineup_feed
    global team_id
    global lineup

    get_todays_date()
    starting_lineup_feed = "http://sanfrancisco.giants.mlb.com/gen/lineups/%s/%s/%s.json" % (year, str(month).zfill(2), str(day).zfill(2))

    feed = Feed(starting_lineup_feed)
    feed.load_and_prepare()
    succeeded, loaded_lineup_data = feed.get_representation

    global players

    if succeeded == False:
        players = None
        return

    lineups_dict  = loaded_lineup_data["list"]

    for entry in lineups_dict:
        # print "%s" % entry
        # print "%s" % entry["team_id"]
        if entry["team_id"] == team_id:
            lineup = entry
            break

    pos = 1

    if "players" in lineup:
        for player in lineup["players"]:
            name_pos = "%d. %s (%s)" % (pos, player.get("last_name"), player.get("position"))
            players.append(name_pos)
            pos += 1
        players = ", ".join(players)

    else:
        print "Players not found."
        players = None
        return

def get_scoreboard_info():
    global year
    global month
    global day

    global giants_pitcher_name
    global giants_pitcher_era

    global end_game_message

    global current_game_status
    global current_game_inning

    master_scoreboard_url = "http://mlb.mlb.com/gdcross/components/game/mlb/year_%s/month_%s/day_%s/master_scoreboard.json" % (year, str(month).zfill(2), str(day).zfill(2))

    feed = Feed(master_scoreboard_url)
    feed.load_and_prepare()
    succeeded, loaded_schedule_json = feed.get_representation
    
    schedule_list = loaded_schedule_json["data"]["games"]["game"]

    send = client.sock.send

    for game in schedule_list:
        try:
            if game["away_team_name"] == "Giants" or game["home_team_name"] == "Giants":
                current_game_status = game["alerts"]["brief_text"]
                # if "Middle 7th" in game["alerts"]["brief_text"]:
                #     msg = "PRIVMSG " + input[2] + " :" + "When the lights.. go down.. in the cityyy... https://www.youtube.com/watch?v=tNG62fULYgI" "\r\n"
                #     send(msg)  # https://www.youtube.com/watch?v=tNG62fULYgI
        except:
            if "winning_pitcher" in game and (game["home_team_name"] == "Giants" or game["away_team_name"] == "Giants"):
                winning_pitcher = "%s %s" % (game["winning_pitcher"]["first"], game["winning_pitcher"]["last"])
                losing_pitcher = "%s %s" % (game["losing_pitcher"]["first"], game["losing_pitcher"]["last"])
                end_game_message = "Game over. Winning pitcher: %s. Losing pitcher: %s." % (winning_pitcher, losing_pitcher)
                current_game_status = ""
            else:
                current_game_status = "No active game."

        if game["away_team_name"] == "Giants":
            if "away_probable_pitcher" in game:
                giants_pitcher_name = "%s %s" % (game["away_probable_pitcher"]["first"], game["away_probable_pitcher"]["last"])
                giants_pitcher_era = game["away_probable_pitcher"]["era"]
                return
            elif "opposing_pitcher" in game:
                giants_pitcher_name = "%s %s" % (game["opposing_pitcher"]["first"], game["opposing_pitcher"]["last"])
                giants_pitcher_era = game["opposing_pitcher"]["era"]
                return
        elif game["home_team_name"] == "Giants":
            if "home_probable_pitcher" in game:
                giants_pitcher_name = "%s %s" % (game["home_probable_pitcher"]["first"], game["home_probable_pitcher"]["last"])
                giants_pitcher_era = game["home_probable_pitcher"]["era"]
                return
            elif "pitcher" in game:
                giants_pitcher_name = "%s %s" % (game["pitcher"]["first"], game["pitcher"]["last"])
                giants_pitcher_era = game["pitcher"]["era"]
                return

current_score_message = ""

is_watching = False
sw = ScoreWatcher()
game_status_thread = threading.Thread(target=sw.run)

def cmd_parser(input):
    global client
    global return_addr
    global players
    global stories
    global is_watching

    # if ":spike021" not in input[0]:
    #     return
    
    destination = ""
    message = ""

    send = client.sock.send

    stats = PlayerStatsParser()

    try:
        destination = input[2]
    except:
        # print "no input[2]"
        destination = "None"

    ret = input[0]
    ret = ret[1:11]

    if "JOIN" in input[1] and ret == "sandlotbot":
        tmp = input[0].split('@', 1)
        return_addr = tmp[1] + " "
    elif "PING" in input[0]:
        msg = "PONG " + return_addr + input[1] + "\r\n"
        client.sock.send(msg)
        print msg
    elif ":@headlines" in input:
        if len(input) == 5 and "refresh" == input[4]:
            load_headlines()
            message =  "Headlines are refreshed."
            client.send_message(destination, message)
            return
        
        elif len(input) == 5 and "top5" == input[4]:
            for index in range(5):
                msg = "(%d) " % (index+1) + stories[index].blurb
                client.send_message(destination, msg)

        elif len(input) < 5:
            msg = "There are %d articles." % len(stories)
            client.send_message(destination, msg)
            return

        try: 
            index = int(input[4]) - 1
        except:
            print "Cannot convert input to int..."
            return

        if index < 0 or index+1 > len(stories):
            return
        
        msg = stories[index].blurb
        link = stories[index].article
        client.send_message(destination, msg)
        client.send_message(destination, link)
    elif ":@today" in input:
        get_todays_date()
        print_today()
        get_scoreboard_info()

        msg = today_game + " PST. " + "Starting pitcher: " + giants_pitcher_name + " with a %s ERA" % (giants_pitcher_era)
        client.send_message(destination, msg)
    elif ":@settopic" in input: # send("TOPIC " + input[2] + " :" + today_game + " PST. " + "Starting pitcher: " + giants_pitcher_name + " with a %s ERA" % (giants_pitcher_era) + "\r\n")
        get_todays_date()
        print_today()
        get_scoreboard_info()

        tomorrow = ""

        if giants_pitcher_name == "":
            get_tomorrows_date()
            print_today()
            get_scoreboard_info()
            tomorrow = " tomorrow"

        if len(input) > 5 and input[4] == "append":
            extra_str = input[5:]
            # msg = today_game + " PST. " + "Starting pitcher: " + giants_pitcher_name + " with a %s ERA." % (giants_pitcher_era) + " %s" % (" ".join(extra_str))
            send("TOPIC " + input[2] + " :" + today_game + " PST%s. " % (tomorrow) + "Starting pitcher: " + giants_pitcher_name + " with a %s ERA." % (giants_pitcher_era) + " %s" % (" ".join(extra_str)) + "\r\n")
            # client.send_message(destination, msg)
        else:
            send("TOPIC " + input[2] + " :" + today_game + " PST%s. " % (tomorrow) + "Starting pitcher: " + giants_pitcher_name + " with a %s ERA" % (giants_pitcher_era) + "\r\n")
    elif ":@status" in input:
        get_scoreboard_info()
        if current_game_status != "":    
            msg = current_game_status
        else:
            msg = end_game_message
        client.send_message(destination, msg)
    elif ":@lineup" in input:
        msg = ""
        parse_lineup_feed()
        if players == None:
            msg = "No lineup. Please check back later."
        else:
            msg = players
            players = list()
        client.send_message(destination, msg)
    elif ":@batter" in input:
        if len(input) < 5:
            msg = "No current data."
            client.send_message(destination, msg)
            return
        stats.parse_stats()
        results = stats.get_batter(input[4])
        for msg in results:    
            client.send_message(destination, msg)
    elif ":@pitcher" in input:
        if len(input) < 5:
            msg = "No current data."
            client.send_message(destination, msg)
            return
        stats.parse_stats()
        results = stats.get_pitcher(input[4])
        for msg in results:    
            client.send_message(destination, msg)
    elif ":@watch" in input:
        if is_watching is False:
            game_status_thread.start()
            is_watching = True
        else:
            sw.terminate()
            is_watching = False
    elif ":@commands" in input:
        msg = "@status (during game), @headlines, @headlines N (choose which story), @headlines top5 (get the top 5 articles' titles with their item numbers), @headlines refresh (manually update @headlines cache), @settopic to set the new topic for the next game (for now only the day of will fetch new info), @settopic append *string* resets topic and appends a given string, @lineup today's game's lineup for SF Giants."
        client.send_message(destination, msg)
    elif ":@src" in input:
        msg = "https://github.com/joshwertheim/sandlotbot - Feel free to send a pull-request!"
        client.send_message(destination, msg)
    elif ":@exit" in input:
        global active
        active = 0

global stories

def load_headlines():
    global headlines_url
    global response_headline
    global headlines_data
    global stories

    headlines_url = "http://sanfrancisco.giants.mlb.com/gen/sf/news/headlines.json"
    
    feed = Feed(headlines_url)
    feed.load_and_prepare()
    succeeded, loaded_headlines_json = feed.get_representation
    length = len(loaded_headlines_json["members"])

    story_elements = []
    story_blurbs = []
    story_url = []

    for index in range(length):
        story_elements.append(loaded_headlines_json["members"][index])

    length = len(story_elements)
    stories = []

    for index in range(length):
        try:
            item = NewsItem(story_elements[index]["althead"], story_elements[index]["url"])
            stories.append(item)
        except:
            print "No althead or url found at index %d; skipping to next item..." % index
            continue

def irc_connection():
    global active
    global readbuffer
    global client
    global return_addr

    send = client.sock.send
    first_time = True
    
    while active:
        readbuffer = readbuffer + client.sock.recv(1024)
        temp = string.split(readbuffer, "\n")
        readbuffer = temp.pop()

        for line in temp:
            line = string.rstrip(line)
            line = string.split(line)
            print line

            if first_time and len(line) > 7 and line[6] == "/NAMES":
                # send("PRIVMSG " + line[3] + " :" + "Hi everyone! My current commands are: @headlines, @headlines N (which article in the list you want), and @today to see the starting time for today's game! Let's win today!" + " \r\n")
                send("PRIVMSG " + line[3] + " :" + "Let's win today! [@commands to see available commands]" + " \r\n")
                first_time = False

            cmd_parser(line)

setup()
get_todays_date()
get_scoreboard_info()

active = 1
readbuffer = ""

headlines_url = ""
response_headline = ""
headlines_data = ""

load_headlines()
irc_connection()

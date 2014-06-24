# usage
# python mlbbot

import sys
import os
import time
from datetime import date
from datetime import datetime
import urllib2
import json
import socket
import string


class NewsItem(object):
    """Creates a NewsItem instance with two properties"""
    blurb = ""
    article = ""

    def __init__(self, blurb, article):
        self.blurb = blurb
        self.article = article

    def printElements(self):
        print self.blurb
        print self.article

class IRCClient(object):
    """Creates an IRCClient instance with basic server config and functions"""

    SERVER = "irc.freenode.net"
    sock = ""
    INIT_CHANNEL = "#sfgiants-test"

    def __init__(self):
        self.sock = socket.socket()
        self.sock.connect((self.SERVER, 6667))

class User(object):
    """Creates a User instance with basic user config and functions"""

    NICK = ""
    IDENT = ""
    REALNAME = ""
    PASS = ""

    def __init__(self, client):
        self.NICK = "sandlotbot"
        self.IDENT = "sandlotbot"
        self.REALNAME = "spike021's mlb bot"
        self.PASS = "b6XH5QmVQLP7rS6"

    def identify(self):
        client.sock.send("NICK %s\r\n" % self.NICK)
        client.sock.send("PASS %s\r\n" % self.PASS)
        client.sock.send("USER %s %s bla :%s\r\n" % (self.IDENT, client.SERVER, self.REALNAME))
        client.sock.send("JOIN %s\r\n" % client.INIT_CHANNEL)

client = ""
user = ""

def setup():
    global client
    global user

    client = IRCClient()
    user = User(client)
    user.identify()


return_addr = ""
today_game = ""

def print_today():
    d = date.today()
    today = d.timetuple()
    year = today[0]
    month = today[1]
    day = today[2]

    full_date = "%s/%s/%s/" % (year, str(month).zfill(2), str(day).zfill(2))

    # print "%d %d %d" % (today[0], today[1], today[2])

    global today_game

    schedule_url = "http://sanfrancisco.giants.mlb.com/gen/schedule/sf/%s_%s.json" % (year, month)
    response_schedule = urllib2.urlopen(schedule_url)
    data = json.load(response_schedule) 
    data = json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')) # pretty printed json file object data
    loaded_json = json.loads(data)

    start_time = ""

    for entry in loaded_json:
        try:
            if full_date in entry["game_id"]:
                versus = entry["away"]["full"] + " @ " + entry["home"]["full"]

                if entry["away"]["full"] == "Giants":
                    start_time = entry["away"]["start_time_local"]
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

def cmd_parser(input):
    global client
    global return_addr
    send = client.sock.send

    # if ":spike021" not in input[0]:
    #     return
    
    if "JOIN" in input[1]:
        tmp = input[0].split('@', 1)
        print "printing tmp %s" % tmp
        return_addr = tmp[1] + " "

    elif "PING" in input[0]:
        msg = "PONG " + return_addr + input[1] + "\r\n"
        send(msg)
        print msg
    elif ":@headlines" in input:
        print "this is the input: %s" % input
        if len(input) == 5 and "refresh" == input[4]:
            print "refreshing. . . ."
            load_headlines()
            return
        elif len(input) < 5:
            send("PRIVMSG " + input[2] + " :" + ("There are %d articles." % len(stories)) + " \r\n")
            return

        try: 
            index = int(input[4]) - 1
        except:
            print "Cannot convert input to int..."
            return

        if index < 0 or index+1 > len(stories): return
        
        msg = "PRIVMSG " + input[2] + " :" + stories[index].blurb + " \r\n"
        link = stories[index].article
        send(msg)
        send("PRIVMSG " + input[2] + " " + link + "\r\n")
    elif ":@today" in input:
        send("PRIVMSG " + input[2] + " :" + today_game + "\r\n")
    elif ":@settopic" in input:
        send("TOPIC " + input[2] + " :" + "Next game: " + today_game + "\r\n")
    elif ":@exit" in input:
        global active
        active = 0

def load_headlines():
    global headlines_url
    global response_headline
    global data

    headlines_url = "http://sanfrancisco.giants.mlb.com/gen/sf/news/headlines.json"
    response_headline = urllib2.urlopen(headlines_url)
    data = json.load(response_headline) 
    data = json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')) # pretty printed json file object data

setup()
print_today()

active = 1
readbuffer = ""

headlines_url = ""
response_headline = ""
data = ""

load_headlines()

loadedJSON = json.loads(data)
length = len(loadedJSON["members"])

story_elements = []
story_blurbs = []
story_url = []

for index in range(length):
    story_elements.append(loadedJSON["members"][index])

length = len(story_elements)

stories = []

for index in range(length):
    try:
        item = NewsItem(story_elements[index]["althead"], story_elements[index]["url"])
        stories.append(item)
    except:
        print "No althead or url found at index %d; skipping to next item..." % index
        continue

while active:
    readbuffer = readbuffer + client.sock.recv(1024)
    temp = string.split(readbuffer, "\n")
    readbuffer = temp.pop()

    for line in temp:
        line = string.rstrip(line)
        line = string.split(line)
        print line

        cmd_parser(line)
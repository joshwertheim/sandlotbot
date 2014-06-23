# usage
# python mlbbot

import sys
import os
import time
from datetime import date
import urllib2
import json
import socket
import string
import json

# d = date.today()
# today = d.timetuple()

class NewsItem(object):
    """docstring for NewsItem"""
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
        self.PASS = "shadow021"

    def identify(self):
        client.sock.send("NICK %s\r\n" % self.NICK)
        client.sock.send("USER %s %s bla :%s\r\n" % (self.IDENT, client.SERVER, self.REALNAME))
        client.sock.send("PASS %s\r\n" % self.PASS)
        client.sock.send("JOIN %s\r\n" % client.INIT_CHANNEL)

client = ""
user = ""

def setup():
    global client
    global user

    client = IRCClient()
    user = User(client)
    user.identify()

# FIX: Add this to pong: c-50-148-164-198.hsd1.ca.comcast.net

return_addr = "" # "c-50-148-164-198.hsd1.ca.comcast.net "

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
    elif ":@headline" in input:
        if len(input) < 5:
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
    elif ":@exit" in input:
        global active
        active = 0

setup()

active = 1
readbuffer = ""

headlinesUrl = "http://sanfrancisco.giants.mlb.com/gen/sf/news/headlines.json"
responseHeadline = urllib2.urlopen(headlinesUrl)
data = json.load(responseHeadline) 
data = json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')) # pretty printed json file object data

loadedJSON = json.loads(data)
length = len(loadedJSON["members"])

storyElements = []
storyBlurbs = []
storyUrls = []

for index in range(length):
    storyElements.append(loadedJSON["members"][index])

length = len(storyElements)

stories = []

for index in range(length):
    try:
        item = NewsItem(storyElements[index]["althead"], storyElements[index]["url"])
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

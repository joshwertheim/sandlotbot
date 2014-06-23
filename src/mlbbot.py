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

def cmd_parser(input):
    global client
    send = client.sock.send
    if ":spike021" not in input[0]:
        return
    if ":PING" in input[0]:
        send("PONG " + index[1] + "\r\n")
    if ":@latest" in input:
            msg = "PRIVMSG " + client.INIT_CHANNEL + " :" + stories[0].blurb + " \r\n"
            link = stories[0].article
            send(msg)
            send("PRIVMSG " + client.INIT_CHANNEL + " " + link + "\r\n")
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
        # print "No althead or url found at index %d; skipping to next item..." % index
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

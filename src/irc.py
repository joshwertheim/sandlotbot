# usage:
# currently meant to be run alongside sandlotbot

import socket
import ConfigParser

debug = False

class IRCClient(object):
    """Creates an IRCClient instance with basic server config and functions"""

    # sets default IRC server settings
    # to-do: *maybe* add support for multiple channels...
    SERVER = "irc.freenode.net"
    sock = ""
    if not debug:
        INIT_CHANNEL = "#sfgiants"
    else:
        INIT_CHANNEL = "#sfgiants-test"

    def __init__(self):
        self.sock = socket.socket()
        self.sock.connect((self.SERVER, 6667))

    # send_message()
    # requires two parameters: destination, message
    # both params expect strings
    # destination: usually input[2] in command parser function, AKA channel target
    # message: the message to be sent. can be simple or more complex
    def send_message(self, destination, message):
        msg = "PRIVMSG " + destination + " :" + message + "\r\n"
        self.sock.send(msg)

class Bot(object):
    """Creates a Bot instance with basic bot config and functions"""

    NICK = ""
    IDENT = ""
    REALNAME = ""
    PASS = ""
    irc_client = ""

    def __init__(self, client):
        config = ConfigParser.RawConfigParser()
        config.read("../resources/prefs.txt")

        self.NICK = config.get('CREDENTIALS', 'NICK')
        self.IDENT = config.get('CREDENTIALS', 'IDENT')
        self.REALNAME = config.get('CREDENTIALS', 'REALNAME')
        self.PASS = config.get('CREDENTIALS', 'PASS')
        self.irc_client = client
        print "nick: %s\nident: %s\nrealname: %s\npass: %s\n" % (self.NICK, self.IDENT, self.REALNAME, self.PASS)

    def identify(self):
        self.irc_client.sock.send("NICK %s\r\n" % self.NICK)
        self.irc_client.sock.send("PASS %s\r\n" % self.PASS)
        self.irc_client.sock.send("USER %s %s bla :%s\r\n" % (self.IDENT, self.irc_client.SERVER, self.REALNAME))
        self.irc_client.sock.send("JOIN %s\r\n" % self.irc_client.INIT_CHANNEL)

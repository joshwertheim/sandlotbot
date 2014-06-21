# usage
# python mlbbot

import sys
import os
import time
from datetime import date
import urllib2
import json

# d = date.today()
# today = d.timetuple()

headlinesUrl = "http://sanfrancisco.giants.mlb.com/gen/sf/news/headlines.json"

responseHeadline = urllib2.urlopen(headlinesUrl)
data = json.load(responseHeadline) 
data = json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')) # pretty printed json file object data

# print data

loadedJSON = json.loads(data)
length = len(loadedJSON["members"])

storyElements = []
storyBlurbs = []

for index in range(length):
    storyElements.append(loadedJSON["members"][index])
    # if "text" in loadedJSON["response"][index]:
    #     # print loadedJSON["response"][index]["text"]
    #     listOfQuotes.append(loadedJSON["response"][index]["text"])
    # elif "body" in loadedJSON["response"][index]:
    #     # print loadedJSON["response"][index]["body"]
    #     listOfQuotes.append(loadedJSON["response"][index]["body"])

for index in range(length):
    storyBlurbs.append(storyElements[index]["althead"])
    print storyBlurbs[index]
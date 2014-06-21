# usage
# python mlbbot

import sys
import os
import time
import urllib2
import json

input_tag = raw_input("Enter a tag... ")
print("Tag entered: " + input_tag)

tag = input_tag #"quote"
api_key = "YDwTx7EpF5KH2ffxeMpE70GQQk4JLsIsrCQkURMQ5u9hrJJniY"

response = urllib2.urlopen("http://api.tumblr.com/v2/tagged?tag=" + tag + "&api_key=" + api_key)
data = json.load(response) 
data = json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')) # pretty printed json file object data

with open('data.json', 'w') as outfile: # save json response file object to data.json
    outfile.write(data)
response.close()

# print data

loadedJSON = json.loads(data)
length = len(loadedJSON["response"])

listOfQuotes = []
allTags = []

for index in range(length):
    allTags.append(loadedJSON["response"][index]["tags"])
    if "text" in loadedJSON["response"][index]:
        # print loadedJSON["response"][index]["text"]
        listOfQuotes.append(loadedJSON["response"][index]["text"])
    elif "body" in loadedJSON["response"][index]:
        # print loadedJSON["response"][index]["body"]
        listOfQuotes.append(loadedJSON["response"][index]["body"])

os.system('cls' if os.name=='nt' else 'clear')

for quote in range(len(listOfQuotes)):
    print listOfQuotes[quote] + "\n"
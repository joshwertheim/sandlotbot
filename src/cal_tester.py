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

full_date = "%s/%s/%s/" % (year, str(month).zfill(2), str(day).zfill(2))
print full_date

# print "%d %d %d" % (today[0], today[1], today[2])

schedule_url = "http://sanfrancisco.giants.mlb.com/gen/schedule/sf/%s_%s.json" % (year, month)
print schedule_url

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

            print versus + " starting at " + new_start_time
    except:
        continue
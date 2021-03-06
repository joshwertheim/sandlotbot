sandlotbot 
==========

IRC bot for retrieving information specific to the San Francisco Giants (for now). This bot is a work in progress. Needs lots of refactoring. More features to come.

Feel free to submit a pull-request! There's much to be done and added.

Currently uses a set of three different JSON feeds provided by the Major League Baseball website. Keep in mind that these could change at any time and break the bot's parser.

To run:

1. Clone this repository to a destination of your choosing
2. Set your command-line terminal to the repo
3. You'll need to create some config.txt type of file (info below) and set up the config parser's path so it knows where it's located
4. Run "python sandlotbot.py"

Example config.txt:
```
[CREDENTIALS]
NICK = sandlotbot
IDENT = sandlotbot
REALNAME = sandlotbot
PASS = xxxxxxxxxxxx
```

Working commands:

* @headlines - prints number of news articles; tends to stay the same (roughly 12)
* @headlines N - prints the title and link to the Nth article
* @headlines top5 - prints the title and link to the top 5 articles
* @headlines refresh - Resets the headlines cache
* @settopic - sets the new topic for the day's game
* @settopic append *str* - will set the topic for the day's game *and* add the string that follows *append*
* @status - prints the status of the current game (not always up-to-date because json isn't constantly updated on mlb.com)
* @lineup - prints the current/upcoming game's lineup (only works the day of)
* @batter *first name* or *last name* - prints some good batting stats for given SF player (includes pitchers' batting stats)
* @pitcher *first name* or *last name* - prints relevant pitcher stats, can be expanded
* @exit - bot closes up shop and disconnects from the default server (freenode in this case)

Obviously there's a bit of overlap here. Hoping to consolidate these in the near future if possible. Suggestions are welcome!

NOTE from MLB website about using their data:

> The accounts, descriptions, data and presentation in the referring page (the "Materials") are proprietary content of MLB Advanced Media, L.P ("MLBAM").  
Only individual, non-commercial, non-bulk use of the Materials is permitted and any other use of the Materials is prohibited without prior written authorization from MLBAM.  
Authorized users of the Materials are prohibited from using the Materials in any commercial manner other than as expressly authorized by MLBAM.

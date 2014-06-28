sandlotbot
==========

IRC bot for retrieving information specific to the San Francisco Giants (for now). This bot is a work in progress. Needs lots of refactoring. More features to come.

Feel free to submit a pull-request!

Currently uses a set of three different JSON feeds provided by the Major League Baseball website. Keep in mind that these could change at any time and break the bot's parser.

To run: simply clone this repository to a destination of your choosing. Set your command-line terminal to the repo, and then just run "python sandlotbot.py"

Working commands:

* @headlines - prints number of news articles; tends to stay the same (roughly 12)
* @headlines N - prints the title and link to the Nth article
* @headlines top5 - prints the title and link to the top 5 articles
* @headlines refresh - Resets the headlines cache
* @settopic - sets the new topic for the day's game
* @settopic append *str* - will set the topic for the day's game *and* add the string that follows *append*
* @status - prints the status of the current game (not always up-to-date because json isn't constantly updated on mlb.com)
* @exit - bot closes up shop and disconnects from the default server (freenode in this case)

Obviously there's a bit of overlap here. Hoping to consolidate these in the near future if possible. Suggestions are welcome!

NOTE from MLB website about using their data:

> The accounts, descriptions, data and presentation in the referring page (the "Materials") are proprietary content of MLB Advanced Media, L.P ("MLBAM").  
Only individual, non-commercial, non-bulk use of the Materials is permitted and any other use of the Materials is prohibited without prior written authorization from MLBAM.  
Authorized users of the Materials are prohibited from using the Materials in any commercial manner other than as expressly authorized by MLBAM.

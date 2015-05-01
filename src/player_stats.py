from datetime import date
import urllib2

import xml.etree.ElementTree as ET

class Batter(object):
    """Creates a Batter object with relevant properties"""
    def __init__(self, first_name, last_name, avg, slg, hr, rbi, so, ops, obp):
        self.first_name = first_name
        self.last_name = last_name
        self.avg = avg
        self.slg = slg
        self.hr = hr
        self.rbi = rbi
        self.so = so
        self.ops = ops
        self.obp = obp

class Pitcher(object):
    """Creates a Pitcher object with relevant properties"""
    def __init__(self, first_name, last_name, era, whip, ip, bb, so, hr):
        self.first_name = first_name
        self.last_name = last_name
        self.era = era
        self.whip = whip
        self.ip = ip
        self.bb = bb
        self.so = so
        self.hr = hr
        
class PlayerStatsParser(object):
    """Creates a PlayerStatsParser object capable of parsing XML at the given URL containing player stats"""
    
    batter_list = list()
    pitcher_list = list()

    # downloads and parses the default URL into a tree using ElementTree
    # sorts stats into either a batter list or pitcher list
    def parse_stats(self):
        d = date.today()
        today = d.timetuple()
        year = today[0]

        url = "http://giants.mlb.com/gdcross/components/team/stats/year_%s/137-stats.xml" % (year)
        request = urllib2.Request(url, headers={"Accept" : "application/xml"})

        data = urllib2.urlopen(request)

        tree = ET.parse(data)
        root = tree.getroot()
        batter_list_xml = root[0]
        pitcher_list_xml = root[1]


        for batter_node in batter_list_xml:
            node_player_name = batter_node.get('NAME_DISPLAY_FIRST_LAST').split(" ")
            node_first_name = node_player_name[0]
            node_last_name = node_player_name[1]
            node_avg = batter_node.get('AVG')
            node_slg = batter_node.get('SLG')
            node_hr = batter_node.get('HR')
            node_rbi = batter_node.get('RBI')
            node_so = batter_node.get('SO')
            node_ops = batter_node.get('OPS')
            node_obp = batter_node.get('OBP')
            batter = Batter(node_first_name, node_last_name, node_avg, node_slg, node_hr, node_rbi, node_so, node_ops, node_obp)
            self.batter_list.append(batter)

        for pitcher_node in pitcher_list_xml:
            node_player_name = pitcher_node.get('NAME_DISPLAY_FIRST_LAST').split(" ")
            node_first_name = node_player_name[0]
            node_last_name = node_player_name[1]
            node_era = pitcher_node.get('ERA')
            node_whip = pitcher_node.get('WHIP')
            node_ip = pitcher_node.get('IP')
            node_bb = pitcher_node.get('BB')
            node_so = pitcher_node.get('SO')
            node_hr = pitcher_node.get('HR')
            pitcher = Pitcher(node_first_name, node_last_name, node_era, node_whip, node_ip, node_bb, node_so, node_hr)
            self.pitcher_list.append(pitcher)

    # gets the batter with the param 'name'
    # capable of retrieving multiple batters with same name
    # for instance '@batter brandon' will return both Crawford and Belt
    def get_batter(self, name):
        results = list()
        for player in self.batter_list:
            msg = ""
            if name.lower() in player.last_name.lower() or name.lower() in player.first_name.lower():
                msg = "%s %s - AVG: %s, SLG: %s, HR: %s, RBI: %s, SO: %s, OPS: %s, OBP: %s" % (player.first_name, player.last_name, player.avg, player.slg, player.hr, player.rbi, player.so, player.ops, player.obp)
                if msg not in results:
                    results.append(msg)
        if results:
            return results
        else:
            results.append("No stats found.")
            return results

    # gets the pitcher with the param 'name'
    # capable of retrieving multiple pitcher with same name if necessary
    def get_pitcher(self, name):
        results = list()
        for player in self.pitcher_list:
            msg = ""
            if name.lower() in player.last_name.lower() or name.lower() in player.first_name.lower():
                msg = "%s %s - ERA: %s, WHIP: %s, IP: %s, BB: %s, SO: %s, HR: %s" % (player.first_name, player.last_name, player.era, player.whip, player.ip, player.bb, player.so, player.hr)
                if msg not in results:
                    results.append(msg)
        if results:
            return results
        else:
            results.append("No stats found.")
            return results

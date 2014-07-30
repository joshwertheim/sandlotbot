import urllib2
import xml.etree.ElementTree as ET

class Batter(object):
    """docstring for Batter"""
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
    """docstring for Pitcher"""
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
    """docstring for PlayerStatsParser"""
    
    batter_list = list()
    pitcher_list = list()

    def parse_stats(self):
        url = "http://giants.mlb.com/gdcross/components/team/stats/year_2014/137-stats.xml"
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

    def get_batter(self, name):
        for player in self.batter_list:
            if name in player.last_name or name in player.first_name:
                msg = "%s %s - AVG: %s, SLG: %s, HR: %s, RBI: %s, SO: %s, OPS: %s, OBP: %s" % (player.first_name, player.last_name, player.avg, player.slg, player.hr, player.rbi, player.so, player.ops, player.obp)
                return msg
        return "No stats found."

    def get_pitcher(self, name):
        for player in self.pitcher_list:
            if name in player.last_name or name in player.first_name:
                msg = "%s %s - ERA: %s, WHIP: %s, IP: %s, BB: %s, SO: %s, HR: %s" % (player.first_name, player.last_name, player.era, player.whip, player.ip, player.bb, player.so, player.hr)
                return msg
        return "No stats found."

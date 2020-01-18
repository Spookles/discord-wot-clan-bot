import requests
import json
from player import Player
from tank import Tank

class Clan:
    #var
    #General information
    id = 0
    name = ""
    tag = ""
    emblem_url = ""
    color = ""
    created_at = ""
    created_by = ""
    activity = ""
    commander = ""
    description = ""
    members_count = 0
    playersCount = 0
    players = []
    tanks = []
    motto = ""
    updated_at = ""
    #Stronghold statistics
    skirmish = {
        'fb_6': {'value': '', 'rank': '', 'rank_delta': ''},
        'fb_8': {'value': '', 'rank': '', 'rank_delta': ''},
        'fb_10': {'value': '', 'rank': '', 'rank_delta': ''}
    }
    sm_6_str = ""
    sm_8_str = ""
    sm_10_str = ""
    global_map = {
        'gm_6': {'value': '', 'rank': '', 'rank_delta': ''},
        'gm_8': {'value': '', 'rank': '', 'rank_delta': ''},
        'gm_10': {'value': '', 'rank': '', 'rank_delta': ''}
    }
    gm_6_str = ""
    gm_8_str = ""
    gm_10_str = ""

    #functions
    def getDetails(self, id):
        api_url = "https://api.worldoftanks.eu/wot/clans/info/?application_id=0ecfda2435a084d16fa9e02ea75ee0db&clan_id=%s" % (id)
        response = requests.get(api_url)
        json = response.json()['data'][str(id)]
        self.color = json['color']
        self.created_at = json['created_at']
        self.description = json['description']
        self.members_count = json['members_count']
        self.motto = json['motto']
        self.updated_at = json['updated_at']
        self.created_by = json['creator_name']
        self.commander = json['leader_name']

    def getRating(self, id):
        api_url = "https://api.worldoftanks.eu/wot/clanratings/clans/?application_id=0ecfda2435a084d16fa9e02ea75ee0db&clan_id=%s" % (id)
        response = requests.get(api_url)
        json = response.json()['data'][str(id)]
        self.skirmish['fb_6'] = json['fb_elo_rating_6']
        self.skirmish['fb_8'] = json['fb_elo_rating_8']
        self.skirmish['fb_10'] = json['fb_elo_rating_10']
        self.global_map['gm_6'] = json['gm_elo_rating_6']
        self.global_map['gm_8'] = json['gm_elo_rating_8']
        self.global_map['gm_10'] = json['gm_elo_rating_10']

        self.sm_6_str = "Rating: **" + str(self.skirmish['fb_6']['value']) + "**\nRank: **" + str(self.skirmish['fb_6']['rank']) + "**\nRank Change: **" + str(self.skirmish['fb_6']['rank_delta']) + "**"
        self.sm_8_str = "Rating: **" + str(self.skirmish['fb_8']['value']) + "**\nRank: **" + str(self.skirmish['fb_8']['rank']) + "**\nRank Change: **" + str(self.skirmish['fb_8']['rank_delta']) + "**"
        self.sm_10_str = "Rating: **" + str(self.skirmish['fb_10']['value']) + "**\nRank: **" + str(self.skirmish['fb_10']['rank']) + "**\nRank Change: **" + str(self.skirmish['fb_10']['rank_delta']) + "**"
        self.gm_6_str = "Rating: **" + str(self.global_map['gm_6']['value']) + "**\nRank: **" + str(self.global_map['gm_6']['rank']) + "**\nRank Change: **" + str(self.global_map['gm_6']['rank_delta']) + "**"
        self.gm_8_str = "Rating: **" + str(self.global_map['gm_8']['value']) + "**\nRank: **" + str(self.global_map['gm_8']['rank']) + "**\nRank Change: **" + str(self.global_map['gm_8']['rank_delta']) + "**"
        self.gm_10_str = "Rating: **" + str(self.global_map['gm_10']['value']) + "**\nRank: **" + str(self.global_map['gm_10']['rank']) + "**\nRank Change: **" + str(self.global_map['gm_10']['rank_delta']) + "**"

    def getPlayers(self):
        #all players in clan, with name & id & player count
        api_url = "https://api.worldoftanks.eu/wot/clans/info/?application_id=1119ac87433be4957549e3f3e83e18d4&clan_id={}&fields=members_count%2C+members.account_id%2C+members.account_name".format(self.id)
        response = requests.get(api_url)
        jsonResponse = response.json()['data'][str(self.id)]

        self.playersCount = jsonResponse['members_count']
        self.players = [0] * self.playersCount

        loopCount = 0
        for member in jsonResponse['members']:
            self.players[loopCount] = Player(member['account_id'], member['account_name'], self.tanks)
            loopCount+=1
    
    def getTankNames(self):
        #https://api.worldoftanks.eu/wot/encyclopedia/vehicles/?application_id=1119ac87433be4957549e3f3e83e18d4&fields=name%2C+tank_id&tier=5%2C6%2C7%2C8%2C9%2C10&page_no=1
        for x in range (1, 6):
            api_url = "https://api.worldoftanks.eu/wot/encyclopedia/vehicles/?application_id=1119ac87433be4957549e3f3e83e18d4&fields=name%2C+tank_id&tier=5%2C6%2C7%2C8%2C9%2C10&page_no={}".format(x)
            response = requests.get(api_url)
            jsonResponse = response.json()['data']
            if x == 1:
                self.tanks = [0] * response.json()['meta']['total']

            for index, item in enumerate(jsonResponse):
                if x == 1:
                    self.tanks[index] = Tank(jsonResponse[item]['tank_id'], jsonResponse[item]['name'])
                else:
                    self.tanks[index + ((x*100)-100)] = Tank(jsonResponse[item]['tank_id'], jsonResponse[item]['name'])


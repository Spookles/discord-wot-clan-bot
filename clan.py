import requests
import json

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


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
    global_map = {
        'gm_6': {'value': '', 'rank': '', 'rank_delta': ''},
        'gm_8': {'value': '', 'rank': '', 'rank_delta': ''},
        'gm_10': {'value': '', 'rank': '', 'rank_delta': ''}
    }

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


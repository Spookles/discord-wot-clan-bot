import requests
import json
from player import Player
from tank import Tank
import discord
import asyncio
import aiohttp

class Clan:
    def __init__(self, _id, _name, _tag, _emblem_url):
        self.id = _id
        self.name = _name
        self.tag = _tag
        self.emblem_url = _emblem_url
        self.send_time = "20:00"
        self.clanIsSet = False
        self.color = ""
        self.created_at = ""
        self.created_by = ""
        self.activity = ""
        self.commander = ""
        self.description = ""
        self.members_count = 0
        self.playersCount = 0
        self.players = []
        self.tanks = []
        self.motto = ""
        self.updated_at = ""
        #Stronghold statistics
        self.skirmish = {
            'fb_6': {'value': '', 'rank': '', 'rank_delta': ''},
            'fb_8': {'value': '', 'rank': '', 'rank_delta': ''},
            'fb_10': {'value': '', 'rank': '', 'rank_delta': ''}
        }
        self.sm_6_str = ""
        self.sm_8_str = ""
        self.sm_10_str = ""
        self.global_map = {
            'gm_6': {'value': '', 'rank': '', 'rank_delta': ''},
            'gm_8': {'value': '', 'rank': '', 'rank_delta': ''},
            'gm_10': {'value': '', 'rank': '', 'rank_delta': ''}
        }
        self.gm_6_str = ""
        self.gm_8_str = ""
        self.gm_10_str = ""

    #functions
    async def getDetails(self, id):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.worldoftanks.eu/wot/clans/info/?application_id=0ecfda2435a084d16fa9e02ea75ee0db&clan_id={}'.format(id)) as r:
                json = (await r.json())['data'][str(id)]
                self.color = json['color']
                self.created_at = json['created_at']
                self.description = json['description']
                self.members_count = json['members_count']
                self.motto = json['motto']
                self.updated_at = json['updated_at']
                self.created_by = json['creator_name']
                self.commander = json['leader_name']

    async def getRating(self, id):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.worldoftanks.eu/wot/clanratings/clans/?application_id=0ecfda2435a084d16fa9e02ea75ee0db&clan_id={}'.format(id)) as r:
                json = (await r.json())['data'][str(id)]
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

    async def getPlayers(self):
        #all players in clan, with name & id & player count
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.worldoftanks.eu/wot/clans/info/?application_id=1119ac87433be4957549e3f3e83e18d4&clan_id={}&fields=members_count%2C+members.account_id%2C+members.account_name'.format(self.id)) as r:
                jsonResponse = (await r.json())['data'][str(self.id)]
                self.playersCount = jsonResponse['members_count']
                self.players = [0] * self.playersCount
                loopCount = 0
                for member in jsonResponse['members']:
                    self.players[loopCount] = Player(member['account_id'], member['account_name'], self.tanks)
                    await self.players[loopCount].retrieveTanks()
                    print("Retrieved all tanks for {} from clan {}.".format(self.players[loopCount].name, self.tag))
                    loopCount+=1
    
    async def getTankNames(self):
        #https://api.worldoftanks.eu/wot/encyclopedia/vehicles/?application_id=1119ac87433be4957549e3f3e83e18d4&fields=name%2C+tank_id&tier=5%2C6%2C7%2C8%2C9%2C10&page_no=1
        for x in range (1, 6):
            async with aiohttp.ClientSession() as session:
                async with session.get('https://api.worldoftanks.eu/wot/encyclopedia/vehicles/?application_id=1119ac87433be4957549e3f3e83e18d4&fields=name%2C+tank_id&tier=5%2C6%2C7%2C8%2C9%2C10&page_no={}'.format(x)) as r:
                    jsonResponse = (await r.json())['data']
                    if x == 1:
                        self.tanks = [0] * (await r.json())['meta']['total']

                    for index, item in enumerate(jsonResponse):
                        if x == 1:
                            self.tanks[index] = Tank(jsonResponse[item]['tank_id'], jsonResponse[item]['name'])
                        else:
                            self.tanks[index + ((x*100)-100)] = Tank(jsonResponse[item]['tank_id'], jsonResponse[item]['name'])


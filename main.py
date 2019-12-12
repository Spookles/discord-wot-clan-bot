import requests
import json
from clan import Clan

clan = Clan()

def retrieveClan(tag):
    api_url = "https://api.worldoftanks.eu/wot/clans/list/?application_id=0ecfda2435a084d16fa9e02ea75ee0db&search=%s" % (tag)
    response = requests.get(api_url)
    json = response.json()['data'][0]
    clan.id = json['clan_id']
    clan.name = json['name']
    clan.tag = json['tag']
    clan.emblem_url = json['emblems']['x256']['wowp']
    print(clan.tag)

retrieveClan('TNKCS')
import os
from dotenv import load_dotenv
import requests
import json
from clan import Clan
import discord
from discord.ext import tasks, commands
import datetime
import asyncio
import aiohttp
import re

class GlobalFunc():
    """Functions that get used by multiple classes and cogs."""

    @staticmethod
    async def getClan(tag):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.worldoftanks.eu/wot/clans/list/?application_id=0ecfda2435a084d16fa9e02ea75ee0db&search={}'.format(tag)) as r:
                if((await r.json())['status'] == "ok" and
                (await r.json())['meta']['count'] >= 1):
                    json = (await r.json())['data'][0]
                    clan = Clan(json['clan_id'], json['name'], json['tag'], json['emblems']['x195']['portal'])
                    await clan.getDetails(clan.id)
                    await clan.getRating(clan.id)
                    return clan
                else:
                    return False

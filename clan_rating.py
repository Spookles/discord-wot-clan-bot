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
from global_func import GlobalFunc

class ClanRating(commands.Cog):
    """This category contains commands that do things with the rating of clans."""
    def __init__(self, _bot, _clanDict):
        self.bot = _bot
        self.clanDict = _clanDict

    @commands.command(brief="Searches and shows basic clan information", description="By giving it an existing clan tag it will look up basic information about the clan. It will show its owner, description, name, and various other info.")
    async def find(self, ctx, clanTag):
        clan = await GlobalFunc.getClan(clanTag)
        if clan:
            embed = await GlobalFunc.embedBuilder(clan, "clan", -1)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Invalid clan tag.")

    @commands.command(brief="Shows the stronghold and global map ratings of a clan", description="Searches a clan by tag and returns stronghold data.")
    async def rating(self, ctx, clanTag):
        clan = await GlobalFunc.getClan(clanTag)
        if clan:
            embed = await GlobalFunc.embedBuilder(clan, "sh&gm", -1)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Invalid clan tag.")
            
    @commands.command(aliases=['sh'], brief="Minimalised version of rating, but for skirmish", description="By using the skirmish command you can retrieve the skirmish rating of a specific clan for a specific tier.\nIt can be called as 'skirmish' or a shorter version 'sh'\nTier 6 : 6/t6/T6\nTier 8 : 8/t8/T8\nTier 10: 10/t10/T10")
    async def skirmish(self, ctx, clanTag, tier):
        clan = await GlobalFunc.getClan(clanTag)
        if clan:
            embed = await GlobalFunc.embedBuilder(clan, "sh", tier)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Invalid clan tag.")

    @commands.command(aliases=['gm'], brief="Minimalised version of rating, but for the global map", description="By using the globalmap command you can retrieve the global map rating of a specific clan for a specific tier.\nIt can be called as 'globalmap' or a shorter version 'gm'\nTier 6 : 6/t6/T6\nTier 8 : 8/t8/T8\nTier 10: 10/t10/T10")
    async def globalmap(self, ctx, clanTag, tier):
        clan = await GlobalFunc.getClan(clanTag)
        if clan:
            embed = await GlobalFunc.embedBuilder(clan, "gm", tier)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Invalid clan tag.")

    @commands.command(brief="", description="")
    async def addMetaTank(self, ctx, tankName):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.worldoftanks.eu/wot/clans/list/?application_id=0ecfda2435a084d16fa9e02ea75ee0db&search={}'.format(tag)) as r:
                if ((await r.json())['status'] == "ok" and
                (await r.json())['meta']['count'] >= 1):
                    json = (await r.json())['data'][0]
                    clan = Clan(json['clan_id'], json['name'], json['tag'], json['emblems']['x195']['portal'])
                    await clan.getDetails(clan.id)
                    await clan.getRating(clan.id)
                    return clan
                else:
                    return False
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

class ClanMembers(commands.Cog):
    """This category contains commands that do things with the members of clans."""
    def __init__(self, _bot, _clanDict):
        self.bot = _bot
        self.clanDict = _clanDict

    @commands.command(brief="This command can grab the MoE of a specific player and tank", description="The bot is very picky, so make sure the names of players and tanks are exactly the same! For proper name reference it might be smart to hit up the Wargaming Developer Room.")
    async def moe(self, ctx, playerName, tankName):
        foundPlayer = False
        if self.clanDict[ctx.guild.id].clanIsSet:
            for x in self.clanDict[ctx.guild.id].players:
                if x.name == playerName:
                    foundPlayer = True
                    for y in x.tanks:
                        if y.name == tankName:
                            await ctx.send("**{}** has **{}** mark(s) on the **{}**.".format(x.name, y.getMark(), y.getName()))
        else:
            await ctx.send("Please set a clan first with '{}setClan clantag'.".format(self.bot.command_prefix))

        if not foundPlayer:
            await ctx.send("Either you misspelled the player name or he does not exist in your clan.")
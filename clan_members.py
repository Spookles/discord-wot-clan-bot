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

class ClanMembers(commands.Cog):
    """This category contains commands that do things with the members of clans."""
    def __init__(self, _bot, _clanDict):
        self.bot = _bot
        self.clanDict = _clanDict

    @commands.command(brief="This command can grab the MoE of a specific player and tank", description="The bot is very picky, so make sure the names of players and tanks are exactly the same! For proper name reference it might be smart to hit up the Wargaming Developer Room.")
    async def moe(self, ctx, playerName, tankName):
        foundPlayer = False
        clan = self.clanDict[ctx.guild.id]
        if tankName != "meta":
            tankName = await GlobalFunc.findTankByName(tankName, clan.tanks)
        if clan.clanIsSet:
            for x in clan.players:
                if x.name == playerName:
                    foundPlayer = True
                    if tankName == "meta":
                        for y in x.tanks:
                            if y.id in clan.metaTanks:
                                await ctx.send("**{}** has **{}** mark(s) on the **{}**.".format(x.name, y.mark, y.name))
                    else:
                        for y in x.tanks:
                            if y.name == tankName:
                                await ctx.send("**{}** has **{}** mark(s) on the **{}**.".format(x.name, y.mark, y.name))
                            elif tankName == "404":
                                await ctx.send("Could not find the tank you were looking for. Try to be more specific.")
        else:
            await ctx.send("Please set a clan first with '{}setClan clantag'.".format(self.bot.command_prefix))

        if not foundPlayer:
            await ctx.send("Either you misspelled the player name or he does not exist in your clan.")

    @commands.command(brief="TESTING ONLY", description="")
    async def increaseMoe(self, ctx, playerName, tankName, moe):
        foundPlayer = False
        if self.clanDict[ctx.guild.id].clanIsSet:
            totalMarks = 0
            for x in self.clanDict[ctx.guild.id].players:
                if x.name == playerName:
                    foundPlayer = True
                    for y in x.tanks:
                        if y.name == tankName:
                            loopCount1 = 0
                            for tankDB in x.tanks:
                                if y.id == tankDB.id:
                                    tankDB.previousMark = tankDB.mark
                                    tankDB.mark = int(moe)
                                    if x.firstLoop != True:
                                        if tankDB.mark != tankDB.previousMark:
                                            x.newMarks[loopCount1] = tankDB
                                            loopCount1+=1
                                            await ctx.send("Set new MoE, going to look for new marks now as usual.")
                                        
                            loopCount = 0
                            for newMarks in x.newMarks:
                                if x.newMarks[loopCount] != 0:
                                    await ctx.send("**{}** : **{}** - **{}** > **{}**".format(x.name, newMarks.name, newMarks.previousMark, newMarks.mark))
                                    x.newMarks[loopCount] = 0
                                    loopCount+=1
                                    totalMarks+=1
            if totalMarks == 0:
                await ctx.send("No new marks today :(")
            #await ctx.send("**{}** has **{}** mark(s) on the **{}**.".format(x.name, y.mark, y.name))
        else:
            await ctx.send("Please set a clan first with '{}setClan clantag'.".format(self.bot.command_prefix))

        if not foundPlayer:
            await ctx.send("Either you misspelled the player name or he does not exist in your clan.")
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
import random
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

class GlobalFunc():
    """Functions that get used by multiple classes and cogs."""

    @staticmethod
    async def getClan(tag):
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

    @staticmethod
    async def embedBuilder(clan, type, tier):
        color_str = "0x" + clan.color[1:]
        if type == "sh&gm":
            embed = discord.Embed(title="[{}] {}".format(clan.tag, clan.name), description=clan.motto, color=int(color_str, 16))
            embed.set_thumbnail(url=clan.emblem_url)
            embed.add_field(name="\u200b", value="Skirmish Rating:", inline=False)
            embed.add_field(name="T6", value=clan.sm_6_str, inline=True)
            embed.add_field(name="T8", value=clan.sm_8_str, inline=True)
            embed.add_field(name="T10", value=clan.sm_10_str, inline=True)
            embed.add_field(name="\u200b", value="Global Map Rating:", inline=False)
            embed.add_field(name="T6", value=clan.gm_6_str, inline=True)
            embed.add_field(name="T8", value=clan.gm_8_str, inline=True)
            embed.add_field(name="T10", value=clan.gm_10_str, inline=True)
            footer_text = "Updated Statistics at: " + str(datetime.datetime.fromtimestamp(clan.updated_at))
            embed.set_footer(text=footer_text)
        elif type == "sh":
            embed = discord.Embed(title="[{}] {}".format(clan.tag, clan.name), description=clan.motto, color=int(color_str, 16))
            embed.add_field(name="\u200b", value="Skirmish Rating:", inline=False)
            if tier == '6' or tier == 't6':
                embed.add_field(name="T6", value=clan.sm_6_str, inline=True)
            elif tier == '8' or tier == 't8':
                embed.add_field(name="T8", value=clan.sm_8_str, inline=True)
            elif tier == '10' or tier == 't10':
                embed.add_field(name="T6", value=clan.sm_10_str, inline=True)
            embed.set_thumbnail(url=clan.emblem_url)
            footer_text = "Updated Statistics at: " + str(datetime.datetime.fromtimestamp(clan.updated_at))
            embed.set_footer(text=footer_text)
        elif type == "gm":
            embed = discord.Embed(title="[{}] {}".format(clan.tag, clan.name), description=clan.motto, color=int(color_str, 16))
            embed.add_field(name="\u200b", value="Global Map Rating:", inline=False)
            if tier == '6' or tier == 't6':
                embed.add_field(name="T6", value=clan.gm_6_str, inline=True)
            elif tier == '8' or tier == 't8':
                embed.add_field(name="T8", value=clan.gm_8_str, inline=True)
            elif tier == '10' or tier == 't10' :
                embed.add_field(name="T6", value=clan.gm_10_str, inline=True)
            embed.set_thumbnail(url=clan.emblem_url)
            footer_text = "Updated Statistics at: " + str(datetime.datetime.fromtimestamp(clan.updated_at))
            embed.set_footer(text=footer_text)
        elif type == "clan":
            embed = discord.Embed(title="[{}] {}".format(clan.tag, clan.name), description=clan.motto, color=int(color_str, 16))
            embed.set_thumbnail(url=clan.emblem_url)
            embed.add_field(name="\u200b", value=clan.description, inline=False)
            embed.add_field(name="Commander", value=clan.commander, inline=True)
            embed.add_field(name="Member Count", value=clan.members_count, inline=True)
            embed.add_field(name="Created at", value=str(datetime.datetime.fromtimestamp(clan.created_at)), inline=False)
            embed.add_field(name="Creator", value=clan.created_by, inline=True)
        return embed

    @staticmethod
    async def checkNewMarks(channel, clan):
        totalMarks = 0
        for member in clan.players:
            await member.retrieveTanks()
            loopCount = 0
            for newMarks in member.newMarks:
                if member.newMarks[loopCount] != 0:
                    if newMarks.mark >= 3:
                        await channel.send("DING DING DING **{}** has reached **3** marks on his {} on to the next!".format(member.name, newMarks.name))
                    else:
                        await channel.send("**{}** earned a new mark on his **{}** {}>**{}** {}".format(member.name, newMarks.name, newMarks.previousMark, newMarks.mark, randomGz()))
                    member.newMarks[loopCount] = 0
                    loopCount+=1
                    totalMarks+=1
        if totalMarks == 0:
            await channel.send("No new marks today :(")
    
    @staticmethod
    async def randomGz():
        r = random.randint(0, 5)
        if r == 0:
            return "good stuff!"
        elif r == 1:
            return "well played!"
        elif r == 2:
            return "amazin'"
        elif r == 3:
            return "aw sheit we got an expert."
        elif r == 4:
            return "he is unstoppable!"
        else:
            return "what a god."

    @staticmethod
    async def findTankByName(name, tanks):
        filteredTanks = []
        for tank in tanks:
            tName = [tank.name]
            t = process.extractOne(name, tName)
            if t[1] >= 50:
                filteredTanks.append(t[0])
        best = process.extractOne(name, filteredTanks)
        for tank in tanks:
            if tank.name == best[0]:
                # print("ID:{} -- NAME:{}".format(tank.id, tank.name))
                return tank.name
        return "404"

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
    def __init__(self, _bot):
        self.bot = _bot

    @commands.command(brief="Searches and shows basic clan information", description="By giving it an existing clan tag it will look up basic information about the clan. It will show its owner, description, name, and various other info.")
    async def find(self, ctx, clanTag):
        clan = await GlobalFunc.getClan(clanTag)
        if(clan):
            color_str = "0x" + clan.color[1:]
            embed = discord.Embed(title="[{}] {}".format(clan.tag, clan.name), description=clan.motto, color=int(color_str, 16))
            embed.set_thumbnail(url=clan.emblem_url)
            embed.add_field(name="\u200b", value=clan.description, inline=False)
            embed.add_field(name="Commander", value=clan.commander, inline=True)
            embed.add_field(name="Member Count", value=clan.members_count, inline=True)
            embed.add_field(name="Created at", value=str(datetime.datetime.fromtimestamp(clan.created_at)), inline=False)
            embed.add_field(name="Creator", value=clan.created_by, inline=True)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Invalid clan tag")

    @commands.command(brief="Shows the stronghold and global map ratings of a clan", description="Searches a clan by tag and returns stronghold data.")
    async def rating(self, ctx, clanTag):
        clan = await GlobalFunc.getClan(clanTag)
        if(clan):
            color_str = "0x" + clan.color[1:]
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
            await ctx.send(embed=embed)
        else:
            await ctx.send("Invalid clan tag")
            
    @commands.command(aliases=['sh'], brief="Minimalised version of rating, but for skirmish", description="By using the skirmish command you can retrieve the skirmish rating of a specific clan for a specific tier.\nIt can be called as 'skirmish' or a shorter version 'sh'\nTier 6 : 6/t6/T6\nTier 8 : 8/t8/T8\nTier 10: 10/t10/T10")
    async def skirmish(self, ctx, clanTag, tier):
        clan = await GlobalFunc.getClan(clanTag)
        if(clan):
            color_str = "0x" + clan.color[1:]
            embed = discord.Embed(title="[{}] {}".format(clan.tag, clan.name), description=clan.motto, color=int(color_str, 16))
            embed.add_field(name="\u200b", value="Skirmish Rating:", inline=False)
            if(tier == '6' or tier == 't6'):
                embed.add_field(name="T6", value=clan.sm_6_str, inline=True)
            elif(tier == '8' or tier == 't8'):
                embed.add_field(name="T8", value=clan.sm_8_str, inline=True)
            elif(tier == '10' or tier == 't10'):
                embed.add_field(name="T6", value=clan.sm_10_str, inline=True)
            embed.set_thumbnail(url=clan.emblem_url)
            footer_text = "Updated Statistics at: " + str(datetime.datetime.fromtimestamp(clan.updated_at))
            embed.set_footer(text=footer_text)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Invalid clan tag")

    @commands.command(aliases=['gm'], brief="Minimalised version of rating, but for the global map", description="By using the globalmap command you can retrieve the global map rating of a specific clan for a specific tier.\nIt can be called as 'globalmap' or a shorter version 'gm'\nTier 6 : 6/t6/T6\nTier 8 : 8/t8/T8\nTier 10: 10/t10/T10")
    async def globalmap(self, ctx, clanTag, tier):
        clan = await GlobalFunc.getClan(clanTag)
        if(clan):
            color_str = "0x" + clan.color[1:]
            embed = discord.Embed(title="[{}] {}".format(clan.tag, clan.name), description=clan.motto, color=int(color_str, 16))
            embed.add_field(name="\u200b", value="Global Map Rating:", inline=False)
            if(tier == '6' or tier == 't6'):
                embed.add_field(name="T6", value=clan.gm_6_str, inline=True)
            elif(tier == '8' or tier == 't8'):
                embed.add_field(name="T8", value=clan.gm_8_str, inline=True)
            elif(tier == '10' or tier == 't10'):
                embed.add_field(name="T6", value=clan.gm_10_str, inline=True)
            embed.set_thumbnail(url=clan.emblem_url)
            footer_text = "Updated Statistics at: " + str(datetime.datetime.fromtimestamp(clan.updated_at))
            embed.set_footer(text=footer_text)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Invalid clan tag")
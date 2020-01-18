import requests
import json
from clan import Clan
import discord
from discord.ext import tasks, commands
import datetime
import asyncio

clan = Clan()
send_time='20:00'
bot = commands.Bot(command_prefix=':')
clanIsSet = False

def getClan(tag):
    api_url = "https://api.worldoftanks.eu/wot/clans/list/?application_id=0ecfda2435a084d16fa9e02ea75ee0db&search={}".format(tag)
    response = requests.get(api_url)
    if(response.json()['status'] == "ok" and
       response.json()['meta']['count'] >= 1):
        json = response.json()['data'][0]
        clan.id = json['clan_id']
        clan.name = json['name']
        clan.tag = json['tag']
        clan.emblem_url = json['emblems']['x195']['portal']
        clan.getDetails(clan.id)
        clan.getRating(clan.id)
        return True
    else:
        return False

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@tasks.loop(seconds=59)
async def sendRatingDaily(id: int, tag: str):
    channel = bot.get_channel(id)
    now = datetime.datetime.strftime(datetime.datetime.now(), '%H:%M')
    if(now == send_time):
        if(getClan(tag)):
            color_str = "0x" + clan.color[1:]
            embed = discord.Embed(title=clan.name, description=clan.motto, color=int(color_str, 16))
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
            await channel.send(embed=embed)
        else:
            await channel.send("Invalid clan tag")

        if clanIsSet == True:
            for member in clan.players:
                member.retrieveTanks()
                loopCount = 0
                if member.newMarks[0] != 0:
                    for newMarks in member.newMarks:
                        await channel.send("**{}** has gained a new mark on his **{}** he had **{}** and now it is **{}** good stuff!".format(member.name, newMarks.name, newMarks.getPreviousMark(), newMarks.getMark()))
                        loopCount+=1
                    member.newMarks = [0] * 100
        else:
            await channel.send("Before checking marks, please set a clan first with '{}setClan clantag'.".format(bot.command_prefix))

@bot.command(name="find", help="Finds a clan.", description="Finds a clan based on the tag and shows various data of the clan. \n Example: '!find TNKCS'")
async def find(ctx, arg):
    if(getClan(arg)):
        color_str = "0x" + clan.color[1:]
        embed = discord.Embed(title=clan.name, description=clan.motto, color=int(color_str, 16))
        embed.set_author(name=arg)
        embed.set_thumbnail(url=clan.emblem_url)
        embed.add_field(name="\u200b", value=clan.description, inline=False)
        embed.add_field(name="Commander", value=clan.commander, inline=True)
        embed.add_field(name="Member Count", value=clan.members_count, inline=True)
        embed.add_field(name="Created at", value=str(datetime.datetime.fromtimestamp(clan.created_at)), inline=False)
        embed.add_field(name="Creator", value=clan.created_by, inline=True)
        await ctx.send(embed=embed)
    else:
        await ctx.send("Invalid clan tag")

@bot.command(name="rating", help="Shows skirmish/global map rating.", description="Retrieves global map and skirmish data of a clan by tag. \n Example: '!rating TNKCS'")
async def rating(ctx, arg):
    if(getClan(arg)):
        color_str = "0x" + clan.color[1:]
        embed = discord.Embed(title=clan.name, description=clan.motto, color=int(color_str, 16))
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
        
@bot.command(name="skirmish", help="Shows skirmish data by tier.", description="Retrieves skirmish data of a specific tier from a clan by tag. \n Example: '!skirmish TNKCS t6'")
async def skirmish(ctx, tag: str, tier: str):
    if(getClan(tag)):
        color_str = "0x" + clan.color[1:]
        embed = discord.Embed(title=clan.name, description=clan.motto, color=int(color_str, 16))
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

@bot.command(name="setDaily", help="Set information for daily updates.", description="Sets the channel the bot is allowed to speak in by itself, it also sets the clan tag you want your daily ratings from.\n Example: '!setDaily TNKCS'")
async def setDaily(ctx, arg):
    sendRatingDaily.start(ctx.channel.id, arg)

@bot.command(name="setClan", help="Sets the clan to check MoE for.")
async def setClan(ctx, arg):
    a = datetime.datetime.now()
    await ctx.send("Retrieving all data for the first time, this might take a while. I'll let you know when I'm finished :)")
    getClan(arg)
    clan.getTankNames()
    clan.getPlayers()
    b = datetime.datetime.now()
    delta = b-a
    await ctx.send("Whew, that took me {} seconds. But we're all done!".format(delta.seconds))
    global clanIsSet
    clanIsSet = True

@bot.command(name="debug")
async def debug(ctx, playerName, tankName):
    if clanIsSet == True:
        for x in clan.players:
            if x.name == playerName:
                for y in x.tanks:
                    if y.name == tankName:
                        await ctx.send("**{}** has **{}** mark(s) on the **{}**.".format(x.name, y.getMark(), y.getName()))
    else:
        await ctx.send("Please set a clan first with '{}setClan clantag'.".format(bot.command_prefix))

@bot.command(name="checkMarks")
async def checkMarks(ctx):
    if clanIsSet == True:
        for member in clan.players:
            member.retrieveTanks()
            loopCount = 0
            if member.newMarks[0] != 0:
                for newMarks in member.newMarks:
                    await ctx.send("**{}** has gained a new mark on his **{}** he had **{}** and now it is **{}** good stuff!".format(member.name, newMarks.name, newMarks.getPreviousMark(), newMarks.getMark()))
                    loopCount+=1
                member.newMarks = [0] * 100
    else:
        await ctx.send("Please set a clan first with '{}setClan clantag'.".format(bot.command_prefix))

bot.run('NjU0ODA1Nzk2NDk1OTQ5ODM3.XiM3MQ.bDYvjM3bbxG9ZuSKCsgaUMLr30s')
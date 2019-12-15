import requests
import json
from clan import Clan
import discord
from discord.ext import tasks, commands
from datetime import datetime
import asyncio

clan = Clan()
send_time='06:00'
bot = commands.Bot(command_prefix='!')

def getClan(tag):
    api_url = "https://api.worldoftanks.eu/wot/clans/list/?application_id=0ecfda2435a084d16fa9e02ea75ee0db&search=%s" % (tag)
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
        print(clan.id)
        return True
    else:
        return False

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@tasks.loop(seconds=50)
async def sendRatingDaily(id: int, tag: str):
    channel = bot.get_channel(id)
    now = datetime.strftime(datetime.now(), '%H:%M')
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
            footer_text = "Updated Statistics at: " + str(datetime.fromtimestamp(clan.updated_at))
            embed.set_footer(text=footer_text)
            await channel.send(embed=embed)
        else:
            await channel.send("Invalid clan tag")

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
        embed.add_field(name="Created at", value=str(datetime.fromtimestamp(clan.created_at)), inline=False)
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
        footer_text = "Updated Statistics at: " + str(datetime.fromtimestamp(clan.updated_at))
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
        footer_text = "Updated Statistics at: " + str(datetime.fromtimestamp(clan.updated_at))
        embed.set_footer(text=footer_text)
        await ctx.send(embed=embed)
    else:
        await ctx.send("Invalid clan tag")

@bot.command(name="setDaily", help="Set information for daily updates.", description="Sets the channel the bot is allowed to speak in by itself, it also sets the clan tag you want your daily ratings from.\n Example: '!setDaily TNKCS'")
async def setDaily(ctx, arg):
    sendRatingDaily.start(ctx.channel.id, arg)

bot.run('NjU0ODA1Nzk2NDk1OTQ5ODM3.XfY1dQ.pVGpXwFdQe9_Or0F06s3rdr_bkk')
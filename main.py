import requests
import json
from clan import Clan
import discord
from discord.ext import commands
from datetime import datetime

clan = Clan()
#client = discord.Client()
bot = commands.Bot(command_prefix='!')

def getClan(tag):
    api_url = "https://api.worldoftanks.eu/wot/clans/list/?application_id=0ecfda2435a084d16fa9e02ea75ee0db&search=%s" % (tag)
    response = requests.get(api_url)
    if(response.json()['status'] == "ok" and
       response.json()['meta']['total'] == 1):
        json = response.json()['data'][0]
        clan.id = json['clan_id']
        clan.name = json['name']
        clan.tag = json['tag']
        clan.emblem_url = json['emblems']['x195']['portal']
        clan.getDetails(clan.id)
        clan.getRating(clan.id)
        print(clan.id)
    else:
        print("Invalid clan tag")

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.command()
async def find(ctx, arg):
    getClan(arg)
    await ctx.send(clan.id)
    await ctx.send(clan.name)

@find.error
async def info_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('No clan tag passed.')

@bot.command()
async def rating(ctx, arg):
    getClan(arg)
    color_str = "0x" + clan.color[1:]
    skirmish_t6 = "Rating: **" + str(clan.skirmish['fb_6']['value']) + "**\nRank: **" + str(clan.skirmish['fb_6']['rank']) + "**\nRank Change: **" + str(clan.skirmish['fb_6']['rank_delta']) + "**"
    skirmish_t8 = "Rating: **" + str(clan.skirmish['fb_8']['value']) + "**\nRank: **" + str(clan.skirmish['fb_8']['rank']) + "**\nRank Change: **" + str(clan.skirmish['fb_8']['rank_delta']) + "**"
    skirmish_t10 = "Rating: **" + str(clan.skirmish['fb_10']['value']) + "**\nRank: **" + str(clan.skirmish['fb_10']['rank']) + "**\nRank Change: **" + str(clan.skirmish['fb_10']['rank_delta']) + "**"
    global_map_t6 = "Rating: **" + str(clan.global_map['gm_6']['value']) + "**\nRank: **" + str(clan.global_map['gm_6']['rank']) + "**\nRank Change: **" + str(clan.global_map['gm_6']['rank_delta']) + "**"
    global_map_t8 = "Rating: **" + str(clan.global_map['gm_8']['value']) + "**\nRank: **" + str(clan.global_map['gm_8']['rank']) + "**\nRank Change: **" + str(clan.global_map['gm_8']['rank_delta']) + "**"
    global_map_t10 = "Rating: **" + str(clan.global_map['gm_10']['value']) + "**\nRank: **" + str(clan.global_map['gm_10']['rank']) + "**\nRank Change: **" + str(clan.global_map['gm_10']['rank_delta']) + "**"
    embed = discord.Embed(title=clan.name, description=clan.motto, color=int(color_str, 16))
    embed.set_thumbnail(url=clan.emblem_url)
    embed.add_field(name="Skirmish Ratings:", value="---", inline=False)
    embed.add_field(name="T6", value=skirmish_t6, inline=True)
    embed.add_field(name="T8", value=skirmish_t8, inline=True)
    embed.add_field(name="T10", value=skirmish_t10, inline=True)
    embed.add_field(name="Global Map Ratings:", value="---", inline=False)
    embed.add_field(name="T6", value=global_map_t6, inline=True)
    embed.add_field(name="T8", value=global_map_t8, inline=True)
    embed.add_field(name="T10", value=global_map_t10, inline=True)
    footer_text = "Updated Statistics at: " + str(datetime.fromtimestamp(clan.updated_at))
    embed.set_footer(text=footer_text)
    await ctx.send(embed=embed)
    # await ctx.send(clan.skirmish['fb_6'])

bot.run('NjU0ODA1Nzk2NDk1OTQ5ODM3.XfUBnQ.oyhe7y3oKeB3SOGqsCawedlts8o')
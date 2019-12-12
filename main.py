import requests
import json
from clan import Clan
import discord
from discord.ext import commands

clan = Clan()
#client = discord.Client()
bot = commands.Bot(command_prefix='$')

def getClan(tag):
    api_url = "https://api.worldoftanks.eu/wot/clans/list/?application_id=0ecfda2435a084d16fa9e02ea75ee0db&search=%s" % (tag)
    response = requests.get(api_url)
    if(response.json()['status'] == "ok" and
       response.json()['meta']['total'] == 1):
        json = response.json()['data'][0]
        clan.id = json['clan_id']
        clan.name = json['name']
        clan.tag = json['tag']
        clan.emblem_url = json['emblems']['x256']['wowp']
        clan.getDetails(clan.id)
        clan.getRating(clan.id)
    else:
        print("Invalid clan tag")

# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return

#     if message.content.startswith('$hello'):
#         await message.channel.send('Hello!')

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.command()
async def FindClan(ctx, arg):
    getClan(arg)
    await ctx.send(clan.name)

@FindClan.error
async def info_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('No clan tag passed.')

@bot.command()
async def PrintRating(ctx, arg):
    getClan(arg)
    await ctx.send(clan.skirmish['fb_6'])

bot.run('NjU0ODA1Nzk2NDk1OTQ5ODM3.XfK5jQ.Fh1hp5E9yZremGH9oGdf6YuPVBI')
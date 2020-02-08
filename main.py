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
from clan_members import ClanMembers
from clan_rating import ClanRating
from global_func import GlobalFunc

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

clanDict = {}
bot = commands.Bot(command_prefix=':')

@bot.event
async def on_ready():
    bot.add_cog(ClanRating(bot, clanDict))
    bot.add_cog(ClanMembers(bot, clanDict))
    for guild in bot.guilds:
        print(
            f'{bot.user} is connected to the following guild:\n'
            f'{guild.name}(id: {guild.id})'
        )

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    raise error

@tasks.loop(minutes=1.0)
async def sendRatingDaily(channel_id, guild_id):
    channel = bot.get_channel(channel_id)
    now = datetime.datetime.strftime(datetime.datetime.now(), '%H:%M')
    clan = clanDict[guild_id]
    clan = await GlobalFunc.getClan(clan.tag)
    if now == clan.send_time:
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
        await clan.getPlayers()
        await GlobalFunc.checkNewMarks(channel, clan)
        print("{}::Updated server {}".format(datetime.datetime.now(), guild_id))

@bot.command(brief="Set channel and clan for daily updates", description="Sets the channel the bot is allowed to speak in by itself. Also starts the automatic messages for daily updates by default at 20:00CE(S)T.")
async def setDaily(ctx):
    if ctx.guild.id in clanDict:
        sendRatingDaily.start(ctx.channel.id, ctx.guild.id)
        await ctx.send("Daily stronghold & global map update will be posted at **{}** CE(S)T in **this** channel. I'll also let you know if people got new Marks of Exellences.".format(clanDict[ctx.guild.id].send_time))
    else:
        await ctx.send("Please set a clan first with '{}setClan clantag'.".format(bot.command_prefix))


@bot.command(brief="Changes the time the bot gives daily updates", description="Change the time at which the bot will update you on stronghold, global map ranks and MoE changes.\nTime is in HH:MM(24:59) format and CE(S)T timezone.")
async def updateTime(ctx, time):
    if ctx.guild.id in clanDict:
        if re.search('^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$', time):
            clanDict[ctx.guild.id].send_time = time
            await ctx.send("Daily update time is now set to **{}** CE(S)T.".format(clanDict[ctx.guild.id].send_time))
        else:
            await ctx.send("Time format is wrong.")
    else :
        await ctx.send("Please set a clan first with '{}setClan clantag'.".format(bot.command_prefix))

#name="setClan", help="Attaches a clan to the server"
@bot.command(brief="Links a clan to your Discord server", description="By using this method a World of Tanks clan will be matched with your server. This will make it possible to have daily updates of your clan!")
async def setClan(ctx, clanTag):
    clan = await GlobalFunc.getClan(clanTag)
    if clan:
        if not ctx.guild.id in clanDict:
            a = datetime.datetime.now()
            await ctx.send("Retrieving all data for the first time, this might take a while. I'll let you know when I'm finished :)")
            await clan.getTankNames()
            await clan.getPlayers()
            clanDict[ctx.guild.id] = clan
            b = datetime.datetime.now()
            delta = b-a
            await ctx.send("Whew, that took me **{}** seconds. But we're all done!".format(delta.seconds))
            clanDict[ctx.guild.id].clanIsSet = True
        else:
            await ctx.send("Server has already set a clan.")
    else:
        await ctx.send("Invalid clan tag.")

@bot.command(brief="pong!", description="Returns the latency of the bot.")
async def ping(ctx):
    await ctx.send("Pong! Latency: **{}**seconds".format(round(bot.latency, 2)))

bot.run(TOKEN)
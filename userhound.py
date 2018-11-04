import discord
import sqlite3
import asyncio
import json
from discord.ext import commands

conn = sqlite3.connect('HoundBot.db')
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS UserRating (User TEXT, Rating TEXT, Issuer TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS OptIn (Guild TEXT unique)")
c.execute("CREATE TABLE IF NOT EXISTS ServerVerification (Guild TEXT unique, Role TEXT, Channel TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS ServerLogging (Guild TEXT unique, Channel TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS Blacklist (Id TEXT unique)")
c.execute("CREATE TABLE IF NOT EXISTS MuteRoles (Guild TEXT unique, Role TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS MutedUsers (Guild TEXT, User TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS MemberPresence (Guild TEXT unique, GreetChannel TEXT, GreetMsg TEXT, GreetDuration TEXT, GreetToggle TEXT, LeaveChannel TEXT, LeaveMsg TEXT, LeaveDuration TEXT, LeaveToggle TEXT, DMMsg TEXT, DMToggle TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS SelfAssignableRoles (Guild TEXT, Role TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS AnnouncementChannels (Guild TEXT unique, Channel TEXT, Role TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS ReportChannels (Guild TEXT unique, Channel TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS ReportMembers (Guild TEXT, Offender TEXT, Reporter TEXT, Reason TEXT, Message TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS NickReqChannels (Guild TEXT unique, Channel TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS NickReqs (Guild TEXT, User TEXT, Nick TEXT, Message TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS VoiceRoles (Guild TEXT, Channel TEXT unique, Role TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS MemberPersistanceGuilds (Guild TEXT unique)")
c.execute("CREATE TABLE IF NOT EXISTS MemberPersistanceUsers (User TEXT, Guild TEXT, Roles TEXT, Nick TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS Prefixes (Guild TEXT unique, Prefix TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS Filters (Guild TEXT, Word TEXT, Filter TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS ChangelogAnnounceChannels (Guild TEXT unique, Channel TEXT)")

from userhoundcogs.Utility import prefixes

with open('config.json') as json_data:
	response_json = json.load(json_data)
	default_prefix = response_json['default_prefix']
	token = response_json['token']

async def get_prefix(bot, message):
	if message.guild:
		try:
			return commands.when_mentioned_or(prefixes[message.guild.id])(bot, message)
		except KeyError:
			return commands.when_mentioned_or(default_prefix)(bot, message)
	else:
		return commands.when_mentioned_or(default_prefix)(bot, message)

bot = commands.Bot(command_prefix = get_prefix, case_insensitive = True, status = discord.Status.idle, activity = discord.Game('starting up...'))
bot.remove_command('help')

startup_extensions = ['userhoundcogs.Main', 'userhoundcogs.Help', 'userhoundcogs.Events', 'userhoundcogs.ServerLogging', 'userhoundcogs.Verification', 'userhoundcogs.OwnerOnly', 'userhoundcogs.Moderation', 'userhoundcogs.MemberPresence', 'userhoundcogs.Snipe', 'userhoundcogs.Utility', 'userhoundcogs.Filters']
for cog in startup_extensions:
	try:
		bot.load_extension(cog)
	except Exception as e:
		print(e)

@bot.event
async def on_ready():
	while True:
		await bot.change_presence(status = discord.Status.online, activity = discord.Activity(name = str(len(bot.users)) + ' users in ' + str(len(bot.guilds)) + ' servers', type = 3))
		await asyncio.sleep(120)

from userhoundcogs.OwnerOnly import blacklist_ids

@bot.event
async def on_message(message):
	if message.guild and message.guild.id in blacklist_ids:
		await message.guild.leave()
	elif message.author.bot or message.author.id in blacklist_ids:
		return

	await bot.process_commands(message)


bot.run(token)

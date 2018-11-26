import discord
import asyncio
import json
import sqlite3
import os
import datetime
from discord.ext import commands

conn = sqlite3.connect('configs/HoundBot.db', detect_types = sqlite3.PARSE_DECLTYPES)
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS Users (User INTEGER unique, CurrencyTotal INTEGER, CurrencyLastClaim TIMESTAMP)")
c.execute("CREATE TABLE IF NOT EXISTS UserRatings (User INTEGER, Rating INTEGER, Issuer INTEGER)")
c.execute("CREATE TABLE IF NOT EXISTS GuildConfig (Guild INTEGER unique, Prefix TEXT, MemberPersistence INTEGER, ServerLog INTEGER)")
c.execute("CREATE TABLE IF NOT EXISTS PersistedUsers (User INTEGER, Guild INTEGER, Roles TEXT, Nick TEXT)")

from cogs.Utility import prefix

with open('configs/settings.json') as json_data:
	response_json = json.load(json_data)

default_prefix = response_json['default_prefix']
token = response_json['token']
del response_json

async def get_prefix(bot, message):
	if message.guild:
		try:
			return commands.when_mentioned_or(prefix[message.guild.id])(bot, message)
		except KeyError:
			return commands.when_mentioned_or(default_prefix)(bot, message)
	else:
		return commands.when_mentioned_or(default_prefix)(bot, message)

bot = commands.AutoShardedBot(command_prefix = get_prefix, case_insensitive = True, fetch_offline_members = True)
bot.remove_command('help')

startup_extensions = ['cogs.Help', 'cogs.Utility']
for cog in startup_extensions:
	try:
		bot.load_extension(cog)
	except Exception as e:
		print(e)

@bot.event
async def on_connect():
	print('Logged in as: ' + bot.user.name)
	print('Caching guilds and users...')
	print()

@bot.event
async def on_ready():
	print('Caching completed.')
	print('Ready to serve ' + str(len(bot.users)) + ' users in ' + str(len(bot.guilds)) + ' servers.')

@bot.event
async def on_command(ctx):
	print()
	print('Command: ' + ctx.message.content)
	print('Server: ' + str(ctx.guild) + ' (' + str(ctx.guild.id) + ')')
	print('Channel: #' + str(ctx.channel) + ' (' + str(ctx.channel.id) + ')')
	print('User: ' + str(ctx.author) + ' (' + str(ctx.author.id) + ')')

@bot.event
async def on_message(message):
	if message.author.bot:
		return
	elif message.content == bot.user.mention:
		return await message.channel.send(content = '**My prefix here is** `' + get_prefix + '`')

	await bot.process_commands(message)


bot.run(token)

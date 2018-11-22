import discord
import asyncio
import json
import sqlite3
import os
from discord.ext import commands

conn = sqlite3.connect('config/HoundBot.db', detect_types = sqlite3.PARSE_DECLTYPES)
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS Users (User INTEGER unique)")
c.execute("CREATE TABLE IF NOT EXISTS GuildConfig (Guild INTEGER unique, Prefix TEXT)")

from cogs.Main import prefix

with open('config/settings.json') as json_data:
	response_json = json.load(json_data)

default_prefix = response_json['default_prefix']
token = response_json['token']
del response_json

async def get_prefix(bot, message):
	if message.guild:
		try:
			return commands.when_mentioned_or(prefix[message.guild.id])(bot, message)
		except KeyError:
			return commands.when_mentioned_or(default_prefix)
	else:
		return commands.when_mentioned_or(default_prefix)

bot = commands.Bot(command_prefix = get_prefix, case_insensitive = True)
bot.remove_command('help')

startup_extensions = ['cogs.Main']
for cog in startup_extensions:
	try:
		bot.load_extension(cog)
	except Exception as e:
		print(e)

@bot.event
async def on_ready():
	print('Logged in as')
	print(bot.user.name)
	print('-----------')

@bot.event
async def on_message(message):
	if message.bot:
		return

	await bot.process_commands(message)


bot.run(token)

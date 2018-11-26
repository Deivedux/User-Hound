import discord
import sqlite3
import asyncio
import json
from discord.ext import commands

conn = sqlite3.connect('configs/HoundBot.db')
c = conn.cursor()

prefix_raw = c.execute("SELECT * FROM GuildConfig").fetchall()
global prefix
prefix = {}
for i in prefix_raw:
	prefix[int(i[0])] = i[1]
del prefix_raw

with open('configs/settings.json') as json_data:
	response_json = json.load(json_data)

response_success = response_json['response_string']['success']
response_error = response_json['response_string']['error']
del response_json

class Main:
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def serverinfo(self, ctx):
		


def setup(bot):
	bot.add_cog(Main(bot))

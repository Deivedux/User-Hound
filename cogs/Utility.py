import discord
import sqlite3
import asyncio
import json
from discord.ext import commands

conn = sqlite3.connect('HoundBot.db')
c = conn.cursor()

prefix_raw = c.execute("SELECT * FROM GuildConfig").fetchall()
global prefix
prefix = {}
for i in prefix_raw:
	prefix[int(i[0])] = i[1]
del prefix_raw

with open('settings.json') as json_data:
	response_json = json.load(json_data)

response_success = response_json['response_string']['success']
response_error = response_json['response_json']['error']
del response_json

class Main:
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def lookup(self, ctx, user_id):
		async with ctx.channel.typing():
			user_id = int(user_id.replace('<', '').replace('!', '').replace('@', ''). replace('>', ''))
			user = self.bot.get_user(user_id)
			if not user:
				try:
					user = await self.bot.get_user_info(user_id)
				except discord.NotFound:
					await ctx.send(content = response_error + ' **User with this ID does not exist.**')


def setup(bot):
	bot.add_cog(Main(bot))

import discord
import sqlite3
import asyncio
import aiohttp
import
from discord.ext import commands

conn = sqlite3.connect('HoundBot.db')
c = conn.cursor()

with open('config.json') as json_data:
	response_json = json.load(json_data)
	owners = response_json['owner_ids']

class Events:
	def __init__(self, bot):
		self.bot = bot

	async def on_ready(self):
		print('Logged in as:')
		print(self.bot.user.name)
		print('------------')

	#async def on_command_error(self, ctx, error):
	#	if isinstance(error, discord.NotFound):
	#		return

	async def on_command(self, ctx):
		try:
			if ctx.guild:
				print('\nCommand: ' + str(ctx.message.content) + '\nServer: ' + str(ctx.guild.name) + ' [' + str(ctx.guild.id) + ']\nUser: ' + str(ctx.author.name) + ' [' + str(ctx.author.id) + ']')
			else:
				print('\nCommand: ' + str(ctx.message.content) + '\nServer: PRIVATE\nUser: ' + str(ctx.author.name) + ' [' + str(ctx.author.id) + ']')
		except:
			pass

	async def on_member_join(self, member):
		if len(member.guild.members) > 20:
			bots = []
			for member in member.guild.members:
				if member.bot:
					bots.append(member)
			result = len(bots) / len(member.guild.members) * 100
			if float(result) > 70.0:
				await member.guild.leave()

	async def on_member_remove(self, member):
		if len(member.guild.members) > 20:
			bots = []
			for member in member.guild.members:
				if member.bot:
					bots.append(member)
			result = len(bots) / len(member.guild.members) * 100
			if float(result) > 70.0:
				await member.guild.leave()

	async def on_guild_join(self, guild):
		if len(guild.members) > 20:
			bots = []
			for member in guild.members:
				if member.bot:
					bots.append(member)
			result = len(bots) / len(guild.members) * 100
			if float(result) > 70.0:
				await guild.leave()

	async def on_reaction_add(self, reaction, user):
		if reaction.emoji == '🗑' and user.id in owners and reaction.message.author == self.bot.user:
			await reaction.message.delete()


def setup(bot):
	bot.add_cog(Events(bot))

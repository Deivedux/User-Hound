import discord
import json
import os
from discord.ext import commands
from cogs.Utility import prefix

with open('config/settings.json') as json_data:
	response_json = json.load(json_data)

default_prefix = response_json['default_prefix']
del response_json

class Help:
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def help(self, ctx, name = None):
		try:
			guild_prefix = prefix[ctx.guild.id]
		except KeyError:
			guild_prefix = default_prefix

		if not name:

			await ctx.send(embed = discord.Embed(title = 'Commands', description = '**Type `' + guild_prefix + 'mdls` to get a list of modules.\nType `' + guild_prefix + 'cmds` to get a list of commands in a module.**'))

		else:

			try:
				with open('commands/' + name.lower() + '.json') as json_data:
					response_json = json.load(json_data)
			except FileNotFoundError:
				await ctx.send(embed = discord.Embed(description = 'Command with that name does not exist.', color = ))


def setup(bot):
	bot.add_cog(Help(bot))

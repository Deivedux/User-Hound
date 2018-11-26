import discord
import json
import os
from discord.ext import commands
from cogs.Utility import prefix

with open('configs/settings.json') as json_data:
	response_json = json.load(json_data)

default_prefix = response_json['default_prefix']
del response_json

with open('configs/commands.json') as json_data:
	commands_json = json.load(json_data)

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

			examples = []
			for i in response_json['examples']:
				examples.append('`' + guild_prefix + i + '`')

			embed = discord.Embed(title = '`' + guild_prefix + response_json['title'] + '`', description = response_json['description'])
			embed.add_field(name = 'Requires Permission', value = response_json['user_perms'], inline = False)
			embed.add_field(name = 'Example', value = ' or '.join(examples))
			embed.set_footer(text = 'Module: ' + response_json['module'])
			await ctx.send(embed = embed)

	@commands.command()
	async def mdls(self, ctx):
		try:
			guild_prefix = prefix[ctx.guild.id]
		except KeyError:
			guild_prefix = default_prefix

		await ctx.send(embed = discord.Embed(title = 'Modules', description = '• Help\n• Utility').set_footer(text = 'Type `' + guild_prefix + 'cmds <module>` to see a list of commands in a module.'))

	@commands.command()
	async def cmds(self, ctx, name):
		try:
			guild_prefix = prefix[ctx.guild.id]
		except KeyError:
			guild_prefix = default_prefix

		'''
		Need ideas for this part rather than manually
		typing out commands for each module.
		'''


def setup(bot):
	bot.add_cog(Help(bot))

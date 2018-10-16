import discord
import datetime
import asyncio
from discord.ext import commands

deleted_messages = {}

class Snipe:
	def __init__(self, bot):
		self.bot = bot

	async def on_message_delete(self, message):
		if not message.author.bot and message.content:
			deleted_messages[message.channel.id] = message

	@commands.command()
	async def snipe(self, ctx):
		if not ctx.guild or not ctx.author.guild_permissions.manage_messages:
			return

		if ctx.channel.id not in deleted_messages.keys():
			await ctx.send(content = 'No messages were deleted from this channel since the last time I was restarted.')
		else:
			embed = discord.Embed(description = deleted_messages[ctx.channel.id].content, color = 0xD4AC0D, timestamp = deleted_messages[ctx.channel.id].created_at)
			embed.set_author(name = str(deleted_messages[ctx.channel.id].author), icon_url = deleted_messages[ctx.channel.id].author.avatar_url)
			await ctx.send(content = 'Last deleted message from this channel...', embed = embed)


def setup(bot):
	bot.add_cog(Snipe(bot))

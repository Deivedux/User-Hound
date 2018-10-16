import discord
import sqlite3
import datetime
from discord.ext import commands

conn = sqlite3.connect('HoundBot.db')
c = conn.cursor()

logging_channels = {}

c.execute("SELECT * FROM ServerLogging")
logging_raw = c.fetchall()
for i in logging_raw:
	logging_channels[int(i[0])] = int(i[1])
del logging_raw

class ServerLogging:
	def __init__(self, bot):
		self.bot = bot

	async def on_message_delete(self, message):
		if not message.content or message.author.bot:
			return

		if message.guild.id in logging_channels.keys():
			channel = self.bot.get_channel(logging_channels[message.guild.id])
			if channel != None:
				embed = discord.Embed(title = '<:messagedelete:439643744833241101> Message Deleted in #' + message.channel.name, description = message.content, color = 0xD4AC0D, timestamp = datetime.datetime.utcnow())
				embed.set_author(name = str(message.author), icon_url = message.author.avatar_url)
				await channel.send(embed = embed)
			else:
				c.execute("DELETE FROM ServerLogging WHERE Guild = " + str(message.guild.id))
				conn.commit()
				del logging_channels[message.guild.id]

	async def on_message_edit(self, before, after):
		if after.author.bot:
			return

		if not after.content or not before.content:
			return

		if before.content == after.content:
			return

		if after.guild.id in logging_channels.keys():
			channel = self.bot.get_channel(logging_channels[after.guild.id])
			if channel != None:
				embed = discord.Embed(title = '<:messageupdate:439643744849887233> Message Edited in #' + after.channel.name, color = 0x2471A3, timestamp = datetime.datetime.utcnow())
				embed.set_author(name = str(after.author), icon_url = after.author.avatar_url)
				embed.add_field(name = 'Before', value = before.content, inline = False)
				embed.add_field(name = 'After', value = after.content)
				await channel.send(embed = embed)
			else:
				c.execute("DELETE FROM ServerLogging WHERE Guild = " + str(after.guild.id))
				conn.commit()
				del logging_channels[after.guild.id]

	async def on_member_join(self, member):
		if member.guild.id in logging_channels.keys():
			channel = self.bot.get_channel(logging_channels[member.guild.id])
			if channel != None:
				embed = discord.Embed(title = '<:memberjoin:439643745089224704> Member Joined', description = member.mention + ' (' + str(member) + ')\n\nThere are now ' + str(len(member.guild.members)) + ' members.', color = 0x28B463, timestamp = datetime.datetime.utcnow())
				await channel.send(embed = embed)
			else:
				c.execute("DELETE FROM ServerLogging WHERE Guild = " + str(member.guild.id))
				conn.commit()
				del logging_channels[member.guild.id]

	async def on_member_remove(self, member):
		if member.guild.id in logging_channels.keys():
			channel = self.bot.get_channel(logging_channels[member.guild.id])
			if channel != None:
				embed = discord.Embed(title = '<:memberleave:439643745059733514> Member Left', description = member.mention + ' (' + str(member) + ')\n\nThere are now ' + str(len(member.guild.members)) + ' members.', color = 0xCB4335, timestamp = datetime.datetime.utcnow())
				await channel.send(embed = embed)
			else:
				c.execute("DELETE FROM ServerLogging WHERE Guild = " + str(member.guild.id))
				conn.commit()
				del logging_channels[member.guild.id]

	async def on_member_update(self, before, after):
		if after.guild.id in logging_channels.keys():
			channel = self.bot.get_channel(logging_channels[after.guild.id])
			if channel != None:
				if str(before.nick) != str(after.nick):
					embed = discord.Embed(title = '<:memberupdate:439643745059733504> Nickname Updated', color = 0x7D3C98, timestamp = datetime.datetime.utcnow())
					embed.set_author(name = str(after), icon_url = after.avatar_url)
					embed.add_field(name = 'Before', value = str(before.nick))
					embed.add_field(name = 'After', value = str(after.nick))
					await channel.send(embed = embed)
			else:
				c.execute("DELETE FROM ServerLogging WHERE Guild = " + str(after.guild.id))
				conn.commit()
				del logging_channels[after.guild.id]

	async def on_member_ban(self, guild, member):
		if guild.id in logging_channels.keys():
			channel = self.bot.get_channel(logging_channels[guild.id])
			if channel != None:
				embed = discord.Embed(title = '<:bancreate:439643744816332810> Member Banned', color = 0xCB4335, timestamp = datetime.datetime.utcnow())
				embed.set_author(name = str(member), icon_url = member.avatar_url)
				await channel.send(embed = embed)
			else:
				c.execute("DELETE FROM ServerLogging WHERE Guild = " + str(guild.id))
				conn.commit()
				del logging_channels[guild.id]

	async def on_member_unban(self, guild, member):
		if guild.id in logging_channels.keys():
			channel = self.bot.get_channel(logging_channels[guild.id])
			if channel != None:
				embed = discord.Embed(title = '<:bandelete:439643744803880960> Member Unbanned', color = 0x28B463, timestamp = datetime.datetime.utcnow())
				embed.set_author(name = str(member), icon_url = member.avatar_url)
				await channel.send(embed = embed)
			else:
				c.execute("DELETE FROM ServerLogging WHERE Guild = " + str(guild.id))
				conn.commit()
				del logging_channels[guild.id]

	@commands.command()
	async def serverlog(self, ctx):
		if not ctx.guild or not ctx.author.guild_permissions.manage_guild:
			return

		perms = ctx.guild.me.permissions_in(ctx.channel)
		if not perms.send_messages:
			return

		if not perms.embed_links:
			return await ctx.send(content = '<:xmark:314349398824058880> **I need `Embed Links` permission in this channel before I can start logging.**')

		try:
			c.execute("INSERT INTO ServerLogging (Guild, Channel) VALUES ('" + str(ctx.guild.id) + "', '" + str(ctx.channel.id) + "')")
			conn.commit()
			logging_channels[ctx.guild.id] = ctx.channel.id
			await ctx.send(content = '<:check:314349398811475968> **Server logging Enabled.**')
		except sqlite3.IntegrityError:
			c.execute("DELETE FROM ServerLogging WHERE Guild = " + str(ctx.guild.id))
			conn.commit()
			del logging_channels[ctx.guild.id]
			await ctx.send(content = '<:check:314349398811475968> **Server logging Disabled.**')


def setup(bot):
	bot.add_cog(ServerLogging(bot))

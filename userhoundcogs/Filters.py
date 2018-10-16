import discord
import sqlite3
import datetime
from discord.ext import commands

conn = sqlite3.connect('HoundBot.db')
c = conn.cursor()

filters_raw = c.execute("SELECT * FROM Filters").fetchall()
filters = {}
for i in filters_raw:
	try:
		filters[int(i[0])][str(i[1])] = str(i[2])
	except KeyError:
		filters[int(i[0])] = {str(i[1]): str(i[2])}
del filters_raw

class Filters:
	def __init__(self, bot):
		self.bot = bot

	async def on_message(self, message):
		if message.guild and not message.author.bot and message.guild.id in filters.keys():
			if message.author.guild_permissions.ban_members:
				return

			for word in filters[message.guild.id].keys():
				if word in message.content.lower().split():
					if filters[message.guild.id][word] == 'D':
						await message.delete()
					elif filters[message.guild.id][word] == 'K':
						await message.delete()

						embed = discord.Embed(title = 'You were Kicked', color = 0xD4AC0D, timestamp = datetime.datetime.utcnow())
						embed.add_field(name = 'Server', value = str(message.guild))
						embed.add_field(name = 'Moderator', value = str(self.bot.user))
						embed.add_field(name = 'Reason', value = '**Auto-kick by message filter.**\n\nServer staff asked me to __kick__ anyone that mentions `' + word + '` in their messages.')
						embed.set_thumbnail(url = message.guild.icon_url)
						try:
							await message.author.send(embed = embed)
						except discord.Forbidden:
							pass

						await message.author.kick(reason = '[ Message Filter ]')
					elif filters[message.guild.id][word] == 'B':
						embed = discord.Embed(title = 'You were Banned', color = 0xD4AC0D, timestamp = datetime.datetime.utcnow())
						embed.add_field(name = 'Server', value = str(message.guild))
						embed.add_field(name = 'Moderator', value = str(self.bot.user))
						embed.add_field(name = 'Reason', value = '**Auto-ban by message filter.**\n\nServer staff asked me to __ban__ anyone that mentions `' + word + '` in their messages.')
						embed.set_thumbnail(url = message.guild.icon_url)
						try:
							await message.author.send(embed = embed)
						except discord.Forbidden:
							pass

						await message.author.ban(delete_message_days = 1, reason = '[ Message Filter ]')

					break

	@commands.command()
	async def filteradd(self, ctx, word: str, action: str):
		if not ctx.guild or not ctx.author.guild_permissions.administrator:
			return

		try:
			if word.lower() in filters[ctx.guild.id].keys():
				return await ctx.send(content = '<:xmark:314349398824058880> **That word is already filtered. Remove it first if you want to change it\'s punishment action.**')

			if len(filters[ctx.guild.id]) >= 10:
				return await ctx.send(content = '<:xmark:314349398824058880> **You have exceeded the amount of filters this server can have.**')
		except KeyError:
			pass
		except discord.Forbidden:
			return

		if action.lower() == 'delete':
			c.execute("INSERT INTO Filters (Guild, Word, Filter) VALUES ('" + str(ctx.guild.id) + "', '" + str(word).lower() + "', 'D')")
			conn.commit()
			try:
				filters[ctx.guild.id][word.lower()] = 'D'
			except KeyError:
				filters[ctx.guild.id] = {word.lower(): 'D'}
		elif action.lower() == 'kick':
			if not ctx.guild.me.guild_permissions.kick_members:
				return await ctx.send(content = '<:xmark:314349398824058880> **Please give me `Kick Members` permission first before assigning me this task.**')
			c.execute("INSERT INTO Filters (Guild, Word, Filter) VALUES ('" + str(ctx.guild.id) + "', '" + str(word).lower() + "', 'K')")
			conn.commit()
			try:
				filters[ctx.guild.id][word.lower()] = 'K'
			except KeyError:
				filters[ctx.guild.id] = {word.lower(): 'K'}
		elif action.lower() == 'ban':
			if not ctx.guild.me.guild_permissions.ban_members:
				return await ctx.send(content = '<:xmark:314349398824058880> **Please give me `Ban Members` permission first before assigning me this task.**')
			c.execute("INSERT INTO Filters (Guild, Word, Filter) VALUES ('" + str(ctx.guild.id) + "', '" + str(word).lower() + "', 'B')")
			conn.commit()
			try:
				filters[ctx.guild.id][word.lower()] = 'B'
			except KeyError:
				filters[ctx.guild.id] = {word.lower(): 'B'}

		await ctx.send(content = '<:check:314349398811475968> **Filter added.**')

	@commands.command()
	async def filterremove(self, ctx, word: str):
		if not ctx.guild or not ctx.author.guild_permissions.administrator:
			return

		if ctx.guild.id in filters.keys() and word.lower() not in filters[ctx.guild.id].keys():
			return await ctx.send(content = '<:xmark:314349398824058880> **That word does not exist.**')

		c.execute("DELETE FROM Filters WHERE Guild = '" + str(ctx.guild.id) + "' AND Word = '" + str(word) + "'")
		conn.commit()
		del filters[ctx.guild.id][word]
		if len(filters[ctx.guild.id]) == 0:
			del filters[ctx.guild.id]

		await ctx.send(content = '<:check:314349398811475968> **Filter removed.**')

	@commands.command()
	async def filters(self, ctx):
		if not ctx.guild or not ctx.author.guild_permissions.administrator:
			return

		filtered_words = []
		try:
			for i in filters[ctx.guild.id].keys():
				filtered_words.append('"' + i + '" -> ' + filters[ctx.guild.id][i])

			await ctx.send(embed = discord.Embed(title = 'Filtered Words', description = '\n'.join(filtered_words).replace('B', 'BAN').replace('D', 'DELETE').replace('K', 'KICK'), color = 0xD4AC0D))
		except KeyError:
			await ctx.send(content = '<:xmark:314349398824058880> **This server does not have any filtered words.**')


def setup(bot):
	bot.add_cog(Filters(bot))

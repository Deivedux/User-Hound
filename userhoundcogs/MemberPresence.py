import discord
import sqlite3
import asyncio
from discord.ext import commands

conn = sqlite3.connect('HoundBot.db')
c = conn.cursor()

default_greet = 'Welcome &user& to the **&server&** server!'
default_bye = '**&user&** has left the server!'

greet_toggle = []
greet_channel = {}
greet_message = {}
greet_duration = {}

leave_toggle = []
leave_channel = {}
leave_message = {}
leave_duration = {}

greet_dm_toggle = []
greet_dm_message = {}

member_presence_raw = c.execute("SELECT * FROM MemberPresence").fetchall()

for i in member_presence_raw:
	if i[4] != None:
		greet_toggle.append(int(i[0]))
	if i[1] != None:
		greet_channel[int(i[0])] = int(i[1])
	if i[2] != None:
		greet_message[int(i[0])] = str(i[2])
	if i[3] != None:
		greet_duration[int(i[0])] = int(i[3])

	if i[8] != None:
		leave_toggle.append(int(i[0]))
	if i[5] != None:
		leave_channel[int(i[0])] = int(i[5])
	if i[6] != None:
		leave_message[int(i[0])] = str(i[6])
	if i[7] != None:
		leave_duration[int(i[0])] = int(i[7])

	if i[10] != None:
		greet_dm_toggle.append(int(i[0]))
	if i[9] != None:
		greet_dm_message[int(i[0])] = str(i[9])

del member_presence_raw

class MemberPresence:
	def __init__(self, bot):
		self.bot = bot

	async def on_member_join(self, member):
		if member.guild.id in greet_toggle and not member.bot:
			channel = self.bot.get_channel(greet_channel[member.guild.id])
			if channel == None:
				c.execute("UPDATE MemberPresence SET GreetChannel = NULL, GreetToggle = NULL WHERE Guild = " + str(member.guild.id))
				conn.commit()
				del greet_channel[member.guild.id]
				greet_toggle.remove(member.guild.id)
			elif not member.permissions_in(channel).read_messages:
				return
			else:
				try:
					if member.guild.id not in greet_message.keys():
						if member.guild.id not in greet_duration.keys():
							await channel.send(content = default_greet.replace('&user&', member.mention).replace('&server&', member.guild.name))
						else:
							await channel.send(content = default_greet.replace('&user&', member.mention).replace('&server&', member.guild.name), delete_after = greet_duration[member.guild.id])
					else:
						if member.guild.id not in greet_duration.keys():
							await channel.send(content = greet_message[member.guild.id].replace('&user&', member.mention).replace('&server&', member.guild.name))
						else:
							await channel.send(content = greet_message[member.guild.id].replace('&user&', member.mention).replace('&server&', member.guild.name), delete_after = greet_duration[member.guild.id])
				except discord.Forbidden:
					pass

		if member.guild.id in greet_dm_toggle and not member.bot:
			try:
				if member.guild.id not in greet_dm_message.keys():
					await member.send(content = default_greet.replace('&user&', member.name).replace('&server&', member.guild.name))
				else:
					await member.send(content = greet_dm_message[member.guild.id].replace('&user&', member.name).replace('&server&', member.guild.name))
			except discord.Forbidden:
				pass

	async def on_member_remove(self, member):
		if member.guild.id in leave_toggle and not member.bot:
			channel = self.bot.get_channel(leave_channel[member.guild.id])
			if channel == None:
				c.execute("UPDATE MemberPresence SET LeaveChannel = NULL, LeaveToggle = NULL WHERE Guild = " + str(member.guild.id))
				conn.commit()
				del leave_channel[member.guild.id]
				leave_toggle.remove(member.guild.id)
			elif not member.permissions_in(channel).read_messages:
				return
			else:
				try:
					if member.guild.id not in leave_message.keys():
						if member.guild.id not in leave_duration.keys():
							await channel.send(content = default_bye.replace('&user&', str(member)).replace('&server&', member.guild.name))
						else:
							await channel.send(content = default_bye.replace('&user&', str(member)).replace('&server&', member.guild.name), delete_after = leave_duration[member.guild.id])
					else:
						if member.guild.id not in leave_duration.keys():
							await channel.send(content = leave_message[member.guild.id].replace('&user&', str(member)).replace('&server&', member.guild.name))
						else:
							await channel.send(content = leave_message[member.guild.id].replace('&user&', str(member)).replace('&server&', member.guild.name), delete_after = leave_duration[member.guild.id])
				except discord.Forbidden:
					pass

	@commands.command()
	async def greetmsg(self, ctx, *, msg = None):
		if not msg:
			if ctx.guild.id not in greet_message.keys():
				await ctx.send(embed = discord.Embed(title = 'Current Greet Message', description = default_greet, color = 0x28B463))
			else:
				await ctx.send(embed = discord.Embed(title = 'Current Greet Message', description = greet_message[ctx.guild.id], color = 0x28B463))
		else:
			if not ctx.guild or not ctx.author.guild_permissions.manage_guild:
				return

			perms = ctx.guild.me.permissions_in(ctx.channel)
			if not perms.send_messages:
				return

			try:
				c.execute("INSERT INTO MemberPresence (Guild, GreetMsg) VALUES ('" + str(ctx.guild.id) + "', '" + str(msg).replace('\'', '\'\'') + "')")
				conn.commit()
			except sqlite3.IntegrityError:
				c.execute("UPDATE MemberPresence SET GreetMsg = '" + str(msg).replace('\'', '\'\'') + "' WHERE Guild = '" + str(ctx.guild.id) + "'")
				conn.commit()
			greet_message[ctx.guild.id] = str(msg)

			await ctx.send(content = '<:check:314349398811475968> **New greet message set.**')

	@commands.command()
	async def greet(self, ctx):
		if not ctx.guild or not ctx.author.guild_permissions.manage_guild:
			return

		perms = ctx.guild.me.permissions_in(ctx.channel)
		if not perms.send_messages:
			return

		if ctx.guild.id not in greet_toggle:
			try:
				c.execute("INSERT INTO MemberPresence (Guild, GreetChannel, GreetToggle) VALUES ('" + str(ctx.guild.id) + "', '" + str(ctx.channel.id) + "', '1')")
				conn.commit()
			except sqlite3.IntegrityError:
				c.execute("UPDATE MemberPresence SET GreetToggle = '1', GreetChannel = '" + str(ctx.channel.id) + "' WHERE Guild = '" + str(ctx.guild.id) + "'")
				conn.commit()
			greet_channel[ctx.guild.id] = ctx.channel.id
			greet_toggle.append(ctx.guild.id)
			await ctx.send(content = '<:check:314349398811475968> **Greet messages enabled in this channel.**')
		else:
			c.execute("UPDATE MemberPresence SET GreetToggle = NULL WHERE Guild = " + str(ctx.guild.id))
			conn.commit()
			greet_toggle.remove(ctx.guild.id)
			await ctx.send(content = '<:check:314349398811475968> **Greet messages disabled.**')

	@commands.command()
	async def greetdel(self, ctx, duration):
		if not ctx.guild or not ctx.author.guild_permissions.manage_guild:
			return

		perms = ctx.guild.me.permissions_in(ctx.channel)
		if not perms.send_messages:
			return

		try:
			duration = int(duration)
		except:
			return

		if duration < 10 and duration != 0:
			return await ctx.send(content = '<:xmark:314349398824058880> **The length of the duration must not be less than 10 seconds.**')
		elif duration > 120:
			return await ctx.send(content = '<:xmark:314349398824058880> **The length of the duration must not be over 2 minutes.**')

		if duration == 0:
			try:
				c.execute("INSERT INTO MemberPresence (Guild, GreetDuration) VALUES ('" + str(ctx.guild.id) + "', NULL)")
				conn.commit()
			except sqlite3.IntegrityError:
				c.execute("UPDATE MemberPresence SET GreetDuration = NULL WHERE Guild = " + str(ctx.guild.id))
				conn.commit()
			if ctx.guild.id in greet_duration.keys():
				del greet_duration[ctx.guild.id]
			await ctx.send(content = '<:check:314349398811475968> **Disabled automatic deletion of greet messages.**')
		else:
			try:
				c.execute("INSERT INTO MemberPresence (Guild, GreetDuration) VALUES ('" + str(ctx.guild.id) + "', '" + str(duration) + "')")
				conn.commit()
			except sqlite3.IntegrityError:
				c.execute("UPDATE MemberPresence SET GreetDuration = '" + str(duration) + "' WHERE Guild = " + str(ctx.guild.id))
				conn.commit()
			greet_duration[ctx.guild.id] = duration
			await ctx.send(content = '<:check:314349398811475968> **Greet messages will now be automatically deleted after ' + str(duration) + ' seconds.**')

	@commands.command()
	async def byemsg(self, ctx, *, msg = None):
		if not msg:
			if ctx.guild.id not in leave_message.keys():
				await ctx.send(embed = discord.Embed(title = 'Current Leave Message', description = default_bye, color = 0x28B463))
			else:
				await ctx.send(embed = discord.Embed(title = 'Current Leave Message', description = leave_message[ctx.guild.id], color = 0x28B463))
		else:
			if not ctx.guild or not ctx.author.guild_permissions.manage_guild:
				return

			perms = ctx.guild.me.permissions_in(ctx.channel)
			if not perms.send_messages:
				return

			try:
				c.execute("INSERT INTO MemberPresence (Guild, LeaveMsg) VALUES ('" + str(ctx.guild.id) + "', '" + str(msg).replace('\'', '\'\'') + "')")
				conn.commit()
			except sqlite3.IntegrityError:
				c.execute("UPDATE MemberPresence SET LeaveMsg = '" + str(msg).replace('\'', '\'\'') + "' WHERE Guild = '" + str(ctx.guild.id) + "'")
				conn.commit()
			leave_message[ctx.guild.id] = str(msg)

			await ctx.send(content = '<:check:314349398811475968> **New leave message set.**')

	@commands.command()
	async def bye(self, ctx):
		if not ctx.guild or not ctx.author.guild_permissions.manage_guild:
			return

		perms = ctx.guild.me.permissions_in(ctx.channel)
		if not perms.send_messages:
			return

		if ctx.guild.id not in leave_toggle:
			try:
				c.execute("INSERT INTO MemberPresence (Guild, LeaveChannel, LeaveToggle) VALUES ('" + str(ctx.guild.id) + "', '" + str(ctx.channel.id) + "', '1')")
				conn.commit()
			except sqlite3.IntegrityError:
				c.execute("UPDATE MemberPresence SET LeaveToggle = '1', LeaveChannel = '" + str(ctx.channel.id) + "' WHERE Guild = '" + str(ctx.guild.id) + "'")
				conn.commit()
			leave_channel[ctx.guild.id] = ctx.channel.id
			leave_toggle.append(ctx.guild.id)
			await ctx.send(content = '<:check:314349398811475968> **Leave messages enabled in this channel.**')
		else:
			c.execute("UPDATE MemberPresence SET LeaveToggle = NULL WHERE Guild = " + str(ctx.guild.id))
			conn.commit()
			leave_toggle.remove(ctx.guild.id)
			await ctx.send(content = '<:check:314349398811475968> **Leave messages disabled.**')

	@commands.command()
	async def byedel(self, ctx, duration):
		if not ctx.guild or not ctx.author.guild_permissions.manage_guild:
			return

		perms = ctx.guild.me.permissions_in(ctx.channel)
		if not perms.send_messages:
			return

		try:
			duration = int(duration)
		except:
			return

		if duration < 10 and duration != 0:
			return await ctx.send(content = '<:xmark:314349398824058880> **The length of the duration must not be less than 10 seconds.**')
		elif duration > 120:
			return await ctx.send(content = '<:xmark:314349398824058880> **The length of the duration must not be over 2 minutes.**')

		if duration == 0:
			try:
				c.execute("INSERT INTO MemberPresence (Guild, LeaveDuration) VALUES ('" + str(ctx.guild.id) + "', NULL)")
				conn.commit()
			except sqlite3.IntegrityError:
				c.execute("UPDATE MemberPresence SET LeaveDuration = NULL WHERE Guild = " + str(ctx.guild.id))
				conn.commit()
			if ctx.guild.id in leave_duration.keys():
				del leave_duration[ctx.guild.id]
			await ctx.send(content = '<:check:314349398811475968> **Disabled automatic deletion of leave messages.**')
		else:
			try:
				c.execute("INSERT INTO MemberPresence (Guild, LeaveDuration) VALUES ('" + str(ctx.guild.id) + "', '" + str(duration) + "')")
				conn.commit()
			except sqlite3.IntegrityError:
				c.execute("UPDATE MemberPresence SET LeaveDuration = '" + str(duration) + "' WHERE Guild = " + str(ctx.guild.id))
				conn.commit()
			leave_duration[ctx.guild.id] = duration
			await ctx.send(content = '<:check:314349398811475968> **Leave messages will now be automatically deleted after ' + str(duration) + ' seconds.**')

	@commands.command()
	async def greetdmmsg(self, ctx, *, msg = None):
		if not msg:
			if ctx.guild.id not in greet_dm_message.keys():
				await ctx.send(embed = discord.Embed(title = 'Current Greet DM Message', description = default_greet, color = 0x28B463))
			else:
				await ctx.send(embed = discord.Embed(title = 'Current Greet DM Message', description = greet_dm_message[ctx.guild.id], color = 0x28B463))
		else:
			if not ctx.guild or not ctx.author.guild_permissions.manage_guild:
				return

			perms = ctx.guild.me.permissions_in(ctx.channel)
			if not perms.send_messages:
				return

			try:
				c.execute("INSERT INTO MemberPresence (Guild, DMMsg) VALUES ('" + str(ctx.guild.id) + "', '" + str(msg).replace('\'', '\'\'') + "')")
				conn.commit()
			except sqlite3.IntegrityError:
				c.execute("UPDATE MemberPresence SET DMMsg = '" + str(msg).replace('\'', '\'\'') + "' WHERE Guild = '" + str(ctx.guild.id) + "'")
				conn.commit()
			greet_dm_message[ctx.guild.id] = str(msg)

			await ctx.send(content = '<:check:314349398811475968> **New greet DM message set.**')

	@commands.command()
	async def greetdm(self, ctx):
		if not ctx.guild or not ctx.author.guild_permissions.manage_guild:
			return

		perms = ctx.guild.me.permissions_in(ctx.channel)
		if not perms.send_messages:
			return

		if ctx.guild.id not in greet_dm_toggle:
			try:
				c.execute("INSERT INTO MemberPresence (Guild, DMToggle) VALUES ('" + str(ctx.guild.id) + "', '1')")
				conn.commit()
			except sqlite3.IntegrityError:
				c.execute("UPDATE MemberPresence SET DMToggle = '1' WHERE Guild = '" + str(ctx.guild.id) + "'")
				conn.commit()
			greet_dm_toggle.append(ctx.guild.id)
			await ctx.send(content = '<:check:314349398811475968> **Greet DM messages enabled.**')
		else:
			c.execute("UPDATE MemberPresence SET DMToggle = NULL WHERE Guild = " + str(ctx.guild.id))
			conn.commit()
			greet_dm_toggle.remove(ctx.guild.id)
			await ctx.send(content = '<:check:314349398811475968> **Greet DM messages disabled.**')


def setup(bot):
	bot.add_cog(MemberPresence(bot))

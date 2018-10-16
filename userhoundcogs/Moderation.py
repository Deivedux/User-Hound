import discord
import datetime
import sqlite3
import random
import asyncio
from discord.ext import commands

conn = sqlite3.connect('HoundBot.db')
c = conn.cursor()

mute_roles_raw = c.execute("SELECT * FROM MuteRoles").fetchall()
mute_roles = {}
for i in mute_roles_raw:
	mute_roles[int(i[0])] = int(i[1])

muted_users_raw = c.execute("SELECT * FROM MutedUsers").fetchall()
muted_users = {}
for i in muted_users_raw:
	try:
		muted_users[int(i[0])].append(int(i[1]))
	except KeyError:
		muted_users[int(i[0])] = [int(i[1])]

report_channels_raw = c.execute("SELECT * FROM ReportChannels").fetchall()
report_channels = {}
for i in report_channels_raw:
	report_channels[int(i[0])] = int(i[1])

voice_roles_raw = c.execute("SELECT * FROM VoiceRoles").fetchall()
voice_roles = {}
for i in voice_roles_raw:
	try:
		voice_roles[int(i[0])][int(i[1])] = int(i[2])
	except KeyError:
		voice_roles[int(i[0])] = {int(i[1]): int(i[2])}
del voice_roles_raw

member_persistance_raw = c.execute("SELECT * FROM MemberPersistanceGuilds").fetchall()
member_persistance = []
for i in member_persistance_raw:
	member_persistance.append(int(i[0]))
del member_persistance_raw

del mute_roles_raw
del muted_users_raw
del report_channels_raw

banned_user = []

class Moderation:
	def __init__(self, bot):
		self.bot = bot

	async def on_voice_state_update(self, member, before, after):
		if before.channel != after.channel:
			if before.channel:
				if member.guild.id in voice_roles.keys() and before.channel.id in voice_roles[member.guild.id].keys():
					role = discord.utils.get(member.guild.roles, id = voice_roles[member.guild.id][before.channel.id])
					if not role:
						c.execute("DELETE FROM VoiceRoles WHERE Role = " + str(voice_roles[member.guild.id][before.channel.id]))
						conn.commit()
						del voice_roles[member.guild.id][before.channel.id]
					else:
						await member.remove_roles(role)

			if after.channel:
				if member.guild.id in voice_roles.keys() and after.channel.id in voice_roles[member.guild.id].keys():
					role = discord.utils.get(member.guild.roles, id = voice_roles[member.guild.id][after.channel.id])
					if not role:
						c.execute("DELETE FROM VoiceRoles WHERE Role = " + str(voice_roles[member.guild.id][after.channel.id]))
						conn.commit()
						del voice_roles[member.guild.id][after.channel.id]
					else:
						await member.add_roles(role)

	async def on_member_ban(self, guild, user):
		if not user.bot and guild.id in member_persistance:
			banned_user.append(user.id)

	async def on_member_remove(self, member):
		if not member.bot and member.guild.id in member_persistance:
			await asyncio.sleep(0.1)
			if member.id in banned_user:
				banned_user.remove(member.id)
				return

			roles = []
			for role in member.roles:
				if role != member.guild.default_role:
					roles.append(str(role.id))

			member_roles = None
			if roles:
				member_roles = '|'.join(roles)

			if member_roles and member.nick:
				c.execute("INSERT INTO MemberPersistanceUsers (User, Guild, Roles, Nick) VALUES ('" + str(member.id) + "', '" + str(member.guild.id) + "', '" + str(member_roles) + "', '" + str(member.nick).replace('\'', '\'\'') + "')")
				conn.commit()
			elif member_roles:
				c.execute("INSERT INTO MemberPersistanceUsers (User, Guild, Roles) VALUES ('" + str(member.id) + "', '" + str(member.guild.id) + "', '" + str(member_roles) + "')")
				conn.commit()
			elif member.nick:
				c.execute("INSERT INTO MemberPersistanceUsers (User, Guild, Nick) VALUES ('" + str(member.id) + "', '" + str(member.guild.id) + "', '" + str(member.nick).replace('\'', '\'\'') + "')")
				conn.commit()

	async def on_member_join(self, member):
		if not member.bot and member.guild.id in member_persistance:
			member_persistance_raw = c.execute("SELECT * FROM MemberPersistanceUsers WHERE Guild = '" + str(member.guild.id) + "' AND User = " + str(member.id)).fetchone()
			if member_persistance_raw != None:
				my_role = None
				for role in member.guild.me.roles:
					if role.permissions.manage_roles or role.permissions.administrator:
						my_role = role
						break

				roles = []

				for i in member_persistance_raw[2].split('|'):
					role = discord.utils.get(member.guild.roles, id = int(i))
					if role != None and role < my_role:
						roles.append(role)

				if member.guild.id in muted_users.keys():
					if member.id in muted_users[member.guild.id]:
						role = discord.utils.get(member.guild.roles, id = mute_roles[member.guild.id])
						if role == None and role < my_role:
							c.execute("DELETE FROM MuteRoles WHERE Guild = " + str(member.guild.id))
							conn.commit()
							del mute_roles[member.guild.id]
						else:
							if role not in role:
								roles.append(role)

				if member.guild.id in voice_roles.keys():
					for i in voice_roles[member.guild.id].values():
						role = discord.utils.get(member.guild.roles, id = i)
						if role != None and role in roles:
							roles.remove(role)

				await member.edit(roles = roles, nick = member_persistance_raw[3], reason = '[ Member Persistance ]')

				c.execute("DELETE FROM MemberPersistanceUsers WHERE Guild = '" + str(member.guild.id) + "' AND User = " + str(member.id))
				conn.commit()
		elif member.guild.id in muted_users.keys():
			if member.id in muted_users[member.guild.id]:
				role = discord.utils.get(member.guild.roles, id = mute_roles[member.guild.id])
				if role == None:
					c.execute("DELETE FROM MuteRoles WHERE Guild = " + str(member.guild.id))
					conn.commit()
					del mute_roles[member.guild.id]
				else:
					await member.add_roles(role, reason = '[ Attempted Mute Evade ]')

	async def on_raw_reaction_add(self, payload):
		if str(payload.emoji) in ['❌', '👢', '🔨', '🔇'] and payload.guild_id in report_channels.keys() and payload.channel_id == report_channels[payload.guild_id]:
			guild = self.bot.get_guild(payload.guild_id)
			user = guild.get_member(payload.user_id)
			channel = guild.get_channel(payload.channel_id)
			msg = await channel.get_message(payload.message_id)
			if not user.bot and msg.author == self.bot.user:
				if str(payload.emoji) == '❌' and user.guild_permissions.ban_members:
					pass
				elif str(payload.emoji) == '👢' and user.guild_permissions.kick_members:
					report = c.execute("SELECT * FROM ReportMembers WHERE Message = " + str(payload.message_id)).fetchone()
					if report == None:
						return

					user_role = None
					for role in user.roles:
						if role != guild.default_role and (role.permissions.kick_members or role.permissions.administrator):
							user_role = role
							break

					member = guild.get_member(int(report[1]))
					if member == None:
						pass
					else:
						if user == guild.owner:
							pass
						elif user_role == None or user_role <= member.top_role:
							return

						embed = discord.Embed(title = 'You were Kicked', color = 0xD4AC0D, timestamp = datetime.datetime.utcnow())
						embed.add_field(name = 'Server', value = str(guild))
						embed.add_field(name = 'Moderator', value = str(user))
						embed.add_field(name = 'Reason', value = report[3])
						embed.set_thumbnail(url = guild.icon_url)
						try:
							await member.send(embed = embed)
						except discord.Forbidden:
							pass

						try:
							await member.kick(reason = report[3])
						except discord.Forbidden:
							return
				elif str(payload.emoji) == '🔨' and user.guild_permissions.ban_members:
					report = c.execute("SELECT * FROM ReportMembers WHERE Message = " + str(payload.message_id)).fetchone()
					if report == None:
						return

					user_role = None
					for role in user.roles:
						if role != guild.default_role and (role.permissions.ban_members or role.permissions.administrator):
							user_role = role
							break

					member = guild.get_member(int(report[1]))
					if member == None:
						member = self.bot.get_user(int(report[1]))
						if member == None:
							member = await self.bot.get_user_info(int(report[1]))

						await guild.ban(member, reason = report[3])
					else:
						if user == guild.owner:
							pass
						elif user_role == None or user_role <= member.top_role:
							return

						embed = discord.Embed(title = 'You were Banned', color = 0xD4AC0D, timestamp = datetime.datetime.utcnow())
						embed.add_field(name = 'Server', value = str(guild))
						embed.add_field(name = 'Moderator', value = str(user))
						embed.add_field(name = 'Reason', value = report[3])
						embed.set_thumbnail(url = guild.icon_url)
						try:
							await member.send(embed = embed)
						except discord.Forbidden:
							pass

						try:
							await member.ban(reason = report[3])
						except discord.Forbidden:
							return
				elif str(payload.emoji) == '🔇' and user.guild_permissions.mute_members:
					report = c.execute("SELECT * FROM ReportMembers WHERE Message = " + str(payload.message_id)).fetchone()
					if report == None:
						return

					user_role = None
					for role in user.roles:
						if role != guild.default_role and (role.permissions.mute_members or role.permissions.administrator):
							user_role = role
							break

					member = guild.get_member(int(report[1]))
					if member == None:
						pass
					else:
						if user == guild.owner:
							pass
						elif user_role == None or user_role <= member.top_role:
							return

						role_raw = c.execute("SELECT Role FROM MuteRoles WHERE Guild = " + str(payload.guild_id)).fetchone()
						if role_raw == None:
							return
						else:
							role = discord.utils.get(guild.roles, id = int(role_raw[0]))
							try:
								await member.add_roles(role, reason = report[3])
							except discord.Forbidden:
								return

							c.execute("INSERT INTO MutedUsers (Guild, User) VALUES ('" + str(payload.guild_id) + "', '" + str(member.id) + "')")
							conn.commit()
							try:
								muted_users[payload.guild_id].append(member.id)
							except KeyError:
								muted_users[payload.guild_id] = [member.id]

							embed = discord.Embed(title = 'You were Muted', color = 0xD4AC0D, timestamp = datetime.datetime.utcnow())
							embed.add_field(name = 'Server', value = str(guild))
							embed.add_field(name = 'Moderator', value = str(user))
							embed.add_field(name = 'Reason', value = report[3])
							embed.set_thumbnail(url = guild.icon_url)
							try:
								await member.send(embed = embed)
							except discord.Forbidden:
								pass
				else:
					return

				c.execute("DELETE FROM ReportMembers WHERE Message = " + str(payload.message_id))
				conn.commit()

				await msg.delete()

	@commands.command(aliases = ['mods'])
	async def moderators(self, ctx):
		online = []
		idle = []
		dnd = []
		offline = []

		for member in ctx.guild.members:
			if member.bot:
				continue

			if (member.guild_permissions.kick_members or member.guild_permissions.ban_members) and member.status == discord.Status.online:
				online.append('**' + str(member) + '**')
			elif (member.guild_permissions.kick_members or member.guild_permissions.ban_members) and member.status == discord.Status.idle:
				idle.append('**' + str(member) + '**')
			elif (member.guild_permissions.kick_members or member.guild_permissions.ban_members) and member.status == discord.Status.dnd:
				dnd.append('**' + str(member) + '**')
			elif (member.guild_permissions.kick_members or member.guild_permissions.ban_members) and member.status == discord.Status.offline:
				offline.append('**' + str(member) + '**')

		if len(online) == 0:
			online.append('None')
		if len(idle) == 0:
			idle.append('None')
		if len(dnd) == 0:
			dnd.append('None')
		if len(offline) == 0:
			offline.append('None')

		await ctx.send(content = '**List of available moderators:**\n<:online2:464520569975603200> ' + ', '.join(online) + '\n<:away2:464520569862357002> ' + ', '.join(idle) + '\n<:dnd2:464520569560498197> ' + ', '.join(dnd) + '\n<:offline2:464520569929334784> ' + ', '.join(offline))

	@commands.command(aliases = ['memberpersist'])
	async def memberpersistance(self, ctx):
		if not ctx.guild or not ctx.author.guild_permissions.manage_guild:
			return

		if not ctx.guild.me.guild_permissions.manage_roles or not ctx.guild.me.guild_permissions.manage_nicknames:
			return await ctx.send(content = '<:xmark:314349398824058880> **I need the `Manage Roles` and `Manage Nicknames` permissions before I can persist member rejoins.**')

		try:

			c.execute("INSERT INTO MemberPersistanceGuilds (Guild) VALUES ('" + str(ctx.guild.id) + "')")
			conn.commit()
			member_persistance.append(ctx.guild.id)

			await ctx.send(content = '<:check:314349398811475968> **Member Persistance enabled.**')

		except sqlite3.IntegrityError:

			c.execute("DELETE FROM MemberPersistanceGuilds WHERE Guild = " + str(ctx.guild.id))
			conn.commit()
			member_persistance.remove(ctx.guild.id)

			await ctx.send(content = '<:check:314349398811475968> **Member Persistance disabled.**')

			c.execute("DELETE FROM MemberPersistanceUsers WHERE Guild = " + str(ctx.guild.id))
			conn.commit()

	@commands.command(aliases = ['k'])
	async def kick(self, ctx, member: discord.Member, *, reason = None):
		if not ctx.guild or not ctx.author.guild_permissions.kick_members:
			return

		if not ctx.guild.me.guild_permissions.kick_members:
			return await ctx.send(content = '<:xmark:314349398824058880> **I do not have `Kick Members` permission.**')

		if ctx.author == ctx.guild.owner:
			pass
		else:
			perm_role = None
			for role in ctx.author.roles:
				if role != ctx.guild.default_role and (role.permissions.kick_members or role.permissions.administrator):
					perm_role = role
					break

			if perm_role == None:
				return
			elif ctx.guild.me.top_role <= member.top_role:
				return await ctx.send(content = '<:xmark:314349398824058880> **I do not have permission to kick that member.**')
			elif perm_role <= member.top_role:
				return await ctx.send(content = '<:xmark:314349398824058880> **You do not have permission to kick that member.**')

		if reason:
			if len(reason) > 512:
				return await ctx.send(content = '<:xmark:314349398824058880> **Reason must not be longer than 512 characters.**')

		embed = discord.Embed(title = 'You were Kicked', color = 0xD4AC0D, timestamp = datetime.datetime.utcnow())
		embed.add_field(name = 'Server', value = str(ctx.guild))
		embed.add_field(name = 'Moderator', value = str(ctx.author))
		if reason:
			embed.add_field(name = 'Reason', value = reason)
		embed.set_thumbnail(url = ctx.guild.icon_url)
		try:
			await member.send(embed = embed)
		except discord.Forbidden:
			pass

		await member.kick(reason = reason)

		embed = discord.Embed(title = 'Member Kicked', color = 0xD4AC0D)
		embed.add_field(name = 'Name', value = str(member))
		embed.add_field(name = 'ID', value = str(member.id))
		if reason:
			embed.add_field(name = 'For', value = reason)
		embed.set_thumbnail(url = member.avatar_url)
		await ctx.send(embed = embed)

	@commands.command(aliases = ['sb'])
	async def softban(self, ctx, member: discord.Member, *, reason = None):
		if not ctx.guild or not ctx.author.guild_permissions.kick_members or not ctx.author.guild_permissions.manage_messages:
			return

		if not ctx.guild.me.guild_permissions.ban_members:
			return await ctx.send(content = '<:xmark:314349398824058880> **I do not have `Ban Members` permission.**')

		if ctx.author == ctx.guild.owner:
			pass
		else:
			perm_role = None
			for role in ctx.author.roles:
				if role != ctx.guild.default_role and ((role.permissions.kick_members and role.permissions.manage_messages) or role.permissions.administrator):
					perm_role = role
					break

			if perm_role == None:
				return
			elif ctx.guild.me.top_role <= member.top_role:
				return await ctx.send(content = '<:xmark:314349398824058880> **I do not have permission to softban that member.**')
			elif perm_role <= member.top_role:
				return await ctx.send(content = '<:xmark:314349398824058880> **You do not have permission to softban that member.**')

		if reason:
			if len(reason) > 512:
				return await ctx.send(content = 'Reason must not be longer than 512 characters.')

		embed = discord.Embed(title = 'You were Softbanned', color = 0xD4AC0D, timestamp = datetime.datetime.utcnow())
		embed.add_field(name = 'Server', value = str(ctx.guild))
		embed.add_field(name = 'Moderator', value = str(ctx.author))
		if reason:
			embed.add_field(name = 'Reason', value = reason)
		embed.set_thumbnail(url = ctx.guild.icon_url)
		try:
			await member.send(embed = embed)
		except discord.Forbidden:
			pass

		await member.ban(reason = reason, delete_message_days = 1)

		embed = discord.Embed(title = 'Member Softbanned', color = 0xD4AC0D)
		embed.add_field(name = 'Name', value = str(member))
		embed.add_field(name = 'ID', value = str(member.id))
		if reason:
			embed.add_field(name = 'For', value = reason)
		embed.set_thumbnail(url = member.avatar_url)
		await ctx.send(embed = embed)

		await member.unban(reason = reason)

	@commands.command(aliases = ['b'])
	async def ban(self, ctx, member: discord.Member, *, reason = None):
		if not ctx.guild or not ctx.author.guild_permissions.ban_members:
			return

		if not ctx.guild.me.guild_permissions.ban_members:
			return await ctx.send(content = '<:xmark:314349398824058880> **I do not have `Ban Members` permission.**')

		if ctx.author == ctx.guild.owner:
			pass
		else:
			perm_role = None
			for role in ctx.author.roles:
				if role != ctx.guild.default_role and (role.permissions.ban_members or role.permissions.administrator):
					perm_role = role
					break

			if perm_role == None:
				return
			elif ctx.guild.me.top_role <= member.top_role:
				return await ctx.send(content = '<:xmark:314349398824058880> **I do not have permission to ban that member.**')
			elif perm_role <= member.top_role:
				return await ctx.send(content = '<:xmark:314349398824058880> **You do not have permission to ban that member.**')

		if reason:
			if len(reason) > 512:
				return await ctx.send(content = 'Reason must not be longer than 512 characters.')

		embed = discord.Embed(title = 'You were Banned', color = 0xD4AC0D, timestamp = datetime.datetime.utcnow())
		embed.add_field(name = 'Server', value = str(ctx.guild))
		embed.add_field(name = 'Moderator', value = str(ctx.author))
		if reason:
			embed.add_field(name = 'Reason', value = reason)
		embed.set_thumbnail(url = ctx.guild.icon_url)
		try:
			await member.send(embed = embed)
		except discord.Forbidden:
			pass

		await member.ban(reason = reason, delete_message_days = 7)

		embed = discord.Embed(title = 'Member Banned', color = 0xD4AC0D)
		embed.add_field(name = 'Name', value = str(member))
		embed.add_field(name = 'ID', value = str(member.id))
		if reason:
			embed.add_field(name = 'For', value = reason)
		embed.set_thumbnail(url = member.avatar_url)
		await ctx.send(embed = embed)

	@commands.command(aliases = ['hb'])
	async def hackban(self, ctx, member_id, *, reason = None):
		if not ctx.guild or not ctx.author.guild_permissions.ban_members:
			return

		if not ctx.guild.me.guild_permissions.ban_members:
			return await ctx.send(content = '<:xmark:314349398824058880> **I do not have `Ban Members` permission.**')

		user = self.bot.get_user(int(member_id))
		if user == None:
			try:
				user = await self.bot.get_user_info(int(member_id))
			except discord.NotFound:
				return await ctx.send(embed = discord.Embed(description = 'That ID does not belong to any user.', color = 0xCB4335))

		if user in ctx.guild.members:
			return await ctx.send(embed = discord.Embed(description = 'The user with the following ID is currently in this server. Please use `!ban` instead.', color = 0xCB4335))

		if reason:
			if len(reason) > 512:
				return await ctx.send(embed = discord.Embed(description = 'Reason must not be longer than 512 characters.', color = 0xCB4335))

		await ctx.guild.ban(user, reason = reason, delete_message_days = 7)

		embed = discord.Embed(title = 'Member Hackbanned', color = 0xD4AC0D)
		embed.add_field(name = 'Name', value = str(user))
		embed.add_field(name = 'ID', value = str(user.id))
		if reason:
			embed.add_field(name = 'For', value = reason)
		embed.set_thumbnail(url = user.avatar_url)
		await ctx.send(embed = embed)

	@commands.command()
	async def prune(self, ctx, action = None):
		perms = ctx.author.permissions_in(ctx.channel)
		if not ctx.guild or not perms.manage_messages:
			return

		perms = ctx.guild.me.permissions_in(ctx.channel)
		if not perms.manage_messages:
			return await ctx.send(content = '<:xmark:314349398824058880> **I do not have `Manage Messages` permission in this channel.**')

		messages = []

		if not action:
			async for message in ctx.channel.history(limit = 100):
				messages.append(message)
		else:
			try:

				action = int(action.replace('<', '').replace('!', '').replace('@', '').replace('>', ''))
				member = ctx.guild.get_member(action)
				if member != None:
					async for message in ctx.channel.history(limit = 100):
						if message.author == member and not message.pinned:
							messages.append(message)
				elif action <= 100:
					async for message in ctx.channel.history(limit = action + 1):
						messages.append(message)
				else:
					return

			except ValueError:

				if action.lower() == 'bots':
					messages.append(ctx.message)
					async for message in ctx.channel.history(limit = 100):
						if message.author.bot and not message.pinned:
							messages.append(message)
				elif action.lower() == 'embeds':
					messages.append(ctx.message)
					async for message in ctx.channel.history(limit = 100):
						if message.embeds and not message.pinned:
							messages.append(message)
				elif action.lower() == 'files':
					messages.append(ctx.message)
					async for message in ctx.channel.history(limit = 100):
						if message.attachments and not message.pinned:
							messages.append(message)
				elif action.lower() == 'self':
					messages.append(ctx.message)
					async for message in ctx.channel.history(limit = 100):
						if message.author == self.bot.user and not message.pinned:
							messages.append(message)
				else:
					return

		await ctx.channel.delete_messages(messages)
		await ctx.send(content = '♻ **Deleted ' + str(len(messages) - 1) + ' messages.**', delete_after = 2)

	@commands.command(aliases = ['kv'])
	async def kickvoice(self, ctx, *, channel: discord.VoiceChannel):
		if not ctx.guild or not ctx.author.guild_permissions.move_members:
			return

		if not ctx.guild.me.guild_permissions.manage_channels or not ctx.guild.me.guild_permissions.move_members:
			return await ctx.send(content = '<:xmark:314349398824058880> **I need `Manage Channels` and `Move Members` permissions to do that.**')

		async with ctx.channel.typing():
			overwrites = {ctx.guild.default_role: discord.PermissionOverwrite(read_messages = False, speak = False), ctx.guild.me: discord.PermissionOverwrite(read_messages = True)}
			v_channel = await ctx.guild.create_voice_channel('Temporary', overwrites = overwrites, category = channel.category)

			members = len(channel.members)
			for member in channel.members:
				await member.move_to(v_channel)

			await v_channel.delete()
			await ctx.send(content = 'Kicked **' + str(members) + '** members from **' + channel.name + '**.')

	@commands.command()
	async def mute(self, ctx, member: discord.Member, *, reason = None):
		if not ctx.guild or not ctx.author.guild_permissions.mute_members:
			return

		if member.bot:
			return await ctx.send(embed = discord.Embed(description = 'I\'d rather not clog my database by keeping *bots* muted...', color = 0xCB4335))

		if not ctx.guild.me.guild_permissions.manage_roles:
			return await ctx.send(content = '<:xmark:314349398824058880> **I do not have `Manage Roles` permission.**')

		if reason:
			if len(reason) > 512:
				return await ctx.send(content = '<:xmark:314349398824058880> **Reason must not be longer than 512 characters.**')

		if ctx.guild.id in muted_users.keys():
			if member.id in muted_users[ctx.guild.id]:
				return await ctx.send(content = '<:xmark:314349398824058880> **That user is already in my database of this server\'s muted members.**')

		if ctx.guild.id not in mute_roles.keys():
			await ctx.send(embed = discord.Embed(description = 'You first need to tell me which role you want me to treat as the *mute role* with `!setmuterole`.', color = 0xD4AC0D))
		else:
			role = discord.utils.get(ctx.guild.roles, id = mute_roles[ctx.guild.id])
			if role == None:
				c.execute("DELETE FROM MuteRoles WHERE Guild = " + str(ctx.guild.id))
				conn.commit()
				del mute_roles[ctx.guild.id]
				await ctx.send(content = '⚠ **It appears that the set mute role no longer exists in this server. Because of that, I am deleting it from my database.**')
			else:
				c.execute("INSERT INTO MutedUsers (Guild, User) VALUES ('" + str(ctx.guild.id) + "', '" + str(member.id) + "')")
				conn.commit()
				try:
					muted_users[ctx.guild.id].append(member.id)
				except KeyError:
					muted_users[ctx.guild.id] = [member.id]

				await member.add_roles(role, reason = reason)

				embed = discord.Embed(title = 'Member Muted', color = 0xD4AC0D)
				embed.add_field(name = 'Name', value = str(member))
				embed.add_field(name = 'ID', value = str(member.id))
				if reason:
					embed.add_field(name = 'For', value = reason)
				embed.set_thumbnail(url = member.avatar_url)
				await ctx.send(embed = embed)

				embed = discord.Embed(title = 'You were Muted', color = 0xD4AC0D, timestamp = datetime.datetime.utcnow())
				embed.add_field(name = 'Server', value = str(ctx.guild))
				embed.add_field(name = 'Moderator', value = str(ctx.author))
				if reason:
					embed.add_field(name = 'Reason', value = reason)
				embed.set_thumbnail(url = ctx.guild.icon_url)
				try:
					await member.send(embed = embed)
				except discord.Forbidden:
					pass

	@commands.command()
	async def unmute(self, ctx, member: discord.Member, *, reason = None):
		if not ctx.guild or not ctx.author.guild_permissions.mute_members:
			return

		if not ctx.guild.me.guild_permissions.manage_roles:
			return await ctx.send(content = '<:xmark:314349398824058880> **I do not have `Manage Roles` permission.**')

		if reason:
			if len(reason) > 512:
				return await ctx.send(content = '<:xmark:314349398824058880> **Reason must not be longer than 512 characters.**')

		if ctx.guild.id not in muted_users.keys():
			return await ctx.send(content = '<:xmark:314349398824058880> **That user is not muted.**')
		else:
			if member.id not in muted_users[ctx.guild.id]:
				return await ctx.send(content = '<:xmark:314349398824058880> **That user is not muted.**')

		if ctx.guild.id not in mute_roles.keys():
			await ctx.send(embed = discord.Embed(description = 'You first need to tell me which role you want me to treat as the *mute role* with `!setmuterole`.', color = 0xD4AC0D))
		else:
			role = discord.utils.get(ctx.guild.roles, id = mute_roles[ctx.guild.id])
			if role == None:
				c.execute("DELETE FROM MuteRoles WHERE Guild = " + str(ctx.guild.id))
				conn.commit()
				del mute_roles[ctx.guild.id]
				await ctx.send(content = '⚠ **It appears that the set mute role no longer exists in this server. Because of that, I will delete it from my database.**')
			else:
				c.execute("DELETE FROM MutedUsers WHERE Guild = '" + str(ctx.guild.id) + "' AND User = '" + str(member.id) + "'")
				conn.commit()
				muted_users[ctx.guild.id].remove(member.id)

				await member.remove_roles(role, reason = reason)

				embed = discord.Embed(title = 'Member Unmuted', color = 0xD4AC0D)
				embed.add_field(name = 'Name', value = str(member))
				embed.add_field(name = 'ID', value = str(member.id))
				if reason:
					embed.add_field(name = 'For', value = reason)
				embed.set_thumbnail(url = member.avatar_url)
				await ctx.send(embed = embed)

				embed = discord.Embed(title = 'You were Unmuted', color = 0xD4AC0D, timestamp = datetime.datetime.utcnow())
				embed.add_field(name = 'Server', value = str(ctx.guild))
				embed.add_field(name = 'Moderator', value = str(ctx.author))
				if reason:
					embed.add_field(name = 'Reason', value = reason)
				embed.set_thumbnail(url = ctx.guild.icon_url)
				try:
					await member.send(embed = embed)
				except discord.Forbidden:
					pass

	@commands.command()
	async def mutelist(self, ctx):
		c.execute("SELECT User FROM MutedUsers WHERE Guild = " + str(ctx.guild.id))
		mutes_raw = c.fetchall()
		mutes = []
		for i in mutes_raw:
			mutes.append(int(i[0]))

		muted_members = []
		for i in mutes:
			member = ctx.guild.get_member(i)
			if member == None:
				continue
			else:
				muted_members.append(str(member) + ' (' + str(member.id) + ')')

		embed = discord.Embed(title = 'Muted Members', description = '\n'.join(muted_members), color = 0xD4AC0D)
		embed.set_footer(text = 'This list does not include members who are not currently in the server, but they are still in my database of this server\'s muted members.')
		await ctx.send(embed = embed)

	@commands.command()
	async def setmuterole(self, ctx, *, role_name):
		if not ctx.guild or not ctx.author.guild_permissions.manage_roles:
			return

		role = discord.utils.get(ctx.guild.roles, name = role_name)
		if role == None:
			await ctx.send(content = '<:xmark:314349398824058880> **I could not find a role with that name.**')
		else:
			try:
				c.execute("INSERT INTO MuteRoles (Guild, Role) VALUES ('" + str(ctx.guild.id) + "', '" + str(role.id) + "')")
				conn.commit()
				mute_roles[ctx.guild.id] = role.id
				await ctx.send(content = '<:check:314349398811475968> **Muted role set.**')
			except sqlite3.IntegrityError:
				c.execute("UPDATE MuteRoles SET Role = '" + str(role.id) + "' WHERE Guild = " + str(ctx.guild.id))
				conn.commit()
				mute_roles[ctx.guild.id] = role.id
				await ctx.send(content = '<:check:314349398811475968> **Muted role set.**')

	@commands.command(aliases = ['vcrole'])
	async def voicerole(self, ctx, *, role: discord.Role = None):
		if not ctx.guild or not ctx.author.guild_permissions.manage_roles:
			return

		if not ctx.author.voice:
			await ctx.send(content = '<:xmark:314349398824058880> **You must be in the voice channel to run this command.**')
		else:
			if role:
				try:
					c.execute("INSERT INTO VoiceRoles (Guild, Channel, Role) VALUES ('" + str(ctx.guild.id) + "', '" + str(ctx.author.voice.channel.id) + "', '" + str(role.id) + "')")
					conn.commit()
				except sqlite3.IntegrityError:
					c.execute("UPDATE VoiceRoles SET Role = '" + str(role.id) + "' WHERE Channel = " + str(ctx.author.voice.channel.id))
					conn.commit()

				try:
					voice_roles[ctx.guild.id][ctx.author.voice.channel.id] = role.id
				except KeyError:
					voice_roles[ctx.guild.id] = {ctx.author.voice.channel.id: role.id}

				await ctx.send(content = '<:check:314349398811475968> **Voice role set for channel `' + str(ctx.author.voice.channel) + '`.**')
			else:
				c.execute("DELETE FROM VoiceRoles WHERE Channel = " + str(ctx.author.voice.channel.id))
				conn.commit()
				del voice_roles[ctx.guild.id][ctx.author.voice.channel.id]

				await ctx.send(content = '<:check:314349398811475968> **Voice role removed for channel `' + str(ctx.author.voice.channel) + '`.**')

	@commands.command()
	async def voiceroles(self, ctx):
		roles = []
		if ctx.guild.id not in voice_roles.keys():
			await ctx.send(embed = discord.Embed(title = 'Voice Roles', color = 0x28B463))
		else:
			for i in voice_roles[ctx.guild.id].keys():
				channel = ctx.guild.get_channel(i)
				role = discord.utils.get(ctx.guild.roles, id = voice_roles[ctx.guild.id][i])
				if not channel or not role:
					c.execute("DELETE FROM VoiceRoles WHERE Channel = " + str(i))
					conn.commit()
					del voice_roles[ctx.guild.id][i]
					roles.append('*Channel or role no longer exist.*')
				else:
					roles.append('\\🔊 **' + str(channel) + '**  ->  <@&' + str(role.id) + '>')

			await ctx.send(embed = discord.Embed(title = 'Voice Roles', description = '\n'.join(roles), color = 0x28B463))

	@commands.command(aliases = ['setreportchan'])
	async def setreportchannel(self, ctx, channel: discord.TextChannel = None):
		if not ctx.guild or not ctx.author.guild_permissions.manage_guild:
			return

		if channel:

			perms = ctx.guild.me.permissions_in(channel)
			if not perms.send_messages or not perms.embed_links or not perms.read_messages or not perms.add_reactions:
				return await ctx.send(content = '<:xmark:314349398824058880> **I do not have enough permissions to send messages in ' + channel.mention + '.**')

			try:
				c.execute("INSERT INTO ReportChannels (Guild, Channel) VALUES ('" + str(ctx.guild.id) + "', '" + str(channel.id) + "')")
				conn.commit()
			except IntegrityError:
				c.execute("UPDATE ReportChannels SET Channel = '" + str(channel.id) + "' WHERE Guild = " + str(ctx.guild.id))
				conn.commit()
			report_channels[ctx.guild.id] = channel.id

			await channel.send(content = '**__Reports channel set. Manual guide:__\n\n• For best performance, make sure that no one, but me and your staff, is able to send messages in this channel. A private channel is recommended that non-staff members can\'t see.\n• Please do not chat in this channel, as I need to be able to find the message to which reaction was added. If the message is too far flooded by other messages, I will not be able to find the message, which is what I\'m relying into to identify the report.\n• Please do __not__ manually delete my messages regarding member reports, as it is meant to be fully reliable with my database.\n• Messages are safely deleted by me whenever necessary (usually after staff takes action to the report).**\n\n*You may delete __this__ message whenever.*')
			await ctx.send(content = '<:check:314349398811475968> **Reports channel set.**')

		else:

			c.execute("DELETE FROM ReportChannels WHERE Guild = " + str(ctx.guild.id))
			conn.commit()
			del report_channels[ctx.guild.id]

			await ctx.send(content = '<:check:314349398811475968> **Reports disabled.**')

	@commands.command()
	async def reportmember(self, ctx, member: discord.Member, *, reason = None):
		if ctx.guild.id not in report_channels:
			return await ctx.send(content = '<:xmark:314349398824058880> **This server has not set up member reports.**')

		if not reason:
			await ctx.send(content = '<:xmark:314349398824058880> **Please provide a reason and/or any evidence of your report.**')
		else:
			reports_raw = c.execute("SELECT Offender FROM ReportMembers WHERE Guild = " + str(ctx.guild.id)).fetchall()
			reports = []
			for i in reports_raw:
				reports.append(int(i[0]))
			if member.id in reports:
				return await ctx.send(content = '<:xmark:314349398824058880> **There is already a pending report on that user.**')

			embed = discord.Embed(title = 'Reported User', color = 0x2471A3)
			embed.add_field(name = 'User', value = member.mention + ' (' + str(member) + ')')
			embed.add_field(name = 'Reporter', value = ctx.author.mention + ' (' + str(ctx.author) + ')')
			embed.add_field(name = 'Reason', value = reason, inline = False)
			embed.add_field(name = 'Staff Action Required', value = '🔇 - Mute\n👢 - Kick\n🔨 - Ban\n❌ - Decline', inline = False)

			channel = self.bot.get_channel(report_channels[ctx.guild.id])
			msg = await channel.send(embed = embed)

			await ctx.send(content = '<:check:314349398811475968> **Report sent. A staff member will investigate your report shortly.**')

			c.execute("INSERT INTO ReportMembers (Guild, Offender, Reporter, Reason, Message) VALUES ('" + str(ctx.guild.id) + "', '" + str(member.id) + "', '" + str(ctx.author.id) + "', '" + str(reason).replace('\'', '\'\'') + "', '" + str(msg.id) + "')")
			conn.commit()

			await msg.add_reaction(emoji = '🔇')
			await msg.add_reaction(emoji = '👢')
			await msg.add_reaction(emoji = '🔨')
			await msg.add_reaction(emoji = '❌')


def setup(bot):
	bot.add_cog(Moderation(bot))

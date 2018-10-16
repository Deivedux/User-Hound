import discord
import sqlite3
import datetime
import asyncio
import random
from discord.ext import commands

conn = sqlite3.connect('HoundBot.db')
c = conn.cursor()

ratelimit = {}

nickreq_channels_raw = c.execute("SELECT * FROM NickReqChannels").fetchall()
nickreq_channels = {}
for i in nickreq_channels_raw:
	nickreq_channels[int(i[0])] = int(i[1])
del nickreq_channels_raw

class Main:
	def __init__(self, bot):
		self.bot = bot

	async def on_raw_reaction_add(self, payload):
		if str(payload.emoji) in ['❌', '✅'] and payload.guild_id in nickreq_channels.keys() and payload.channel_id == nickreq_channels[payload.guild_id]:
			guild = self.bot.get_guild(payload.guild_id)
			user = guild.get_member(payload.user_id)
			channel = guild.get_channel(payload.channel_id)
			msg = await channel.get_message(payload.message_id)
			if not user.bot and msg.author == self.bot.user and user.guild_permissions.manage_nicknames:
				if str(payload.emoji) == '❌':
					pass
				elif str(payload.emoji) == '✅':
					req = c.execute("SELECT * FROM NickReqs WHERE Message = " + str(payload.message_id)).fetchone()
					if req == None:
						return

					user_role = None
					for role in user.roles:
						if role != guild.default_role and (role.permissions.manage_nicknames or role.permissions.administrator):
							user_role = role
							break

					member = guild.get_member(int(req[1]))
					if member == None:
						msg_confirm = await channel.send(content = '**' + user.mention + ', it appears that the member that requested this nickname has left the server. Do you want to __cancel__ their request instead or __wait__ until they will join back?**')
						def check(m):
							return m.author == user and m.channel == channel and m.content.lower() in ['cancel', 'wait']

						try:
							confirm = await self.bot.wait_for('message', check = check, timeout = 120)
						except asyncio.TimeoutError:
							return await msg_confirm.delete()

						if confirm.content.lower() == 'wait':
							return await channel.delete_messages([msg_confirm, confirm])
						elif confirm.content.lower() == 'cancel':
							await channel.delete_messages([msg_confirm, confirm])
					else:
						if user == guild.owner:
							pass
						elif user_role == None or user_role <= member.top_role:
							return

						try:
							await member.edit(nick = req[2])
						except discord.Forbidden:
							return await channel.send(content = '<:xmark:314349398824058880> **I do not have enough permissions to change that user\'s nickname in this server.**', delete_after = 7)
				else:
					return

				c.execute("DELETE FROM NickReqs WHERE Message = " + str(payload.message_id))
				conn.commit()

				await msg.delete()

	@commands.command()
	async def lookup(self, ctx, user_id):
		try:
			user_id = int(user_id.replace('<', '').replace('@', '').replace('!', '').replace('>', ''))
		except:
			return await ctx.send(content = '<:xmark:314349398824058880> **Please enter a valid ID or a user mention.**')

		if ctx.author.id in ratelimit.keys():
			if len(ratelimit[ctx.author.id]) == 2:
				return await ctx.send(content = ':octagonal_sign: **You can use lookup-related commands 2 times in 20 seconds.**', delete_after = 5)

		try:
			ratelimit[ctx.author.id].append(ctx.message.id)
		except KeyError:
			ratelimit[ctx.author.id] = [ctx.message.id]

		msg = await ctx.send(content = '<a:loading:460897928051949568>')
		user = self.bot.get_user(user_id)
		if user == None:
			try:
				user = await self.bot.get_user_info(user_id)
			except discord.NotFound:
				await msg.edit(content = '<:xmark:314349398824058880> **This ID does not belong to any user.**')
				await asyncio.sleep(20)
				ratelimit[ctx.author.id].remove(ctx.message.id)
				if len(ratelimit[ctx.author.id]) == 0:
					del ratelimit[ctx.author.id]
				return

		total_rating = c.execute("SELECT Rating FROM UserRating WHERE User = " + str(user_id)).fetchall()
		positive_rating = []
		negative_rating = []
		for i in total_rating:
			if i[0] == '1':
				positive_rating.append(i)
			elif i[0] == '0':
				negative_rating.append(i)

		servers = []
		for guild in self.bot.guilds:
			if user in guild.members:
				servers.append(guild)

		embed = discord.Embed(title = 'Normal User')
		embed.add_field(name = 'Name', value = user.name + '#' + user.discriminator)
		embed.add_field(name = 'ID', value = str(user.id))
		embed.add_field(name = 'Joined Discord At', value = user.created_at)
		embed.add_field(name = 'Is Bot', value = str(user.bot))
		embed.add_field(name = 'Mutual Servers', value = str(len(servers)))
		embed.add_field(name = 'Uprates / Downrates', value = '**' + str(len(positive_rating)) + '** / **' + str(len(negative_rating)) + '**', inline = False)
		embed.set_thumbnail(url = user.avatar_url)
		await msg.edit(content = None, embed = embed)
		await asyncio.sleep(20)
		ratelimit[ctx.author.id].remove(ctx.message.id)
		if len(ratelimit[ctx.author.id]) == 0:
			del ratelimit[ctx.author.id]

	@commands.command()
	async def uprate(self, ctx, user_id):
		try:
			user_id = int(user_id.replace('<', '').replace('@', '').replace('!', '').replace('>', ''))
		except:
			return await ctx.send(content = '<:xmark:314349398824058880> **Please enter a valid ID or a user mention.**')

		if user_id == ctx.author.id:
			return await ctx.send(content = '<:xmark:314349398824058880> **You can\'t rate yourself.**')

		if ctx.author.id in ratelimit.keys():
			if len(ratelimit[ctx.author.id]) == 2:
				return await ctx.send(content = ':octagonal_sign: **You can use lookup-related commands 2 times in 20 seconds.**', delete_after = 5)

		try:
			ratelimit[ctx.author.id].append(ctx.message.id)
		except KeyError:
			ratelimit[ctx.author.id] = [ctx.message.id]

		msg = await ctx.send(content = '<a:loading:460897928051949568>')
		user = self.bot.get_user(user_id)
		if user == None:
			try:
				user = await self.bot.get_user_info(user_id)
			except discord.NotFound:
				await msg.edit(content = '<:xmark:314349398824058880> **This ID does not belong to any user.**')
				await asyncio.sleep(20)
				ratelimit[ctx.author.id].remove(ctx.message.id)
				if len(ratelimit[ctx.author.id]) == 0:
					del ratelimit[ctx.author.id]
				return

		user_rate = c.execute("SELECT User FROM UserRating WHERE Issuer = " + str(ctx.author.id)).fetchall()
		if str(user_id) not in str(user_rate):
			c.execute("INSERT INTO UserRating (User, Rating, Issuer) VALUES ('" + str(user_id) + "', '1', '" + str(ctx.author.id) + "')")
			conn.commit()
		else:
			c.execute("UPDATE UserRating SET Rating = '1' WHERE Issuer = '" + str(ctx.author.id) + "' AND User = '" + str(user_id) + "'")
			conn.commit()

		embed = discord.Embed(title = 'Uprated', description = str(user), color = 0x28B463)
		embed.set_thumbnail(url = user.avatar_url)
		await msg.edit(content = None, embed = embed)

		await asyncio.sleep(20)
		ratelimit[ctx.author.id].remove(ctx.message.id)
		if len(ratelimit[ctx.author.id]) == 0:
			del ratelimit[ctx.author.id]

	@commands.command()
	async def downrate(self, ctx, user_id):
		try:
			user_id = int(user_id.replace('<', '').replace('@', '').replace('!', '').replace('>', ''))
		except:
			return await ctx.send(content = '<:xmark:314349398824058880> **Please enter a valid ID or a user mention.**')

		if ctx.author.id in ratelimit.keys():
			if len(ratelimit[ctx.author.id]) == 2:
				return await ctx.send(content = ':octagonal_sign: **You can use lookup-related commands 2 times in 20 seconds.**', delete_after = 5)

		if user_id == ctx.author.id:
			return await ctx.send(content = '<:xmark:314349398824058880> **You can\'t rate yourself.**')

		try:
			ratelimit[ctx.author.id].append(ctx.message.id)
		except KeyError:
			ratelimit[ctx.author.id] = [ctx.message.id]

		msg = await ctx.send(content = '<a:loading:460897928051949568>')
		user = self.bot.get_user(user_id)
		if user == None:
			try:
				user = await self.bot.get_user_info(user_id)
			except discord.NotFound:
				await msg.edit(content = '<:xmark:314349398824058880> **This ID does not belong to any user.**')
				await asyncio.sleep(20)
				ratelimit[ctx.author.id].remove(ctx.message.id)
				if len(ratelimit[ctx.author.id]) == 0:
					del ratelimit[ctx.author.id]
				return

		user_rate = c.execute("SELECT User FROM UserRating WHERE Issuer = " + str(ctx.author.id)).fetchall()
		if str(user_id) not in str(user_rate):
			c.execute("INSERT INTO UserRating (User, Rating, Issuer) VALUES ('" + str(user_id) + "', '0', '" + str(ctx.author.id) + "')")
			conn.commit()
		else:
			c.execute("UPDATE UserRating SET Rating = '0' WHERE Issuer = '" + str(ctx.author.id) + "' AND User = '" + str(user_id) + "'")
			conn.commit()

		embed = discord.Embed(title = 'Downrated', description = str(user), color = 0xCB4335)
		embed.set_thumbnail(url = user.avatar_url)
		await msg.edit(content = None, embed = embed)

		await asyncio.sleep(20)
		ratelimit[ctx.author.id].remove(ctx.message.id)
		if len(ratelimit[ctx.author.id]) == 0:
			del ratelimit[ctx.author.id]

	@commands.command(aliases = ['randserv'])
	async def randomserver(self, ctx):
		if not ctx.guild:
			pass
		else:
			perms = ctx.guild.me.permissions_in(ctx.channel)
			if not perms.send_messages:
				return

		opted_in = c.execute("SELECT Guild FROM OptIn").fetchall()
		servers = []
		for i in opted_in:
			servers.append(int(i[0]))

		invite = None
		while len(servers) > 0:
			random_server = random.choice(servers)
			guild = self.bot.get_guild(random_server)
			if guild == None or guild == ctx.guild:
				servers.remove(random_server)
				continue
			for channel in guild.text_channels:
				try:
					invite = await channel.create_invite(reason = '!randserv', max_age = 300, max_uses = 1)
					break
				except discord.Forbidden:
					pass
			if invite != None:
				break
			servers.remove(random_server)

		if invite != None:
			try:
				await ctx.author.send(content = invite)
				await ctx.send(content = ':mailbox_with_mail: **Check your Direct Messages.**')
			except discord.Forbidden:
				await ctx.send(content = '<:xmark:314349398824058880> **Please enable Direct Messages and try again.**')
		else:
			await ctx.send(content = 'No server is currently opt-in, or all servers that are did not give me permission to create invites to any of their text channels.')

	@commands.command()
	async def banlog(self, ctx):
		if ctx.author.id == 415570038175825930 or ctx.author.id == 145878866429345792:
			pass
		elif not ctx.guild or not ctx.author.guild_permissions.manage_guild:
			return

		perms = ctx.guild.me.permissions_in(ctx.channel)
		if not perms.send_messages:
			return

		try:
			c.execute("INSERT INTO Logging (Guild, Channel) VALUES ('" + str(ctx.guild.id) + "', '" + str(ctx.channel.id) + "')")
			conn.commit()
			await ctx.send(content = '<:check:314349398811475968> **I will alert this channel when a globally banned user joins this server.**\n\nIn the meantime, please support the service, free of charge, by upvoting me on **<https://discordbots.org/bot/461914170028326913/vote>**.')
		except sqlite3.IntegrityError:
			c.execute("DELETE FROM Logging WHERE Guild = " + str(ctx.guild.id))
			conn.commit()
			await ctx.send(content = '<:check:314349398811475968> **I will no longer post global ban related notifications.**')

	@commands.command()
	async def opt(self, ctx):
		if not ctx.guild or not ctx.author.guild_permissions.manage_guild:
			return

		perms = ctx.guild.me.permissions_in(ctx.channel)
		if not perms.send_messages:
			return

		try:
			c.execute("INSERT INTO OptIn (Guild) VALUES ('" + str(ctx.guild.id) + "')")
			conn.commit()
			await ctx.send(content = '<:check:314349398811475968> **This server has been Opt-in.**')
		except sqlite3.IntegrityError:
			c.execute("DELETE FROM OptIn WHERE Guild = " + str(ctx.guild.id))
			conn.commit()
			await ctx.send(content = '<:check:314349398811475968> **This server has been Opt-out.**')

	@commands.command()
	async def setnickchannel(self, ctx, channel: discord.TextChannel = None):
		if not ctx.guild or not ctx.author.guild_permissions.manage_guild:
			return

		if channel:

			perms = ctx.guild.me.permissions_in(channel)
			if not perms.send_messages or not perms.embed_links or not perms.read_messages or not perms.add_reactions:
				return await ctx.send(content = '<:xmark:314349398824058880> **I do not have one or more permissions in ' + channel.mention + ':\n• Read Messages\n• Send Messages\n• Embed Links\n• Add Reactions**')

			try:
				c.execute("INSERT INTO NickReqChannels (Guild, Channel) VALUES ('" + str(ctx.guild.id) + "', '" + str(channel.id) + "')")
				conn.commit()
			except sqlite3.IntegrityError:
				c.execute("UPDATE NickReqChannels SET Channel = '" + str(channel.id) + "' WHERE Guild = " + str(ctx.guild.id))
				conn.commit()
			nickreq_channels[ctx.guild.id] = channel.id

			await channel.send(content = '**__Nick requests channel set. Manual guide:__\n\n• For best performance, make sure that no one, but me, is able to send messages in this channel. A private channel is recommended that non-staff members can\'t see.\n• Please do __not__ manually delete my messages regarding nickname requests, as it is meant to be fully reliable with my database.\n• Messages are safely deleted by me whenever necessary (usually after staff takes action to the request).**\n\n*You may delete __this__ message whenever.*')
			await ctx.send(content = '<:check:314349398811475968> **Nick requests channel has been set to ' + channel.mention + '.**')

		else:

			c.execute("DELETE FROM NickReqChannels WHERE Guild = " + str(ctx.guild.id))
			conn.commit()
			del nickreq_channels[ctx.guild.id]

			await ctx.send(content = '<:check:314349398811475968> **Nick requests disabled.**')

			c.execute("DELETE FROM NickReqs WHERE Guild = " + str(ctx.guild.id))
			conn.commit()

	@commands.command(aliases = ['nickreq'])
	async def nickrequest(self, ctx, *, nick = None):
		if ctx.guild.id not in nickreq_channels.keys():
			return await ctx.send(content = '<:xmark:314349398824058880> **This server is not set up for nick requests.**')

		if ctx.author.guild_permissions.change_nickname:
			return await ctx.send(content = '<:xmark:314349398824058880> **No need for a nick request if you can do it yourself.**')

		if not nick:
			await ctx.send(content = '<:xmark:314349398824058880> **Please provide a nickname you want to request.**')
		elif len(nick) > 32 or '\n' in nick:
			await ctx.send(content = '<:xmark:314349398824058880> **A nickname must not be longer than 32 characters and containt new lines.**')
		else:
			reqs_raw = c.execute("SELECT User FROM NickReqs WHERE Guild = " + str(ctx.guild.id)).fetchall()
			reqs = []
			for i in reqs_raw:
				reqs.append(int(i[0]))
			if ctx.author.id in reqs:
				return await ctx.send(content = '<:xmark:314349398824058880> **You already have a pending nick request in this server.**')

			embed = discord.Embed(title = 'Nick Request', color = 0x2471A3)
			embed.add_field(name = 'User', value = ctx.author.mention + ' (' + str(ctx.author) + ')', inline = False)
			embed.add_field(name = 'From', value = ctx.author.display_name)
			embed.add_field(name = 'To', value = nick)
			embed.add_field(name = 'Staff Action Required', value = '✅ - Accept\n❌ - Decline', inline = False)

			channel = self.bot.get_channel(nickreq_channels[ctx.guild.id])
			msg = await channel.send(embed = embed)

			await ctx.send(content = '<:check:314349398811475968> **Nick request sent. A staff member will review it shortly.**')

			c.execute("INSERT INTO NickReqs (Guild, User, Nick, Message) VALUES ('" + str(ctx.guild.id) + "', '" + str(ctx.author.id) + "', '" + str(nick).replace('\'', '\'\'') + "', '" + str(msg.id) + "')")
			conn.commit()

			await msg.add_reaction(emoji = '✅')
			await msg.add_reaction(emoji = '❌')


def setup(bot):
	bot.add_cog(Main(bot))

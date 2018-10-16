import discord
import sqlite3
import asyncio
import time
from discord.ext import commands

conn = sqlite3.connect('HoundBot.db')
c = conn.cursor()

announce_limit = []

prefixes_raw = c.execute("SELECT * FROM Prefixes").fetchall()
global prefixes
prefixes = {}
for i in prefixes_raw:
	prefixes[int(i[0])] = str(i[1])
del prefixes_raw

class Utility:
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def prefix(self, ctx, *, prefix = None):
		if not ctx.guild:
			return

		if not prefix:

			try:
				guild_prefix = prefixes[ctx.guild.id]
			except KeyError:
				guild_prefix = '-'

			await ctx.send(content = '**My prefix here is `' + guild_prefix + '`.**')

		else:

			if not ctx.author.guild_permissions.administrator:
				return

			if len(prefix) > 5 or '\n' in prefix:
				return await ctx.send(content = '<:xmark:314349398824058880> **Invalid prefix format. Make sure of the following:\n• Prefix is not over 5 characters long.\n• Prefix does not contain new lines.**')

			try:
				c.execute("INSERT INTO Prefixes (Guild, Prefix) VALUES ('" + str(ctx.guild.id) + "', '" + str(prefix).replace('\'', '\'\'') + "')")
				conn.commit()
			except sqlite3.IntegrityError:
				c.execute("UPDATE Prefixes SET Prefix = '" + str(prefix).replace('\'', '\'\'') + "' WHERE Guild = " + str(ctx.guild.id))
				conn.commit()
			prefixes[ctx.guild.id] = prefix

			await ctx.send(content = '<:check:314349398811475968> **Prefix changed to `' + prefix + '`.**')

	@commands.command(aliases = ['uinfo'])
	async def userinfo(self, ctx, *, member: discord.Member = None):
		if not member:
			member = ctx.author

		if member.status == discord.Status.online:
			user_status = '<:online2:464520569975603200> **Online**'
		elif member.status == discord.Status.idle:
			user_status = '<:away2:464520569862357002> **Away**'
		elif member.status == discord.Status.dnd:
			user_status = '<:dnd2:464520569560498197> **Do not Disturb**'
		elif member.status == discord.Status.offline:
			user_status = '<:offline2:464520569929334784> **Offline**'

		roles = []
		for role in ctx.guild.role_hierarchy:
			if role in member.roles:
				roles.append('<@&' + str(role.id) + '>')
		del roles[-1]

		embed = discord.Embed(title = 'About Member', color = 0x28B463)
		embed.add_field(name = 'User', value = str(member))
		embed.add_field(name = 'ID', value = str(member.id))
		if member.nick:
			embed.add_field(name = 'Nickname', value = str(member.nick))
		embed.add_field(name = 'Status', value = user_status)
		embed.add_field(name = 'Joined At', value = member.joined_at)
		if roles:
			embed.add_field(name = 'Roles', value = ', '.join(roles))
		embed.set_thumbnail(url = member.avatar_url)

		await ctx.send(embed = embed)

	@commands.command(aliases = ['av'])
	async def avatar(self, ctx, member: discord.Member = None):
		if not member:
			member = ctx.author

		await ctx.send(embed = discord.Embed(title = str(member), color = 0x28B463).set_image(url = member.avatar_url))

	@commands.command(aliases = ['sinfo'])
	async def serverinfo(self, ctx):
		if ctx.guild.verification_level == discord.VerificationLevel.none:
			verification = 0
		elif ctx.guild.verification_level == discord.VerificationLevel.low:
			verification = 1
		elif ctx.guild.verification_level == discord.VerificationLevel.medium:
			verification = 2
		elif ctx.guild.verification_level == discord.VerificationLevel.high:
			verification = 3
		elif ctx.guild.verification_level == discord.VerificationLevel.extreme:
			verification = 4

		member_bots = []
		for member in ctx.guild.members:
			if member.bot:
				member_bots.append(member)

		if ctx.guild.mfa_level == 1:
			fa_level = '<:check:314349398811475968> Enabled'
		else:
			fa_level = '<:xmark:314349398824058880> Disabled'

		if ctx.guild.explicit_content_filter == discord.ContentFilter.disabled:
			content_filter = '<:xmark:314349398824058880> Disabled'
		elif ctx.guild.explicit_content_filter == discord.ContentFilter.no_role:
			content_filter = '<:empty:314349398723264512> No Roles'
		elif ctx.guild.explicit_content_filter == discord.ContentFilter.all_members:
			content_filter = '<:check:314349398811475968> Enabled'

		embed = discord.Embed(title = 'About Server', color = 0x28B463, timestamp = ctx.guild.created_at)
		embed.add_field(name = 'Name', value = str(ctx.guild))
		embed.add_field(name = 'ID', value = str(ctx.guild.id))
		embed.add_field(name = 'Owner', value = str(ctx.guild.owner))
		embed.add_field(name = 'Verification', value = '**Level:** ' + str(verification))
		embed.add_field(name = 'Region', value = str(ctx.guild.region))
		embed.add_field(name = 'Is Large', value = str(ctx.guild.large))
		embed.add_field(name = '2FA Requirement', value = str(fa_level))
		embed.add_field(name = 'Content Filter', value = str(content_filter))
		embed.add_field(name = 'Members', value = '**Users:** ' + str(ctx.guild.member_count - len(member_bots)) + '\n**Bots:** ' + str(len(member_bots)) + '\n**Total:** ' + str(ctx.guild.member_count))
		embed.add_field(name = 'Channels', value = '**Text:** ' + str(len(ctx.guild.text_channels)) + '\n**Voice:** ' + str(len(ctx.guild.voice_channels)))
		embed.set_thumbnail(url = ctx.guild.icon_url)
		embed.set_footer(text = 'Created At')

		await ctx.send(embed = embed)

	@commands.command(aliases = ['asar'])
	async def addselfassignrole(self, ctx, *, role: discord.Role):
		if not ctx.guild or not ctx.author.guild_permissions.manage_roles:
			return

		guild_roles = c.execute("SELECT Role FROM SelfAssignableRoles WHERE Guild = " + str(ctx.guild.id)).fetchall()
		roles = []
		for i in guild_roles:
			roles.append(int(i[0]))

		if role.id not in roles:
			c.execute("INSERT INTO SelfAssignableRoles (Guild, Role) VALUES ('" + str(ctx.guild.id) + "', '" + str(role.id) + "')")
			conn.commit()
			await ctx.send(content = '<:check:314349398811475968> **Role `' + str(role) + '` added.**')
		else:
			await ctx.send(content = '<:xmark:314349398824058880> **That role is already self-assignable.**')

	@commands.command(aliases = ['rsar'])
	async def removeselfassignrole(self, ctx, *, role: discord.Role):
		if not ctx.guild or not ctx.author.guild_permissions.manage_roles:
			return

		guild_roles = c.execute("SELECT Role FROM SelfAssignableRoles WHERE Guild = " + str(ctx.guild.id)).fetchall()
		roles = []
		for i in guild_roles:
			roles.append(int(i[0]))

		if role.id in roles:
			c.execute("DELETE FROM SelfAssignableRoles WHERE Role = " + str(role.id))
			conn.commit()
			await ctx.send(content = '<:check:314349398811475968> **Role `' + str(role) + '` removed.**')
		else:
			await ctx.send(content = '<:xmark:314349398824058880> **That role is not self-assignable.**')

	@commands.command(aliases = ['lsar'])
	async def listselfassignroles(self, ctx):
		guild_roles = c.execute("SELECT Role FROM SelfAssignableRoles WHERE Guild = " + str(ctx.guild.id)).fetchall()
		roles = []
		for i in guild_roles:
			role = discord.utils.get(ctx.guild.roles, id = int(i[0]))
			if role == None:
				c.execute("DELETE FROM SelfAssignableRoles WHERE Role = " + str(role.id))
				conn.commit()
			else:
				roles.append(str(role) + ' (' + str(role.id) + ')')

		await ctx.send(embed = discord.Embed(title = 'List of Self-assignable roles', description = '\n'.join(roles), color = 0x28B463))

	@commands.command(aliases = ['gr'])
	async def giverole(self, ctx, *, role: discord.Role):
		guild_roles = c.execute("SELECT Role FROM SelfAssignableRoles WHERE Guild = " + str(ctx.guild.id)).fetchall()
		roles = []
		for i in guild_roles:
			roles.append(int(i[0]))

		if role.id in roles:
			await ctx.author.add_roles(role)
			await ctx.send(content = '<:check:314349398811475968> **Assigned `' + str(role) + '` role.**')

	@commands.command(aliases = ['rr'])
	async def removerole(self, ctx, *, role: discord.Role):
		guild_roles = c.execute("SELECT Role FROM SelfAssignableRoles WHERE Guild = " + str(ctx.guild.id)).fetchall()
		roles = []
		for i in guild_roles:
			roles.append(int(i[0]))

		if role.id in roles:
			await ctx.author.remove_roles(role)
			await ctx.send(content = '<:check:314349398811475968> **Removed `' + str(role) + '` role.**')

	@commands.command()
	async def setannounce(self, ctx, channel: discord.TextChannel, *, role: discord.Role):
		if not ctx.guild or not ctx.author.guild_permissions.manage_guild:
			return

		try:
			c.execute("INSERT INTO AnnouncementChannels (Guild, Channel, Role) VALUES ('" + str(ctx.guild.id) + "', '" + str(channel.id) + "', '" + str(role.id) + "')")
			conn.commit()
		except sqlite3.IntegrityError:
			c.execute("UPDATE AnnouncementChannels SET Channel = '" + str(channel.id) + "', Role = '" + str(role.id) + "' WHERE Guild = " + str(ctx.guild.id))
			conn.commit()

		await ctx.send(content = '<:check:314349398811475968> **Set ' + channel.mention + ' channel and `' + str(role) + '` role as tools for announcements.**')

	@commands.command()
	async def announce(self, ctx, *, msg):
		if not ctx.guild or not ctx.author.guild_permissions.mention_everyone:
			return

		if ctx.guild.id in announce_limit:
			return await ctx.send(content = '<:xmark:314349398824058880> **Announcements are limited to a message per 10 minutes to avoid spam/abuse.**')

		announce = c.execute("SELECT * FROM AnnouncementChannels WHERE Guild = " + str(ctx.guild.id)).fetchone()
		if announce == None:
			await ctx.send(content = '<:xmark:314349398824058880> **This server is not set up for announcements yet.**')
		else:
			role = discord.utils.get(ctx.guild.roles, id = int(announce[2]))
			if role == None:
				return await ctx.send(content = '<:xmark:314349398824058880> **It seems like the set announcements role no longer exists. Please set a new one.**')

			channel = self.bot.get_channel(int(announce[1]))
			if channel == None:
				return await ctx.send(content = '<:xmark:314349398824058880> **It seems like the set announcements channel no longer exists. Please set a new one.**')
			perms = ctx.guild.me.permissions_in(channel)
			if not perms.send_messages or not perms.embed_links:
				return await ctx.send(content = '<:xmark:314349398824058880> **I seem to be limited from posting messages to the announcement channel. Please check my permissions and try again.**')

			try:
				await role.edit(mentionable = True)
			except discord.Forbidden:
				return await ctx.send(content = '<:xmark:314349398824058880> **I require to have necessary permissions in order to edit the `' + str(role) + '` role.**')

			if ctx.author.colour != discord.Colour.default():
				embed = discord.Embed(description = msg, color = ctx.author.color)
			else:
				embed = discord.Embed(description = msg)
			embed.set_author(name = str(ctx.author), icon_url = ctx.author.avatar_url)
			if ctx.message.attachments:
				embed.set_image(url = ctx.message.attachments[0].url)
			await channel.send(content = role.mention, embed = embed)

			announce_limit.append(ctx.guild.id)

			await role.edit(mentionable = False)

			await ctx.send(content = '<:check:314349398811475968> **Announcement successfully sent.**')

			await asyncio.sleep(600)
			announce_limit.remove(ctx.guild.id)


def setup(bot):
	bot.add_cog(Utility(bot))

import discord
import sqlite3
from discord.ext import commands

conn = sqlite3.connect('HoundBot.db')
c = conn.cursor()

verify_channels = {}

c.execute("SELECT * FROM ServerVerification")
channel_raw = c.fetchall()
for i in channel_raw:
	verify_channels[int(i[0])] = [int(i[2]), int(i[1])]
del channel_raw

class Verification:
	def __init__(self, bot):
		self.bot = bot

	async def on_message(self, message):
		if message.guild and message.guild.id in verify_channels.keys():
			if message.channel.id == verify_channels[message.guild.id][0]:
				perms = message.author.permissions_in(message.channel)
				if not perms.manage_messages:
					await message.delete()

	@commands.command()
	async def verification(self, ctx, *, role_name = None):
		if not ctx.guild or not ctx.author.guild_permissions.administrator:
			return

		perms = ctx.guild.me.permissions_in(ctx.channel)
		if not perms.send_messages:
			return

		if not role_name:
			return
		elif role_name == 'off':
			c.execute("DELETE FROM ServerVerification WHERE Guild = " + str(ctx.guild.id))
			conn.commit()
			del verify_channels[ctx.guild.id]
			await ctx.send(content = '**Verification disabled.**')
		else:
			if not ctx.guild.me.permissions_in(ctx.channel).manage_messages or not ctx.guild.me.guild_permissions.manage_roles:
				return await ctx.send(content = 'Before enabling this feature, make sure I have ALL of the following permissions:\n\n• **Manage Roles**\n• **Manage Messages** (at least only in this channel)\n\nMake sure that the role you want me to assign after `!agree` is below my highest role with Manage Roles permission in role hierarchy.')

			role = discord.utils.get(ctx.guild.roles, name = role_name)
			if role == None:
				return await ctx.send(content = 'I did not find the role with this name. Please check if there are\'t any typos.')

			try:
				c.execute("INSERT INTO ServerVerification (Guild, Role, Channel) VALUES ('" + str(ctx.guild.id) + "', '" + str(role.id) + "', '" + str(ctx.channel.id) + "')")
				conn.commit()
				verify_channels[ctx.guild.id] = [ctx.channel.id, role.id]
				await ctx.send(content = '**Verification enabled in this channel.**\n\n• Every new message sent here will be deleted, unless it was sent by member with Manage Messages permission.\n• `!agree` command enabled in this channel. Generaly servers use this to enforce people to agree to their server rules before gaining full access to the server.\n• Do note that I will be ASSIGNING your provided role to users after `!agree`, not REMOVING it. There are many reasons why it is better to do this way. Join my support server if you want to know those reasons.\n• Manual role permissions configuration is required. For example: make sure that members __without__ this role can not chat in other channels but here, and the opposite for __with__ the role.\n• Type `!verification off` to disable.\n\nDelete these unnecessary messages once you are done reading them.')
			except sqlite3.IntegrityError:
				return await ctx.send(content = 'This server already has verification enabled. Type `!verification off` to disable it.')

	@commands.command()
	async def agree(self, ctx):
		if ctx.guild.id in verify_channels.keys():
			if ctx.channel.id == verify_channels[ctx.guild.id][0]:
				role = discord.utils.get(ctx.guild.roles, id = verify_channels[ctx.guild.id][1])
				if role != None:
					await ctx.author.add_roles(role)
				else:
					c.execute("DELETE FROM ServerVerification WHERE Guild = " + str(ctx.guild.id))
					conn.commit()
					verify_channels.remove(ctx.channel.id)
					await ctx.send(content = ctx.guild.owner.mention + ', it seems that the role I need to assign after `-agree` no longer exists.\n\n**Verification disabled.**')


def setup(bot):
	bot.add_cog(Verification(bot))

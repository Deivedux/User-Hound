import discord

class AntiBotFarm:
	def __init__(self, bot):
		self.bot = bot

	'''
	This file is dedicated to comparing normal servers
	with bot-farm servers, and leaving them if they are
	exceeding the bot percentage ratio against the
	total amount of members.

	Bot-farm servers are considered to be the most annoying
	and resource heavy servers, since all their dedication
	is to add as many bots as they can and (possibly) spam
	their commands "for fun", and maybe even intentionally
	make them be stuck in a some sort of loop, whether it
	is by responding to other bots, or spam the commands
	so much that they never stop responding with the same
	message.

	This bot is already made to prevent itself from
	responding to other bots, so this file is just an
	external secondary way to prevent users from "abusing"
	the bots.
	'''

	async def on_ready(self):
		for guild in self.bot.guilds:
			bots = 0
			for member in guild.members:
				if member.bot:
					bots+=1

			result = guild.member_count - bots
			if result > 70.0:
				await guild.leave()

	async def on_member_join(self, member):
		bots = 0
		for member in member.guild.members:
			if member.bot:
				bots+=1

		result = member.guild.member_count - bots
		if result > 70.0:
			await member.guild.leave()

	async def on_member_remove(self, member):
		bots = 0
		for member in member.guild.members:
			if member.bot:
				bots+=1

		result = member.guild.member_count - bots
		if result > 70.0:
			await member.guild.leave()


def setup(bot):
	bot.add_cog(AntiBotFarm(bot))

import discord
import sqlite3
import asyncio
from discord.ext import commands

conn = sqlite3.connect('HoundBot.db')
c = conn.cursor()

prefix_raw = c.execute("SELECT * FROM GuildConfig").fetchall()
global prefix
prefix = {}
for i in prefix_raw:
	prefix[int(i[0])] = i[1]
del prefix_raw

class Main:
	def __init__(self, bot):
		self.bot = bot


def setup(bot):
	bot.add_cog(Main(bot))

import discord
from discord.ext import commands

class Help:
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def help(self, ctx, command = None):
		'''
		Before someone starts accusing this "terrible" help design
		initially the code was not meant to be open-source
		so I didn't care about how dirty or clean the code was
		and right now I'm too busy to make this look cleaner

		So if this really bothers someone
		you are free to remake this into a whatever version you want
		and even include external files if you want, I don't care
		'''
		if not command:
			await ctx.send(content = '**Type `modules` to see a list of modules.\nType `cmds <module>` to see a list of commands in a module.**')
		elif command.lower() == 'help':
			embed = discord.Embed()
			embed.add_field(name = '`help`', value = 'Shows help message, or command related help.')
			embed.add_field(name = 'Requires Permissions', value = 'None', inline = False)
			embed.add_field(name = 'Example', value = '`help`')
			await ctx.send(embed = embed)
		elif command.lower() == 'invite':
			embed = discord.Embed()
			embed.add_field(name = '`invite`', value = 'Invite me to your server.')
			embed.add_field(name = 'Requires Permissions', value = 'None', inline = False)
			embed.add_field(name = 'Example', value = '`invite`')
			await ctx.send(embed = embed)
		elif command.lower() == 'cmds':
			embed = discord.Embed()
			embed.add_field(name = '`cmds`', value = 'Shows a list of commands.')
			embed.add_field(name = 'Requires Permissions', value = 'None', inline = False)
			embed.add_field(name = 'Example', value = '`cmds`')
			await ctx.send(embed = embed)
		elif command.lower() == 'lookup':
			embed = discord.Embed()
			embed.add_field(name = '`lookup`', value = 'Shows information about the user. Use a user ID to look up a user outside of the server.')
			embed.add_field(name = 'Requires Permissions', value = 'None', inline = False)
			embed.add_field(name = 'Example', value = '`lookup 461914170028326913`')
			await ctx.send(embed = embed)
		elif command.lower() == 'uprate':
			embed = discord.Embed()
			embed.add_field(name = '`uprate`', value = 'Rate the user positively.')
			embed.add_field(name = 'Requires Permissions', value = 'None', inline = False)
			embed.add_field(name = 'Example', value = '`uprate 461914170028326913`')
			await ctx.send(embed = embed)
		elif command.lower() == 'downrate':
			embed = discord.Embed()
			embed.add_field(name = '`downrate`', value = 'Rate the user negatively.')
			embed.add_field(name = 'Requires Permissions', value = 'None', inline = False)
			embed.add_field(name = 'Example', value = '`downrate 461914170028326913`')
			await ctx.send(embed = embed)
		elif command.lower() == 'randomserver':
			embed = discord.Embed()
			embed.add_field(name = '`randomserver` / `randserv`', value = 'Get an invite to a random server. The targeted server must be `opt`in to receive members that way, otherwise no invite is returned.')
			embed.add_field(name = 'Requires Permissions', value = 'None', inline = False)
			embed.add_field(name = 'Example', value = '`randserv`')
			await ctx.send(embed = embed)
		elif command.lower() == 'serverlog':
			embed = discord.Embed()
			embed.add_field(name = '`serverlog`', value = 'Log events that happen in the server.')
			embed.add_field(name = 'Requires Permissions', value = 'Manage Server', inline = False)
			embed.add_field(name = 'Example', value = '`serverlog`')
			await ctx.send(embed = embed)
		elif command.lower() == 'moderators':
			embed = discord.Embed()
			embed.add_field(name = '`moderators` / `mods`', value = 'Lists all current server moderators sorted by user status. More specifically, this lists users with `Ban Members` permission.')
			embed.add_field(name = 'Requires Permissions', value = 'None', inline = False)
			embed.add_field(name = 'Example', value = '`moderators`')
			await ctx.send(embed = embed)
		elif command.lower() == 'kick':
			embed = discord.Embed()
			embed.add_field(name = '`kick` / `k`', value = 'Kicks a user from the server with an optional reason.')
			embed.add_field(name = 'Requires Permissions', value = 'Kick Members', inline = False)
			embed.add_field(name = 'Example', value = '`kick @SomeDude Get out of here`')
			await ctx.send(embed = embed)
		elif command.lower() == 'softban':
			embed = discord.Embed()
			embed.add_field(name = '`softban` / `sb`', value = 'Kicks a user from the server (and deletes 1 day worth of their messages) with an optional reason.')
			embed.add_field(name = 'Requires Permissions', value = 'Kick Members and Manage Messages', inline = False)
			embed.add_field(name = 'Example', value = '`softban @SomeDude Just clearing out your messages`')
			await ctx.send(embed = embed)
		elif command.lower() == 'ban':
			embed = discord.Embed()
			embed.add_field(name = '`ban` / `b`', value = 'Bans a user from the server (and deletes 7 days worth of their messages) with an optional reason.')
			embed.add_field(name = 'Requires Permissions', value = 'Ban Members', inline = False)
			embed.add_field(name = 'Example', value = '`ban @SomeDude Your behavior is toxic`')
			await ctx.send(embed = embed)
		elif command.lower() == 'hackban':
			embed = discord.Embed()
			embed.add_field(name = '`hackban` / `hb`', value = 'Bans a user using their ID without them being in the server.')
			embed.add_field(name = 'Requires Permissions', value = 'Ban Members', inline = False)
			embed.add_field(name = 'Example', value = '`hackban @SomeDude`')
			await ctx.send(embed = embed)
		elif command.lower() == 'mute':
			embed = discord.Embed()
			embed.add_field(name = '`mute`', value = 'Mutes a user with an optional reason.')
			embed.add_field(name = 'Requires Permissions', value = 'Mute Members', inline = False)
			embed.add_field(name = 'Example', value = '`mute @SomeDude Spamming`')
			await ctx.send(embed = embed)
		elif command.lower() == 'unmute':
			embed = discord.Embed()
			embed.add_field(name = '`mute`', value = 'Unmutes a user with an optional reason.')
			embed.add_field(name = 'Requires Permissions', value = 'Mute Members', inline = False)
			embed.add_field(name = 'Example', value = '`unmute @SomeDude Appealed`')
			await ctx.send(embed = embed)
		elif command.lower() == 'mutelist':
			embed = discord.Embed()
			embed.add_field(name = '`mutelist`', value = 'Get a list of muted members.')
			embed.add_field(name = 'Requires Permissions', value = 'None', inline = False)
			embed.add_field(name = 'Example', value = '`mutelist`')
			await ctx.send(embed = embed)
		elif command.lower() == 'setmuterole':
			embed = discord.Embed()
			embed.add_field(name = '`setmuterole`', value = 'Set\'s a mute role to be used to mute users with.')
			embed.add_field(name = 'Requires Permissions', value = 'Manage Roles', inline = False)
			embed.add_field(name = 'Example', value = '`setmuterole Muted`')
			await ctx.send(embed = embed)
		elif command.lower() == 'opt':
			embed = discord.Embed()
			embed.add_field(name = '`opt`', value = 'Optin your server. That will allow users to randomize your server with `randserv` and send them an invite link to it. Repeat the command to optout again.')
			embed.add_field(name = 'Requires Permissions', value = 'Manage Server', inline = False)
			embed.add_field(name = 'Example', value = '`opt`')
			await ctx.send(embed = embed)
		elif command.lower() == 'greet':
			embed = discord.Embed()
			embed.add_field(name = '`greet`', value = 'Enable welcome messages in the current channel, or disable them.')
			embed.add_field(name = 'Requires Permissions', value = 'Manage Server', inline = False)
			embed.add_field(name = 'Example', value = '`greet`')
			await ctx.send(embed = embed)
		elif command.lower() == 'bye':
			embed = discord.Embed()
			embed.add_field(name = '`bye`', value = 'Enable leave messages in the current channel, or disable them.')
			embed.add_field(name = 'Requires Permissions', value = 'Manage Server', inline = False)
			embed.add_field(name = 'Example', value = '`bye`')
			await ctx.send(embed = embed)
		elif command.lower() == 'greetmsg':
			embed = discord.Embed()
			embed.add_field(name = '`greetmsg`', value = 'Set a new welcome message.\n\n`&user&` - mention the member in the message.\n`&server&` - mention the server\'s name in the message.')
			embed.add_field(name = 'Requires Permissions', value = 'Manage Server', inline = False)
			embed.add_field(name = 'Example', value = '`greetmsg Welcome &user&!`')
			await ctx.send(embed = embed)
		elif command.lower() == 'byemsg':
			embed = discord.Embed()
			embed.add_field(name = '`byemsg`', value = 'Set a leave welcome message.\n\n`&user&` - mention the member in the message.\n`&server&` - mention the server\'s name in the message.')
			embed.add_field(name = 'Requires Permissions', value = 'Manage Server', inline = False)
			embed.add_field(name = 'Example', value = '`byemsg **&user&** has just left.`')
			await ctx.send(embed = embed)
		elif command.lower() == 'greetdel':
			embed = discord.Embed()
			embed.add_field(name = '`greetdel`', value = 'After how long (in seconds) the welcome message will be autimatically deleted. 0 to disable.')
			embed.add_field(name = 'Requires Permissions', value = 'Manage Server', inline = False)
			embed.add_field(name = 'Example', value = '`greetdel 30` or `greetdel 0`')
			await ctx.send(embed = embed)
		elif command.lower() == 'byedel':
			embed = discord.Embed()
			embed.add_field(name = '`byedel`', value = 'After how long (in seconds) the leave message will be autimatically deleted. 0 to disable.')
			embed.add_field(name = 'Requires Permissions', value = 'Manage Server', inline = False)
			embed.add_field(name = 'Example', value = '`byedel 30` or `byedel 0`')
			await ctx.send(embed = embed)
		elif command.lower() == 'prune':
			embed = discord.Embed()
			embed.add_field(name = '`prune`', value = 'Deletes a specified amount/type of messages.\n\n`@member` - deletes messages sent by a specific member.\n`bots` - deletes messages sent by bots.\n`embeds` - deletes messages containing embeds.\n`files` - deletes messages containing attached files.\n`self` - deletes own messages.\n`100` - deletes the last X messages.\n`No Argument` - deletes last 100 messages.')
			embed.add_field(name = 'Requires Permissions', value = 'Manage Messages', inline = False)
			embed.add_field(name = 'Example', value = '`prune` or `prune @ThisGuy` or `prune 30` or `prune bots`')
			await ctx.send(embed = embed)
		elif command.lower() == 'snipe':
			embed = discord.Embed()
			embed.add_field(name = '`snipe`', value = 'Reveal the last deleted message in the current channel.')
			embed.add_field(name = 'Requires Permissions', value = 'Manage Messages', inline = False)
			embed.add_field(name = 'Example', value = '`snipe`')
			await ctx.send(embed = embed)
		elif command.lower() == 'userinfo':
			embed = discord.Embed()
			embed.add_field(name = '`userinfo` / `uinfo`', value = 'Gets information about a specific server member.')
			embed.add_field(name = 'Requires Permissions', value = 'None', inline = False)
			embed.add_field(name = 'Example', value = '`userinfo` or `userinfo @ThisGuy`')
			await ctx.send(embed = embed)
		elif command.lower() == 'serverinfo':
			embed = discord.Embed()
			embed.add_field(name = '`serverinfo` / `sinfo`', value = 'Gets information about the current server.')
			embed.add_field(name = 'Requires Permissions', value = 'None', inline = False)
			embed.add_field(name = 'Example', value = '`sinfo`')
			await ctx.send(embed = embed)
		elif command.lower() == 'kickvoice':
			embed = discord.Embed()
			embed.add_field(name = '`kickvoice` / `kv`', value = 'Kicks everyone out of the specified voice channel.')
			embed.add_field(name = 'Requires Permissions', value = 'Move Members', inline = False)
			embed.add_field(name = 'Example', value = '`kickvoice General` or `kv 418460889159565353`')
			await ctx.send(embed = embed)
		elif command.lower() == 'addselfassignrole':
			embed = discord.Embed()
			embed.add_field(name = '`addselfassignrole` / `asar`', value = 'Add a role to the list of selfassignable roles.')
			embed.add_field(name = 'Requires Permissions', value = 'Manage Roles', inline = False)
			embed.add_field(name = 'Example', value = '`asar NSFW`')
			await ctx.send(embed = embed)
		elif command.lower() == 'removeselfassignrole':
			embed = discord.Embed()
			embed.add_field(name = '`removeselfassignrole` / `rsar`', value = 'Remove a role from the list of selfassignable roles.')
			embed.add_field(name = 'Requires Permissions', value = 'Manage Roles', inline = False)
			embed.add_field(name = 'Example', value = '`rsar NSFW`')
			await ctx.send(embed = embed)
		elif command.lower() == 'listselfassignroles':
			embed = discord.Embed()
			embed.add_field(name = '`listselfassignroles` / `lsar`', value = 'List all selfassignable roles.')
			embed.add_field(name = 'Requires Permissions', value = 'None', inline = False)
			embed.add_field(name = 'Example', value = '`lsar`')
			await ctx.send(embed = embed)
		elif command.lower() == 'giverole':
			embed = discord.Embed()
			embed.add_field(name = '`giverole` / `gr`', value = 'Assign a selfassignable role to yourself of your choice.')
			embed.add_field(name = 'Requires Permissions', value = 'None', inline = False)
			embed.add_field(name = 'Example', value = '`gr NSFW`')
			await ctx.send(embed = embed)
		elif command.lower() == 'removerole':
			embed = discord.Embed()
			embed.add_field(name = '`removerole` / `rr`', value = 'Remove a selfassignable role from yourself of your choice.')
			embed.add_field(name = 'Requires Permissions', value = 'None', inline = False)
			embed.add_field(name = 'Example', value = '`rr NSFW`')
			await ctx.send(embed = embed)
		elif command.lower() == 'setannounce':
			embed = discord.Embed()
			embed.add_field(name = '`setannounce`', value = 'Set an announcements channel to be used to send announcements to, and a role that will be automatically pinged during announcements. The first argument must represent a channel, and the second argument must represent a (nonpingable) role.')
			embed.add_field(name = 'Requires Permissions', value = 'Manage Server', inline = False)
			embed.add_field(name = 'Example', value = '`setannounce #announcements Updates`')
			await ctx.send(embed = embed)
		elif command.lower() == 'announce':
			embed = discord.Embed()
			embed.add_field(name = '`announce`', value = 'Post an announcement message in set announcements channel and automatically mention an announcements role.')
			embed.add_field(name = 'Requires Permissions', value = 'Mention Everyone', inline = False)
			embed.add_field(name = 'Example', value = '`announce This is an announcement!`')
			await ctx.send(embed = embed)
		elif command.lower() == 'setnickchannel':
			embed = discord.Embed()
			embed.add_field(name = '`setnickchannel`', value = 'Set a channel for nickname submission and approval.')
			embed.add_field(name = 'Requires Permissions', value = 'Manage Server', inline = False)
			embed.add_field(name = 'Example', value = '`setnickchannel #nickreqs`')
			await ctx.send(embed = embed)
		elif command.lower() == 'nickrequest':
			embed = discord.Embed()
			embed.add_field(name = '`nickrequest` / `nickreq`', value = 'Request your name to be change to something of your choice.')
			embed.add_field(name = 'Requires Permissions', value = 'None', inline = False)
			embed.add_field(name = 'Example', value = '`nickreq Andrew`')
			await ctx.send(embed = embed)
		elif command.lower() == 'setreportchannel':
			embed = discord.Embed()
			embed.add_field(name = '`setreportchannel`', value = 'Set a channel where user reports will be submitted. Staff members will be able to use one of the reactions to apply the appropriate punishment towards the reported offender.')
			embed.add_field(name = 'Requires Permissions', value = 'Manage Server', inline = False)
			embed.add_field(name = 'Example', value = '`setreportchannel #reportlogs`')
			await ctx.send(embed = embed)
		elif command.lower() == 'reportmember':
			embed = discord.Embed()
			embed.add_field(name = '`reportmember`', value = 'Report a member to the server staff for their inappropriate behavior.')
			embed.add_field(name = 'Requires Permissions', value = 'None', inline = False)
			embed.add_field(name = 'Example', value = '`reportmember @BadGuy Being very toxic.`')
			await ctx.send(embed = embed)
		elif command.lower() == 'voicerole':
			embed = discord.Embed()
			embed.add_field(name = '`voicerole`', value = 'Set a role that will be assigned to users while they are connected to a specific voice channel. One role per voice channel. You have to be connected to the voice channel to identify which channel you want to attach to a role. Provide no arguments to remove.')
			embed.add_field(name = 'Requires Permissions', value = 'Manage Roles', inline = False)
			embed.add_field(name = 'Example', value = '`voicerole Some Role` or `voicerole`')
			await ctx.send(embed = embed)
		elif command.lower() == 'voiceroles':
			embed = discord.Embed()
			embed.add_field(name = '`voiceroles`', value = 'See the list of all current voice roles.')
			embed.add_field(name = 'Requires Permissions', value = 'None', inline = False)
			embed.add_field(name = 'Example', value = '`voiceroles`')
			await ctx.send(embed = embed)
		elif command.lower() == 'memberpersistance':
			embed = discord.Embed()
			embed.add_field(name = '`memberpersistance` / `memberpersist`', value = 'Toggles Member Persistance in the server. If a member leaves the server, their roles and nick will be saved for when they will join again, they will receive back everything they had.')
			embed.add_field(name = 'Requires Permissions', value = 'Manage Server', inline = False)
			embed.add_field(name = 'Example', value = '`memberpersist`')
			await ctx.send(embed = embed)
		elif command.lower() == 'prefix':
			embed = discord.Embed()
			embed.add_field(name = '`prefix`', value = 'Shows the currently set prefix, or set a new one for the current server.')
			embed.add_field(name = 'Requires Permissions', value = 'Administrator', inline = False)
			embed.add_field(name = 'Example', value = '`prefix` or `prefix !`')
			await ctx.send(embed = embed)
		elif command.lower() == 'avatar':
			embed = discord.Embed()
			embed.add_field(name = '`avatar` / `av`', value = 'Shows your, or provided member\'s, avatar in full size.')
			embed.add_field(name = 'Requires Permissions', value = 'None', inline = False)
			embed.add_field(name = 'Example', value = '`av @ThisGuy`')
			await ctx.send(embed = embed)
		elif command.lower() == 'greetdmmsg':
			embed = discord.Embed()
			embed.add_field(name = '`greetdmmsg`', value = 'Set a new welcome DM message.\n\n`&user&` - mention the member in the message.\n`&server&` - mention the server\'s name in the message.')
			embed.add_field(name = 'Requires Permissions', value = 'Manage Server', inline = False)
			embed.add_field(name = 'Example', value = '`greetdmmsg` or `greetdmmsg Welcome &user& to &server&!`')
			await ctx.send(embed = embed)
		elif command.lower() == 'greetdm':
			embed = discord.Embed()
			embed.add_field(name = '`greetdm`', value = 'Toggle welcome DM messages in the current server.')
			embed.add_field(name = 'Requires Permissions', value = 'Manage Server', inline = False)
			embed.add_field(name = 'Example', value = '`greetdm`')
			await ctx.send(embed = embed)
		elif command.lower() == 'filteradd':
			embed = discord.Embed()
			embed.add_field(name = '`filteradd`', value = 'Add a word to the list of filtered words. If a word will be mentioned in a message, an appropriate action will be taken.\n\n`delete` - deletes the message.\n`kick` - deletes the message and kicks the message author.\n`ban` - bans the message author and deletes 1 day worth of their messages.')
			embed.add_field(name = 'Requires Permissions', value = 'Administrator', inline = False)
			embed.add_field(name = 'Example', value = '`filteradd "bad word" delete` or `filteradd "n.. word" ban`')
			await ctx.send(embed = embed)
		elif command.lower() == 'filterremove':
			embed = discord.Embed()
			embed.add_field(name = '`filterremove`', value = 'Remove a filtered word from the list of filtered words.')
			embed.add_field(name = 'Requires Permissions', value = 'Administrator', inline = False)
			embed.add_field(name = 'Example', value = '`filterremove "bad word"`')
			await ctx.send(embed = embed)
		elif command.lower() == 'filters':
			embed = discord.Embed()
			embed.add_field(name = '`filters`', value = 'View a list of filtered words.')
			embed.add_field(name = 'Requires Permissions', value = 'Administrator', inline = False)
			embed.add_field(name = 'Example', value = '`filters`')
			await ctx.send(embed = embed)
		elif command.lower() == 'setchangelogs':
			embed = discord.Embed()
			embed.add_field(name = '`setchangelogs`', value = 'Set a channel where User Hound will be posting changelog announcements.')
			embed.add_field(name = 'Requires Permissions', value = 'Manage Server', inline = False)
			embed.add_field(name = 'Example', value = '`setchangelogs`')
			await ctx.send(embed = embed)
		else:
			await ctx.send(content = '<:xmark:314349398824058880> **That command does not exist.**')

	@commands.command(aliases = ['links', 'link', 'support'])
	async def invite(self, ctx):
		await ctx.send(embed = discord.Embed(description = '[**Add me**](https://discordapp.com/oauth2/authorize?client_id=461914170028326913&permissions=84992&scope=bot)\n[**Support server**](https://discord.gg/sbySHxA)\n[**Buy my owner Latte**](https://www.paypal.me/Deivedux)', color = 0x28B463))

	@commands.command()
	async def cmds(self, ctx, module):
		if module.lower() == 'help':
			embed = discord.Embed(title = 'Help', color = 0x2ECC71)
			embed.add_field(name = 'help', value = 'Shows help message, or command related help.', inline = False)
			embed.add_field(name = 'invite', value = 'Invite me to your server.', inline = False)
			embed.add_field(name = 'commands', value = 'Shows a list of commands for a specified module.', inline = False)
			embed.add_field(name = 'modules', value = 'Shows a list of modules', inline = False)
			embed.set_footer(text = 'Type `help <command>` to see more information on a command.')
			await ctx.send(embed = embed)

		if module.lower() == 'lookup':
			embed = discord.Embed(title = 'User Lookup', color = 0x2ECC71)
			embed.add_field(name = 'lookup', value = 'Shows information about the user. Use a user ID to look up a user outside of the server.', inline = False)
			embed.add_field(name = 'uprate', value = 'Rate the user positively.', inline = False)
			embed.add_field(name = 'downrate', value = 'Rate the user negatively.', inline = False)
			embed.add_field(name = '__NOTE__', value = '**User Hound** uses a way to receive user information without having any mutual servers, and that is a very heavy feature for discord to handle if this will be spammed. So for security measures, you may use these commands only 2 times per 20 seconds universally.')
			embed.set_footer(text = 'Type `help <command>` to see more information on a command.')
			await ctx.send(embed = embed)

		if module.lower() == 'filters':
			embed = discord.Embed(title = 'User Lookup', color = 0x2ECC71)
			embed.add_field(name = 'filteradd', value = 'Add a word to the list of filtered words. If a word will be mentioned in a message, an appropriate action will be taken.', inline = False)
			embed.add_field(name = 'filterremove', value = 'Remove a filtered word from the list of filtered words.', inline = False)
			embed.add_field(name = 'filters', value = 'View a list of filtered words.', inline = False)
			embed.set_footer(text = 'Type `help <command>` to see more information on a command.')
			await ctx.send(embed = embed)

		if module.lower() == 'utility':
			embed = discord.Embed(title = 'User Lookup', color = 0x2ECC71)
			embed.add_field(name = 'prefix', value = 'See the currently set prefix, or set a new one for the current server.', inline = False)
			embed.add_field(name = 'setchangelogs', value = 'Set a channel where User Hound will be posting changelog announcements.', inline = False)
			embed.add_field(name = 'memberpersistance', value = 'Enables or disables Members Persistance in the server.', inline = False)
			embed.add_field(name = 'userinfo', value = 'Gets information about a specific server member.', inline = False)
			embed.add_field(name = 'serverinfo', value = 'Gets information about the current server.', inline = False)
			embed.add_field(name = 'addselfassignrole', value = 'Add a role to the list of selfassignable roles.', inline = False)
			embed.add_field(name = 'removeselfassignrole', value = 'Remove a role from the list of selfassignable roles.', inline = False)
			embed.add_field(name = 'listselfassignroles', value = 'List all selfassignable roles.', inline = False)
			embed.add_field(name = 'giverole', value = 'Assign a selfassignable role to yourself of your choice.', inline = False)
			embed.add_field(name = 'removerole', value = 'Remove a selfassignable role from yourself of your choice.', inline = False)
			embed.add_field(name = 'voicerole', value = 'Set a role that will be assigned to users while they are connected to a specific voice channel.', inline = False)
			embed.add_field(name = 'voiceroles', value = 'See the list of all current voice roles.', inline = False)
			embed.add_field(name = 'setannounce', value = 'Set an announcements channel to be used to send announcements to, and a role that will be automatically pinged during announcements.', inline = False)
			embed.add_field(name = 'announce', value = 'Post an announcement message in set announcements channel and automatically mention an announcements role.', inline = False)
			embed.add_field(name = 'setnickchannel', value = 'Set a channel for nickname submission and approval.', inline = False)
			embed.add_field(name = 'nickrequest', value = 'Request your name to be change to something of your choice.', inline = False)
			embed.set_footer(text = 'Type `help <command>` to see more information on a command.')
			await ctx.send(embed = embed)

		if module.lower() == 'memberpresence':
			embed = discord.Embed(title = 'Member Presence', color = 0x2ECC71)
			embed.add_field(name = 'greetmsg', value = 'Set a new welcome message. Type `help greetmsg` for more details.', inline = False)
			embed.add_field(name = 'greetdmmsg', value = 'Set a new welcome DM message. Type `help greetdmmsg` for more details.', inline = False)
			embed.add_field(name = 'byemsg', value = 'Set a new leave message. Type `help byemsg` for more details.', inline = False)
			embed.add_field(name = 'greetdel', value = 'After how long (in seconds) the welcome message will be autimatically deleted. 0 to disable.', inline = False)
			embed.add_field(name = 'byedel', value = 'After how long (in seconds) the leave message will be autimatically deleted. 0 to disable.', inline = False)
			embed.add_field(name = 'greet', value = 'Enable welcome messages in the current channel, or disable them.', inline = False)
			embed.add_field(name = 'greetdm', value = 'Toggle welcome DM messages in the current server.', inline = False)
			embed.add_field(name = 'bye', value = 'Enable leave messages in the current channel, or disable them.', inline = False)
			embed.set_footer(text = 'Type `help <command>` to see more information on a command.')
			await ctx.send(embed = embed)

		if module.lower() == 'listing':
			embed = discord.Embed(title = 'Server Listing', color = 0x2ECC71)
			embed.add_field(name = 'opt', value = 'Optin your server. That will allow users to randomize your server with `randserv` and send them an invite link to it. Repeat the command to optout again.', inline = False)
			embed.add_field(name = 'randomserver', value = 'Get an invite to a random server. The targeted server must be `opt`in to receive members that way, otherwise no invite is returned.', inline = False)
			embed.set_footer(text = 'Type `help <command>` to see more information on a command.')
			await ctx.send(embed = embed)

		if module.lower() == 'moderation':
			embed = discord.Embed(title = 'Moderation', color = 0x2ECC71)
			embed.add_field(name = 'moderators', value = 'Lists all current server moderators sorted by user status.', inline = False)
			embed.add_field(name = 'snipe', value = 'Reveal the last deleted message in the current channel.', inline = False)
			embed.add_field(name = 'kick', value = 'Kicks a user from the server with an optional reason.', inline = False)
			embed.add_field(name = 'softban', value = 'Kicks a user from the server (and deletes 1 day worth of their messages) with an optional reason.', inline = False)
			embed.add_field(name = 'ban', value = 'Bans a user from the server (and deletes 7 days worth of their messages) with an optional reason.', inline = False)
			embed.add_field(name = 'hackban', value = 'Bans a user using their ID without them being in the server.', inline = False)
			embed.add_field(name = 'prune', value = 'Deletes a specified amount/type of messages. Type `help prune` for more details.', inline = False)
			embed.add_field(name = 'kickvoice', value = 'Kicks everyone out of the specified voice channel.', inline = False)
			embed.add_field(name = 'setreportchannel', value = 'Set a channel where user reports will be submitted. Staff members will be able to use one of the reactions to apply the appropriate punishment towards the reported offender.', inline = False)
			embed.add_field(name = 'reportmember', value = 'Report a member to the server staff for their inappropriate behavior.', inline = False)
			embed.add_field(name = 'mute', value = 'Mutes a user with an optional reason.', inline = False)
			embed.add_field(name = 'unmute', value = 'Unmutes a user with an optional reason.', inline = False)
			embed.add_field(name = 'mutelist', value = 'Get a list of muted members.', inline = False)
			embed.add_field(name = 'setmuterole', value = 'Set\'s a mute role to be used to mute users with.', inline = False)
			embed.set_footer(text = 'Type `help <command>` to see more information on a command.')
			await ctx.send(embed = embed)

	@commands.command(aliases = ['mdls'])
	async def modules(self, ctx):
		embed = discord.Embed(title = 'Modules', description = '• Help\n• Lookup\n• Moderation\n• Filters\n• Utility\n• MemberPresence\n• Listing', color = 0x2ECC71)
		embed.set_footer(text = 'Type `cmds <module>` to see a list of commands in a module.')
		await ctx.send(embed = embed)


def setup(bot):
	bot.add_cog(Help(bot))

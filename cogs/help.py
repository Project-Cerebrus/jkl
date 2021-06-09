import discord
from discord.ext import commands
from discord.errors import Forbidden


async def send_embed(ctx, embed):
	"""
	Function that handles the sending of embeds
	-> Takes context and embed to send
	- tries to send embed in channel
	- tries to send normal message when that fails
	- tries to send embed private with information abot missing permissions
	If this all fails: https://youtu.be/dQw4w9WgXcQ
	"""
	try:
		await ctx.send(embed=embed)
	except Forbidden:
		try:
			await ctx.send("Hey, seems like I can't send embeds. Please check my permissions :)")
		except Forbidden:
			await ctx.author.send(
				f"Hey, seems like I can't send any message in {ctx.channel.name} on {ctx.guild.name}\n"
				f"May you inform the server team about this issue? :slight_smile: ", embed=embed)
def sortaliases(aliases):
	if aliases == []:
		aliases = "No Aliases"
		return aliases
	else:
		aliases = str(aliases).replace('\'', '').replace('[','').replace(']','')
		return aliases


class Help(commands.Cog):
	"""Sends this help message"""
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	# @commands.bot_has_permissions(add_reactions=True,embed_links=True)
	async def help(self, ctx, *,input=None):
		"""Shows all modules of that bot"""

	# !SET THOSE VARIABLES TO MAKE THE COG FUNCTIONAL!
		prefix = 'f?'
		version =  'v0.5'
		
		# setting owner name - if you don't wanna be mentioned remove line 49-60 and adjust help text (line 88) 
		owner = "775198018441838642"

			# checks if cog parameter was given
			# if not: sending all modules and commands not associated with a cog
		if not input:
				# checks if owner is on this server - used to 'tag' owner
				try:
					owner = ctx.guild.get_member(owner).mention

				except AttributeError as e:
					owner = owner

				# starting to build embed
				emb = discord.Embed(title='Commands and Modules', color=discord.Color.blue(),
									description=f'Use `{prefix}help <module/command>` to gain more information about that module')

				# iterating trough cogs, gathering descriptions
				cogs_desc = '\n'
				for cog in self.bot.cogs:
					if cog == "Help" or cog == "blacklist":
						pass
					else:
						cogs_desc += f'`{cog}`: {self.bot.cogs[cog].__doc__}\n\n'

				# adding 'list' of cogs to embed
				emb.add_field(name='Modules\n', value=cogs_desc, inline=False)

				# integrating trough uncategorized commands
				commands_desc = ''
				for command in self.bot.walk_commands():
					# if cog not in a cog
					# listing command if cog name is None and command isn't hidden
					if not command.cog_name and not command.hidden and command.name != 'evaluate':
						commands_desc += f'{command.name} - {command.help}\n'

				# adding those commands to embed
				if commands_desc:
					emb.add_field(name='Not belonging to a module', value=commands_desc, inline=False)

				# setting information about author
				emb.add_field(name="About", value=f"This Bot is developed and maintained by **The Cerebrus Team**:\n<@775198018441838642>,<@746904488396324864> and <@750755612505407530>\nThis Bot is [open source](https://github.com/Project-Cerebrus/jkl) and easily accessible.")
				emb.set_footer(text=f"Running {version} © The Cerebrus Team")

		else:
			for cog in self.bot.cogs:
				if input.lower() in cog.lower():
					found = False

					# making title - getting description from doc-string below class
					emb = discord.Embed(title=f'{cog} - Commands', description=self.bot.cogs[cog].__doc__,color=discord.Color.green())

					# getting commands from cog
					for command in self.bot.get_cog(cog).get_commands():
						if found == False:
							if not command.hidden:
								if command.aliases != []:
									aliases = list(command.aliases)
									aliases = str(aliases).replace('\'', '').replace('[','').replace(']','').replace(', ', '/')
									emb.add_field(name=f"`{prefix}{command.name}/{aliases} {command.signature}`", value=command.help, inline=False)
								else:
									emb.add_field(name=f"`{prefix}{command.name} {command.signature}`", value=command.help, inline=False)
					return await ctx.send(embed=emb)
					found = True
				else:
					for command in self.bot.commands:
						if input.lower() == command.name.lower() or input.lower() in command.aliases:
							aliases = list(command.aliases)
							aliases=sortaliases(aliases)
							emb = discord.Embed(title=f"Command Help: {command.name}", description=f"**Usage:** `{prefix}{command.name} {command.signature}`\n**Aliases:** `{aliases}`\n**Description:** {command.help}", colour = discord.Color.green())
							return await ctx.send(embed=emb)
						else:
							emb = discord.Embed(title='Not Found', description=f"Could not find a command/module with the name `{input}`", color = discord.Color.red())

			# sending reply embed using our own function defined above
		await send_embed(ctx, emb)


def setup(bot):
	bot.add_cog(Help(bot))
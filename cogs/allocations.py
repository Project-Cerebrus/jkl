from discord.ext.commands import Cog, command, has_permissions, has_any_role
import discord, json
from library import funcs, constants


class allocations(Cog, name='Allocations'):
	"""Organized system for allocating moderators to their categories. (Moderator Only)"""
	def __init__(self, bot):
		self.bot = bot

	@command(name='moderate', aliases = ('claim',))
	async def _claim(self, ctx, *,category:str):
		"""Allows you to claim your category"""
		role1 = discord.utils.get(ctx.guild.roles, id=constants.Roles.SMOD)
		role2 = discord.utils.get(ctx.guild.roles, id=constants.Roles.MOD)
		role3 = discord.utils.get(ctx.guild.roles, id=constants.Roles.TMOD)
		if role1 not in ctx.author.roles and role2 not in ctx.author.roles and role3 not in ctx.author.roles:
			return
		categories = ["general", "trading and mm", "modmail, support and fake events", "appeals"]
		for lol in categories:
			if category in lol:
				category = lol
		if role1 == ctx.author.top_role or role1 in ctx.author.roles:
			categ = "smods"
		elif role2 == ctx.author.top_role or role2 in ctx.author.roles:
			categ = "mods"
		elif role3 == ctx.author.top_role or role3 in ctx.author.roles:
			categ = "tmods"
		x = funcs.addmod(ctx.author, category, categ)
		if x == 1:
			return await ctx.send('This category has reached its max limit.')
		elif x == 2:
			return await ctx.send('You already have claimed this category!')
		await ctx.send(f'Added you to **{category}**')
	
	@command(name='mycategory')
	async def mycateg(self,ctx):
		"""Shows your category"""
		role1 = discord.utils.get(ctx.guild.roles, id=constants.Roles.SMOD)
		role2 = discord.utils.get(ctx.guild.roles, id=constants.Roles.MOD)
		role3 = discord.utils.get(ctx.guild.roles, id=constants.Roles.TMOD)
		if role1 not in ctx.author.roles and role2 not in ctx.author.roles and role3 not in ctx.author.roles:
			return
		with open('data/allocs.json','r') as f:
			main = json.load(f)
		try:
			cat = main["users"][str(ctx.author.id)]
		except KeyError:
			await ctx.send(f"You have not claimed a category.\nUse `!claim <category>` to do so.")
		await ctx.send(f'You are assigned to **{cat}**')
	
	@command(name='categories', aliases = ['allocations', 'allocs'])
	@has_permissions(manage_guild=True)
	async def categs(self, ctx):
		"""Only admins, shows the list of all categories"""
		with open('data/allocs.json','r') as f:
			main = json.load(f)
		final = ""
		for category in main["main"]:
			finaladd = f"\n**↷₊˚ʚ  {category} ·˚**\n"
			for smod in main["main"][category]["smods"]:
				smoduser = self.bot.get_user(smod)
				finaladd += f"ʚ `{smoduser}` **(Senior Mod)**\n"
			for mod in main["main"][category]["mods"]:
				smoduser = self.bot.get_user(mod)
				finaladd += f"ʚ `{smoduser}` (Mod)\n"
			for tmod in main["main"][category]["tmods"]:
				smoduser = self.bot.get_user(tmod)
				finaladd += f"ʚ `{smoduser}` (Trial Mod)\n"
			final += finaladd
		embed = discord.Embed(title='Category Assignments', description = final, color = discord.Color.random())
		await ctx.send(embed=embed)
	
	@command(name='forceassign', aliases= ['assign'])
	@has_permissions(manage_guild=True)
	async def forceassign(self, ctx, user:discord.Member, *, category:str):
		"""Allows admins to forceassign someone to a category"""
		role1 = discord.utils.get(ctx.guild.roles, id=constants.Roles.SMOD)
		role2 = discord.utils.get(ctx.guild.roles, id=constants.Roles.MOD)
		role3 = discord.utils.get(ctx.guild.roles, id=constants.Roles.TMOD)
		categories = ["general", "trading and mm", "modmail, support and fake events", "appeals"]
		for lol in categories:
			if category in lol:
				category = lol
		if role1 == user.top_role or role1 in user.roles:
			categ = "smods"
		elif role2 == user.top_role or role2 in user.roles:
			categ = "mods"
		elif role3 == user.top_role or role3 in user.roles:
			categ = "tmods"
		else:
			return await ctx.send('Could not detect if the user is a senior, trial or normal mod.')
		x = funcs.addmod(user, category, categ)
		if x == 1:
			return await ctx.send('This category has reached its max limit.')
		elif x == 2:
			return await ctx.send('This user has already claimed this category!')
		await ctx.send(f'Added {user.name} to **{category}**')

	@command(name='forceremove', aliases = ['remove'])
	@has_permissions(manage_guild=True)
	async def forceremove(self, ctx, user:discord.Member):
		"""Allows admins to forceremove someone from a category"""
		with open('data/allocs.json','r') as f:
			main = json.load(f)
		try:
			categ = main["users"][str(user.id)]
		except KeyError:
			return await ctx.send('I could not find this user in my database.')
		main["main"][categ][type].remove(user.id)
		with open('data/allocs.json','w') as f:
			json.dump(main,f)
		await ctx.send(f'Removed {user.name} from **{categ}**')

	@command(name='resetcategs', aliases = ['resetallocs'])
	@has_permissions(manage_guild=True)
	async def _resetcategs(self,ctx):
		"""Allows admins to reset all allocation data (careful)"""
		data = {"main": {"general": {"smods": [], "mods": [], "tmods": []}, "trading and mm": {"smods": [], "mods": [], "tmods": []}, "modmail, support and fake events": {"smods": [], "mods": [], "tmods": []}, "appeals": {"smods": [], "mods": [], "tmods": []}}, "users": {}}
		with open("data/allocs.json", "w") as f:
			json.dump(data,f)
		await ctx.send('Reset all category data.')



def setup(bot):
	bot.add_cog(allocations(bot))
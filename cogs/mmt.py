from discord.ext.commands import Cog, command, has_permissions
import discord, json
from library import funcs


class mmt(Cog, name='Middleman Trades'):
	"""Allows <@&796489689069518869> to give access to the mm trading channel and monitors their progress. Admins can view who used it the most and who did least. (Only middleman and admins)"""
	def __init__(self, bot):
		self.bot = bot

	@command(name='mmt')
	async def _mmt(self,ctx, user1:discord.Member, user2:discord.Member):
		"""The main command allowing middlemen to give the traders access to MM Trading"""
		role = discord.utils.get(ctx.guild.roles, id=796489689069518869)
		if role not in ctx.author.roles:
			return
		mrole = discord.utils.get(ctx.guild.roles, id=797213775337357342)
		if mrole in user1.roles and mrole in user2.roles:
			return await ctx.send('These users already have the access role!')
		funcs.open_user(ctx.author)
		user = ctx.author
		users = funcs.get_users_data()
		users[str(user.id)]["mmts"] += 1
		funcs.dump(users)
		await user1.add_roles(mrole)
		await user2.add_roles(mrole)
		await ctx.message.add_reaction('👍')

	@command(name='unmmt')
	async def _unmmt(self,ctx, user1:discord.Member, user2:discord.Member):
		"""Allows middlemen to manually remove the MM Trading Access"""
		role = discord.utils.get(ctx.guild.roles, id=796489689069518869)
		if role not in ctx.author.roles:
			return
		funcs.open_user(ctx.author)
		mrole = discord.utils.get(ctx.guild.roles, id=797213775337357342)
		if mrole not in user1.roles and mrole not in user2.roles:
			return await ctx.send('These users don\'t have the access role!')
		await user1.remove_roles(mrole)
		await user2.remove_roles(mrole)
		await ctx.message.add_reaction('👍')

	@command(name='topmmt', aliases = ['top'])
	@has_permissions(manage_guild=True)
	async def topmmt(self,ctx,x=1):
		"""Shows the Top middlemen who used the command most."""
		users = funcs.get_users_data()
		leader_board = []
		total = []
		for user in users:
			name = int(user)
			total_amount = users[user]["mmts"]
			leader_board.append((name,total_amount))
			total.append(total_amount)

		m=1
		def last(n):
			return n[m]
		sorted_list = sorted(leader_board, key=last, reverse=True)
		final = ""
		i = 0
		while i < x:
			item = sorted_list[i]
			name = self.bot.get_user(int(item[0])).name
			final += f"{i+1}. {name}: {item[1]}\n"
			i+=1

		em = discord.Embed(title = f"Top {x} MMT Users" , description = final, color = discord.Color.green())
		
		await ctx.send(embed = em)

	@command(name='lowmmt', aliases = ['low'])
	@has_permissions(manage_guild=True)
	async def lowmmt(self,ctx,x=1):
		"""Shows the middlemen who were least active and helps in demotions"""
		users = funcs.get_users_data()
		leader_board = []
		total = []
		for user in users:
			name = int(user)
			total_amount = users[user]["mmts"]
			leader_board.append((name,total_amount))
			total.append(total_amount)

		m=1
		def last(n):
			return n[m]
		sorted_list = sorted(leader_board, key=last)
		final = ""
		i = 0
		while i < len(sorted_list):
			item = sorted_list[i]
			name = self.bot.get_user(int(item[0])).name
			final += f"{i+1}. {name}: {item[1]}\n"
			i+=1

		em = discord.Embed(title = f"Lowest {x} MMT Users" , description = final, color = discord.Color.red())
		
		await ctx.send(embed = em)

	@command(name='resetmmts', aliases = ['resetmmt'])
	@has_permissions(manage_guild=True)
	async def _resetcategs(self,ctx):
		"""Resets complete middlemen data."""
		data = {}
		with open("data/allocs.json", "w") as f:
			json.dump(data,f)
		await ctx.send('Reset all category data.')

def setup(bot):
	bot.add_cog(mmt(bot))



from discord.ext.commands import Cog, command, has_permissions
import discord, json
from library import funcs


class blacklist(Cog, name='blacklist'):
	"""In DEVELOPMENT. NOT TO BE USED."""
	def __init__(self, bot):
		self.bot = bot

	@command(name="blinfo")
	async def blinfo(self,ctx,user):
		"""Get the reason why the user was blacklisted and by whom."""
		try:
			user = int(user)
		except:
			user = user.replace("<@","").replace("!","").replace(">","")
		userid = int(user)
		with open('data/blacklist.json','r') as f:
			black = json.load(f)
		if str(userid) not in black:
			return await ctx.send("User not blacklisted")
		else:
			reason = black[str(userid)]["reason"]
			blby = black[str(userid)]["blby"]
			embed = discord.Embed(title="Blacklist Information",description=f"**Reason:** {reason}\n**Blacklisted by:** <@{blby}>",color=ctx.author.color)
			try:
				user = self.bot.get_user(userid)
				embed.set_thumbnail(url=user.avatar_url)
			except:
				pass
			await ctx.send(embed=embed)


	@command(name='blacklist',aliases=["bl"])
	@has_permissions(kick_members=True)
	async def blacklist(self, ctx, user, *, reason="None given"):
		"""Blacklist a user in or not in the server. Roles will be auto-assigned on joining."""
		try:
			user = int(user)
		except:
			user = user.replace("<@","").replace("!","").replace(">","")
		userid = int(user)
		role2 = discord.utils.get(ctx.guild.roles, id=851389137491197952)
		role3 = discord.utils.get(ctx.guild.roles, id=851389163789615144)
		role4 = discord.utils.get(ctx.guild.roles, id=851389179690745867)
		"""role2 = discord.utils.get(ctx.guild.roles, id=761540775523123220)
		role3 = discord.utils.get(ctx.guild.roles, id=752263653495144538)"""
		with open('data/blacklist.json','r') as f:
			black = json.load(f)
		user = ctx.guild.get_member(userid)
		if userid in black:
			return await ctx.send('Already Blacklisted.')
		if not user:
			black[str(user.id)] = {}
			black[str(user.id)]["reason"] = reason
			black[str(user.id)]["blby"] = ctx.author.id
			with open('data/blacklist.json','w') as z:
				json.dump(black,z)
		else:
			black[str(user.id)] = {}
			black[str(user.id)]["reason"] = reason
			black[str(user.id)]["blby"] = ctx.author.id
			with open('data/blacklist.json','w') as z:
				json.dump(black,z)
			await user.add_roles(role2)
			await user.add_roles(role3)
			await user.add_roles(role4)
		await ctx.send(f'Blacklisted User <@{userid}> with reason - {reason}')



	
def setup(bot):
	bot.add_cog(blacklist(bot))
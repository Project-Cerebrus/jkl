import discord, os, io, traceback, textwrap
from discord.ext import commands
from contextlib import redirect_stdout
import inspect

bot = commands.Bot(command_prefix="d?", intents = discord.Intents.all())
TOKEN = os.environ['TOKEN']
bot.remove_command("help")
 #replace this with your token, DO NOT remove the "", put it inside them only

@bot.event
async def on_ready():
	print(f"ready\n{bot.user.id}")
	await bot.change_presence(status = discord.Status.do_not_disturb, activity=discord.Activity(type=discord.ActivityType.watching, name=f"Dank Trades Grow"))

@bot.event
async def on_command_error(ctx,error):
	if isinstance(error, commands.CommandOnCooldown):
		return await ctx.send(error)
	elif isinstance(error, commands.MissingRequiredArgument):
		return await ctx.send(error)
	elif isinstance(error, commands.CommandNotFound):
		return await ctx.send(error)
	elif isinstance(error, commands.CheckFailure):
		return
	else:
		await ctx.send(error)
		raise error

def cleanup_code(content):
	"""Automatically removes code blocks from the code."""
	# remove ```py\n```
	if content.startswith('```') and content.endswith('```'):
		return '\n'.join(content.split('\n')[1:-1])

	# remove `foo`
	return content.strip('` \n')

@bot.command(name='evaluate', aliases = ['eval', 'e'])
async def _eval(ctx, *, body: str):
	"""Evaluates a python code (developer only)"""
	_last_result = None
	if ctx.author.id not in [746904488396324864, 422967413295022080, 775198018441838642]:
		return
	"""Evaluates a code"""

	env = {
		'bot': bot,
		'ctx': ctx,
		'channel': ctx.channel,
		'author': ctx.author,
		'guild': ctx.guild,
		'message': ctx.message,
		'_': _last_result
	}

	env.update(globals())

	body = cleanup_code(body)
	stdout = io.StringIO()

	to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

	try:
		exec(to_compile, env)
	except Exception as e:
		return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

	func = env['func']
	try:
		with redirect_stdout(stdout):
			ret = await func()
	except Exception as e:
		value = stdout.getvalue()
		await ctx.send(f'**Error:**\n```py\n{value}{traceback.format_exc()}\n```')
	else:
		value = stdout.getvalue()
		try:
			await ctx.message.add_reaction('\u2705')
		except:
			pass

		if ret is None:
			if value:
				await ctx.send(f'```py\n{value}\n```')
		else:
			_last_result = ret
			await ctx.send(f'```py\n{value}{ret}\n```')

for file in os.listdir('cogs/'):
    if file.endswith('.py'):
        bot.load_extension(f'cogs.{file[:-3]}')


bot.run(TOKEN)

import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='>')

@bot.command()
async def ping(ctx):
	await ctx.send('pong')

@bot.command()
async def takecaresteve(ctx):
	await ctx.send('you too')

bot.run('NjA1ODM2MzcwNzQ5MDMwNDkw.XUCVYg.Ajcuh_sZGvz9-c-ovM_9Rf05Xo4')
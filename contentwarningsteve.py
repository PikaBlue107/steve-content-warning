import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='>')

@bot.command()
async def ping(ctx):
	await ctx.send('pong')

@bot.command()
async def takecaresteve(ctx):
	await ctx.send('you too')

bot.run('NjA1ODM2MzcwNzQ5MDMwNDkw.XUDRcQ.Mz9kAdGz9MwdgQWAC8NLORhYMKs')
import discord
from discord.ext import commands
from discord import client
import json

with open("auth.json", "r") as auth_file:
	auth_string = auth_file.dumps(token)

BOT_ID = 605836370749030490

bot = commands.Bot(command_prefix='>')

@bot.command()
async def ping(channel):
	await channel.send('pong')

@bot.command()
async def takecaresteve(channel):
	await channel.send('you too')

def is_not_me():
	def  predicate(ctx):
		return ctx.message.author.id != BOT_ID
	return commands.check(predicate)

@bot.listen('on_message')
@is_me()
async def copy_message(msg):
	channel = msg.channel
	await channel.send("did someone say something?")



bot.run('NjA1ODM2MzcwNzQ5MDMwNDkw.XUL_Zg.nxT6PCLXgCQWNkBOTDvdVBwjHOU')
import discord
from discord.ext import commands
from discord import client
import json

with open("auth.json", "r") as auth_file:
	auth_string = json.load(auth_file)["token"]
with open("package.json", "r") as data_file:
	data = json.load(data_file)
#TODO exit if auth.json or package.json not found
BOT_NAME = data["name"]
BOT_VERSION = data["version"]
BOT_DESC = data["description"]
BOT_MAIN = data["main"]
BOT_AUTHOR = data["author"]
BOT_DEPENDENCIES = data["dependencies"]
BOT_ID = 605836370749030490
TESTING_ID = 607087546333265920

bot = commands.Bot(command_prefix='>')

@bot.command()
async def ping(channel):
	await channel.send('pong')

@bot.command()
async def takecaresteve(channel):
	await channel.send('you too')

def is_not_me():
	print("hello?")
	def  predicate(ctx):
		print(ctx.message.author.id, BOT_ID)
		return ctx.message.author.id != BOT_ID
	print("hi")
	return commands.check(predicate)

@bot.listen('on_message')
@is_not_me()
async def copy_message(msg):
	if msg.author.bot: return
	channel = msg.channel
	if channel.id != TESTING_ID: return
	await channel.send(msg.content)



bot.run(auth_string)
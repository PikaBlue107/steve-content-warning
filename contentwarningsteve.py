import discord
from discord.ext import commands
from discord import client
import json


#Load 
try:
	auth_file = open("auth.json", "r")
	auth_string = json.load(auth_file)["token"]
except FileNotFoundError:
	print("Authorization file does not exist. Exiting...")
	exit()
except ValueError:
	print("auth.json is corrupted. Retrieve a new auth.json file, then relaunch. Exiting...")
	exit()
finally:
	auth_file.close()

try:
	package_file = open("package.json", "r")
	package = json.load(package_file)
except FileNotFoundError:
	print("package.json file does not exist. Exiting...")
	exit()
except ValueError:
	print("package.json is corrupted. Retreive a new package.json file, then relaunch. Exiting...")
	exit()
finally:
	package_file.close()

try:
	data_file = open("data.json", "r")
	data = json.load(data_file)
except FileNotFoundError:
	print("No data file found. Creating new file...")
	data = {
		"filters" : ()
	}
	with open("data.json", "w") as data_file:
		json.dump(data, data_file)
	print("Data file created.")
except ValueError:
	print("data.json is corrupted. Please fix the file manually, or delete it to restart with a fresh data file. Exiting...")
	exit()
finally:
	data_file.close()

print(data)

#TODO exit if auth.json or package.json not found
BOT_NAME = package["name"]
BOT_VERSION = package["version"]
BOT_DESC = package["description"]
BOT_MAIN = package["main"]
BOT_AUTHOR = package["author"]
BOT_DEPENDENCIES = package["dependencies"]
BOT_ID = 605836370749030490
TESTING_ID = 607087546333265920
OWNER_ID = 138461123899949057

bot = commands.Bot(command_prefix='>', description = BOT_DESC, owner_id = OWNER_ID, activity = discord.Activity(name = "Listening Closely"))

@bot.command()
async def ping(channel):
	await channel.send('pong')

@bot.command()
async def takecaresteve(channel):
	await channel.send('you too')

@bot.command()
async def seelist(channel, confirm=None):
	#TODO are you sure?
	print(data["filters"])
	await channel.send(data["filters"])

@bot.command()
async def add(channel, keyword):
	data["filters"].append(keyword)
	with open("data.json", "w") as data_file:
		json.dump(data, data_file)
	str = "Added keyword {} to filter list".format(keyword)
	print(str)
	await channel.send(str)

@bot.command()
async def remove(channel, keyword):
	try:
		data["filters"].remove(keyword)
		print("Successfully removed word from filter list.")
		await channel.send("Successfully removed word from filter list.")
	except ValueError:
		print("Word not fould in filter list.")
		await channel.send("Word not fould in filter list.")

def is_not_me():
	print("hello?")
	def  predicate(ctx):
		print(ctx.message.author.id, BOT_ID)
		return ctx.message.author.id != BOT_ID
	print("hi")
	return commands.check(predicate)

@bot.command()
async def shutdown(channel):
	with open("data.json", "w") as data_file:
		json.dump(data, data_file)
	await bot.logout()
	exit()

#@bot.listen('on_message')
@is_not_me()
async def copy_message(msg):
	if msg.author.bot: return
	channel = msg.channel
	if channel.id != TESTING_ID: return
	await channel.send(msg.content)

@bot.listen("on_message")
async def filter_message(msg):
	if msg.author.bot: return
	channel = msg.channel
	if channel.id != TESTING_ID: return
	filterIndex = []
	for filter in data["filters"]:
		index = msg.content.upper().find(filter.upper())
		if index > -1: filterIndex.append((index, index + len(filter)))
	if len(filterIndex) > 0:
		filterIndex.sort()
		reply = generate_message(msg.content, filterIndex)
		await channel.send(reply)



#TODO make bot generate filtered message when a filter word is detected
def generate_message(str, filterIndex):
	new = ""
	index = 0

	for filter in filterIndex:
		new = new + str[index:filter[0]] + "||" + str[filter[0]:filter[1]] + "||"
		index = filter[1]
		print(new)
	new = new + str[index:]

	print(new)

	return new


bot.run(auth_string)
print("hello")
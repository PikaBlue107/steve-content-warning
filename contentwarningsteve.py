import discord
from discord.ext import commands
from discord import client
from discord import errors
import json
import urllib.request


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

#TODO remove
@bot.command()
async def ping(channel):
	await channel.send('pong')

#TODO remove
@bot.command()
async def takecaresteve(channel):
	await channel.send('you too')

@bot.command()	#TODO delete_after?
async def seelist(channel, confirm=None):
	#TODO are you sure?
	print(data["filters"])
	await channel.send(data["filters"])

@bot.command()	#TODO delete_after?
async def add(channel, keyword):
	data["filters"].append(keyword)
	with open("data.json", "w") as data_file:
		json.dump(data, data_file)
	str = "Added keyword {} to filter list".format(keyword)
	print(str)
	await channel.send(str)

@bot.command()	#TODO delete_after?
async def remove(channel, keyword):
	try:
		data["filters"].remove(keyword)
		print("Successfully removed word from filter list.")
		await channel.send("Successfully removed word from filter list.")
	except ValueError:
		print("Word not fould in filter list.")
		await channel.send("Word not fould in filter list.")

def is_not_me():	#TODO get working
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

@bot.listen("on_message")
async def filter_message(msg):

	#TODO turn into decorations
	channel = msg.channel
	if msg.author.bot: return
	if channel.id != TESTING_ID: return

	#Nested fucntion, inserts spoiler tags ||content|| around finter words
	def generate_message(str, filterIndex):
		new = ""
		index = 0
		for filter in filterIndex:
			new = new + str[index:filter[0]] + "||" + str[filter[0]:filter[1]] + "||"
			index = filter[1]
		new = new + str[index:]
		print(new)
		return new

	#Scan for filter words
	filterIndex = []
	for filter in data["filters"]:
		index = msg.content.upper().find(filter.upper())
		if index > -1: filterIndex.append((index, index + len(filter)))


	if len(filterIndex) > 0: #Filter words found, enact filter protocol
		
		#Sort filtered words from the beginning of the message to the end
		filterIndex.sort()
		
		#Generate a reply message using generate_message nested function
		reply = generate_message(msg.content, filterIndex)

		#Delete user's message
		await msg.delete()

		#Switch to user's profile picture and username
		path_user = str(msg.author.avatar_url)
		print(path_user)
		username = msg.author.name
		req = urllib.request.Request(path_user, headers={'User-Agent' : "Magic Browser"})
		with urllib.request.urlopen(req) as con:
			pfp = con.read()
			await bot.user.edit(username=username, avatar=pfp)


		#Send message back to channel
		await channel.send(reply)

		#Switch back to Steve username and profile picture
		path_steve = "businessman.jpg"
		username = "Steve, Content Warning Expert"
		with open(path_steve, 'rb') as fp:
			pfp = fp.read()
			await bot.user.edit(username=username, avatar=pfp)
	
try:
	bot.run(auth_string)
except errors.LoginFailure: #TODO allow token update in console window
	print("Login unsuccessful. Please provide a new login token in auth.json. Exiting...")

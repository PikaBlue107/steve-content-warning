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
	guilds_file = open("guilds.json", "r")
	guilds = json.load(guilds_file)
except FileNotFoundError:
	print("No guilds file found. Creating new file...")
	guilds = {}
	with open("guilds.json", "w") as guilds_file:
		json.dump(guilds, guilds_file)
	print("Guilds file created.")
except ValueError:
	print("guilds.json is corrupted. Please fix the file manually, or delete it to restart with a fresh guilds file. Exiting...")
	exit()
finally:
	guilds_file.close()

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
BOT_COMMAND_PREFIX='>'

cur_channel = None

bot = commands.Bot(command_prefix=BOT_COMMAND_PREFIX, description = BOT_DESC, owner_id = OWNER_ID, activity = discord.Activity(name = "Listening Closely"))




def register_guild(guild_id):
	print(guild_id)
	print(type(guild_id))
	guilds[int(guild_id)] = {
		"whitelist": [],
		"blacklist": [],
		"whitelist_enable": False,
		"filters": []
	}
	guilds[5] = "test"
	print(guilds)
	save()


async def pp(str):
	print(str)
	await cur_channel.send(str)

def save():
	print(guilds)
	with open("guilds.json", "w") as guilds_file:
		json.dump(guilds, guilds_file)



#possibly never to be used
def remove_guild(guild_id):
	data.pop(guild_id)
	save()


def is_not_me():	#TODO get working
	print("hello?")
	def  predicate(ctx):
		print(ctx.message.author.id, BOT_ID)
		return ctx.message.author.id != BOT_ID
	print("hi")
	return commands.check(predicate)

@bot.command()
async def shutdown(channel):
	with open("guilds.json", "w") as guilds_file:
		json.dump(guilds, guilds_file)
	await bot.logout()
	exit()


#COMMANDS


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
	global cur_channel
	cur_channel = channel
	guild_id = channel.guild.id
	await pp(type(guild_id))
	await pp(guilds)
	await pp(guild_id)
	await pp(guild_id in guilds.keys())


	if guild_id in guilds.keys():
		#TODO are you sure?
		filters = guilds[guild_id]["filters"]
		await pp(filters)
	else:
		await pp("No data for server '" + channel.guild.name + "'")

@bot.command()	#TODO delete_after?
async def add(channel, keyword):
	global cur_channel
	cur_channel = channel
	guild_id = channel.guild.id

	if guild_id not in guilds:
		register_guild(guild_id)
	guilds[guild_id]["filters"].append(keyword)
	with open("guilds.json", "w") as guilds_file:
		json.dump(guilds, guilds_file)
	await pp("Added keyword {} to filter list".format(keyword))


@bot.command()	#TODO delete_after?
async def remove(channel, keyword):
	global cur_channel
	cur_channel = channel
	guild_id = channel.guild.id
	if guild_id not in guilds:
		await pp("No data for server '" + channel.guild.name + "'")
	try:
		guilds[guild_id]["filters"].remove(keyword)
		await pp("Successfully removed word from filter list.")
	except ValueError:
		await pp("Word not found in filter list.")


async def whitelist_on():
	guilds[guild_id]["whitelist_enable"] = True
	await pp("Whitelist mode enabled, blacklist off.")
async def blacklist_on():
	guilds[guild_id]["whitelist_enable"] = False
	await pp("Blacklist mode enabled, whitelist off.")

@bot.command()
async def whitelist(channel, argument):
	global cur_channel
	cur_channel = channel
	guild_id = channel.guild.id
	if guild_id not in guilds:
		register_guild(guild_id)

	if argument is None:
		guilds[guild_id]["whitelist"].append(channel.id)
		await pp('#' + channel.name + "added to whitelist.")
	elif argument == "print":
		await pp(guilds[guild_id]["blacklist"])
	elif argument.startswith("<#"):
		channel_id = argument.strip(('<','#','>'))
		guilds[guild_id]["whitelist"].append(channel_id)
		await pp('#' + channel.guild.get_channel(channel_id).name + "added to whitelist.")
	elif argument.lower() == "on": await whitelist_on()
	elif argument.lower() == "off": await blacklist_on()
	elif argument.lower() == "toggle":
		if guilds[guild_id]["whitelist_enable"]: await blacklist_on()
		else: await whitelist_on()
	else:
		for cnl in channel.guild.channels:
			if cnl.name == argument:
				channel_id = cnl.id
				guilds[guild_id]["whitelist"].append(channel_id)
				return
		await pp("Unable to process command. Type a #channel-name, channel-name, or a setting such as 'on', 'off', 'toggle', or 'print'")

@bot.command()
async def blacklist(channel, argument):
	guild_id = channel.guild.id
	if guild_id not in guilds:
		register_guild(guild_id)

	if argument is None:
		guilds[guild_id]["blacklist"].append(channel.id)
		await pp('#' + channel.name + "added to blacklist.")
	elif argument == "print":
		await pp(guilds[guild_id]["blacklist"])
	elif argument.startswith("<#"):
		channel_id = argument.strip(('<','#','>'))
		guilds[guild_id]["blacklist"].append(channel_id)
		await pp('#' + channel.guild.get_channel(channel_id).name + "added to blacklist.")
	elif argument.lower() == "on": await blacklist_on()
	elif argument.lower() == "off": await whitelist_on()
	elif argument.lower() == "toggle":
		if guilds[guild_id]["whitelist_enable"]: await blacklist_on()
		else: await whitelist_on()
	else:
		for cnl in channel.guild.channels:
			if cnl.name == argument:
				channel_id = cnl.id
				guilds[guild_id]["blacklist"].append(channel_id)
				return
		await pp("Unable to process command. Type a #channel-name, channel-name, or a setting such as 'on', 'off', 'toggle', or 'print'")




@bot.listen("on_message")
async def filter_message(msg):

	#TODO turn into decorations
	channel = msg.channel
	guild_id = channel.guild.id
	if msg.author.bot: return
	if channel.guild.id not in guilds: return
	if msg.content.startswith(BOT_COMMAND_PREFIX): return


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
	for filter in guilds[guild_id]["filters"]:
		index = msg.content.upper().find(filter.upper())
		if index > -1: filterIndex.append((index, index + len(filter)))


	if len(filterIndex) > 0: #Filter words found, enact filter protocol
		
		#Sort filtered words from the beginning of the message to the end
		filterIndex.sort()
		
		#Generate a reply message using generate_message nested function
		reply = generate_message(msg.content, filterIndex)


		#Get the user's profile picture and nickname
		path_user = msg.author.avatar_url
		nickname = msg.author.display_name
		
		#Create an Embed object with the user's filtered post
		embed = discord.Embed(
  			description=reply,
  			color=0xecce8b
		)
		embed.set_author(name=nickname, icon_url=path_user)

		#Send message back to channel
		await channel.send(embed=embed)
		print(reply)
		
		#Delete user's message
		await msg.delete()
	
try:
	bot.run(auth_string)
except errors.LoginFailure: #TODO allow token update in console window
	print("Login unsuccessful. Please provide a new login token in auth.json. Exiting...")
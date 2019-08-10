import discord
from discord.ext import commands
from discord import client
from discord import errors
import json
import pickle
import urllib.request




#PRIORITY BUGS
#TODO figure out file structure

#MAJOR BUGS

#NEW FEATURES
#TODO Toggle all-filter per user

#MINOR BUGS/ALTERATIONS
#TODO improve logic in change_list
#TODO decorator-ify repeated pre-function code

cur_ctx = None


class History:
	time = None
	user = None
	safeword = None
	nick = None
	def __init__(self, time, user, nick, safeword=None):
		self.time = time
		self.user = user
		self.nick = nick
		self.safeword = safeword

def register_guild(guild_id):
	print(guild_id)
	print(type(guild_id))
	guilds[int(guild_id)] = {
		"whitelist": {},
		"blacklist": {},
		"whitelist_enable": False,
		"filters": {}
	}
	print(guilds)
	save()


async def pp(str):
	print(str)
	await cur_ctx.send(str)

def save():
	print(guilds)
	with open("guilds.pickle", "wb") as guilds_file:
		pickle.dump(guilds, guilds_file)

def make_history(ctx, safeword=None):
	return History(time=ctx.message.created_at, user=ctx.author.id, nick=ctx.author.display_name, safeword=safeword)

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
async def shutdown(ctx):
	save()
	await bot.logout()
	exit()


#COMMANDS


#TODO remove
@bot.command()
async def ping(ctx):
	await ctx.send('pong')

#TODO remove
@bot.command()
async def takecaresteve(ctx):
	await ctx.send('you too')

@bot.command()	#TODO delete_after?
async def seelist(ctx, confirm=None):
	global cur_ctx
	cur_ctx = ctx
	guild_id = ctx.guild.id
	await pp(type(guild_id))
	await pp(guilds)
	await pp(guild_id)
	await pp(guild_id in guilds.keys())


	if guild_id in guilds.keys():
		#TODO are you sure?
		filters = guilds[guild_id]["filters"]
		await pp(filters)
	else:
		await pp("No data for server '" + ctx.guild.name + "'")

@bot.command()	#TODO delete_after?
async def add(ctx, keyword):
	global cur_ctx
	cur_ctx = ctx

	guild_id = ctx.guild.id
	if guild_id not in guilds:
		register_guild(guild_id)

	guilds[guild_id]["filters"][keyword] = make_history(ctx)
	save()
	await pp("Added keyword {} to filter list".format(keyword))


@bot.command()	#TODO delete_after?
async def remove(ctx, keyword):
	global cur_ctx
	cur_ctx = ctx
	guild_id = ctx.guild.id
	if guild_id not in guilds:
		await pp("No data for server '" + ctx.guild.name + "'")
	try:
		guilds[guild_id]["filters"].pop(keyword)
		await pp("Successfully removed word from filter list.")
	except ValueError:
		await pp("Word not found in filter list.")

async def change_list(ctx, white, argument=None):
	async def whitelist_on():
		guilds[guild_id]["whitelist_enable"] = True
		await pp("Whitelist mode enabled, blacklist off.")
	async def blacklist_on():
		guilds[guild_id]["whitelist_enable"] = False
		await pp("Blacklist mode enabled, whitelist off.")

	global cur_ctx
	cur_ctx = ctx

	guild_id = ctx.guild.id
	if guild_id not in guilds:
		register_guild(guild_id)
	channel = ctx.channel

	history = make_history(ctx)
	string = "whitelist" if white else "blacklist"

	if argument is None:
		guilds[guild_id][string][channel_id] = history
		await pp('#' + channel.name + "added to " + string + ".")
	elif argument == "print":
		await pp(guilds[guild_id][string])
	elif argument.startswith("<#"):
		channel_id = int(argument.strip('<').strip('#').strip('>'))
		guilds[guild_id][string][channel_id] = history
		await pp('#' + ctx.guild.get_channel(channel_id).name + " added to " + string + ".")
	elif argument.lower() == "on": await whitelist_on() if white else await blacklist_on()
	elif argument.lower() == "off": await blacklist_on() if white else await whitelist_on()
	elif argument.lower() == "toggle":
		if guilds[guild_id]["whitelist_enable"]: await blacklist_on()
		else: await whitelist_on()
	else:
		for cnl in ctx.guild.channels:
			if cnl.name == argument:
				channel_id = cnl.id
				guilds[guild_id][string][channel_id] = history
				return
		await pp("Unable to process command. Type a #channel-name, channel-name, or a setting such as 'on', 'off', 'toggle', or 'print'")
	save()

@bot.command()
async def whitelist(ctx, argument=None):
	change_list(ctx=ctx, white=True, argument=argument)
	
@bot.command()
async def blacklist(ctx, argument):
	change_list(ctx=ctx, white=False, argument=argument)


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
	guilds_file = open("guilds.pickle", "rb")
	guilds = pickle.load(guilds_file)
except FileNotFoundError:
	print("No guilds file found. Creating new file...")
	guilds = {}
	with open("guilds.pickle", "wb") as guilds_file:
		pickle.dump(guilds, guilds_file)
	print("Guilds file created.")
except ValueError:
	print("guilds.pickle is corrupted. Please fix the file manually, or delete it to restart with a fresh guilds file. Exiting...")
	exit()
finally:
	guilds_file.close()

#Declare variables
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

#Initialize
bot = commands.Bot(command_prefix=BOT_COMMAND_PREFIX, description = BOT_DESC, owner_id = OWNER_ID, activity = discord.Activity(name = "Listening Closely"))

#Run
try:
	bot.run(auth_string)
except errors.LoginFailure:
	print("Login unsuccessful. Please provide a new login token in auth.json. Exiting...")
#Discord
import discord
from discord.ext import commands
from discord import errors

#Error handling
from pickle import UnpicklingError
from json import JSONDecodeError

#My files
from steveIO import SteveIO


AUTH_LOC = "auth.json"
PACKAGE_LOC = "package.json"
GUILDS_LOC = "guilds.pickle"

#Create IO Object for loading and saving data
io = SteveIO(auth_loc=AUTH_LOC, package_loc=PACKAGE_LOC, guilds_loc=GUILDS_LOC)

#Error codes
SUCCESS = 0
AUTH_MISSING = 1
AUTH_CORRUPT = 2
PACKAGE_MISSING = 3
PACKAGE_CORRUPT = 4
GUILDS_CORRUPT = 5

try:
	auth_string = io.loadAuth()
except FileNotFoundError:
	print("auth.json not found at filepath '" + AUTH_LOC + "'. Exiting...")
	exit(AUTH_MISSING)
except JSONDecodeError:
	print(AUTH_LOC + " is unreadable by JSON. Please fix manually or by retrieving a new auth.json file. Exiting...")
	exit(AUTH_CORRUPT)

try:
	package = io.loadPackage()
except FileNotFoundError:
	print("package.json not found at filepath '" + PACKAGE_LOC + "'. Exiting...")
	exit(PACKAGE_MISSING)
except JSONDecodeError:
	print(PACKAGE_LOC + " is unreadable by JSON. Please fix manually or by retrieving a new package.json file. Exiting...")
	exit(PACKAGE_CORRUPT)

try:
	guilds = io.loadGuilds()
except UnpicklingError:
	print(GUILDS_LOC + " is unreadable by Python Pickle. Remove guilds.pickle from destination '" + GUILDS_LOC + "' and then restart to generate a blank file. Exiting...")
	exit(GUILDS_CORRUPT)

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

cur_ctx = None


#Initialize
bot = commands.Bot(command_prefix=BOT_COMMAND_PREFIX, description = BOT_DESC, owner_id = OWNER_ID)

def start():
	try:
		bot.run(auth_string)
	except errors.LoginFailure:
		print("Login unsuccessful. Please provide a new login token in auth.json. Exiting...")
		exit(2)




def register_guild(guild_id):
	print(guild_id)
	print(type(guild_id))
	guilds[int(guild_id)] = {
		"whitelist": {},
		"blacklist": {},
		"whitelist_enable": False,
		"filters": {},
		"bot_channel": None
	}
	print(guilds)
	io.save(guilds)

def update_guild(guild):
	guild["bot_channel"] = None


async def pp(str):
	print(str)
	await cur_ctx.send(str)

def make_history(ctx, safeword=None):
	return History(time=ctx.message.created_at, user=ctx.author.id, nick=ctx.author.display_name, safeword=safeword)

#possibly never to be used
def remove_guild(guild_id):
	data.pop(guild_id)
	io.save(guilds)


# def is_not_me():	#TODO get working
# 	print("hello?")
# 	def  predicate(ctx):
# 		print(ctx.message.author.id, BOT_ID)
# 		return ctx.message.author.id != BOT_ID
# 	print("hi")
# 	return commands.check(predicate)

@bot.command()
async def shutdown(ctx):
	print("shutdown")
	with open("tmp.txt", "w") as tmp:
		tmp.write("false")
	io.save(guilds)
	await bot.logout()

@bot.command()
async def restart(ctx):
	with open("tmp.txt", "w") as tmp:
		tmp.write("true")
	io.save(guilds)
	await bot.logout()

#TODO override close
#async def close(self, return=ret):



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
	io.save(guilds)
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
	channel_id = ctx.channel.id

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
	io.save(guilds)

@bot.command()
async def whitelist(ctx, argument=None):
	await change_list(ctx=ctx, white=True, argument=argument)
	
@bot.command()
async def blacklist(ctx, argument):
	await change_list(ctx=ctx, white=False, argument=argument)


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


	# @self.event
	# async def on_ready():
	# 	for guild_id in list(guilds.keys()):
start()
import json
import pickle
import sys
from history import History

class SteveIO:
	AUTH_LOC_DEFAULT = "auth.json"
	PACKAGE_LOC_DEFAULT = "package.json"
	GUILDS_LOC_DEFAULT = "guilds.pickle"

	

	def __init__(self, auth_loc=AUTH_LOC_DEFAULT, package_loc=PACKAGE_LOC_DEFAULT, guilds_loc=GUILDS_LOC_DEFAULT):
		self.AUTH_LOC = auth_loc
		self.PACKAGE_LOC = package_loc
		self.GUILDS_LOC = guilds_loc

	def loadAuth(self):
		with open(self.AUTH_LOC, "r") as auth_file:
			auth_string = json.load(auth_file)["token"]
			return auth_string

	def loadPackage(self):
		with open(self.PACKAGE_LOC, "r") as package_file:
			package = json.load(package_file)
			return package

	def loadGuilds(self):
		try:
			with open(self.GUILDS_LOC, "rb") as guilds_file:	#will close guilds_file if json throws an error
				guilds = pickle.load(guilds_file)
		except FileNotFoundError:	#catches FileNotFoundError so that we can create a fresh guilds file
			print("No guilds file found. Creating new guilds file.")
			guilds = {}
			with open(self.GUILDS_LOC, "wb") as guilds_file:
				pickle.dump(guilds, guilds_file)


		return guilds

	def save(self, guilds):
		print("Saving to file '" + self.GUILDS_LOC + "': " + str(guilds))
		with open(self.GUILDS_LOC, "wb") as guilds_file:
			pickle.dump(guilds, guilds_file)
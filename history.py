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
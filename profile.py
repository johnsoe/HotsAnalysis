
class HeroStats:

	def __init__(self, name):
		self.name = name
		self.level = 0
		self.gamesPlayed = 0
		self.winrate = 0.0

	def __str__(self):
		return "{} level {} with {} games played at a {}% winrate".format(self.name, self.level, self.gamesPlayed, self.winrate)

	def toJSON(self):
		return {
			"name" : self.name,
			"level" : self.level,
			"gamesPlayed": self.gamesPlayed,
			"winrate" : self.winrate
		}

class MapStats:

	def __init__(self, name):
		self.name = name
		self.gamesPlayed = 0
		self.winrate = 0.0

	def __str__(self):
		return "{} played {} times with a {}% winrate".format(self.name, self.gamesPlayed, self.winrate)

	def toJSON(self):
		return {
			"name" : self.name,
			"gamesPlayed": self.gamesPlayed,
			"winrate" : self.winrate
		}

class EnemyHeroStats:

	def __init__(self, name):
		self.name = name
		self.gamesPlayed = 0
		self.winrate = 0.0

	def __str__(self):
		return "{} played against {} times with a {}% winrate".format(self.name, self.gamesPlayed, self.winrate)

	def toJSON(self):
		return {
			"name" : self.name,
			"gamesPlayed": self.gamesPlayed,
			"winrate" : self.winrate
		}

class Profile:

	def __init__(self, hotslogsId):
		self.hotslogsId = hotslogsId
		self.heroes = []
		self.maps = []
		self.enemies = []

	def toJSON(self):
		return {
			"hotslogsId": self.hotslogsId,
			"heroes": [hero.toJSON() for hero in self.heroes],
			"maps": [aMap.toJSON() for aMap in self.maps],
			"enemies": [enemy.toJSON() for enemy in self.enemies]
		}
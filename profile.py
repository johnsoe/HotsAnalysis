
class HeroStats:

	def __init__(self, name):
		self.name = name
		self.level = 0
		self.gamesPlayed = 0
		self.winrate = 0.0

	def __str__(self):
		return "{} level {} with {} games played at a {}% winrate".format(self.name, self.level, self.gamesPlayed, self.winrate)

class MapStats:

	def __init__(self, name):
		self.name = name
		self.gamesPlayed = 0
		self.winrate = 0.0

	def __str__(self):
		return "{} played {} times with a {}% winrate".format(self.name, self.gamesPlayed, self.winrate)

class EnemyHeroStats:

	def __init__(self, name):
		self.name = name
		self.gamesPlayed = 0
		self.winrate = 0.0

	def __str__(self):
		return "{} played against {} times with a {}% winrate".format(self.name, self.gamesPlayed, self.winrate)
		
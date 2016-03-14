
class HeroStat:

	def __init__(self, name):
		self.name = name
		self.level = 0
		self.gamesPlayed = 0
		self.winrate = 0.0

	def __str__(self):
		return "{} level: {} games: {} rate: {}".format(self.name, self.level, self.gamesPlayed, self.winrate)
		
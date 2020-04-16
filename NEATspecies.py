import neat
class Species:
	def __init__(self, members):
		self.members = members
		self.c1 = random.random()
		self.c2 = random.random() #d = c1(E/N) + c2(D/N) + c3W
		self.c3 = random.random()
		self.N = len(members)
		self.fitness = None

	def average_fitness():
		fit = 0
		count = 0
		for i in self.members:
			if i.fitness != None:
				fit += i.fitness
				count += 1
		if count == 0:
			return
		else:
			self.fitness = fit / count

class Habitat:
	def __init__(self, species):
		self.species = species
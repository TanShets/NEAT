import neat
class Species:
	def __init__(self, num, members):
		self.num = num #Basically identification number for a species
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

	def findDeviation(member, new_member):
		innov = {}
		sources = {}
		outs = {}
		gene2 = [None for i in range(len(member.genes))]
		E = 0
		D = 0
		W = 0
		no_of_weights = 0 #Gives the number of corresponding genes

		for i in range(len(member.genes)):
			if innov.get(member.genes[i].innovation, -1) == -1:
				innov[member.genes[i].innovation] = [i]
			else:
				innov[member.genes[i].innovation].append(i)

			if sources.get(member.genes[i].start, -1) == -1:
				sources[member.genes[i].start] = [i]
			else:
				sources[member.genes[i].start].append(i)

			if outs.get(member.genes[i].out, -1) == -1:
				outs[member.genes[i].out] = [i]
			else:
				outs[member.genes[i].out].append(i)

		for i in member.genes:
			inn = set(innov.get(i.innovation))
			src = set(sources.get(i.start))
			out = set(outs.get(i.out))
			if len(inn.intersection(src.intersection(out))) > 0:
				common = list(inn.intersection(src.intersection(out)))[0]
				if gene2[common] == None:
					gene2[common] = i #Only genes with exact innovation num, source and des correspond to each other
				else:
					gene2.append(i) #Duplicate gene
			else:
				gene2.append(i)

		for i in range(len(member.genes)):
			if gene2[i] != None:
				W += member.genes[i].weight - gene2[i].weight
				no_of_weights += 1
			else:
				D += 1
		if len(gene2) > len(member.genes):
			E = len(gen2) - len(member.genes)
		#Note: It's very likely that N in the formula denotes the number of matching genes
		
		if no_of_weights > 0:
			d = self.c1 * (E / no_of_weights) + self.c2 * (D / no_of_weights) + self.c3 * (W / no_of_weights)
		else:
			d = self.c1 * (E / self.N) + self.c2 * (D / self.N) + self.c3 * (W / self.N)

		return d

	def Species_Deviation(new_member):
		d = 0
		for i in self.members:
			d += findDeviation(i, new_member)
		d /= self.N
		return d

	def New_Generation(new_member, isFirst):
		if isFirst:
			self.members = [new_member]
			self.N = 1
			self.fitness = None
		else:
			self.members.append(new_member)
			self.N += 1

	def Insertion_Sort(capacity):
		best = []
		for i in self.members:
			j = 0
			while j < len(best) and i.fitness < best[j].fitness:
				j += 1
			if j == len(best) and j < capacity:
				best.append(i)
			else:
				if j < len(best):
					best.insert(j, i)
					if len(best) == capacity + 1:
						best.pop()
		return best

	def Crossing(percentage_best):
		capacity = int(percentage_best * self.N / 100)
		best = self.Insertion_Sort(capacity)
		new_children = []
		for i in range(self.N):
			parent1 = random.choice(best)
			parent2 = random.choice(self.members)
			new_child = parent1.Cross_over(parent2)
			new_children.append(new_child)
		return new_children

class Habitat:
	def __init__(self, species, critical_deviation, percentage_best):
		self.species = species
		self.critical_deviation = critical_deviation
		self.percentage_best = percentage_best

	def findSpecies(new_children):
		dicti = {}
		dicti1 = {}
		for new_child in new_children:
			isplaced = False
			for i in range(len(self.species)):
				d = self.species[i].Species_Deviation(new_child)
				dicti[self.species[i].num] = i
				dicti1[i] = True
				if d <= self.critical_deviation:
					new_child.species = self.species[i].num
					self.species[i].members.append(new_child)
					self.species[i].N += 1
					isplaced = True
					break

			if not isplaced:
				nx = len(self.species)
				new_child.species = nx
				new_members = [new_child]
				new_species = Species(nx, new_members)
				self.species.append(new_species)

		for i in new_children:
			self.species[i.species].New_Generation(i, dicti1[i.species])
			if dicti1.get(i.species):
				dicti[i.species] = False

	def obtain_New_Generation():
		new_children = []
		for i in self.species:
			new_child = i.Crossing()
			new_children += new_child
		chance = random.randint(0, 100)
		if chance < 4:
			new_child = self.InterSpecies_Cross_over()
			new_children.append(new_child)
		self.findSpecies(new_children)

	def InterSpecies_Cross_over():
		species1 = random.choice(self.species)
		species2 = species1
		while species2 == species1:
			species2 = random.choice(self.species)
		parent1 = random.choice(species1.members)
		parent2 = random.choice(species2.members)
		new_child = parent1.Cross_over(parent2)
		return new_child
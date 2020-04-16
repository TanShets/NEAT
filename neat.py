import random
import copy
types_neuron = {
	'Input': 0,
	'Hidden': 1,
	'Output': 2
}

class Gene:
	def __init__(self, start, out, innovation): #The most basic constructor for a gene
		self.start = start
		self.out = out
		x = random.randint(1, 20) * random.random() #Randomly generated number between (0, 20) for the weight
		while x == 0:
			x = random.randint(1, 20) * random.random()
		self.weight = pow(-1, random.randint(0, 2)) * x #Considering possibility of a negative weight
		self.innovation = innovation #Innovation number will arise from ancestor gene
		y = random.randint(1, 11) * random.random() + 0.25
		if y <= 0.5:
			self.status = False #Status is randomly decided to determine whether a gene is active or not
		else:
			self.status = True #Probability of it being inactive is 2.5%
	
	def __init__(self, num, gene, isStart): #Used for mutated genes
		if isStart:
			self.__init__(num, gene.out, gene.innovation) #Random number is the source here
		else:
			self.__init__(gene.start, num, gene.innovation) #Destination was random

	def mutate_weight_status(): #Changes the weight of a gene as well has some chances of disabling or enabling a gene
		wt = 0
		while wt == 0:
			wt = pow(-1, random.randint(0, 2)) * random.randint(1, 20) * random.random()
		self.weight = wt
		stat = random.randint(1, 11) * random.random() + 0.25
		if y <= 0.5: #Chance of disabling = 2.5%
			self.status = False
		else:
			self.status = True

class Node:
	def __init__(self, num, typef): #Holds the number, as well as type of node.
		self.num = num
		self.type = typef

class Genome:
	def __init__(self, nodes, genes): #Contains a list of nodes and genes
		self.nodes = nodes
		self.genes = genes
	
	def findNode(num):
		for i in self.nodes:
			if i.num == num:
				return i
		return None

	def create_new_node():
		xnodes = [i.num for i in self.nodes]
		x = max(xnodes) + 1 #New value will have new number which is sequential
		new_node = Node(x, 1) #It means any new neuron will always be in the hidden layer
		self.nodes.append(new_node)
		y = min(xnodes)
		l = len(self.genes)
		i = random.randint(0, l)
		while findNode(self.genes[i].start).type == 0:
			i = random.randint(0, l)
		new_gene = Gene(x, self.genes[i], True) #A gene with new vertex as a source will always arise
		self.genes.append(new_gene)
		number = random.randint(1, 11) * random.random()
		if number < 3: #There is a 20% chance of getting a gene with new node as destination
			i = random.randint(0, l)
			while findNode(self.genes[i].out).type == 2:
				i = random.randint(0, l)
			new_gene = Gene(x, self.genes[i], False)
			self.genes.append(new_gene)
	#No Restrictions, we not have prevented the mutation of genes which do a src change for those with i/p as source, and change in des where main output is destination.
	def add_gene():
		x = random.choice(self.genes)
		y = random.choice(self.nodes)
		val = random.randint(0, 2)
		new_gene = None
		if val == 0: #In this case we're making a random value as the out value
			while y.type == 0:
				y = random.choice(self.nodes)
			new_gene = Gene(y.num, x, False)
		else:
			while y.type == 2:
				y = random.choice(self.nodes)
			new_gene = Gene(y.num, x, True)
		self.genes.append(new_gene)

	def shouldMutate():
		chance = random.randint(0, 100) #Basically 1 to 100 are all fair game
		if chance < 8: #Therefore you only have an 8% chance for mutation
			self.Mutate()
		else:
			return

	def Mutate():
		chance = random.randint(0, 3)
		if chance == 0:
			i = random.randint(0, len(self.genes))
			self.genes[i].mutate_weight_status()
		elif chance == 1:
			self.create_new_node()
		else:
			self.add_gene()

	def Cross_over(mate):
		self.shouldMutate() #Essentially mutates before crossing
		mate.shouldMutate()
		child = None
		child_nodes = list(set(self.genes).union(set(mate.genes)))
		nodal = {}
		child_genes = [] #Genes with the same Innovation number will be crossed
		innov = {}
		sources = {}
		outs = {}
		gene1 = copy.deepcopy(self.genes)
		gene2 = [None for i in range(len(self.genes))]
		for i in range(len(gene1)):
			if innov.get(gene1[i].innovation, -1) == -1:
				innov[gene1[i].innovation] = [i]
			else:
				innov[gene1[i].innovation].append(i)

			if sources.get(gene1[i].start, -1) == -1:
				sources[gene1[i].start] = [i]
			else:
				sources[gene1[i].start].append(i)

			if outs.get(gene1[i].out, -1) == -1:
				outs[gene1[i].out] = [i]
			else:
				outs[gene1[i].out].append(i)
		
		for i in mate.genes: #gene2 matches gene1 in terms of corresponding genes
			inn = set(innov.get(i.innovation))
			src = set(sources.get(i.start))
			out = set(outs.get(i.out))
			common = None
			if len(inn.intersection(src.intersection(out))) > 0:
				common = list(inn.intersection(src.intersection(out)))[0] #Perfectly matching genes
				gene2[common] = i
			elif len(inn.intersection(src)) > 0:
				common = list(inn.intersection(src))
				n = len(common)
				j = 0
				while j < n:
					if common[j] == None:
						break
					else:
						j += 1
				
				if j == n:
					gene2.append(i) #Excess gene
				else:
					gene2[common[j]] = i #Matching in innovation number and source
			elif len(inn.intersection(out)) > 0:
				common = list(inn.intersection(out))
				n = len(common)
				j = 0
				while j < n:
					if common[j] == None:
						break
					else:
						j += 1

				if j == n:
					gene2.append(i) #Excess gene
				else:
					gene2[common[j]] = i #Matching in innovation number and destination
			else:
				gene2.append(i) #Excess gene

		for i in range(len(gene1)):
			x = random.randint(0, 2)
			if x == 0:
				x = gene1[i]
			else:
				x = gene2[i]
			
			if x != None:
				if not nodal.get(x.start, False):
					nodal[x.start] = True

				if not nodal.get(x.out, False):
					nodal[x.out] = True
				child_genes.append(x)

		for i in child_nodes:
			if not nodal.get(i, False):
				child_nodes.remove(i)

		child = Genome(child_nodes, child_genes)
		return child
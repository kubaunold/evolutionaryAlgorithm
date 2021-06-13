import random

# evolution strategy (mu + lambda) of the ackley objective function
from numpy import asarray, exp, sqrt, cos, e, pi, argsort
from numpy.random import randn, rand, seed, normal

# objective function
def objective(v):
	x, y = v
	return -20.0 * exp(-0.2 * sqrt(0.5 * (x**2 + y**2))) - exp(0.5 * (cos(2 * pi * x) + cos(2 * pi * y))) + e + 20


# check if a point is within the bounds of the search
def in_bounds(point, bounds):
	# enumerate all dimensions of the point
	for d in range(len(bounds)):
		# check if out of bounds for this dimension
		if point[d] < bounds[d, 0] or point[d] > bounds[d, 1]:
			return False
	return True

# mutate point
def mutate(point, sigmaNormal):
	mutant = list()
	mutant = point.copy()
	
	# parameters for normal noise
	muNormal, sigmaNormal = 0, sigmaNormal # mean and standard deviation

	# enumerate all dimensions of the point
	for d in range(len(point)):

		mutant[d] = point[d] + normal(muNormal, sigmaNormal, 1)[0]   

	return mutant



# evolution strategy (mu + lambda) algorithm
def es_plus(objective, bounds, n_iter, step_size, mu, lam):
	best, best_eval = None, 1e+10
	# calculate the number of children per parent
	n_children = int(lam / mu)

	### INITIAL POPULATION - of mu-parents size
	init_pop = list()
	for _ in range(mu):    # create first parents
		candidate = None
		while candidate is None or not in_bounds(candidate, bounds):
			### bounds[:, 0] - select first colum
			candidate = bounds[:, 0] + rand(len(bounds)) * (bounds[:, 1] - bounds[:, 0])
		init_pop.append(candidate)

	parents = list()
	parents = init_pop

	n_iter = 1

	### PERFORMING EVOLUTION
	for epoch in range(n_iter):
		print(f"Epoka {epoch}:")
		### GENERATE POPULATION
		offspring = list()
		# temporary population of cloned parents (as many as lam-children)
		offspring = [random.choice(parents) for _ in range(lam)]
		
		#####################################################################
		print(f"INITIAL OFFSPRING:")
		for o in range(len(offspring)): print(f"osobnik {o}: {offspring[o]}")
		#####################################################################

		### CROSSING
		percentageOfCrossing = 0.20
		indexesForCrossing = range(int(percentageOfCrossing*lam))		#0..4
		# uncrossedIndexes = range(int(percentageOfCrossing*lam), lam)#5..20
		# first 20% will be crossed
		for i in indexesForCrossing:
			# specimen will be crossed
			specimen = offspring[i]

			# 2nd parent selected for crossing
			specimens_spouse = None 
			while (specimens_spouse is None) or (specimens_spouse is specimen):
				specimens_spouse = random.choice(parents)

			# crossing of specimen
			for gene_idx in range(len(specimen)):	# gene here is x1, x2, ...
				if(random.choice([True, False])):	# if True, then take gene from spouse
					specimen[gene_idx] = specimens_spouse[gene_idx]

			offspring[i] = specimen

		#####################################################################
		print(f"AFTER CROSSING of {percentageOfCrossing*100}%:")
		for o in range(len(offspring)): print(f"osobnik {o}: {offspring[o]}")
		#####################################################################

		### MUTATION
		# now mutate whole offspring
		offspring = [mutate(unit, step_size) for unit in offspring]

		#####################################################################
		print("AFTER MUTATION offspring:")
		for o in range(len(offspring)): print(f"osobnik {o}: {offspring[o]}")
		#####################################################################

		#



	# # rank first parents
	# #TODO

	# ## REPRODUCTION - process of creating children
	# # from first mu parents creat lambda children
	# first_offspring = list()
	# for _ in range(lam):	# create first children
	# 	candidate = None
	# 	while candidate is None or not in_bounds(candidate, bounds):
	# 		candidate = random.choice(first_parents)
	# 		# MUTATION
	# 		candidate += 
		



	
	# # perform the search
	# for epoch in range(n_iter):
	# 	# evaluate fitness for the population
	# 	scores = [objective(c) for c in population]
	# 	# rank scores in ascending order
	# 	ranks = argsort(argsort(scores))
	# 	# select the indexes for the top mu ranked solutions
	# 	selected = [i for i,_ in enumerate(ranks) if ranks[i] < mu]
	# 	# create children from parents
	# 	children = list()
	# 	for i in selected:
	# 		# check if this parent is the best solution ever seen
	# 		if scores[i] < best_eval:
	# 			best, best_eval = population[i], scores[i]
	# 			print('Epoka %d, Najlepszy osobnik: f(%s) = %.5f' % (epoch, best, best_eval))
			
	# 		# keep the parent
	# 		children.append(population[i])
	# 		# create children for parent
	# 		for _ in range(n_children):
	# 			child = None
	# 			while child is None or not in_bounds(child, bounds):
	# 				child = population[i] + randn(len(bounds)) * step_size
	# 			children.append(child)
	# 	# replace population with children
	# 	population = children
	return [best, best_eval]


if __name__=='__main__':
	print("You invoked 'esPlus' by name!")

	# seed the pseudorandom number generator
	seed(1)
	# define range for input
	bounds = asarray([[-5.0, 5.0], [-5.0, 5.0]])
	# define the total iterations
	n_iter = 10
	# define the maximum step size
	step_size = 0.15
	# number of parents selected each iteration
	mu = 5
	# the number of children generated by parents; Number of whole population
	lam = 10

	# perform the evolution strategy (mu + lambda) search
	best, score = es_plus(objective, bounds, n_iter, step_size, mu, lam)
	print('Done!')
	print('f(%s) = %f' % (best, score))
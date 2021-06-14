import random

# evolution strategy (mu + lambda) of the ackley objective function
from numpy import asarray, exp, sqrt, cos, e, pi, argsort, append, array
from numpy.random import randn, rand, seed, normal

# objective function
def objective(v):
	x, y = v
	return -20.0 * exp(-0.2 * sqrt(0.5 * (x**2 + y**2))) - exp(0.5 * (cos(2 * pi * x) + cos(2 * pi * y))) + e + 20


# check if a point is within the bounds of the search
# added also checking inside restrictions
def in_bounds(point, bounds, fo):
	# enumerate all dimensions of the point
	for d in range(len(bounds)):
		# check if out of bounds for this dimension
		if point[d] < bounds[d, 0] or point[d] > bounds[d, 1]:
			return False

	if not fo.satisfiesRestrictions(point):
		return False
	
	return True

# mutate point
def mutate(point, sigmaNormal, bounds, fo):
	mutant = list()
	mutant = point.copy()
	
	# parameters for normal noise
	muNormal, sigmaNormal = 0, sigmaNormal # mean and standard deviation
	
	# enumerate all dimensions of the point and mutate them
	for d in range(len(point)):
		mutant[d] = point[d].copy() + normal(muNormal, sigmaNormal, 1)[0]

	while mutant is None or not in_bounds(mutant, bounds, fo):
		# enumerate all dimensions of the point and mutate them
		for d in range(len(point)):
			mutant[d] = point[d].copy() + normal(muNormal, sigmaNormal, 1)[0]

	return mutant



# evolution strategy (mu + lambda) algorithm
def es_plus(objective, bounds, n_iter, step_size, mu, lam, fo):
	boe_point = None			# best of epoch point
	boe_value = float('inf')	# f(boe_point)
	

	# calculate the number of children per parent
	# n_children = int(lam / mu)

	### INITIAL POPULATION - of mu-parents size
	init_pop = list()
	for _ in range(mu):    # create first parents
		candidate = None
		while candidate is None or not in_bounds(candidate, bounds, fo):
			### bounds[:, 0] - select first colum
			candidate = bounds[:, 0] + rand(len(bounds)) * (bounds[:, 1] - bounds[:, 0])
		init_pop.append(candidate)

	parents = list()
	parents = init_pop

	# n_iter = 1

	### PERFORMING EVOLUTION
	for epoch in range(n_iter):
		print(f"Epoka {epoch+1}:")
		### GENERATE POPULATION
		offspring = list()
		# temporary population of cloned parents (as many as lam=children)
		offspring = [random.choice(parents) for _ in range(lam)]
		
		# #####################################################################
		# print(f"INITIAL OFFSPRING:")
		# for o in range(len(offspring)): print(f"osobnik {o}: {offspring[o]}")
		# #####################################################################

		### CROSSING (checked for bounds)
		percentageOfCrossing = 0.20
		indexesForCrossing = range(int(percentageOfCrossing*lam))		#0..4
		# uncrossedIndexes = range(int(percentageOfCrossing*lam), lam)#5..20
		# first 20% will be crossed
		for i in indexesForCrossing:
			# specimen that will be crossed
			specimen = None
			while specimen is None or not in_bounds(specimen, bounds, fo):
				specimen = offspring[i].copy()

				# 2nd parent selected for crossing
				specimens_spouse = None 
				while (specimens_spouse is None) or (specimens_spouse is specimen):
					specimens_spouse = random.choice(parents).copy()

				# crossing of specimen
				for gene_idx in range(len(specimen)):	# gene here is x1, x2, ...
					if(random.choice([True, False])):	# if True, then take gene from spouse
						specimen[gene_idx] = specimens_spouse[gene_idx].copy()

			offspring[i] = specimen.copy()

		# #####################################################################
		# print(f"AFTER CROSSING of {percentageOfCrossing*100}%:")
		# for o in range(len(offspring)): print(f"osobnik {o}: {offspring[o]}")
		# #####################################################################

		### MUTATION (checked for bounds)
		# now mutate whole offspring and check if in bounds
		offspring = [mutate(unit, step_size, bounds, fo) for unit in offspring]

		# #####################################################################
		# print("AFTER MUTATION offspring:")
		# for o in range(len(offspring)): print(f"osobnik {o}: {offspring[o]}")
		# #####################################################################

		# now make it MIU + LAMBDA - add parents to offspring
		for p in parents:
			offspring.append(p)

		### FITNESS EVALUATION
		# evaluate fitness for the population
		scores = [objective(c) for c in offspring]
		# rank scores in ascending order
		ranks = argsort(argsort(scores))

		# selected indexes - mu indices
		selected = [count for count,_ in enumerate(scores) if ranks[count]<mu]
		
		# teraz mam 5 rodziców do rozrodu
		# oni będą moją nową populacją
		
		parents = list()	# empty the parents list
		for i in selected:
			parents.append(offspring[i])	# add there best of offspring
			if scores[i] < boe_value:
				# boe_value = scores[i].copy()	# copy dla bezpieczenstwa
				boe_value = scores[i]
				boe_point = offspring[i].copy()
		
		# print best of epoch
		print('Najlepszy osobnik z epoki %d i wcześniejszych: f(%s) = %.7f' % (epoch+1, boe_point, boe_value))
		
		if(epoch+1==n_iter):
			finalPoints = parents.copy()

	return [boe_point, boe_value, finalPoints]


if __name__=='__main__':
	print("You invoked 'esPlus' by name!")

	# seed the pseudorandom number generator
	seed(1)
	# define range for input
	bounds = asarray([[-5.0, 5.0], [-5.0, 5.0]])
	# define the total iterations
	n_iter = 5000
	# define the maximum step size
	step_size = 0.15
	# number of parents selected each iteration
	mu = 50
	# the number of children generated by parents; Number of whole population
	lam = 100
	
	fo = None

	# perform the evolution strategy (mu + lambda) search
	best, score, _ = es_plus(objective, bounds, n_iter, step_size, mu, lam, fo)
	print('Done!')
	print('f(%s) = %f' % (best, score))
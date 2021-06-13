# evolution strategy (mu + lambda) of the ackley objective function
from numpy import asarray, exp, sqrt, cos, e, pi, argsort
from numpy.random import randn, rand, seed

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

# evolution strategy (mu + lambda) algorithm
def es_plus(objective, bounds, n_iter, step_size, mu, lam):
	best, best_eval = None, 1e+10
	# calculate the number of children per parent
	n_children = int(lam / mu)
	# initial population
	population = list()
	for _ in range(lam):    # for each citizen of current population
		candidate = None
		while candidate is None or not in_bounds(candidate, bounds):
			### bounds[:, 0] - select first colum
			candidate = bounds[:, 0] + rand(len(bounds)) * (bounds[:, 1] - bounds[:, 0])
		population.append(candidate)
	
	# perform the search
	for epoch in range(n_iter):
		# evaluate fitness for the population
		scores = [objective(c) for c in population]
		# rank scores in ascending order
		ranks = argsort(argsort(scores))
		# select the indexes for the top mu ranked solutions
		selected = [i for i,_ in enumerate(ranks) if ranks[i] < mu]
		# create children from parents
		children = list()
		for i in selected:
			# check if this parent is the best solution ever seen
			if scores[i] < best_eval:
				best, best_eval = population[i], scores[i]
				print('Epoka %d, Najlepszy osobnik: f(%s) = %.5f' % (epoch, best, best_eval))
			
			# keep the parent
			children.append(population[i])
			# create children for parent
			for _ in range(n_children):
				child = None
				while child is None or not in_bounds(child, bounds):
					child = population[i] + randn(len(bounds)) * step_size
				children.append(child)
		# replace population with children
		population = children
	return [best, best_eval]

# seed the pseudorandom number generator
seed(1)
# define range for input
bounds = asarray([[-5.0, 5.0], [-5.0, 5.0]])
# define the total iterations
n_iter = 5000
# define the maximum step size
step_size = 0.15
# number of parents selected
mu = 20
# the number of children generated by parents
lam = 100
# perform the evolution strategy (mu + lambda) search
best, score = es_plus(objective, bounds, n_iter, step_size, mu, lam)
print('Done!')
print('f(%s) = %f' % (best, score))
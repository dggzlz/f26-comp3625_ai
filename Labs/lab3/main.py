from search_problem import AirportProblem
from scipy.optimize import minimize
import pygad
import numpy as np
import matplotlib.pyplot as plt


# instantiate the search problem
problem = AirportProblem(n_cities=30, n_airports=3)

# example of how to get the sum of distances for a solution array
x1, y1, x2, y2, x3, y3 = np.random.rand(6)
dists = problem.sum_city_distances([x1, y1, x2, y2, x3, y3])



# TASK 1: solve for best airport locations using the gradient-descent (CG) approach
# YOUR CODE HERE
def func_wrap(parameters):
    return problem.sum_city_distances(parameters)
result = minimize(func_wrap, x0=np.random.rand(6), method="CG")

print(f"\n---------------------------------------- CG Results ----------------------------------------")
print(f"Best airport locations: {result.x}")
print(f"Sum of distances: {result.fun}")


# TASK 2: solve for best airport locations using a genetic algorithm approach
# YOUR CODE HERE
def fitness_func(ga_instance, solution, solution_idx):
    '''
    Implement your fitness function here.
    :param ga_instance: a reference to the GA object - this param is just to comply with PyGad's required function signature; you wont need it
    :param solution: the candidate solution to measure fitness for: an array of locations [x1, y1, x2, y2...]
    :param solution_idx: the index of this solution within the bigger population. You won't need to use this either.
    :return: the solution's fitness score (Remember that GAs *maximize* fitness, but we want to *minimize* distance)
    '''
    distance = problem.sum_city_distances(solution)

    # GA needs to maximize fitness, so flip the sign: a smaller distance gives a higher fitness
    fitness = -distance
    return fitness

def xover_func(parents, offspring_size, ga_instance):
    '''
    Implement your crossover function here.
    A good crossover should combine information from two (or more) parents in some way.
    :param parents: an array containing all the parents to use in this round of crossovers (the number of parents selected is controlled by the GA params)
    :param offspring_size: the number of new (crossed-over) solutions this function should produce
    :param ga_instance: a reference to the GA object - this param is just to comply with PyGad's required function signature; you wont need it
    :return: array of new solutions
    '''
    offspring = []
    for _ in range(offspring_size[0]):
        # randomly pick two different parents
        parent_index = np.random.choice(len(parents), 2, replace=False)
        parent1 = parents[parent_index[0]]
        parent2 = parents[parent_index[1]]

        # cross the two parents together
        alpha = np.random.random()
        child = alpha * parent1 + (1 - alpha) * parent2
        offspring.append(child)

    return np.array(offspring)

# instantiate the PyGad GA object
# for more info on GA params: https://pygad.readthedocs.io/en/latest/pygad.html#init
# for defining your own selection, mutation, or crossover operations:
#    https://pygad.readthedocs.io/en/latest/utils.html#user-defined-crossover-mutation-and-parent-selection-operators
ga_instance = pygad.GA(num_generations=200,
                       num_parents_mating=10,
                       fitness_func=fitness_func,
                       sol_per_pop=50,
                       num_genes=problem.n_airports * 2, # length of a solution vector (x-y coords for each airport)
                       init_range_low=0.0,    # cities are placed between 0 and 1
                       init_range_high=1.0,
                       parent_selection_type='tournament',
                       crossover_type=xover_func,
                       mutation_type='random',
                       mutation_by_replacement=True,
                       random_mutation_min_val=0.0,
                       random_mutation_max_val=1.0,
                       mutation_percent_genes=20)  # about 1 of the 6 genes gets mutated

# run and get results
ga_instance.run()
solution, solution_fitness, solution_idx = ga_instance.best_solution()
print(f"\n---------------------------------------- GA Results ----------------------------------------")
print(f"Best airport locations: {solution}")
print(f"Sum of distances: {-solution_fitness}")  # flip the sign back to get the distance


# TASK 3
# plot the cities and the solutions found
# YOUR CODE HERE



# TASK 4:
# What insights did you gain into genetic algorithms during this lab?



# GAs are considered to be particularly powerful (if slow) search algorithms.
# Did you find they significantly outperformed the CG method in this problem? Why do you think that is?
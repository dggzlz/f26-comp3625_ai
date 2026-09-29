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

def func_wrapper(parameters):
    return problem.sum_city_distances(parameters)

x0 = np.random.rand(6)
solution = minimize(fun=func_wrapper, x0=x0, method='CG')



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
    ## your code here

def xover_func(parents, offspring_size, ga_instance):
    '''
    Implement your crossover function here.
    A good crossover should combine information from two (or more) parents in some way.
    :param parents: an array containing all the parents to use in this round of crossovers (the number of parents selected is controlled by the GA params)
    :param offspring_size: the number of new (crossed-over) solutions this function should produce
    :param ga_instance: a reference to the GA object - this param is just to comply with PyGad's required function signature; you wont need it
    :return: array of new solutions
    '''
    ## your code here

# instantiate the PyGad GA object
# for more info on GA params: https://pygad.readthedocs.io/en/latest/pygad.html#init
# for defining your own selection, mutation, or crossover operations:
#    https://pygad.readthedocs.io/en/latest/utils.html#user-defined-crossover-mutation-and-parent-selection-operators
# ga_instance = pygad.GA(num_generations=,
#                        num_parents_mating=,
#                        fitness_func=,
#                        sol_per_pop=,
#                        num_genes=problem.n_airports * 2, # length of a solution vector (x-y coords for each airport)
#                        init_range_low=,
#                        init_range_high=,
#                        parent_selection_type=,
#                        crossover_type=,
#                        mutation_type='random',
#                        mutation_by_replacement=True,
#                        random_mutation_min_val=,
#                        random_mutation_max_val=,
#                        mutation_percent_genes=)

# # run and get results
# ga_instance.run()
# solution, solution_fitness, solution_idx = ga_instance.best_solution()
# print(solution_fitness)


# TASK 3
# plot the cities and the solutions found
# YOUR CODE HERE



# TASK 4: 
# What insights did you gain into genetic algorithms during this lab?



# GAs are considered to be particularly powerful (if slow) search algorithms.
# Did you find they significantly outperformed the CG method in this problem? Why do you think that is?
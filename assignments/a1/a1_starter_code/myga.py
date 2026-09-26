# population ← collection of population_size random solutions
# new_population ← empty collection
# repeat
# fitness_scores ← fitness_function(population)
# for i = 1 to population_size
#   parent1, parent2 ← selection_operator(population, fitness_scores, 2)
# 	child ← crossover_operator(parent1, parent2)
# 	if (probability p_mutate)then child ← mutation_operator(child)
# 	new_population.add(child)
# 	population  ← new_population
# until some individual is sufficiently fit

import numpy as np

class Individual:
    def __init__(self, fitness_score=0):
        fitness_score = fitness_score
        
    def get_fitness_score(self):
        return self.fitness_score

class MyGA:
    
    def __init__(self, num_gens, top_of_gen, pop_size, fitness_func, init_range_high,
                init_range_low, num_genes, parent_selection_type, crossover_type,
                mutation_type, mutation_percent_genes):
        
        num_gens = num_gens
        top_of_gen = top_of_gen
        population = [Individual()] * pop_size
        fitness_func = fitness_func
        high_range = init_range_high 
        low_range = init_range_low
        num_genes = num_genes
        parent_selection_type = parent_selection_type
        xover_type = crossover_tyoe
        mutation_type = mutation_type
        mutation_percent_genes = mutation_percent_genes
    
    def select(self, population):
        
        return parent1, parent2
    
    def xover(self):
        return

    def mutate(self):
        return
    
    def run(self):
        
        for i in range(self.pop_size):
            parent1, parent2 = selection_operator(population, fitness_scores, 2)
            child = xover(parent1, parent2)
            if np.random.random() < p_mutate:
                child = mutation_operator(child)
            new_pop.add(child)
        
        population = new_pop
        return
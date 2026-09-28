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
        
    def getFitnessScore(self):
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
    
    def select(self, pop, target, T):
        """
        https://numpy.org/devdocs/reference/random/generated/numpy.random.choice.html
        """
        
        f_max = max(self.getAllFitnessScores())
        
        expo = (self.getAllFitnessScores() - f_max) / T
        botlz_prob = np.exp(expo) / np.exp(expo).sum()
        
        # rand_prob = np.random.uniform(0, 1, size=1)
        # running_total = 0
        # selected = []
        # for i in range(len(pop)):
        #     running_total += self.boltz_prob(pop[i], T, f_max)
        #     if rand_prob < running_total:
        #         selected.append(pop[i])
        #         rand_prob = np.random.uniform(0, 1, size=1)
        #         if len(selected) >= target:
        #             break
        return np.random.choice(pop, size=target, p=boltz_prob)
    
    # def boltz_prob(self, individual, T, f_max):
        
    #     f_scaled = individual.getFitnessScore() - f_max
    #     sum_pop = (self.getAllFitnessScores() - f_max) / T
    #     botlz_prob = np.exp((f_scaled) / T) / np.exp(sum_pop).sum()
    #     return botlz_prob
    
    def xover(self):
        alpha = np.random.rand()
        offspring1 = alpha * parent1 + (1 - alpha) * parent2
        offspring2 = (1 - alpha) * parent1 + alpha * parent2
        
        if np.random.rand() > .50:
            return offspring1
        return offspring2
        
        

    def mutate(self):
        n = len(child)
        end = np.random.randint(1, n)
        start = np.random.randint(0, n - end)
        segment = child[start:start + end]
        segment = np.random.shuffle(segment)
        child[start:start + end] = segment
        return
    
    def getAllFitnessScore(self):
        fitness_scores = []
        for i in range(len(self.pop)):
            fitness_score.append(self.pop[i].getFitnessScore)
        return np.array(fitness_scores)
    
    def run(self):
        
        for i in range(self.pop_size):
            parent1, parent2 = selection_operator(population, fitness_scores, 2)
            child = xover(parent1, parent2)
            if np.random.random() < p_mutate:
                child = mutation_operator(child)
            new_pop.add(child)
        
        population = new_pop
        return
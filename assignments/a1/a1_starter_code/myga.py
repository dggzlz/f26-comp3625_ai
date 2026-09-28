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
    def __init__(self, genes, fitness_score=0):
        genes = genes
        fitness_score = fitness_score
        
    def getFitnessScore(self):
        return self.fitness_score
    
    def setFitnessScore(self, new_score):
        self.fitness_score = new_score

    def setGenes(self, genes):
        self.genes = genes
    
    def getGenes(self):
        return self.genes
    
    def __gt__(self, other):
        return self.fitness_score > other.fitness_score 

class MyGA:
    
    def __init__(self,  num_genrations, num_parents, pop_size, fitness_func,
                high_range, low_range, num_genes, mut_prob):
        
        num_generation = num_generations
        num_parents = num_parents
        pop = [Individual()] * pop_size
        fitness_func = fitness_func
        # high_range = high_range
        # low_range = low_range
        num_genes = num_genes
        mut_prob = mut_prob
        
        pop = [self.pop[i].addGenes(np.uniform(low_range, high_range, size=num_genes)) for i in range(pop_size)]
    
    def select(self, target, T):
        """
        https://numpy.org/devdocs/reference/random/generated/numpy.random.choice.html
        
        ##### Note to myself:
        
        I believe the logic is broken:
        choice takes a ndarray, but pop is a list of Individual
        
        I need to create an array of their scores, and then
        i can pass that, but if i pass that, choice will return 
        those scores, not the selected parents, right?
        
        returns the scores of the parents and then fidn those parents
        in pop.
        """
        
        # first calc their scores
        # f_scaled is a ndarray
        f_scaled = self.getAllScores()
        
        f_max = max(f_scaled)
        
        # numpy uses vectorization, i.e. this operation 
        # is applied across the ndarray
        expression = np.exp((f_scaled - f_max) / T)
        
        # creates and nd.array of prob
        # corresponding to each score
        botlz_prob = expression / expression.sum()
        
        parent1, parent2 = np.random.choice(f_scaled, size=target, p=boltz_prob)
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
        return parent1, parent2
    
    # def boltz_prob(self, individual, T, f_max):
        
    #     f_scaled = individual.getFitnessScore() - f_max
    #     sum_pop = (self.getAllFitnessScores() - f_max) / T
    #     botlz_prob = np.exp((f_scaled) / T) / np.exp(sum_pop).sum()
    #     return botlz_prob
    
    def xover(self, parent1, parent2):
        
        ##### Note: should i return 1 or both?
        alpha = np.random.rand()
        offspring1 = alpha * parent1 + (1 - alpha) * parent2
        offspring2 = (1 - alpha) * parent1 + alpha * parent2
        
        if np.random.rand() > .50:
            return offspring1
        return offspring2

    def mutate(self, child):
        """
        https://stackoverflow.com/questions/3793786/how-to-get-random-slice-of-python-list-of-constant-size-smallest-code
        """
        n = len(child)
        # randomly choose the end
        end = np.random.randint(1, n)
        # define start with high = n - end
        start = np.random.randint(0, n - end)
        # choose the segment
        segment = child[start:start + end]
        # scramble segment
        segment = np.random.shuffle(segment)
        # reassign segment to child
        
        ##### Notes: is this allow?
        child[start:start + end] = segment
        return child
    
    def getAllScores(self):
        fitness_scores = []
        for i in range(len(self.pop)):
            fitness_score.append(self.pop[i].getFitnessScore())
        return np.array(fitness_scores)
    
    def applyFitness(self):
        
        for indi in self.pop:
            score = fitness_func(indi)
            indi.setFitnessScore(score) 
    
    def run(self, cooling=0.95, T=0.10):
        new_gen = self.pop
        
        # first prev is the pop itself
        prev_gens = self.pop
        
        # as a starter
        best_descendent = self.pop[0]
    
        for _ in range(self.num_generations):
            T *= cooling
            new_gen.applyFitness()
            # Select candidates
            parent1, parent2 = self.select(target=2, T=T)
            # create offspring
            child = self.xover(parent1, parent2)
            # chance of mutation
            if np.random.rand() < self.mutation_prob:
                child = self.mutate(child)
            
            
            ##### Note: do i need to remove parents each gen?
            self.population.append(child)
            prev_gens.append(child)
            
            # choose the best 
            ##### note: is the child always best of the gen?
            if child > best_descendent:
                best_descendent = child
            
            # if many generations havent improved, stop
            ##### Note: This is a bug
            if prev_gens.mean() == prev_gen[0]:
                break
        
        return best_descendent.getGenes()
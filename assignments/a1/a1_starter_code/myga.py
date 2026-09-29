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
        self.genes = genes
        self.fitness_score = fitness_score
        
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
    
    def __init__(self,  num_generations, num_parents, pop_size, fitness_func,
                high_range, low_range, num_genes, mut_prob):
        
        self.num_generation = num_generations
        self.num_parents = num_parents
        self.pop_size = pop_size
        self.fitness_func = fitness_func
        self.num_genes = num_genes
        self.mut_prob = mut_prob
        
        
        self.pop = []
        for i in range(pop_size):
            genes = np.random.uniform(low_range, high_range, size=num_genes)
            self.pop.append(Individual(genes))
        
        self.best_genes = self.pop[0].getGenes()
    
    
    def select(self, target, T):
        """
        https://numpy.org/devdocs/reference/random/generated/numpy.random.choice.html

        """
        
        # first calc their scores
        # f_scaled is a ndarray
        f_scaled = self.getAllScores()
        
        f_max = max(f_scaled)
        
        # numpy uses vectorization, i.e. this operation 
        # is applied across the ndarray
        expression = np.exp((f_max - f_scaled) / T)
        
        # creates and nd.array of prob
        # corresponding to each score
        boltz_prob = expression / expression.sum()
        
        idxs = np.random.choice(np.arange(self.pop_size),replace=False, size=target, p=boltz_prob)
        parents = [self.pop[i] for i in idxs]

        return parents
    
    def xover(self, parents):
        
        parent1, parent2 = parents
        ##### Note: should i return 1 or both?
        ##### Note: I should try to generalize this? (maybe too much?)
        alpha = np.random.rand()

        p1_genes = parent1.getGenes()
        p2_genes = parent2.getGenes()

        offspring1 = Individual(genes=alpha * p1_genes + (1 - alpha) * p2_genes)
        offspring2 = Individual(genes=(1 - alpha) * p1_genes + alpha * p2_genes)
        
        return (offspring1, offspring2)

    def mutate(self, children):
        """
        https://stackoverflow.com/questions/3793786/how-to-get-random-slice-of-python-list-of-constant-size-smallest-code
        """
        mutated_children = []
        for child in children:
            genes = np.random.uniform(0, 1, size=self.num_genes)
            # genes = child.getGenes()
            # n = len(genes)
            # randomly choose the end
            # end = np.random.randint(1, n)
            # define start with high = n - end
            # start = np.random.randint(0, n - end)
            # choose the segment
            # segment = genes[start:start + end]
            # scramble segment
            # segment = np.random.uniform(0, 1, size=len(segment))
            # reassign segment to child
            
            ##### Notes: is this allowed?
            # genes[start:start + end] = segment
            
            child.setGenes(genes)
            
            mutated_children.append(child)
        return tuple(mutated_children)
    
    def getAllScores(self):
        fitness_scores = []
        for i in range(len(self.pop)):
            fitness_scores.append(self.pop[i].getFitnessScore())
        return np.array(fitness_scores)
    
    def applyFitness(self):
        
        for indi in self.pop:
            score = self.fitness_func(indi.getGenes())
            indi.setFitnessScore(score) 
            
    def findFittest(self):
        find_fittest = lambda x:x.getFitnessScore()
        return max(self.pop, key=find_fittest)
    
    def getFittest(self):
        return self.best_genes
    
    def run(self, cooling=0.95, T=0.10):
        new_gen = []
                
        # as a starter
        #best_descendent = self.pop[0]
    
        for _ in range(self.pop_size):
            T *= cooling
            self.applyFitness()
            curr_pop = self.pop
            # Select candidates
            parents = self.select(target=self.num_parents, T=T)
            # create offspring
            children = self.xover(parents)
            # chance of mutation
            if np.random.rand() < self.mut_prob:
                children = self.mutate(children)
            
            ##### Note: do i need to remove parents each gen?
            # remove two individuals for the new gen and add children, mantain same size
            # [b for a, b in zip(x, y) if a]
            mask = np.isin(self.pop, parents, invert=True)
            self.pop = [indi for masking, indi in zip(mask, self.pop) if masking]
            
            for child in children:
                self.pop.append(child)
            
            new_gen = self.pop        
        self.best_genes = self.findFittest()
        return new_gen
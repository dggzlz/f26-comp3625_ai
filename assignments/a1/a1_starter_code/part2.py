from translator import UniversalTranslator
import numpy as np
import string

def fitness_function(settings):
    """
    Name: fitness_function
    Parameters: settings - a size n array of values between 0 and 1
    Purpose: Evaluates the fitness of the given settings by passing them through the UniversalTranslator and calculating a fitness score.
             The fitness score is based on the number of words decoded from the translated message.
    Returns: fitness_score - a float representing the fitness score of the given settings.
    """
    translated_string = translator.translate(settings)
    segments = translated_string.split()

    reward = 0
    for code in segments:
        code_segments = code.strip(string.punctuation)
    
        if code_segments.isalpha():
            reward += 1

    fitness_score = reward / len(segments) if len(segments) > 0 else 0.0  # avoids division by zero
    return fitness_score

def create_init_pop(pop_size, n_dim):
    """
    Name: create_init_pop
    Parameters: pop_size - the number of settings to create in the initial population
                n_dim - the number of dimensions for each setting
    Purpose: Creates an initial population of random settings, each with n_dim knobs (values between 0 and 1).
    Returns: population - a numpy array of shape (pop_size, n_dim) containing the initial population of settings.
    """
    population = []
    for _ in range(pop_size):
        individual = np.random.uniform(0, 1, n_dim)  # generate n_dim random values between 0 and 1
        population.append(individual)
    return np.array(population)

def selection(population, fitness_scores, tournament_size=3):
    """
    Name: selection
    Parameters: population - a numpy array of shape (pop_size, n_dim) containing the population of settings
                fitness_scores - a numpy array of shape (pop_size,) containing the fitness scores for each individual
                tournament_size - the number of individuals to include in each tournament
    Purpose: Selects individuals from the population based on their fitness scores using tournament selection.
    Returns: selected_individuals - a numpy array of shape (pop_size, n_dim) containing the selected individuals.
    """
    selected = []
    for _ in range(len(population)):
        tournament_index = np.random.choice(len(population), tournament_size, replace=False)  # randomly select individuals for the tournament
        winner = tournament_index[np.argmax(fitness_scores[tournament_index])]  # select the individual with the highest fitness score)
        selected.append(population[winner])
    return np.array(selected)

def crossover(parent1, parent2):
    """
    Name: crossover
    Parameters: parent1 - a numpy array of shape (n_dim,) representing the first parent
                parent2 - a numpy array of shape (n_dim,) representing the second parent
    Purpose: Performs blend crossover between two parents to create two children. The children inherit settings from both parents.
             A random alpha value between 0 and 1 is chosen, and each child is the weighted average of the parents: child1 takes alpha of
             parent1 and (1 - alpha) of parent2, and child2 takes the reverse. Since each knob of a child lies between the parents' values
             for that knob, the children always stay within the 0 - 1 bounds.
    Returns: (child1, child2) - a tuple of two numpy arrays of shape (n_dim,) representing the children created from the parents.
    """
    alpha = np.random.random()  # randomly select a value between 0 and 1 for interpolation
    child1 = alpha * parent1 + (1 - alpha) * parent2  # create child by interpolating between parents
    child2 = alpha * parent2 + (1 - alpha) * parent1  # mirror of child1, with the parent weights swapped
    return child1, child2

def mutation(individual, mutation_rate=0.1):
    """
    Name: mutation
    Parameters: individual - a numpy array of shape (n_dim,) representing the settings to mutate
                mutation_rate - the probability that each knob is mutated
    Purpose: Randomly nudges some of the individual's knobs to keep diversity in the population. Each knob independently
             has a mutation_rate chance of being changed by a random amount between -0.1 and 0.1, then all knobs are
             clipped to stay within the bounds of 0 - 1. The original individual is not modified.
    Returns: mutated - a numpy array of shape (n_dim,) representing the mutated settings.
    """
    mutated = np.copy(individual)  # copy so the original individual is not modified
    for i in range(len(mutated)):
        if np.random.random() < mutation_rate:  # mutate this knob with probability mutation_rate
            mutated[i] += np.random.uniform(-0.1, 0.1)  # small adjustment so it doesn't overshoot the 0 - 1 bound
    return np.clip(mutated, 0.0, 1.0)  # ensures that the bounds for each setting stay within 0 - 1

def ga(n_dim, pop_size=200, generations=30, crossover_rate=0.8, mutation_rate=0.1, tournament_size=3, elite_size=2):
    population = create_init_pop(pop_size, n_dim)
    best_rate = 0
    best_settings = population[0]

    for gen in range(generations):
        # eval each individual once per generation and store fitness score in numpy array
        fitness_scores = []
        for individual in population:
            score = fitness_function(individual)
            fitness_scores.append(score)
        fitness_scores = np.array(fitness_scores)

        gen_best = np.argmax(fitness_scores)
        gen_best_rate = fitness_scores[gen_best]

        if gen_best_rate > best_rate:
            best_rate = gen_best_rate
            best_settings = population[gen_best]

        print(f"Generation {gen + 1}: Best fitness = {gen_best_rate * 100}, Overall best fitness = {best_rate * 100}")

        next_population = []
        sorted_index = np.argsort(fitness_scores)  # sort indices of fitness scores from lowest to highest
        for i in range(elite_size):
            elite = sorted_index[pop_size - 1 - i]  # get from end of list, where highest fitness is
            next_population.append(population[elite])  # add elite to next generation

        parents = selection(population, fitness_scores, tournament_size)

        j = 0
        while len(next_population) < pop_size:
            if j + 1 >= pop_size:
                j = 0

            parent1 = parents[j]
            parent2 = parents[j + 1]
            j = j + 2

            if np.random.random() < crossover_rate:
                children = crossover(parent1, parent2)
                child1 = children[0]
                child2 = children[1]
            else:
                child1 = np.copy(parent1)
                child2 = np.copy(parent2)

            child1 = mutation(child1, mutation_rate)
            next_population.append(child1)

            if len(next_population) < pop_size:
                child2 = mutation(child2, mutation_rate)
                next_population.append(child2)

        population = np.array(next_population)

    return (best_settings, best_rate)



# create the UniversalTranslator object, with 10 knobs
translator = UniversalTranslator(n_dim=10)
# population = create_init_pop(20, n_dim=translator.n_dim)
# fitness_scores = np.array([fitness_function(ind) for ind in population])
# selected = selection(population, fitness_scores)

# print("Fitness:", fitness_scores)
# print("Mean fitness before:", fitness_scores.mean())
# print("Mean fitness of selected:", np.array([fitness_function(s) for s in selected]).mean())

best_settings, best_rate = ga(n_dim=translator.n_dim)
print(f"Best Rate: {best_rate * 100}")
print(f"Best Settings: {best_settings}")
print(translator.translate(best_settings))


# demo of how to use the UniversalTranslator object. You can delete these lines
#random_settings = np.random.random(size=10)
#translated_string = translator.translate(random_settings)
#print(translated_string)

# print total number of settings evaluated
print(f'# settings tried: {translator.n_settings_tried()}')
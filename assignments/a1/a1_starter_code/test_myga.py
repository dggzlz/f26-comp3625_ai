from myga import Individual, MyGA
from translator import UniversalTranslator
import numpy as np
import time

t0 = time.time()

# create the UniversalTranslator object, with 10 knobs
translator = UniversalTranslator(n_dim=10)

def fitness_func(settings): 
  """ 
Name: func_wrapper 
Parameters: Size 2 array with numbers between 0 - 1
Purpose: Takes in an array of two values between 0 and 1 and passes it through the translator to convert 
         some sequences of numbers to words/letters.
         Parses each white space of the translated message, giving as a mixed list of numbers and words. 
         Iterate through the list and detect which indices are solely letters, therefore a word has been decoded. 
         +1 reward for each word detected out of the entire list, then divide that number by the total to achieve 
         a decode_rate given the setting applied.
  """
  translated_string = translator.translate(settings)
  segments = translated_string.split()

  reward = 0
  for code in segments: 
    if code.isalpha(): 
      reward += 1   

  decode_rate = reward / len(segments) 

  return decode_rate

ga = MyGA(
    num_generations=25, 
    num_parents=2, 
    pop_size=100, 
    fitness_func=fitness_func,
    high_range=1, 
    low_range=0, 
    num_genes=10, 
    mut_prob=0.10)

convergence = 0.0001
prev_gens = [ga.getAllScores().sum()]
gen_std = np.std(prev_gens)
new_pop = []

n = 0
num_generations = 25
while n < num_generations and (len(prev_gens) < 10 or gen_std > convergence):

    new_pop = ga.run()
    
    if len(prev_gens) >= 10:
        prev_gens.pop(0)
    
    prev_gens.append(ga.getAllScores().sum())
    gen_std = np.std(prev_gens)
    n += 1 


best_candidate = ga.getFittest()
best_rate = best_candidate.getFitnessScore()
best_genes = best_candidate.getGenes()
            
# settings, rate = sim_annealing(func_wrapper, settings=rng.random(size=2), n=100, T=1000)
print(translator.translate(best_genes))

t1 = time.time()
total = t1-t0
print("\nTotal time ran:", total)
print("Best Candidate")
print("Rate:", best_rate)
print("Genes:", best_genes)
# print(abs(rate) * 100)
    


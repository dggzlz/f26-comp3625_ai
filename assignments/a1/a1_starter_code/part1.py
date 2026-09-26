from translator import UniversalTranslator
import numpy as np

# create the UniversalTranslator object, with 2 knobs
translator = UniversalTranslator(n_dim=2)

#Simulated Annealing 
# Random Array of Two values between 0 and 1
rng = np.random.default_rng()

def func_wrapper(settings): 
  """ 
Name: func_wrapper 
Parameters: Size 2 array with numbers between 0 - 1
Purpose: Takes in an array of two values between 0 and 1 and passes it through the translator to convert 
         some sequences of numbers to words/letters.
         Parses each white space of the translated message, giving as a mixed list of numbers and words. 
         Iterate through the list and detect which indices are solely letters, therefore a word has been decoded. 
         +1 reward for each word detected out of the entire list, then divide that number by the total to achieve 
         a decode_rate given the setting applied.
Returns: decode_rate - a float between 0 and 1, representing the percentage of words decoded from the translated message.
  """
  translated_string = translator.translate(settings)
  segments = translated_string.split()

  reward = 0
  for code in segments: 
    if code.isalpha(): 
      reward += 1   

  decode_rate = reward / len(segments) 

  return decode_rate

def sim_annealing(f, settings, n=100, T=1000):
  """
  Name: sim_annealing
  Parameters: f - function wrapper, settings - array of two values between 0 and 1, n - number of iterations, T - initial temperature
  Purpose: Implements the simulated annealing algorithm to optimize the settings for the translator. With each iteration,
           temperature is decreased by 1%. A neighbour (next) is created by independently rolling a random number to add or subtract for each knob,
           then also clipped to ensure it stays within the bounds of 0 - 1. The neighbour is then evaluated and compared to the current settings,
           if it is better than the current settings, it is saved as the best settings. Delta_e is the difference in decode rate between the neighbour
           and the current settings. If the niehgbour is better, it is always accepted, if it is worse, it is accepted with a probability of e^(delta_e/T),
           so slightly worse moves are more likely to be accepted than worse moves. This allows the search to escape local maxima early and makes bad moves
           less likely as the temperature decreases.
  Returns: (best_settings, best_rate) - a tuple containing the best settings found over the whole search and its decode rate.
  """
  current = settings 
  multiplier = 0.99
  best_rate = 0
  best_settings = [0] * len(settings)

  for _ in range(n): 
    T *= multiplier 

    #Indpendently roll a random number to add or subtract for each knob
    choice = np.random.uniform(-0.1, 0.1, size=len(settings)) # small adjustments so that they don't overshoot the 0 - 1 bound
    next = current + choice
    #Ensures that the bounds for each setting stay within 0 - 1
    next = np.clip(next, 0.0, 1.0)

    f_next = f(next)

    if f_next > best_rate: 
      best_rate = f_next
      best_settings = next
  
    f_curr = f(current) 
    #Multiplying delta_e by 100 since without it would be a very small number, causing calculations to always accept bad settings
    delta_e = (f_next - f_curr) * 100

    if delta_e > 0: 
      current = next 
    elif np.random.random() < np.exp(((delta_e)/T)): 
      current = next  

  return(best_settings, best_rate) 

# settings, rate = sim_annealing(func_wrapper, settings=rng.random(size=2), n=100, T=1000)
# print(translator.translate(settings))
# print(settings)
# print(abs(rate) * 100)

best_rate = 0
best_settings = None
for i in range(20): 
  settings, rate = sim_annealing(func_wrapper, settings=rng.random(size=2), n=500, T=1000)
  print(f"Attempt {i + 1} Settings: {settings} Decode rate: {abs(rate) * 100}")
  if rate > best_rate: 
    best_rate = rate 
    best_settings = settings 

print(f"Best Rate: {best_rate * 100}")
print(f"Best Settings: {best_settings}")

from translator import UniversalTranslator
import numpy as np

# create the UniversalTranslator object, with 2 knobs
translator = UniversalTranslator(n_dim=2)

# demo of how to use the UniversalTranslator object. You can delete these lines
# sample_settings = [0.2, 0.5]
# translated_string = translator.translate(sample_settings)
# print(translated_string) 

# print total number of settings evaluated
#print(f'# settings tried: {translator.n_settings_tried()}')

#Simulated Annealing 

# Random Array of Two values between 0 and 1
rng = np.random.default_rng()
settings = rng.random(size=2)
#settings = [0.2, 0.7]

def func_wrapper(settings): 
  translated_string = translator.translate(settings)
  segments = translated_string.split()

  reward = 0
  for code in segments: 
    if code.isalpha(): 
      reward += 1   

  decode_rate = reward / len(segments) 

  return -decode_rate

def sim_annealing(f, settings, n=100, T=1000): 
  current = settings 
  multiplier = 0.95
  best_rate = 0
  best_settings = [0,0]

  for _ in range(n): 
    T *= multiplier 

    #flip coin, when adding to choice, must be within 0 - 1 bounds
    choice = np.random.rand(len(settings)) * 0.09 # makes the numbers smaller so that they don't overshoot the 0 - 1 bound
    if np.random.random() > .50:
      next = current - choice
    else: 
      next = current + choice  
    #Ensures that the bounds for each setting stay within 0 - 1
    next = np.clip(next, 0.0, 1.0)

    f_next = f(next)

    if f_next < best_rate: 
      best_rate = f_next
      best_settings = next
  
    f_curr = f(current) 
    #Multiplying delta_e by 100 since without it would be a very small number, causing calculations to always accept bad settings
    delta_e = (f_next - f_curr) * 100

    if delta_e < 0: 
      current = next 
      best_rate = f_next 
    elif np.random.random() < np.exp(((-delta_e)/T)): 
      current = next  

  return(best_settings, best_rate) 

settings, rate = sim_annealing(func_wrapper, settings=rng.random(size=2), T=1000)
print(translator.translate(settings))
print(settings)
print(abs(rate) * 100)

# print(f"{segments}\n")

# print(f"Settings: {settings}")

# #Item Count
# print(f"Amount of Segmented Words (Constant): {len(segments)}")

# #Character Count
# print(f"Amount of characters {len(translated_string)}") 

# print(f"Amount of words decoded from Segment {reward}")

# print(f"Percentage of Words Decoded: {(reward / len(segments)) * 100}")
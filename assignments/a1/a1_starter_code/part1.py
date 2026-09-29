from translator import UniversalTranslator
import numpy as np
import matplotlib.pyplot as plt
import string

# create the UniversalTranslator object, with 2 knobs
translator = UniversalTranslator(n_dim=2)

# Simulated Annealing 
# Random Array of Two values between 0 and 1
rng = np.random.default_rng()

# the logs for everything tried
all_settings = []
all_rates = []

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
  """
  translated_string = translator.translate(settings)
  segments = translated_string.split()

  reward = 0
  for code in segments: 
    # Removes punctuation from segmented codes
    code_segment = code.strip(string.punctuation)
    
    # Check if code is solely characters
    if code_segment.isalpha(): 
      reward += 1 

  decode_rate = reward / len(segments) 

  # log the attempt for the plot
  all_settings.append(np.array(settings, copy=True))
  all_rates.append(decode_rate)

  return decode_rate

def sim_annealing(f, settings, n=100, T=1000): 
  current = settings 
  multiplier = 0.99
  best_rate = 0
  best_settings = [0] * len(settings)

  f_curr = f(current) 

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
  
    #Multiplying delta_e by 100 since without it would be a very small number, causing calculations to always accept bad settings
    delta_e = (f_next - f_curr) * 100

    if delta_e > 0: 
      current = next
      f_curr = f_next 
    elif np.random.random() < np.exp(((delta_e)/T)): 
      current = next 
      f_curr = f_next
     
  return(best_settings, best_rate) 

# settings, rate = sim_annealing(func_wrapper, settings=rng.random(size=2), n=100, T=1000)
# print(translator.translate(settings))
# print(settings)
# print(abs(rate) * 100)

best_rate = 0
best_settings = None
for i in range(1): 
  settings, rate = sim_annealing(func_wrapper, settings=rng.random(size=2), n=1000, T=1000)
  print(f"Attempt {i + 1} Settings: {settings} Decode rate: {abs(rate) * 100}")
  if rate > best_rate: 
    best_rate = rate 
    best_settings = settings 

print(f"Best Rate: {best_rate * 100}")
print(f"Best Settings: {best_settings}")

print(f"Total settings tried: {translator.n_settings_tried()}")
plt_settings = np.array(all_settings) 
decode_rate = np.array(all_rates)   

# generate a scatter plot
plt.scatter(x=plt_settings[:, 0],
            y=plt_settings[:, 1],
            c=decode_rate,
            vmin=0, vmax=1)

# add colorbar and gridlines
cbar = plt.colorbar(label="decode rate")
plt.grid()

# add labels
plt.xlabel('knob 0 setting')
plt.ylabel('knob 1 setting')
plt.title('decode rates for settings tried')

# display
plt.show()
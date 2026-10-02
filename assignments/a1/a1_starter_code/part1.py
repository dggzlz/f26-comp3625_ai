"""
===============================================================================
Course:         COMP 3625: Artificial Intelligence
Assignment:     Assignment 1
File:           part1.py

Author(s):      Edwin Pang
                John Galang
                Tarun Jaswal
                Diego Gonzalez R.
                
Date:           2026-10-01

Dependencies:   numpy, matplotlib, UniversalTranslator, string
===============================================================================
"""
from translator import UniversalTranslator
import numpy as np
import matplotlib.pyplot as plt
import string

# create the UniversalTranslator object, with 2 knobs
translator = UniversalTranslator(n_dim=2)
rng = np.random.default_rng()

# the logs for everything tried
all_settings = []
all_rates = []

def func_wrapper(settings): 
  """ 
  Name: func_wrapper 
  Parameters: 
        Size 2 array with numbers between 0 - 1

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
    # Removes punctuation from segmented codes
    code_segment = code.strip(string.punctuation)
    
    # Check if code are solely letters
    if code_segment.isalpha(): 
      reward += 1 

  decode_rate = reward / len(segments) 

  # log the attempt for the plot
  all_settings.append(np.array(settings, copy=True))
  all_rates.append(decode_rate)

  return decode_rate

def sim_annealing(f, settings, n=100, T=1000):
  """
  Name: sim_annealing
  Parameters: 
            f - function wrapper, 
            settings - array of two values between 0 and 1, 
            n - number of iterations, 
            T - initial temperature
            
  Purpose: Implements the simulated annealing algorithm to optimize the settings for the translator. With each iteration,
           temperature is decreased by 1%. A neighbour (next) is created by independently rolling a random number to add or subtract for each knob,
           then also clipped to ensure it stays within the bounds of 0 - 1. The neighbour is then evaluated and compared to the current settings,
           if it is better than the current settings, it is saved as the best settings. Delta_e is the difference in decode rate between the neighbour
           and the current settings. If the niehgbour is better, it is always accepted, if it is worse, it is accepted with a probability of e^(delta_e/T),
           so slightly worse moves are more likely to be accepted than worse moves. This allows the search to escape local maxima early and makes bad moves
           less likely as the temperature decreases.
           
  Returns: (best_settings, best_rate) - a tuple containing the best settings found over the whole search and its decode rate.
  """
  settings_size = len(settings)
  current = settings 
  multiplier = 0.99
  best_rate = 0
  best_settings = [0] * settings_size

  # calculate f(current) before the loop, not need to re calculate within the loop
  f_curr = f(current) 

  for _ in range(n): 
    # descrease by multiplier
    T *= multiplier 

    #Indpendently roll a random number to add or subtract for each knob
    choice = np.random.uniform(-0.1, 0.1, size=settings_size) # small adjustments so that they don't overshoot the 0 - 1 bound
    successor = current + choice
    #Ensures that the bounds for each setting stay within 0 - 1
    successor = np.clip(successor, 0.0, 1.0)

    
    f_next = f(successor)

    if f_next > best_rate: 
      best_rate = f_next
      best_settings = successor
  
    #Multiplying delta_e by 100 since without it would be a very small number, causing calculations to always accept bad settings
    delta_e = (f_next - f_curr) * 100

    if delta_e > 0: 
      current = successor
      f_curr = f_next 
    elif np.random.random() < np.exp(((delta_e)/T)): 
      current = successor 
      f_curr = f_next
     
  return(best_settings, best_rate) 

def run_search(restarts=1, knobs=2):
    """
    Name: run_search
    Description: 
      Execute a multi-restart simulated annealing search to optimize settings.

      Runs multiple independent runs of simulated annealing initialized with random
      starting configurations, logs progress per attempt, and prints the overall
      best-performing parameters and decode rate.

    Parameters
      restarts : int, default=1
        The number of independent simulated annealing search runs to execute.
      
      knobs : int, default=2
        The number of parameter settings (dimensions) to optimize.

      Returns:
        None
        Results are printed directly to standard output.

    Notes:
    This function relies on several external/global variables:

    - rng: A NumPy random number generator instance.
    - func_wrapper: The objective function passed to the optimizer.
    - sim_annealing: The optimization routine returning (settings, rate).
    - translator: An object tracking evaluation metrics (n_settings_tried).
    """
    best_rate = 0
    best_settings = None
    
    # main loop to run the simulated annealing
    for i in range(restarts): 
        start_settings = rng.random(size=knobs) # random settings
        settings, rate = sim_annealing(func_wrapper, settings=start_settings, n=1000, T=1000)
        print(f"Attempt {i + 1} Settings: {settings} Decode rate: {rate * 100:.2f}%")
        
        # keep track of the best solution
        if rate > best_rate: 
            best_rate = rate 
            best_settings = settings 

    print(f"\n--- Final Results ---")
    print(f"Best Rate: {best_rate * 100:.2f}%")
    print(f"Best Settings: {best_settings}")
    print(f"Total settings tried: {translator.n_settings_tried()}")

def plot_results():
    """
    Plot a 2D scatter plot of evaluated settings and their decode rates.

    Visualizes the search history across the first two parameter dimensions
    (`knob 0` and `knob 1`), color-coding each point according to its decode
    success rate on a fixed scale from 0 to 1.

    Parameters: None

    Returns: None
    Displays the generated Matplotlib figure window.

    Notes:

    This function expects the following variables to exist in the global or
    outer scope:

    - all_settings: Sequence of coordinate-like settings, where each item
    has at least 2 dimensions indexed as [:, 0] and [:, 1].

    - all_rates: Sequence of numeric decode rates corresponding to all_settings.

    - np: The NumPy module.

    - plt: The Matplotlib pyplot module.
    """
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
    
if __name__ == "__main__":
  run_search(restarts=1, knobs=2)
  plot_results()
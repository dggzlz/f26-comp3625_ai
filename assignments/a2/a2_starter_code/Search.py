import numpy as np
import pandas as pd

class SimAnnealing:
    """
    Uses Simulated Annealing to search for the optimal hyperparameters (epochs, step_size) 
    by maximizing the profit returned by the fitness function.
    """
    def __init__(self, fitness, T=20000, cooling_rate=0.95, step_size=(50, 0.05), n=100):
        """
        Initializes the search algorithm.

        Parameters:
        fitness : callable - A function that evaluates hyperparameters and returns the total profit.
        T : float - The starting temperature, controlling the balance between exploration and exploitation.
        cooling_rate : float - The multiplier that decreases T, transitioning the search from exploring to exploiting.
        step_size : tuple - The standard deviation for the random steps taken for each hyperparameter.
        n : int - The number of iterations to run the search.
        """
        
        self.func = fitness              # Address to the fitness function
        self.T = T                       
        self.cooling_rate = cooling_rate
        self.step_size = step_size
        self.iterations = n
        
        # initialized to 0 first
        self.best_candidates = 0         # optimal hyperparameters
        self.best_profit = 0             # what the optimal set returns as optimal profit 
    
    def sim_annealing(self):
        """
        Executes the main search loop to find optimal hyperparameters.
        Generates neighboring candidate solutions and accepts them based on 
        profit improvement or a temperature-dependent probability to escape local optima.
        """
        
        curr_candidates = self.best_candidates
        f_curr = self.best_profit

        for _ in range(self.iterations): 
        
            # Generate a neighboring solution by applying random Gaussian noise to each hyperparameter
            candidate_1 = np.random.normal(loc=0.0, scale=self.step_size[0])
            candidate_2 = np.random.normal(loc=0.0, scale=self.step_size[1])
            candidates = np.array([candidate_1, candidate_2])
            successor = curr_candidates + candidates
            
            # Enforce hard boundaries (minimum 1 epoch, minimum 0.001 learning rate)
            mins = np.array([1, 0.001])
            successor = np.clip(successor, mins, None)

            f_next = self.func(successor)
            
            # Update the global best if the new profit is the highest seen so far
            if f_next > self.best_profit: 
                self.best_profit = f_next
                self.best_candidates = successor

            # Calculate the difference in profit between the new state and the current state
            delta_e = f_next - f_curr

            if delta_e > 0: 
                # Always accept the move if it results in a higher profit
                curr_candidates = successor
                f_curr = f_next 
            elif np.random.random() < np.exp(((delta_e)/self.T)): 
                # Occasionally accept a worse profit to escape local optima.
                # As Temperature (T) decreases, the chance of accepting a worse move approaches zero.
                curr_candidates = successor 
                f_curr = f_next
                
            # Cool down the temperature to shift the algorithm from exploring to exploiting
            self.T *= self.cooling_rate 
    
    def get_hyperparams(self):
        """Getter method to return final hyperparameters"""
        epochs, alpha = self.best_candidates
        return int(epochs), float(round(alpha, 2))
    
    def run(self, baseline):
        """
        Initializes the search with a baseline set of hyperparameters and 
        starts the simulated annealing optimization process.

        Parameters:
        baseline : np.array - The starting values for the hyperparameters (e.g., [epochs, alpha]).
        """
        # Set the initial hyperparameters as the global best starting point
        self.best_candidates = baseline
        
        # Evaluate the baseline to establish the starting profit
        self.best_profit = self.func(baseline)
        
        # Trigger the main simulated annealing loop
        self.sim_annealing()

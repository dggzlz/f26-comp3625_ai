import numpy as np
import pandas as pd

class SimAnnealing:
    def __init__(self, fitness, T=1000, cooling_rate=0.95, step_size=(50, 0.05), n=100):
        self.func = fitness
        self.T = T
        self.cooling_rate = cooling_rate
        self.step_size = step_size
        self.best_candidates = 0
        self.best_profit = 0
        self.curr_candidates = 0
        self.curr_profit = 0
        self.iterations = n
    
    def sim_annealing(self):
        f_curr = self.curr_profit

        for _ in range(self.iterations): 
        
            #Indpendently roll a random number to add or subtract for each knob
            candidate_1 = np.random.normal(loc=0.0, scale=self.step_size[0])
            candidate_2 = np.random.normal(loc=0.0, scale=self.step_size[1])
            candidates = np.array([candidate_1, candidate_2])
            successor = self.curr_candidates + candidates
            mins = np.array([1, 0.001])
            successor = np.clip(successor, mins, None)

            f_next = self.func(successor)
            
            if f_next > self.best_profit: 
                self.best_profit = f_next
                self.best_candidates = successor
        
            #Multiplying delta_e by 100 since without it would be a very small number, causing calculations to always accept bad settings
            delta_e = (f_next - f_curr) * 100

            if delta_e > 0: 
                self.curr_candidates = successor
                f_curr = f_next 
            elif np.random.random() < np.exp(((delta_e)/self.T)): 
                self.curr_candidates = successor 
                f_curr = f_next
                
            # descrease by multiplier
            self.T *= self.cooling_rate 
            
    def run(self, baseline):
        self.best_candidates = baseline
        self.best_profit = self.func(baseline)
        self.curr_candidates = self.best_candidates
        self.curr_profit = self.best_profit
        self.sim_annealing()
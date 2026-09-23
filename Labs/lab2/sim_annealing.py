import numpy as np

def mysim_annealing(f, params, n, T=1000):
    current = params
    multiplier = 0.95

    for _ in range(n): #T decreasing to 0 over n iterations:
        T *= multiplier
        
        # flip a coin
        choice = np.random.rand(len(params))
        if np.random.random() > .50:
            successor = current - choice
        else:
            successor = current + choice
    
        delta_e = f(successor) - f(current)
        
        if delta_e < 0:
            current = successor
        else:
            exp = np.exp(((-delta_e)/T))    
            if np.random.random() < exp:
                current = successor

    return current
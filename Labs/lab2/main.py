from gymnasium.envs.classic_control.cartpole import CartPoleEnv
from agent import CartPoleAgent
import numpy as np
np.set_printoptions(precision=2)
from scipy.optimize import minimize
import matplotlib.pyplot as plt
from pathlib import Path

# Directory where main.py is located
script_dir = Path(__file__).parent
file_path = script_dir / "performance_plot.png"

def test_agent(parameters, render=False):
    """
    This function tests a CartPoleAgent with the given weights.
    The agent is tested over 10 episodes, and the total number of steps achieved is returned.
    """

    max_steps_per_episode = 500
    cumulative_reward = 0

    for rep in range(10):
        agent = CartPoleAgent(parameters)
        env = CartPoleEnv(render_mode="human" if render else None)
        

        observation, info = env.reset()

        for step in range(max_steps_per_episode):
            action = agent.get_action(observation)
            observation, reward, terminated, truncated, info = env.step(action)
            cumulative_reward += reward
            if terminated or truncated:
                break

    print(f'tested parameters: {parameters}, cumulative reward: {cumulative_reward}')
    return cumulative_reward

# watch how an agent with randomly-initialized parameters does:
# test_agent(parameters=np.random.uniform(-1, 1, size=5), render=True)


# Write a search to find the best parameters for the CartPoleAgent.
# YOUR CODE HERE
def mysim_annealing(f, params, iters=500, T=1000):
    """
    Search Algorithm using simulated annealing
    
    Args:  
        f (function): the loss function that returns the score for the search
        params (np.array): the initial parameters to pass to the function
        iters (int): number of iterations for the search
        T (int): a integer that decreases to 0 over n iterations
    
    Returns:
        a tuple with the best parameters, the cumulative reward, 
        and a list of the history of the rewards
    """
    current = params
    multiplier = 0.95
    best_score = 0
    best_history = []
    f_curr = f(current)
    for _ in range(iters):
        # T decreases by the multiplier
        T *= multiplier
        
        # flip a coin
        choice = np.random.rand(len(params))
        if np.random.random() > .50:
            successor = current - choice
        else:
            successor = current + choice

        # using loss function (f(x)) to calculate delta_e
        f_succ = f(successor)
        delta_e = f_succ - f_curr
        
        if delta_e < 0:
            current = successor
            best_score = f_succ    
        elif np.random.random() < np.exp(((-delta_e)/T)): # accept successor with a chance of e^(-ΔE/T)
            current = successor
            best_score = f_succ
        
        f_curr = f_succ
        best_history.append(abs(best_score))

    return (current, best_score, best_history)

def func_wrapper(parameters):
    return -test_agent(parameters)

result, score, history = mysim_annealing(func_wrapper, params=np.random.uniform(-1, 1, size=5))

print(f"Results: {result}; Score: {abs(score)}")
plt.plot(history)
plt.title("Simulated Annealing Performance")
plt.xlabel("Number of Iterations")
plt.ylabel("Cumulative Reward")
plt.savefig(file_path)

test_agent(result, render=True) 

# OLD via Minimize Function
# ================================
#result = minimize(func_wrapper, x0=np.random.uniform(-1, 1, size=5), method="CG")
# best = -result.fun
# for _ in range(100):
#     r = minimize(func_wrapper, params=np.random.uniform(-1, 1, size=5), method="CG")
#     if (-r.fun) > best:
#         best = -r.fun
#         result = r
#         print("\n", "="*50, "FOUND A BETTER ONE", "="*50, "\n")

# print("FUN:", result.fun)
# ================================
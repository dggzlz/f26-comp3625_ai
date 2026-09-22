import numpy as np
from gymnasium.envs.classic_control.cartpole import CartPoleEnv


class CartPoleAgent:
    """
    This class represents an agent that can interact with the CartPole environment. 
    It uses a linear combination of the observation features and parameters to determine the action to take (either pushing left or right). 
    That is,
        z = (observation[0] * parameters[0]) + (observation[1] * parameters[1]) + ... + parameters[n]   ← the last parameter is a bias term, like the y-intercept of a linear regression model
        and
        action = right if z > 0 else left
    The parameters that define the agent's behavior are provided during initialization.
    """

    def __init__(self, parameters):
        self.parameters = np.array(parameters)

    def get_action(self, observation):
        z = self.parameters[:-1].dot(observation) + self.parameters[-1]
        action = 1 if z > 0 else 0
        return action

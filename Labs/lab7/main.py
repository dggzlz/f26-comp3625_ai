from environments import RusselNorvigMDP


# instantiate the MDP (the one from the lectures... which is actually from the textbook)
# it will be useful to pull up the image of the MDP in the slides
mdp = RusselNorvigMDP(movement_cost=-0.04)

# in this MDP, the "state" is the agent's current position or (x,y) coordinates.
# the agent starts at (1, 1)
# the action is a number: either 0, 1, 2, or 3. 0 = move North, 1 = move East, 2 = move South, 3 = move West
# the object exposes transition probabilities through the get_transition_probabilities method:
start_state = (1, 1)
action_taken = 0
new_states = mdp.get_transition_probabilities(state=start_state, action=action_taken)

# note the get_transition_probabilities method returns a dictionary of new_state -> probability
print(f'distribution over new states after executing action {action_taken} from state {start_state} = {new_states}')

# use the get_reward method to get the reward for a given state transition
r = mdp.get_reward(state=(1,1), action=0, new_state=(1, 2))
print(f'reward for moving from (1,1) to (1,2) is {r}')

# get available actions using the get_actions method 
# (for this MDP it's always the same 4 actions, but in other MDPs it may depend on the state)
print(f'actions possible from (1,1): {mdp.get_actions((1,1))}')

# iterate through all states in the MDP using the all_states method
print('all states: ', end=' ')
for state in mdp.all_states():
    print(state, end=' ')
print(f'{len(mdp.all_states())} states in total')

# create tables for Q and Q_prime. Initialize to zero
# we'll implement these as nested dictionaries: Q[state][action] is the Q value for the state-action pair 
Q = {s: {a: 0 for a in mdp.get_actions(s)} for s in mdp.all_states()}
Q_prime = {s: {a: 0 for a in mdp.get_actions(s)} for s in mdp.all_states()}


# TASK 1: implement your value iteration algorithm here (use γ=0.99)
y = 0.99
run = 10000
for _ in range(run):
    for state in mdp.all_states():
        for action in mdp.get_actions(state=state):
            # get the bellman equation ready
            probs_dict = mdp.get_transition_probabilities(state=state, action=action)
            bellman_sum = 0

            for new_state, probability in probs_dict.items():
                reward = mdp.get_reward(state=state, action=action, new_state=new_state)
                best_utitily = max(Q[new_state].values())
                bellman_sum += probability * (reward + y * best_utitily)
            
            Q_prime[state][action] = bellman_sum                
    Q = Q_prime


# try printing out the Q values for states (4, 1) (3, 2) and (1, 1). Do they make sense?
print(f'Q values for (4, 1): {Q[(4, 1)]}')
print(f'Q values for (3, 2): {Q[(3, 2)]}')
print(f'Q values for (3, 3): {Q[(3, 3)]}')
print(f'Q values for (1, 1): {Q[(1, 1)]}')

# yes, they make sense (actions: 0=N, 1=E, 2=S, 3=W):
# (4, 1): West is best, moving away from -1. North is worst because it heads into -1.
# (3, 2): North is best, moving towards +1. East is worst because it heads into -1.
# (1, 1): North is best, starting the route around the wall to +1.



# TASK 2:
# now change the movement cost (line 6) to -2 (high punishment for every movement). how does this change the best action for (3, 2), and why?

# The best action changes from North to East, straight into the -1 state.
# Each move costs -2, so taking the -1 and ending the game right away is cheaper than walking to +1.

# now change the movement cost to -0.01 (low punishment for every movement). how does this change the best action for (3, 2), and why?

# The best action changes from North to West, into the wall at (2, 2).
# North has a 10% chance of slipping into -1, but West has none. Moves are so cheap that wasting a few is worth it to stay safe.

# now try +1 (a large reward for every movement). How does this change the best action for state (3, 3), and why?

# The best action changes from East to West, away from the +1 state.
# Every move now earns a reward and reaching +1 ends the game, so the agent wants to keep moving forever.
# West is the only action with no chance of entering the +1 state.
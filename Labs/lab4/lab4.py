"""
Your name(s):
Edwin Pang           - 201729758
John Galang          - 201719861
Tarun Jaswal         - 201720549
Diego Gonzalez Reyes - 201724348
"""
# clientA's utility function: U($) = 0.2 * ln($/1000 + 1)
# clientB's utility function: U($) = 0.14 * ln($/200 + 1)
# clientC's utility function: U($) = 1.43 * ln($/100,000 + 1)

# Task 1
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# General function -> U($) = multiplier * ln(money/denom + 1)

def utility(multiplier, money, denom):
    return multiplier * np.log(money/denom + 1)

money_range = np.arange(0, 100001)  # Sample data.

# multiplier
client_a_mult = 0.2
client_b_mult = 0.14
client_c_mult = 1.43

# denominators
client_a_denom = 1000
client_b_denom = 200
client_c_denom = 100000

# calculate their utility function
client_a = utility(client_a_mult, money_range, client_a_denom)
client_b = utility(client_b_mult, money_range, client_b_denom)
client_c = utility(client_c_mult, money_range, client_c_denom)

# plot results
fig, ax = plt.subplots(figsize=(10, 5.4), layout='constrained')
ax.plot(money_range, client_a, label='client a')  
ax.plot(money_range, client_b, label='client b')  
ax.plot(money_range, client_c, label='client c')  
ax.set_xlabel('Money')  
ax.set_ylabel('Utility')  
ax.set_title("Utility functions for Clients")  
ax.legend()  

plt.grid()
plt.show()

# From the plot we can observe that Client C is closer to a linear utiliy model whereas Client A and B are genuine logarithimic models. 
# This means that Client A and B are risk-averse, meaning that they prefer actions that guarantee wealth shown by the rapid increase 
# in utility near the start of the graph. However, at higher wealth levels, they will avoid gambling to get more money 
# because they want to minimize the risk of losing their current wealth, depicted by the flattening slope near the end of the graph. 

# Client C on the other hand shows a near constant slope which means that they are risk-neutral. This means they will continously 
# take risks regardless of current wealth. The value of money that is earned never changes since its decisions are made to maximize 
# monetary payouts and ignoring possible risk.
# ============================================================================================================

# Task 2 

# if an investement pays m amount of dollars with probability p, or zero with probability (1 - p)
# then we can say the expected utility equals:
# EU(m) = U(m) * p + U(0) * (1 - p) = U(m) * p
# EU(m) = p * mult * ln(m/d + 1)

df = pd.read_csv('investment_data.csv')

# get the neccessary data to operate 
payout = df['payout']
probs = df['p_payout']
multipliers = np.array([client_a_mult, client_a_mult, client_b_mult, client_b_mult, client_c_mult, client_c_mult])
denoms = np.array([client_a_denom, client_a_denom, client_b_denom, client_b_denom, client_c_denom, client_c_denom])

# create new column
df['expected_utility'] = probs * multipliers * np.log(payout/denoms + 1)

# take U($) and do some algebraic operations.
# from U($) = mult * ln(money/denom + 1)
# U($) -> u (utility)
# money -> amount (A(u))
# denom -> d
# by doing some operations we get -> amount = d * (e^(u/mult) - 1)
# final function -> A(u) = d * (e^(u/mult) - 1)

eu = df['expected_utility']
df['amount'] = denoms * (np.exp(eu / multipliers) - 1)
print(f"{df}\n")

# Inverse payout Client A = 1000    * (EXP(EU / 0.2) - 1)
# Inverse payout Client B = 200     * (EXP(EU / 0.14) - 1)
# Inverse payout Client C = 100000  * (EXP(EU / 1.43) - 1)

# ============================================================================================================

# Task 3

# Each investment should be sold to Client C since they attempt to maximize payout despite the risk it carries.
# Since their utility curve is near linear, they will gamble monetary gain by their exact mathematical odds, resulting in the 
# highest cash evaluation for each row  
# Client A and B on the other hand are logarithmic, meaning that if there is high risk, they will penalize the value of monetary gain.  

client_a_eu =  probs * utility(client_a_mult, payout, client_a_denom)
client_b_eu =  probs * utility(client_b_mult, payout, client_b_denom)
client_c_eu =  probs * utility(client_c_mult, payout, client_c_denom)
df['Client_A_investment'] = client_a_denom * (np.exp(client_a_eu/client_a_mult) - 1)
df['Client_B_investment'] = client_b_denom * (np.exp(client_b_eu/client_b_mult) - 1)
df['Client_C_investment'] = client_c_denom * (np.exp(client_c_eu/client_c_mult) - 1)
print(f"{df}\n")

# For example, the first investment with Client A, having a 60% chance of 80000$ should be sold to Client C, as 
max_price = df['Client_C_investment'][0]
print(f"C's maximum price is ${max_price:,.2f}\n")
# its maximum price it could be sold for is $42,286.44

# Calculate Client A's utility gain first
client_a_gain = utility(client_a_mult, max_price, client_a_denom) # 0.75
client_a_eu = df['expected_utility'][0]                           # 0.53
print(f"Client A's utility gain is 0.2 * ln({max_price:.2f} / 1000 + 1) = {client_a_gain:,.2f} - {client_a_eu:,.2f} = {client_a_gain - client_a_eu:,.2f}")
# Meaning their expected utlity score increased.

# Calculate Client C's utility gain now
client_c_eu = probs[0] * utility(client_c_mult, payout[0], client_c_denom) # 0.50
client_c_gain = utility(client_c_mult, max_price, client_c_denom)          # 0.50
print(f"Client C's utility gain is 1.43 * ln({max_price:.2f} / 100000 + 1) = {client_c_gain:,.2f} - {client_c_eu:,.2f} = {client_c_gain - client_c_eu:,.2f}")
# Meaning their expected utility score remains the same.

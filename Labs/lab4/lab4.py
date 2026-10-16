# clientA's utility function: U($) = 0.2 * ln($/1000 + 1)
# clientB's utility function: U($) = 0.14 * ln($/200 + 1)
# clientC's utility function: U($) = 1.43 * ln($/100,000 + 1)

# Task 1
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

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
# plt.show()

# From the plot we can observe that Client C is closer to a linear utiliy model whereas Client A and B are genuine logarithimic models. 
# This means that Client A and B are risk-averse, meaning that they prefer actions that guarantee wealth shown by the rapid increase 
# in utility near the start of the graph. However, at higher wealth levels, they will avoid gambling to get more money 
# because they want to minimize the risk of losing their current wealth, depicted by the flattening slope near the end of the graph. 

# Client C on the other hand shows a near constant slope which means that they are risk-neutral. This means they will continously 
# take risks regardless of current wealth. The value of money that is earned never changes since its decisions are made to maximize 
# monetary payouts and ignoring possible risk.

# Task 2 - 


# To get expected utility:

# if an investement pays m amount of dollars with probability p,
# or zero with probability (1 - p)
# then we can say the expected utility equals:
# EU(m) = U(m) * p + U(0) * (1 - p) = U(m) * p
# EU(m) = p * a * ln(m/d + 1)

def expected_utility(multiplier, money, prob, denom):
    return prob * multiplier * np.log(money/denom + 1)

df = pd.read_csv('investment_data.csv')

# get the neccessary data to operate 
payout = df['payout']
probs = df['p_payout']
multipliers = np.array([client_a_mult, client_a_mult, client_b_mult, client_b_mult, client_c_mult, client_c_mult])
denoms = np.array([client_a_denom, client_a_denom, client_b_denom, client_b_denom, client_c_denom, client_c_denom])

df['expected_utility'] = expected_utility(multipliers, payout, probs, denoms)

print(df)

# take U($) and do some algebraic operations.
# from U($) = mult * ln(money/denom + 1)
# U($) -> u (utility)
# money -> amount (A(u))
# denom -> d
# by doing some operations we get -> amount = d * (e^(u/mult) - 1)
# final function -> A(u) = d * (e^(u/mult) - 1)

def inversed_utility(denom, utility, mult):
    return denom * (np.exp(utility / mult) - 1)

eu = df['expected_utility']
df['U(payout)'] = inversed_utility(denoms, eu, multipliers)
print(df)

# Inverse payout Client A = 1000    * (EXP(EU / 0.2) - 1)
# Inverse payout Client B = 200     * (EXP(EU / 0.14) - 1)
# Inverse payout Client C = 100000  * (EXP(EU / 1.43) - 1)

# owner	    p_payout payout		U(payout)	    EU		            Inv_Client_A	Inv_Client_B	Inv_Client_C	
# clientA	0.6	    80000		0.8788898309	0.5273338986		12966.61017	    8447.175982	    44594.7714	
# clientA	0.5	    20000		0.6089044875	0.3044522438		3582.575695	    1559.836614	    23726.5456	
# clientB	0.9	    100000		0.8703248542	0.7832923687		49222.43522	    53612.59667	    72936.95173	
# clientB	0.4	    40000		0.7424626871	0.2969850749		3414.635955	    1468.431646	    23082.15466	
# clientC	0.1	    10000		0.1362935571	0.01362935571		70.52242669	    20.44977857	    957.6582777	
# clientC	0.05	90000		0.9178510572	0.04589255286		257.9240267	    77.58336863	    3261.321824	



# Task 3 - 

# Each investment should be sold to Client C since they attempt to maximize payout despite the risk it carries.
# Since their utility curve is near linear, they will gamble monetary gain by their exact mathematical odds, resulting in the 
# highest cash evaluation for each row  
# Client A and B on the other hand are logarithmic, meaning that if there is high risk, they will penalize the value of monetary gain.  

# For example, the first investment with Client A, having a 60% chance of 80000$ should be sold to Client C as 
# its maximum price it could be sold for is 44594.7714$
# Client A's utility gain is (0.2 * ln(44594.7714 / 1000 + 1 ) = 0.7639 - 0.5273 = 0.2366, meaning their expected utlity score increased.
# Client C's utility gain is (1.43 * ln(44594.7714 / 100000 + 1 ) = 0.5273 - 0.5273 = 0, meaning their expected utility score remains the same.
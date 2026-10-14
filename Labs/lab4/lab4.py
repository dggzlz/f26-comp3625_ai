# clientA's utility function: U($) = 0.2 * ln($/1000 + 1)
# clientB's utility function: U($) = 0.14 * ln($/200 + 1)
# clientC's utility function: U($) = 1.43 * ln($/100,000 + 1)

# Task 1
import matplotlib.pyplot as plt
import numpy as np

def utility(prob, money, denom):
    return prob * np.log(money/denom + 1)

x = np.arange(0, 100000)  # Sample data.

client_a = utility(0.2, x, 1000)
client_b = utility(0.14, x, 200)
client_c = utility(1.43, x, 100000)

fig, ax = plt.subplots(figsize=(10, 5.4), layout='constrained')
ax.plot(x, client_a, label='client a')  
ax.plot(x, client_b, label='client b')  
ax.plot(x, client_c, label='client c')  
ax.set_xlabel('x label')  
ax.set_ylabel('y label')  
ax.set_title("Simple Plot")  
ax.legend()  

plt.grid()
plt.show()

# From the plot we can observe that client C is closer to a linear utiliy model whears client A and B are genuine logarithimic models. 
# This means that for Client A and B, are more risk-averse with a cumulative money value near 0 - 20000. Overtime as the slope flattens out,
# potential big payouts aren't worth the risk of losing what they already have. 
# Client C on the other hand shows a constant slope which means that they will continueously take risks as it wants to maximize money gain.

# Task 2 - 

# Inverse payout Client A = 1000    * (EXP(EU / 0.2) - 1)
# Inverse payout Client B = 200     * (EXP(EU / 0.14) - 1)
# Inverse payout Client C = 100000  * (EXP(EU / 1.43) - 1)

# owner	    p_payout payout		U(payout)	    EU		            CE_Client_A	    CE_Client_B	    CE_Client_C	
# clientA	0.6	    80000		0.8788898309	0.5273338986		12966.61017	    8447.175982	    44594.7714	
# clientA	0.5	    20000		0.6089044875	0.3044522438		3582.575695	    1559.836614	    23726.5456	
# clientB	0.9	    100000		0.8703248542	0.7832923687		49222.43522	    53612.59667	    72936.95173	
# clientB	0.4	    40000		0.7424626871	0.2969850749		3414.635955	    1468.431646	    23082.15466	
# clientC	0.1	    10000		0.1362935571	0.01362935571		70.52242669	    20.44977857	    957.6582777	
# clientC	0.05	90000		0.9178510572	0.04589255286		257.9240267	    77.58336863	    3261.321824	
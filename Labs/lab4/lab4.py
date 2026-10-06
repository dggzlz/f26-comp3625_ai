# clientA's utility function: U($) = 0.2 * ln($/1000 + 1)
# clientB's utility function: U($) = 0.14 * ln($/200 + 1)
# clientC's utility function: U($) = 1.43 * ln($/100,000 + 1)

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

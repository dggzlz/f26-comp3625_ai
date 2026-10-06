# clientA's utility function: U($) = 0.2 * ln($/1000 + 1)
# clientB's utility function: U($) = 0.14 * ln($/200 + 1)
# clientC's utility function: U($) = 1.43 * ln($/100,000 + 1)

import matplotlib.pyplot as plt
import numpy as np

def utility(prob, money, denom):
    return prob * ln(money/denom + 1)

x = np.linspace(0, 2, 100)  # Sample data.

client_a = utility(0.2, x, 1000)
client_b = utility(0.14, x, 200)
client_c = utility(1.43, x, 100000)

# Note that even in the OO-style, we use `.pyplot.figure` to create the Figure.
fig, ax = plt.subplots(figsize=(5, 2.7), layout='constrained')
ax.plot(x, utility(0.2, x, 1000), label='client a')  # Plot some data on the Axes.
ax.plot(x, utility(0.14, x, 200), label='client b')  # Plot more data on the Axes...
ax.plot(x, utility(1.43, x, 100000), label='client c')  # ... and some more.
ax.set_xlabel('x label')  # Add an x-label to the Axes.
ax.set_ylabel('y label')  # Add a y-label to the Axes.
ax.set_title("Simple Plot")  # Add a title to the Axes.
ax.legend()  # Add a legend.


plt.show()

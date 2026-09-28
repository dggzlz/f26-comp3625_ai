import numpy as np
mylist = np.arange(10)
print(mylist)

N = len(mylist)
L = np.random.randint(1, N)
print("L=", L)
start = np.random.randint(0, N-L)
print("start:", start)
print(mylist[start:start+L])
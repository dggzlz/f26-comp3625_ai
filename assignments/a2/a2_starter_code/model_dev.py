import pandas as pd
import numoy as np
import sklearn 


# Part I -- pre-loading and set up

# standard way of keeping randomness the same at every run
np.random.seed(42)

# load historical customer data
customer_data = pd.read_csv('./data/customer_data.csv', index_col=None)
customer_claims = pd.read_csv('./data/customer_claims.csv', index_col=None)

# at random assign instances to train and test sets
split = 0.666 # data 67/33 split
train_idx = np.random.random(size=customer_data.shape[0]) < split

# separate into features (X) and classes (y), for training and test sets
x_train = customer_data.loc[train_idx]
x_test = customer_claims.loc[train_idx]
y_train = customer_data.loc[~train_idx]
y_test = customer_claims.loc[~train_idx]


# write your code to develop your agent program here.
# you can, of course, add additional .py files as needed.


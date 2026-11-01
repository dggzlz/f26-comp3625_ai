import pandas as pd
<<<<<<< HEAD
import numpy as np
=======
import numoy as np
import sklearn 


# Part I -- pre-loading and set up

# standard way of keeping randomness the same at every run
np.random.seed(42)
>>>>>>> lab6-diego

# load historical customer data
customer_data_df = pd.read_csv('data/customer_data.csv', index_col=None)
customer_claims_df = pd.read_csv('data/customer_claims.csv', index_col=None)['claim']

<<<<<<< HEAD
# randomly assign instances to training and test sets
train_idx = np.random.random(size=customer_data_df.shape[0]) < 0.666

# separate into training and test sets
x_train = customer_data_df.loc[train_idx]
y_train = customer_claims_df.loc[train_idx]
x_test = customer_data_df.loc[~train_idx]
y_test = customer_claims_df.loc[~train_idx]
=======
# at random assign instances to train and test sets
split = 0.666 # data 67/33 split
train_idx = np.random.random(size=customer_data.shape[0]) < split

# separate into features (X) and classes (y), for training and test sets
x_train = customer_data.loc[train_idx]
x_test = customer_claims.loc[train_idx]
y_train = customer_data.loc[~train_idx]
y_test = customer_claims.loc[~train_idx]

>>>>>>> lab6-diego

# write your code to develop your agent program here.
# you can, of course, add additional .py files as needed.


import pandas as pd
import numpy as np

# load historical customer data
customer_data_df = pd.read_csv('data/customer_data.csv', index_col=None)
customer_claims_df = pd.read_csv('data/customer_claims.csv', index_col=None)['claim']

# randomly assign instances to training and test sets
train_idx = np.random.random(size=customer_data_df.shape[0]) < 0.666

# separate into training and test sets
x_train = customer_data_df.loc[train_idx]
y_train = customer_claims_df.loc[train_idx]
x_test = customer_data_df.loc[~train_idx]
y_test = customer_claims_df.loc[~train_idx]

# write your code to develop your agent program here.
# you can, of course, add additional .py files as needed.


import pandas as pd
import numpy as np
import sklearn 
from utility import set_premiums, expected_utility_uninsured, max_acceptable_premium
from KNN import KNN
import time


# start = time.time()
# p_claims = model.predict_proba(x_test)
# end = time.time()
# print("Running total", end-start)
# coverage = x_test['coverage_amount'].to_numpy()
# premium, viable = set_premiums(p_claims, coverage)

# v_coverage = coverage[viable]
# v_premium = premium[viable]
# v_p_claims = p_claims[viable]

# profit_margin = (v_premium - (v_p_claims * v_coverage)) / v_coverage
# idx = np.argsort(profit_margin)[::-1]


def evualate_scales(model: KNN, set_tests: tuple, candidates_scales):
    x_test, y_test = set_tests
    model.scale_factor = candidates_scales
    start = time.time()
    p_claims = model.predict_proba(x_test)
    end = time.time()
    print("Running total", end-start)
    coverage = x_test['coverage_amount'].to_numpy()
    premium, viable = set_premiums(p_claims, coverage)

    v_coverage = coverage[viable]
    v_premium = premium[viable]
    v_p_claims = p_claims[viable]

    profit_margin = (v_premium - (v_p_claims * v_coverage)) / v_coverage
    idx = np.argsort(profit_margin)[::-1]
    profitable_customers = np.cumsum(v_coverage[idx]) <= 100000000
    money_in = v_premium[idx][profitable_customers].sum()
    money_out = ((((y_test.to_numpy())[viable])[idx])[profitable_customers] * v_coverage[idx][profitable_customers]).sum()
    return money_in - money_out

if __name__ == "__main__":
    # Part I -- pre-loading and set up

    # standard way of keeping randomness the same at every run
    np.random.seed(42)

    # load historical customer data
    customer_data_df = pd.read_csv('data/customer_data.csv', index_col=None)
    customer_claims_df = pd.read_csv('data/customer_claims.csv', index_col=None)['claim']

    # at random assign instances to train and test sets
    split = 0.666 # data 67/33 split
    train_idx = np.random.random(size=customer_data_df.shape[0]) < split

    # separate into features (X) and classes (y), for training and test sets
    x_train = customer_data_df.loc[train_idx]
    y_train = customer_claims_df.loc[train_idx]
    x_test = customer_data_df.loc[~train_idx]
    y_test = customer_claims_df.loc[~train_idx]

    # write your code to develop your agent program here.
    # you can, of course, add additional .py files as needed.

    model = KNN()
    model.fit(x_train, y_train)    

    total_profit = evualate_scales

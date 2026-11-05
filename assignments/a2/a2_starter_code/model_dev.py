import pandas as pd
import numpy as np
import sklearn 
from utility import set_premiums, expected_utility_uninsured, max_acceptable_premium
from search import SimAnnealing
from LogisticRegression import LogisticRegression
import time


def evualate_profit(model, test_sets: tuple, limit=100000000):
    x_test, y_test = test_sets
    
    p_claims = model.predict_proba(x_test)
    coverage = x_test['coverage_amount'].to_numpy()
    premium, viable = set_premiums(p_claims, coverage)

    v_coverage = coverage[viable]
    v_premium = premium[viable]
    v_p_claims = p_claims[viable]

    profit_margin = (v_premium - (v_p_claims * v_coverage)) / v_coverage
    idx = np.argsort(profit_margin)[::-1]
    profitable_customers = np.cumsum(v_coverage[idx]) <= limit
    money_in = v_premium[idx][profitable_customers].sum()
    money_out = ((((y_test.to_numpy())[viable])[idx])[profitable_customers] * v_coverage[idx][profitable_customers]).sum()
    return money_in - money_out    

def train_and_eval(params, train_set, test_set):
    epochs, step = params
    x_train, y_train = train_set

    model = LogisticRegression(int(epochs), step)
    model.fit(x_train, y_train)
    return evualate_profit(model, test_set)

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
    test_set = (customer_data_df.loc[~train_idx], customer_claims_df.loc[~train_idx])

    # write your code to develop your agent program here.
    # you can, of course, add additional .py files as needed.
    

    print("Starting timer")
    start = time.time()
    
    model = LogisticRegression()
    model.fit(x_train, y_train)   

    total_profit = evualate_profit(model, test_set)
    wrapper = lambda params: train_and_eval(params, (x_train, y_train), test_set)
    search = SimAnnealing(fitness=wrapper)
    baseline = np.array([model.epochs, model.step])
    search.run(baseline=baseline)
    print("best candidates", search.best_candidates)
    print("best profit", search.best_profit)
    
    # build model with optimal hyperparameters
    epochs, step = search.best_candidates
    model = LogisticRegression(epochs=int(epochs), step=round(step, 2))
    model.fit(x_train, y_train)
    final_profit = evualate_profit(model, test_set)
    print("Final profit", final_profit)
    end = time.time()
    print("Running total", end-start)
    
    
    

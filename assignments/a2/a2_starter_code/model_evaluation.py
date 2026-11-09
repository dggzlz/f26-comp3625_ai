import pandas as pd
import numpy as np
import pickle
import os
from utility import set_premiums
from LogisticRegression import LogisticRegression 

LIMIT = 100_000_000

def load_model():
    """Loads serialized model to program"""
    model_path = "./model/final_model.pkl" if os.path.exists("./model/final_model.pkl") else "final_model.pkl"
    with open(model_path, "rb") as f:
        return pickle.load(f)

def set_premium(customer_data: pd.DataFrame) -> pd.DataFrame:
    """
    Accepts a dataframe of data on potential customers, identifies which customers to take on,
    and sets premiums for them.

    :param customer_data: a dataframe with the same columns as customer_data.csv
    :return: a DataFrame of the same length as customer_data, with the following columns:
            p_claim: your estimated probability that each customer in customer_data will make a claim
            desired_customer: a boolean column indicating which customers you want to take on
            premium: the amount of the premium to charge each customer
    """
    model = load_model()

    # Estimate probability of claim for each customer
    p_claim = model.predict_proba(customer_data)

    # Calculate premiums and check economic viability using utility curve
    coverage = customer_data["coverage_amount"].to_numpy()
    premium, viable = set_premiums(p_claim, coverage)

    # Pick highest profit margin customers up to $100M total coverage
    desired_customer = np.zeros(len(customer_data), dtype=bool)

    expected_cost = p_claim * coverage
    expected_profit = premium - expected_cost
    profit_margin = expected_profit / coverage

    # Customers who are not viable get -1 margin so they are never prioritized
    profit_margin[~viable] = -1

    # Sort by profit margin in descending order
    sorted_margins = np.argsort(profit_margin)[::-1]
    total_coverage = 0

    for i in sorted_margins:
        # Stop selecting when no remaining customers are profitable
        if profit_margin[i] <= 0:
            break

        # Only accept if coverage fits under $100M 
        if total_coverage + coverage[i] <= LIMIT:
            desired_customer[i] = True
            total_coverage += coverage[i]

    # Use the same row labels as the input so each result lines up with its customer
    result = pd.DataFrame(index=customer_data.index)
    result["p_claim"] = p_claim
    result["desired_customer"] = desired_customer
    result["premium"] = premium

    return result 

if __name__ == "__main__":

    data_path = "data/customer_data.csv" if os.path.exists("data/customer_data.csv") else "customer_data.csv"
    test_df = pd.read_csv(data_path)

    # Testing
    # n = LIMIT
    # print("\n--- Testing on n amount of customers ---")
    # sample_df = test_df.iloc[:n].copy()
    # sample_results = set_premium(sample_df)
    # print(sample_results)
    # print(sample_results["desired_customer"].value_counts())

    print("\n--- Model Evaluation ---")
    results = set_premium(test_df)

    accepted_customers = results["desired_customer"]
    total_selected = accepted_customers.sum()
    selected_coverage = test_df.loc[accepted_customers, "coverage_amount"].sum()
    total_premiums = results.loc[accepted_customers, "premium"].sum()

    print(f"Total customers evaluated: {len(test_df):,}")
    print(f"Total customers selected:  {total_selected}")
    print(f"Total coverage: ${selected_coverage:,.2f} / ${LIMIT:,.2f}")
    print(f"Under $100M cap satisfied: {selected_coverage <= LIMIT}")
    print(f"Total premiums collected:  ${total_premiums:,.2f}") 
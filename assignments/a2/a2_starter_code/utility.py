import numpy as np

# constants from the utility curve: U($) = -263.31 + 22.09 ln($ + 150,000)
A = -263.31
B = 22.09
WEALTH = 150000

def utility(dollars):
    return A + B * np.log(dollars + WEALTH)

def expected_utility_uninsured(p_claim, coverage):
    utility_if_claim = utility(-coverage)  # customer pays for the full loss themselves
    utility_if_no_claim = utility(0)       # nothing happens
    return p_claim * utility_if_claim + (1 - p_claim) * utility_if_no_claim

def max_acceptable_premium(p_claim, coverage):
    eu = expected_utility_uninsured(p_claim, coverage)
    return WEALTH - np.exp((eu - A) / B)

def set_premiums(p_claim, coverage, margin=0.2):
    expected_cost = p_claim * coverage  # what we expect to pay out on average
    premium = expected_cost * (1 + margin)

    # cap the premium so the customer still gets a utility benefit
    premium = np.minimum(premium, max_acceptable_premium(p_claim, coverage) - 1)
    premium = np.maximum(premium, 0)  # never charge a negative premium

    # utility check: insurance must beat the lottery of going uninsured
    customer_benefits = utility(-premium) > expected_utility_uninsured(p_claim, coverage)

    # profit check: premium must be more than what we expect to pay out
    company_profits = premium > expected_cost

    viable = customer_benefits & company_profits
    return premium, viable

if __name__ == "__main__":
    # worked example: 10% chance of claiming on $100,000 coverage
    p = 0.1
    coverage = 100000

    premium, viable = set_premiums(p, coverage)
    print(f"Expected cost:            ${p * coverage:,.2f}")
    print(f"Max acceptable premium:   ${max_acceptable_premium(p, coverage):,.2f}")
    print(f"Premium at 20% margin:    ${premium:,.2f}  Viable: {viable}")
    print(f"U(-premium) = {utility(-premium):.4f} vs EU(uninsured) = {expected_utility_uninsured(p, coverage):.4f}")

    # several customers at once
    p_claims = np.array([0.0, 0.05, 0.3, 0.9])
    coverages = np.array([50000, 140000, 70000, 1000])
    premiums, viable = set_premiums(p_claims, coverages)
    print(f"\nPremiums: {np.round(premiums, 2)}")
    print(f"Viable:   {viable}")

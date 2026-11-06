import numpy as np

# constants from the utility curve: U($) = -263.31 + 22.09 ln($ + 150,000)
A = -263.31
B = 22.09
WEALTH = 150000

def utility(dollars):
    """
    Calculates the logarithmic utility value for a given monetary amount.

    Parameters:
    dollars : float or np.array - The monetary value (positive or negative) to evaluate.

    Returns:
    float or np.array - The calculated utility value.
    """
    return A + B * np.log(dollars + WEALTH)

def expected_utility_uninsured(p_claim, coverage):
    """
    Calculates the expected utility for a customer who chooses to remain uninsured.
    It weights the utility of paying the full loss by the probability of a claim, 
    and the utility of zero loss by the probability of no claim.

    Parameters:
    p_claim : float or np.array - The probability of a claim occurring (0 to 1).
    coverage : float or np.array - The total financial loss if a claim occurs.
    """
    utility_if_claim = utility(-coverage)  # customer pays for the full loss themselves
    utility_if_no_claim = utility(0)       # nothing happens
    return p_claim * utility_if_claim + (1 - p_claim) * utility_if_no_claim

def max_acceptable_premium(p_claim, coverage):
    """
    Determines the absolute maximum premium a customer is willing to pay before 
    choosing to remain uninsured becomes mathematically better.

    Parameters:
    p_claim : float or np.array - The probability of a claim occurring.
    coverage : float or np.array - The total potential financial loss.

    Returns:
    float or np.array - The maximum premium amount in dollars.
    """
    eu = expected_utility_uninsured(p_claim, coverage)
    
    # Inverse of the utility function to solve for the exact maximum dollar amount
    return WEALTH - np.exp((eu - A) / B)

def set_premiums(p_claim, coverage, margin=0.2):
    """
    Calculates the optimal premium to charge and evaluates if the policy is mathematically viable.
    A policy is viable only if the customer benefits (utility check) AND the company profits.

    Parameters:
    p_claim : float or np.array - The predicted probability of a claim.
    coverage : float or np.array - The maximum payout amount for the policy.
    margin : float - The profit margin applied over the expected cost (default 20%).

    Returns:
    tuple - (premium: float or np.array, viable: bool or np.array) representing the calculated 
            dollar amount to charge and whether the policy makes economic sense for both parties.
    """
    # Calculate base expected cost and apply the company's profit margin
    expected_cost = p_claim * coverage  # what we expect to pay out on average
    premium = expected_cost * (1 + margin)

    # cap the premium so the customer still gets a utility benefit
    premium = np.minimum(premium, max_acceptable_premium(p_claim, coverage) - 1)
    premium = np.maximum(premium, 0)  # never charge a negative premium

    # utility check: insurance must beat the lottery of going uninsured
    customer_benefits = utility(-premium) > expected_utility_uninsured(p_claim, coverage)

    # profit check: premium must be more than what we expect to pay out
    company_profits = premium > expected_cost

    # Both economic conditions must be strictly true for the policy to be sold
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

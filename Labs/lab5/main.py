from scipy.io import arff
import pandas as pd
import numpy as np
from scipy.optimize import minimize

# Load the ARFF file into a pandas dataframe
data, meta = arff.loadarff('diabetes.arff')
df = pd.DataFrame(data)
df['class'] = df['class'].str.decode('utf-8')

# see what the data table looks like
print(df)

# split into predictors X and target Y
X = df.drop('class', axis=1)
Y = df['class']

# write a function that applies a specified linear decision threshold to the entire dataset
# and returns the predictions of diabetes risk
def linear_decision(w: np.array) -> np.array:
    """
    apply a linear decision threshold to the predictors X
    :param w: array of weights and bias. Should be length-9: [w1, w2... w8, b]
    :return: numpy array of predictions for each case in X
    """
    # your code here
    max_len = len(w)
    return X @ w[:max_len - 1] + w[max_len - 1]

# write a function that computes the entropy of patient classes in the two groups created by the linear decision threshold
def decision_entropy(w: np.array) -> float:
    """
    compute the average entropy of the 2 patient groups created by the linear decision threshold
    :param w: array of weights and bias. Should be length-9: [w1, w2... w8, b]
    :return: entropy in the actual classes (as contained in Y) of patients in each group
            (remember when computing average entropy, to weight by the size of each group - see slide 19)
    """
    # your code here
    
    # create a binary mask    
    at_risk = linear_decision(w) > 0

    patients = len(df)
    
    # get the two groups
    group1 = Y.loc[at_risk]
    group2 = Y.loc[~at_risk]

    # calculate the entropies
    entropy_g1 = calc_entropy(group1)
    entropy_g2 = calc_entropy(group2)
    
    avg_entropy = (len(group1) / patients * entropy_g1) + (len(group2) / patients * entropy_g2)
    return avg_entropy

def calc_entropy(group):
    length = len(group)
    
    if length == 0:
        return 0
    
    prob_1 = (group > 0).sum() / length
    prob_2 = (group <= 0).sum() / length
    
    if prob_1 == 0 and prob_2 == 0:
        return 0
    elif prob_1 == 0:
        return -(prob_2 * np.log2(prob_2))
    elif prob_2 == 0:
        return -(prob_1 * np.log2(prob_1))
        
    entropy = (prob_1 * np.log2(prob_1)) + (prob_2 * np.log2(prob_2))
    return -entropy
    
# write a search that finds the best (entropy-minimizing) weights and bias terms
# YOUR CODE HERE

# turn Y into a Serie of 1s and 0s
Y = (Y == 'tested_positive').astype(int)

# get baseline entropy
baseline = calc_entropy(Y)
print(f"\nBaseline entropy: {baseline:.4f}")

# initialize search step
x0 = np.random.uniform(-1.0, 1.0, size=len(X.columns) + 1)
search = minimize(decision_entropy, x0)

# optimized entropy
print(f"Optimized entropy: {search.fun:.4f}")
# get optimal weights
optimal_weights = search.x
print("optimal weights:", optimal_weights)

# ___Reflection questions:___

# 1) What was the baseline entropy of the whole dataset? What is the entropy after your classifier splits it into two groups?
"""
The baseline entropy can be calculated with the initial column Y, giving a baseline of 0.9331.
After the classifier, the entropy is closely similar, being ~0.9309.
"""

# 2) what effect does b have in the classification?
"""
Here, b is a offset that dictates the boundary of the classification. It tells the classifier where the 
boundary is, and decides how hard is for a patient to be at risk or not.
"""

# 3) what does the model tell us about the relationship between the clinical measurements and diabetes? Which measurements contibute to risk of diabetes, and which reduce it?
print(f"\nFeatures: {X.columns}")
"""
The combination of these features tell us that the increase or decrease of each one of them will determine whether the patient could be at risk or not.
E.g. Being older increases the risk of diabetes. In this case, if age feature increases, it moves the patient past the threshold to being at_risk. 
"""

# 4) A pure hill-climbing search would not be ideal here. Do you know why?
"""
Hill-climbing (HC) is a greedy algorithm. HC will take the first set that improves the minimazation and will terminate the search and returns those values.
In this case, a bad threshold may flag patients in the wrong group, or group them all in only one! 
"""

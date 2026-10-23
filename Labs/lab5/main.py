"""
Your name(s):
Edwin Pang           - 201729758
John Galang          - 201719861
Tarun Jaswal         - 201720549
Diego Gonzalez Reyes - 201724348
"""
from scipy.io import arff
from scipy.optimize import dual_annealing
import pandas as pd
import numpy as np
import os

# Load the ARFF file into a pandas dataframe (found next to this file, so it runs from any folder)
folder = os.path.dirname(os.path.abspath(__file__))
data, meta = arff.loadarff(os.path.join(folder, 'diabetes.arff'))
df = pd.DataFrame(data)
df['class'] = df['class'].str.decode('utf-8')

# see what the data table looks like
print(df)

# split into predictors X and target Y
X = df.drop('class', axis=1)
Y = df['class']

# scale each measurement to mean 0, std 1 so the weights can be compared to each other
X = (X - X.mean()) / X.std()

# 1 = tested_positive, 0 = tested_negative
Y = (Y == 'tested_positive').astype(int)

def entropy(labels):
# Computes the entropy of a group of 0/1 labels using -p*log2(p) - (1-p)*log2(1-p), where p is the fraction positive
    if len(labels) == 0:
        return 0.0

    p = np.mean(labels)  # fraction of positive patients
    if p == 0 or p == 1:
        return 0.0  # pure group, also avoids log2(0)

    return -p * np.log2(p) - (1 - p) * np.log2(1 - p) #returns float between 0 and 1


# write a function that applies a specified linear decision threshold to the entire dataset
# and returns the predictions of diabetes risk
def linear_decision(w: np.array) -> np.array:
# Predicts each patient at risk if w•m + b > 0, using the first 8 values of w as weights and the last as b
    weights = w[:8]
    b = w[8]
    return (X @ weights + b).to_numpy() > 0 # matrix multiplication of X and weights, then add bias b, then return boolean array of predictions


# write a function that computes the entropy of patient classes in the two groups created by the linear decision threshold
def decision_entropy(w: np.array) -> float:
# Splits patients by linear_decision and returns the size-weighted average entropy of the two groups
    predictions = linear_decision(w)
    positive_group = Y[predictions]   # actual classes of patients predicted at risk
    negative_group = Y[~predictions]  # actual classes of patients predicted not at risk

    n = len(Y)
    return len(positive_group) / n * entropy(positive_group) + len(negative_group) / n * entropy(negative_group)


# write a search that finds the best (entropy-minimizing) weights and bias terms
def run_search(restarts=10):
# Runs dual_annealing several times to find the weights and bias with the lowest decision_entropy, keeping the best
    bounds = [(-1, 1)] * 9  # 8 weights + 1 bias
    best_w = None
    best_entropy = 1.0  # entropy is never above 1

    for i in range(restarts):
        result = dual_annealing(decision_entropy, bounds=bounds, seed=i)
        print(f"Attempt {i + 1} Entropy: {result.fun:.4f}")

        # keep track of the best solution
        if result.fun < best_entropy:
            best_entropy = result.fun
            best_w = result.x

    return (best_w, best_entropy)


if __name__ == "__main__":
    best_w, best_entropy = run_search()

    # entropy doesn't care which group is called "at risk", so the search may return the flipped threshold.
    # if most predictions are wrong, flip the signs so the "at risk" group is the mostly-positive one
    accuracy = np.mean(linear_decision(best_w) == Y)
    if accuracy < 0.5:
        best_w = -best_w
        accuracy = 1 - accuracy

    print(f"\n--- Final Results ---")
    print(f"Baseline entropy (whole dataset): {entropy(Y):.4f}")
    print(f"Best entropy (after split):       {best_entropy:.4f}")
    print(f"Accuracy:                         {accuracy * 100:.2f}%")
    print(f"\nWeights:")
    print(pd.Series(best_w, index=list(X.columns) + ['b']).round(3))



# ___Reflection questions:___

# 1) What was the baseline entropy of the whole dataset? What is the entropy after your classifier splits it into two groups?
#    Baseline entropy is 0.9331. After the split it drops to 0.7024 (about 79% accuracy).

# 2) what effect does b have in the classification?
#    b shifts the threshold. A bigger b predicts more patients at risk, a smaller b predicts fewer.

# 3) what does the model tell us about the relationship between the clinical measurements and diabetes? Which measurements contibute to risk of diabetes, and which reduce it?
#    Glucose increases risk the most (weight 0.944), followed by BMI, pregnancies and family history (pedigree).
#    Skin thickness, insulin and age barely matter. Blood pressure is the only one that slightly reduces risk (weight -0.274).

# 4) A pure hill-climbing search would not be ideal here. Do you know why?
#    Small weight changes usually don't change the entropy at all, so the search space is mostly flat.
#    A hill-climber would find no better neighbour and get stuck.

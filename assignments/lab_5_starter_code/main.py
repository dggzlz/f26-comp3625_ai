from scipy.io import arff
import pandas as pd
import numpy as np



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
    pass
    # your code here


# write a function that computes the entropy of patient classes in the two groups created by the linear decision threshold
def decision_entropy(w: np.array) -> float:
    """
    compute the average entropy of the 2 patient groups created by the linear decision threshold
    :param w: array of weights and bias. Should be length-9: [w1, w2... w8, b]
    :return: entropy in the actual classes (as contained in Y) of patients in each group
            (remember when computing average entropy, to weight by the size of each group - see slide 19)
    """
    pass
    # your code here


# write a search that finds the best (entropy-minimizing) weights and bias terms
# YOUR CODE HERE




# ___Reflection questions:___

# 1) What was the baseline entropy of the whole dataset? What is the entropy after your classifier splits it into two groups?


# 2) what effect does b have in the classification?


# 3) what does the model tell us about the relationship between the clinical measurements and diabetes? Which measurements contibute to risk of diabetes, and which reduce it?


# 4) A pure hill-climbing search would not be ideal here. Do you know why?

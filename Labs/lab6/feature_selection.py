import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
import warnings
warnings.filterwarnings("ignore")

# YOUR NAME(s): 
"""
Edwin Pang
John Galang
Tarun Jaswal
Diego Gonzalez
"""

# In this exercise we will write a hill-climbing search to find the best subset of features to use for learning
np.random.seed(42)

# load the "wine" dataset into a dataframe
# It contains 178 instances of wines, with various features. Each is classified into 1 of 3 categories
df = pd.read_csv('wine.csv', index_col=None)

# randomly assign instances to training and test sets (50% each for illustration purposes - 66.6% training maybe more typical)
train_idx = np.random.random(size=df.shape[0]) < 0.50

# separate into features (X) and classes (Y), for training and test sets
x_train = df.drop('class', axis=1).loc[train_idx]
y_train = df['class'].loc[train_idx]
x_test = df.drop('class', axis=1).loc[~train_idx]
y_test = df['class'].loc[~train_idx]

# instantiate the LogisticRegression object to use in the search

model = KNeighborsClassifier(n_neighbors=4)
# Uncomment for Logistic Regression
# model = LogisticRegression()
model.fit(x_train, y_train)
# calculate model's accuracy with 13 features
initial_accuracy = (model.predict(x_test) == y_test).mean()

# The dataset includes 13 features. Some may be redundant, or irrelevant to the prediction of wine category.
# Let's find the best subset of features to use for supervised learning
# write a search that incrementally builds the optimal feature subset (the subset that gets best accuracy on test set)
# The search can go forward (adding features one by one) or backward (removing features one by one)
# stop the search when another addition/removal would not improve accuracy.
# Note that you can get the complete list of feature names like this: x_train.columns, or as a set: set(x_train.columns)
# and you can reduce the dataframe to a subset of features like this: x_train_subset = x_train[desired_features_list]

best_score = initial_accuracy
features_set = set(x_train.columns)
optimal_subset = features_set.copy()

while True:
    best_round_score = best_score # keep track of best accuracy
    feature_to_drop = ""          # keep track which feature to drop
    
    # at each iteration test accuracy by dropping a feature at a time
    for feature in optimal_subset:
        subset = list(optimal_subset - set([feature])) # test model without this feature
        x_train_subset = x_train[subset]      # take the subset from x_train
        x_test_subset = x_test[subset]        # make sure to match the test set to the same number of features
        model.fit(x_train_subset, y_train)    # train model
        preds = model.predict(x_test_subset)  # test model
        curr_score = (preds == y_test).mean() # calculate accuracy
        
        if curr_score > best_round_score:
            best_round_score = curr_score
            feature_to_drop = feature
    
    # if model not improved then terminate loop
    if best_round_score > best_score:
        best_score = best_round_score
        optimal_subset.remove(feature_to_drop)
    else:        
        break
    
print(f"\nOptimal features:           {', '.join([feature for feature in optimal_subset])}")
print(f"Optimal features' Accuracy: {best_score:.2f}")
print(f"All features' Accuracy:     {initial_accuracy:.2f}")

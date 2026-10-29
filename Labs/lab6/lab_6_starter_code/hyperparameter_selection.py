import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier


# YOUR NAME(s): 
"""
Edwin Pang
John Galang
Tarun Jaswal
Diego Gonzalez
"""
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


# perform a grid search of criterion, max_depth, and ccp_alpha parameters to see what gives the best decision tree.
# (by "best" we mean best classification accuracy on the test dataset)
# this nested loop may help get you started:
best_acc = 0
params = ()

for criterion in ['gini', 'entropy', 'log_loss']:
    for max_depth in range(1, 6):
        for ccp_alpha in np.arange(0, 0.25, 0.01):
            # instatiate model
            clf = DecisionTreeClassifier(criterion=criterion, max_depth=max_depth, ccp_alpha=ccp_alpha)
            clf.fit(x_train, y_train)           # train model   
            preds = clf.predict(x_test)         # test model
            accuracy = (preds == y_test).mean() # calculate accuracy

            # keep track of which params perform best
            if accuracy > best_acc:
                best_acc = accuracy
                params = (criterion, max_depth, ccp_alpha)

                print(f"\nTraining Accuracy: {accuracy:.2f}")
                print(f"Criterion:         {criterion}")
                print(f"Max depth:         {max_depth}")
                print(f"ccp alpha:         {ccp_alpha}")
                
print(f"\nBest params: {', '.join([str(param) for param in params])}")
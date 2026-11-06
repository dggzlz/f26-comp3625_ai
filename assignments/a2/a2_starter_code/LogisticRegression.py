import numpy as np  
import pandas as pd

# https://www.geeksforgeeks.org/machine-learning/what-is-data-normalization/
# https://www.geeksforgeeks.org/machine-learning/understanding-logistic-regression/# https://developers.google.com/machine-learning/crash-course/numerical-data/normalization
class LogisticRegression:
    """
    A custom machine learning model that builds and trains using Logistic Regression. 
    It performs binary classification by utilizing Gradient Descent to optimize weights 
    and the Sigmoid function to output probabilities.
    """
    def __init__(self, epochs=1000, alpha=0.5):
        """
        Initializes the Logistic Regression model with hyperparameters

        Parameters:
        epochs : int - The number of iterations the gradient descent loop will run.
        alpha : float - The learning rate (step size) for weight updates.
        """
        self.bias = 0
        self.w = None
        self.epochs = epochs
        self.alpha = alpha
        self.x_max = 0
        self.x_min = 0

    def fit(self, X, y):
        """
        Take training data and train model as a eager-learner.

        Parameters:
        X : pd.DataFrame - Contains features for training 
        y : pd.Series - Contains label for supervised model
        """
        
        # turn data in numpy array
        X = X.to_numpy()
        y = y.to_numpy()

        # set min and max for data normalization
        self.x_max = np.max(X, axis=0) 
        self.x_min = np.min(X, axis=0)

        # initialize weights and normalize data
        self.w = np.zeros(X.shape[1])
        X = self.normalization(X)
        
        # train the model and find best set of w and the bias
        for _ in range(self.epochs):
            # calculate z for the sigmoid function
            z = np.dot(X, self.w) + self.bias
            
            # calculate the error
            error = self.sigmoid(z) - y
            
            # calculate the slope
            gradient = np.dot(X.T, error) / X.shape[0]
            
            # update w and bias
            self.w -= gradient * self.alpha 
            self.bias -= np.mean(error) * self.alpha
            
    def predict_proba(self, X):
        """
        Takes a set of new data and outputs the probability of each data point to fall either in the desire two classes

        Parameters:
        X : np.array or pd.Dataframe - Dataset to be predicted onto classes
        
        Returns:
        np.array of probabilities
        """
        # normalize data first
        X = self.normalization(np.asarray(X))
        
        # calculate z for sigmoid
        z = np.dot(X, self.w) + self.bias
        return self.sigmoid(z)
    
    def sigmoid(self, z):
        """
        Calculate the sigmoid curve for the model

        Parameters:
        z : np.array - 1D array for calculating the coordinates for each customer
        
        Returns:
        np.array of probabilities
        """
        return 1 / (1 + np.exp(-z))
    
    def normalization(self, X):
        """
        Sets data between ranges 0 - 1 (normalization process)

        Parameters:
        X : np.array - Dataset to normalize.
        """
        return (X - self.x_min) / (self.x_max - self.x_min)

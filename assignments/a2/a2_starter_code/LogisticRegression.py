import numpy as np  
import pandas as pd

# https://www.geeksforgeeks.org/machine-learning/understanding-logistic-regression/# https://developers.google.com/machine-learning/crash-course/numerical-data/normalization
class LogisticRegression:
    def __init__(self, epochs=1000, step=0.5):
        self.bias = 0
        self.w = None
        self.epochs = epochs
        self.step = step
        self.x_max = 0
        self.x_min = 0

    def sigmoid(self, z):
        return 1 / (1 + np.exp(-z))
    
    def fit(self, X, y):
        X = X.to_numpy()
        y = y.to_numpy()

        self.x_max = np.max(X, axis=0) 
        self.x_min = np.min(X, axis=0)

        self.w = np.zeros(X.shape[1])
        X = self.normalization(X)
        
        for _ in range(self.epochs):
            z = np.dot(X, self.w) + self.bias
            error = self.sigmoid(z) - y
            gradient = np.dot(X.T, error) / X.shape[0]
            self.w -= gradient * self.step 
            self.bias -= np.mean(error) * self.step
            
    def predict_proba(self, X):
        X = self.normalization(np.asarray(X))
        z = np.dot(X, self.w) + self.bias
        return self.sigmoid(z)

    def normalization(self, X):
        return (X - self.x_min) / (self.x_max - self.x_min)

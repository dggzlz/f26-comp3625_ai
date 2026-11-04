import numpy as np  
import pandas as pd

# https://www.geeksforgeeks.org/machine-learning/what-is-data-normalization/
# https://www.geeksforgeeks.org/machine-learning/k-nearest-neighbours/
# https://www.geeksforgeeks.org/theory-of-computation/boyer-moore-majority-voting-algorithm/
# https://developers.google.com/machine-learning/crash-course/numerical-data/normalization
class KNN:
    def __init__(self, n_neighbours=5, metric='euclidean'):
        self.neighbours = n_neighbours
        self.calc_dist = self.euclidean_dist if metric == 'euclidean' else self.manhattan_dist
        self.x_min = 0
        self.x_max = 0
        self.class_feature = 0
        self.norm_data = 0
        self.scale_factor = 0
        self.dataset = 0

    def fit(self, X, y):
        self.x_max = np.max(X, axis=0)
        self.x_min = np.min(X, axis=0)
        self.scale_factor = self.x_max - self.x_min
        self.dataset = X
        self.norm_data = self.normalization(X)
        self.class_feature = y.to_numpy()
    
    def euclidean_dist(self, data):
        a = data
        b = self.dataset
        scaler = self.scale_factor
        return np.sqrt(np.sum(((a - b) * scaler)**2, axis=2))

    def manhattan_dist(self, norm2):
        return np.sum(np.abs(norm2 - self.norm_data), axis=1)
    
    def predict_proba(self, data):
            
        # norm_data = (self.normalization(data)).to_numpy()
        data = data.to_numpy()[:, np.newaxis, :]
        calc = self.calc_dist(data)
        idx = np.argsort(calc, axis=1)[:,:self.neighbours]
        return self.class_feature[idx].mean(axis=1)
        # proba = []
        # for row in range(norm_data.shape[0]):
        #     calc = self.calc_dist(norm_data[row])
        #     idx = np.argsort(calc)[:self.neighbours]
        #     closest_neighbours = self.class_feature[idx]
        #     proba.append(closest_neighbours.mean())
        # return proba
    
    def predict(self, test_set):
        self.predict_proba(test_set)
    # DO NOT ERASE
    # def normalization(self, data):
    #     return (data - self.x_min) / self.scale_factor

    def normalization(self, data):
        return (data - self.x_min) / (self.x_max - self.x_min)

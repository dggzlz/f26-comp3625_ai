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

    def fit(self, x_train, y_train):
        self.x_max = np.max(x_train, axis=0)
        self.x_min = np.min(x_train, axis=0)
        self.scale_factor = self.x_max - self.x_min
        self.norm_data = self.normalization(x_train)
        self.class_feature = y_train
    
    def euclidean_dist(self, norm2):
        return np.sqrt(np.sum((norm2 - self.norm_data)**2, axis=1))

    def manhattan_dist(self, norm2):
        return np.sum(np.abs(norm2 - self.norm_data), axis=1)
    
    def predict_proba(self, data):
            
        norm_data = self.normalization(data)
        proba = []
        for row in range(norm_data.shape[0]):
            calc = self.calc_dist(norm_data[row])
            idx = np.argsort(calc)[:self.neighbours]
            closest_neighbours = self.class_feature[idx]
            proba.append(closest_neighbours.mean())
        return proba
    
    # DO NOT ERASE
    # def normalization(self, data):
    #     return (data - self.x_min) / self.scale_factor

    def normalization(self, data):
        return (data - self.x_min) / (self.x_max - self.x_min)

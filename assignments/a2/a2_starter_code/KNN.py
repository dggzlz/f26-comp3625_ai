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
        X = X.to_numpy()
        self.dataset = X
        self.x_max = np.max(X, axis=0)
        self.x_min = np.min(X, axis=0)
        self.scale_factor = self.x_max - self.x_min
        self.class_feature = y.to_numpy()
    
    def euclidean_dist(self, data):
        a = data
        b = self.dataset
        scaler = self.scale_factor
        return np.sum(((a - b) * scaler)**2, axis=2)

    def manhattan_dist(self, norm2):
        return np.sum(np.abs(norm2 - self.norm_data), axis=1)
    
    def predict_proba(self, data):
        data = data.to_numpy()[:, np.newaxis, :]
        jump = 150
        final_dist = []
        
        for row in range(0, data.shape[0], jump):
            batch = data[row: row + jump]
            calc = self.calc_dist(batch)
            idx = np.argpartition(calc, self.neighbours, axis=1)[:,:self.neighbours]
            final_dist.append(self.class_feature[idx].mean(axis=1))
        return np.concatenate(final_dist, axis=0)

    def predict(self, test_set):
        self.predict_proba(test_set)

    def normalization(self, data):
        return (data - self.x_min) / (self.x_max - self.x_min)

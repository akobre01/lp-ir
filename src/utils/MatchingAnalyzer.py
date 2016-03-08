import numpy as np
import sys

class MatchingAnalyzer:

    def __init__(self, ws, assn_mat, T=0.0, max_assn=sys.maxint):
        self.weights = ws
        self.assignments = assn_mat
        self.makespan = T
        self.alpha = max_assn

    def paper_scores(self):
        return np.sum(self.assignments * self.weights, axis=0)

    def ms_vio(self):
        return filter(lambda x: x < self.makespan, self.paper_scores())

    def num_ms_vio(self):
        return len(filter(lambda x: x < self.makespan, self.paper_scores()))

    def min_ms_vio(self):
        return min(map(lambda x: self.makespan - x, self.ms_vio()))

    def max_ms_vio(self):
        return max(map(lambda x: self.makespan - x, self.ms_vio()))

    def mean_ms_vio(self):
        return np.mean(map(lambda x: self.makespan - x, self.ms_vio()))

    def std_ms_vio(self):
        return np.std(map(lambda x: self.makespan - x, self.ms_vio()))

    def mean_score(self):
        return np.mean(self.paper_scores())

    def std_score(self):
        return np.std(self.paper_scores())

    def max_score(self):
        return max(self.paper_scores())

    def min_score(self):
        return min(self.paper_scores())

    def max_weight(self):
        return np.max(self.weights)

    def obj(self):
        return np.sum(self.assignments * self.weights)

    def rev_assns(self):
        return np.sum(self.assignments, axis=1)

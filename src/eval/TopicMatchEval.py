import argparse
import numpy as np

class TopicMatchEval(object):
    """
    An object that represents a solved instance of RAP with reviewers and
    papers represented by topic vectors.
    """

    def __init__(self, rev_mat, pap_mat, assign_mat):
        self.rev_mat = rev_mat        # rev x topics
        self.pap_mat = pap_mat        # pap x topics
        self.assign_mat = assign_mat  # rev x pap

    def rev_group(self, paper):
        return np.nonzero(self.assign_mat[:,paper])[0]

    def group_scores(self):
        group_scores = {}
        for i in range(np.size(self.assign_mat,axis=1)):
            group = self.rev_group(i)
            # assert that the group is the correct size?
            group_max = np.amax(self.rev_mat[group], axis=0)
            group_scores[i] = np.sum(np.minimum(group_max, self.pap_mat[i])) / float(np.sum(self.pap_mat[i]))
        return group_scores

    def group_based_assignment_score(self):
        score_map = self.group_scores()
        total = 0.0
        for i,v in score_map.iteritems():
            total += v
        return total

    def individual_based_assignment_score(self):
        individual_score = 0.0
        for i in range(np.size(self.assign_mat, axis=1)):
            group = self.rev_group(i)
            for rev in group:
                individual_score += np.sum(np.minimum(self.rev_mat[rev], self.pap_mat[i])) / float(np.sum(self.pap_mat[i]))
        return individual_score

    def superiority_score(self, other):
        my_group_scores = self.group_scores()
        other_group_scores = other.group_scores()
        for i in my_group_scores.keys():
            assert i in other_group_scores
        for i in other_group_scores.keys():
            assert i in my_group_scores.keys()

        my_wins = 0.0
        for i,v in my_group_scores.iteritems():
            if v >= other_group_scores[i]:
                my_wins += 1.0
        return my_wins / len(my_group_scores.keys())

    def fraction_better_score(self, other):
        my_group_scores = self.group_scores()
        other_group_scores = other.group_scores()
        for i in my_group_scores.keys():
            assert i in other_group_scores
        for i in other_group_scores.keys():
            assert i in my_group_scores.keys()

        my_wins = 0.0
        for i,v in my_group_scores.iteritems():
            if v > other_group_scores[i]:
                my_wins += 1.0
        return my_wins / len(my_group_scores.keys())

    def absolute_better_score(self, other):
        my_group_scores = self.group_scores()
        other_group_scores = other.group_scores()
        for i in my_group_scores.keys():
            assert i in other_group_scores
        for i in other_group_scores.keys():
            assert i in my_group_scores.keys()

        my_wins = 0.0
        for i,v in my_group_scores.iteritems():
            if v > other_group_scores[i]:
                my_wins += 1.0
            elif v < other_group_scores[i]:
                my_wins -= 1.0
        return my_wins

    def fraction_of_best_possible(self):
        my_group_scores = self.group_scores()
        total_score = 0.0
        best_possible = 0.0
        for i in range(np.size(self.pap_mat, axis=0)):
            total_score += my_group_scores[i]
            best_possible += np.sum(self.pap_mat[i])
        return total_score / best_possible


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Arguments for analyzing a single topic matching.')
    parser.add_argument('rev_mat', type=str, help='the file from which to read the rev_mat')
    parser.add_argument('pap_mat', type=str, help='the file from which to read the pap_mat')
    parser.add_argument('assign_mat', type=str, help='the file from which to read the assign_mat')

    args = parser.parse_args()

    rev_mat = np.load(args.rev_mat)
    pap_mat = np.load(args.pap_mat)
    assign_mat = np.load(args.assign_mat)
    tme = TopicMatchEval(rev_mat,pap_mat,assign_mat)
    print "INDIVIDUAL SCORE: %f" % tme.individual_based_assignment_score()
    print "GROUP SCORE: %f" % tme.group_based_assignment_score()

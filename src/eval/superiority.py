import argparse
import numpy as np

from TopicMatchEval import TopicMatchEval

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Arguments for analyzing a single topic matching.')
    parser.add_argument('rev_mat', type=str, help='the file from which to read the rev_mat')
    parser.add_argument('pap_mat', type=str, help='the file from which to read the pap_mat')
    parser.add_argument('assign_mat1', type=str, help='the file from which to read the assign_mat1')
    parser.add_argument('assign_mat2', type=str, help='the file from which to read the assign_mat2')

    args = parser.parse_args()

    rev_mat = np.load(args.rev_mat)
    pap_mat = np.load(args.pap_mat)
    assign_mat1 = np.load(args.assign_mat1)
    assign_mat2 = np.load(args.assign_mat2)
    tme1 = TopicMatchEval(rev_mat,pap_mat,assign_mat1)
    tme2 = TopicMatchEval(rev_mat,pap_mat,assign_mat2)
    print "PAPERS: %d" % np.size(pap_mat, axis=0)
    print "REVS: %d" % np.size(rev_mat, axis=0)

    assert np.sum(assign_mat1[:,0]) == np.sum(assign_mat2[:,0])
    assert np.sum(assign_mat1[:,0]) == np.sum(assign_mat1[:,1])

    print "REV Per PAPL %d" % np.sum(assign_mat1[:,0])
    print "INDIVIDUAL SCORE1: %f" % tme1.individual_based_assignment_score()
    print "INDIVIDUAL SCORE2: %f" % tme2.individual_based_assignment_score()
    print "GROUP SCORE1: %f" % tme1.group_based_assignment_score()
    print "GROUP SCORE2: %f" % tme2.group_based_assignment_score()
    print "FRACTION BEST POSSIBLE1: %f" % tme1.fraction_of_best_possible()
    print "FRACTION BEST POSSIBLE2: %f" % tme2.fraction_of_best_possible()
    print "SUPERIORITY 1 >= 2: %f" % tme1.superiority_score(tme2)
    print "SUPERIORITY 1 > 2: %f" % tme1.fraction_better_score(tme2)
    print "SUPERIORITY (ABSOLUTE) 1 > 2: %f" % tme1.absolute_better_score(tme2)

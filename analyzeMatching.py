from MatchingAnalyzer import MatchingAnalyzer

import argparse
import numpy as np
import sys


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='profile the input files for analysis')
    parser.add_argument('weight_file', type=str, help='the file from which to load the weights')
    parser.add_argument('assignment_file', type=str, help='the file from the reviewer assignment should be loaded')
    parser.add_argument('-m', '--makespan_file', type=str, help='optional arg to load makespan')
    parser.add_argument('-a', '--alpha_file', type=str, help='optional arg to load reviewer alpha (max number of papers reviewed by any reviwer')
    args = parser.parse_args()

    weights = np.genfromtxt(args.weight_file)
    assignments = np.genfromtxt(args.assignment_file, delimiter=',')
    makespan = np.genfromtxt(args.makespan_file, delimiter=',') if args.makespan_file else 0.0
    alpha = np.genfromtxt(args.alpha_file, delimiter=',') if args.alpha_file else sys.maxint

    analyzer = MatchingAnalyzer(weights, assignments, makespan, alpha)
    print "obj | min | max | mean"
    print "%0.2f" % analyzer.obj()
    print "%0.2f | %0.2f | %0.2f" % (analyzer.min_score(), analyzer.max_score(), analyzer.mean_score())
    print
    print "makespan | # violations | min vio | max vio | mean vio | max rev weight"
    print "%0.2f | %d (%0.1f%%) | %0.2f | %0.2f | %0.2f | %0.2f" % (analyzer.makespan, analyzer.num_ms_vio(), 100.0 * analyzer.num_ms_vio() / len(analyzer.weights[0]), analyzer.min_ms_vio(), analyzer.max_ms_vio(), analyzer.mean_ms_vio(), analyzer.max_weight())
    print "ALG & obj & #violations & mean violation & std violation"
    print " & %0.2f | %d (%0.1f%%) & %0.2f & %0.2f\\\\" % (analyzer.obj(), analyzer.num_ms_vio(), 100.0 * analyzer.num_ms_vio() / len(analyzer.weights[0]), analyzer.mean_ms_vio(), analyzer.std_ms_vio())

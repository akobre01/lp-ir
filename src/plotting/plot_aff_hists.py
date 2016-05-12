import argparse
import numpy as np
import os

from matplotlib import pyplot as plt

def mat_from_file(f):
    return np.load(f)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Input directories.')
    parser.add_argument('title', type=str, help='Title of the plot')
    parser.add_argument('xlabel', type=str, help='label for the x-axis')
    parser.add_argument('ylabel', type=str, help='label for the y-axis')
    parser.add_argument('bins', type=str, help='the number of bins to plot')
    parser.add_argument('assignment_file', type=str, help='the file that stores the assignment matrix')
    parser.add_argument('weight_file', type=str, help='the file that stores the reviewer affinities (tensor)')
    parser.add_argument('paper_tensor_file', nargs='?', default=None, type=str, help='the file that stores the paper topics tensor')

    args = parser.parse_args()

    assignments = mat_from_file(args.assignment_file)
    weights = mat_from_file(args.weight_file)

    if args.paper_tensor_file:
        # if you're in here, we treat the 'weight_file' as the reviewer_tensor
        n_tops = np.size(weights, axis=2)
        paper_tensor = mat_from_file(args.paper_tensor_file)
        assignment_tensor = np.tile(assignments[:,:,np.newaxis], (1,1,n_tops))
        assigned_reviewers = weights * assignment_tensor

        # create a paper x topic matrix of the best scores per reviewer
        group_max_score = np.amax(assignment_tensor, axis=0)
        group_eff_score = np.minimum(group_max_score, paper_tensor[0,:,:])

        print group_eff_score
        print group_eff_score.shape
        print paper_tensor[0,:,:]
        print paper_tensor[0,:,:].shape

        # get max score per paper
        fractional_group_score = group_eff_score / paper_tensor[0,:,:]

        affinities = fractional_group_score.reshape(-1)

        # what you want to do here is to figure out the score per topic per paper
        # but you want that score as a fraction of the max paper score
        # you should also output a histogram, as above, of summed scores per paper
    else:
        affinities = np.sum(assignments * weights, axis=0)

    print affinities
    plt.clf()
    plt.figure(1)
    plt.subplot(111)
#    plt.hist(affinities, bins=args.bins)
    plt.hist(affinities)
    plt.xlabel(args.xlabel)
    plt.ylabel(args.ylabel)
    plt.title(args.title)
    plt.xlim(0,5)
    plt.show()

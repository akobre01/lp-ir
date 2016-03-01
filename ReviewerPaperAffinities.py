from collections import defaultdict
from matplotlib import pyplot as plt

import argparse
import json
import numpy as np
import os
import xml.etree.ElementTree as ET

class ReviewerPaperAffinities:
    """A representation of the reviewer paper affinitiy matrix.
    Mainly used to read an external XML file and generate the
    matrix
    """

    def __init__(self, xmlFile):
        self.aff_dict = defaultdict(dict)
        self.all_subs = {}
        self.all_revs = {}
        self.sub_count = 0
        self.rev_count = 0
        tree = ET.parse(xmlFile)
        root = tree.getroot()
        for submission in root:
            sub_id = submission.attrib['submissionId']
            if sub_id not in self.all_subs:
                self.all_subs[sub_id] = self.sub_count
                self.sub_count += 1
            for reviewer in submission:
                rev_id = reviewer.attrib['email']
                score = float(reviewer.attrib['score'])
                if rev_id not in self.all_revs:
                    self.all_revs[rev_id] = self.rev_count
                    self.rev_count += 1
                self.aff_dict[sub_id][rev_id] = score

    def toMatrix(self):
        """Convert the xml to a np array"""
        aff_mat = np.zeros((self.rev_count, self.sub_count))
        for sub_id, sub_idx in self.all_subs.iteritems():
            for rev_id, rev_idx in self.all_revs.iteritems():
                aff_mat[rev_idx][sub_idx] = self.aff_dict[sub_id][rev_id]
        return aff_mat

    def serialize(self, outdir):

        try:
            os.makedirs('./matching-inputs/%s/' % outdir)
        except OSError, e:
            if e.errno != 17:
                raise # This was not a "directory exist" error..


        aff_mat = self.toMatrix()
        # Create stats file
        f = open('./matching-inputs/%s/stats.txt' % outdir, 'w')
        f.write("PAPERS: %d\n" % self.sub_count)
        f.write("REVIEWERS: %d\n" % self.rev_count)
        f.write("MEAN SCORE: %f\n" % np.mean(aff_mat))
        f.write("MAX SCORE: %f\n" % np.max(aff_mat))
        f.write("MIN SCORE: %f\n" % np.min(aff_mat))
        f.close()

        # Create map from reviewer to index
        f = open('./matching-inputs/%s/revidx.json' % outdir, 'w')
        f.write(json.dumps(self.all_revs))
        f.close()

        # Create map from submission to index
        f = open('./matching-inputs/%s/subidx.json' % outdir, 'w')
        f.write(json.dumps(self.all_subs))
        f.close()

        # Create weights file
        np.savetxt('./matching-inputs/%s/weights.txt' % outdir, aff_mat)

        # Create histogram of weights
        plt.hist(np.ravel(aff_mat), bins=100)
        plt.title(outdir)
        plt.xlabel('scores')
        plt.ylabel('#reviewers with score')
        plt.savefig('./matching-inputs/%s/hist.png' % outdir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Input File')
    parser.add_argument('scorefile', type=str, help='The absolute path of the score file')
    parser.add_argument('base_outdir', type=str, help='The name of the directory under matching-inputs to store the output')

    args = parser.parse_args()
    rpa = ReviewerPaperAffinities(args.scorefile)
    rpa.serialize(args.base_outdir)

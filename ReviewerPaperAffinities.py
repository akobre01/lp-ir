from collections import defaultdict
from matplotlib import pyplot as plt

import numpy as np
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


if __name__ == "__main__":
    rpa = ReviewerPaperAffinities("data/toronto_scores.xml")
    print rpa.sub_count
    print rpa.rev_count
    print rpa.aff_dict.keys()[:5]
    aff_mat = rpa.toMatrix()
    print aff_mat.shape
    print "MEAN: %f" % np.mean(aff_mat)
    print "MAX: %f" % np.max(aff_mat)
    print "MIN: %f" % np.min(aff_mat)
    print "SHAPE: %s" % np.ravel(aff_mat).shape
    plt.hist(np.ravel(aff_mat))
    plt.show()

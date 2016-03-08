import argparse
import numpy as np
import xml.etree.ElementTree as ET


def create_weights_from_xml(filename):
    tree = ET.parse(filename)
    scores_matrix = tree.getroot()
    score_dict = {}
    paper_to_index = {}
    reviewer_to_index = {}
    paper_counter = 0
    reviewer_counter = 0
    for paper in scores_matrix:
        submissionId = paper.attrib['submissionId']
        if submissionId not in paper_to_index:
            paper_to_index[submissionId] = paper_counter
            paper_counter += 1

        score_dict[submissionId] = {}
        for reviewer in paper:
            email = reviewer.attrib['email']
            score = reviewer.attrib['score']
            if email not in reviewer_to_index:
                reviewer_to_index[email] = reviewer_counter
                reviewer_counter += 1

            score_dict[submissionId][email] = score

    score_mat = np.zeros((reviewer_counter, paper_counter))
    for pap, revs in score_dict.iteritems():
        j = paper_to_index[pap]
        for email, score in revs.iteritems():
            i = reviewer_to_index[email]
            score_mat[i,j] = score

    return score_mat



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Input File')
    parser.add_argument('scorefile', type=str, help='The absolute path of the file to parse')

    args = parser.parse_args()

    weights = create_weights_from_xml(args.scorefile)
    print "[NON ZEROS]: %d" % np.count_nonzero(weights)
    print "[SHAPE] %s" % str(weights.shape)

    np.savetxt('./weights/tpms.out', weights)

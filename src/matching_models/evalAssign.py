import numpy as np
from WGRAP import WGRAP
from matplotlib import pyplot as plt

if __name__ == "__main__":
    rev_mat_file = "/Users/akobren/software/repos/git/lp-ir/data/train/kou_et_al/kou_rev_mat_dbdm.npy"
    pap_mat_file = "/Users/akobren/software/repos/git/lp-ir/data/train/kou_et_al/kou_pap_mat_dbdm.npy"
    beta = 3
    rev_mat = np.load(rev_mat_file)
    pap_mat = np.load(pap_mat_file)
    num_rev = np.size(rev_mat, axis=0)
    num_pap = np.size(pap_mat, axis=0)
    alpha = np.ceil(num_pap * beta / num_rev)
    wgrap = WGRAP(rev_mat, pap_mat, alpha, beta)

    out_file = "../../data/train/kou_et_al/wgrap-dbdm-%d-%d-assign-refine-9" % (alpha, beta)
    assign_mat = np.load(out_file + ".npy")
    wgrap.curr_assignment = assign_mat
    print wgrap.score_assignment()

    paper_scores = []
    topic_scores = []
    for i in range(np.size(pap_mat, axis=0)):
        rev_group = wgrap.curr_rev_group(i)
        paper_scores.append(wgrap.group_score(rev_group, i))
        group_max = np.amax(wgrap.rev_mat[rev_group], axis=0)
        topic_coverage = np.minimum(group_max, wgrap.pap_mat[i,:]) / wgrap.pap_mat[i,:]
        for topic in filter(lambda x: not np.isnan(x), topic_coverage):
            assert topic <= 1.0
            assert topic >= 0.0
            topic_scores.append(topic)

    plt.hist(paper_scores, bins=50)
    plt.title('WGRAP Assignment Quality')
    plt.xlabel('Group Score')
    plt.ylabel('# of Papers')
    plt.show()

    plt.hist(filter(lambda x: x < 1.0, paper_scores), bins=50)
    plt.title('WGRAP Assignment Quality (scores < 1.0)')
    plt.xlabel('Group Score')
    plt.ylabel('# of Papers')
    plt.show()

    plt.hist(topic_scores, bins=50)
    plt.title('WGRAP Assignment Quality (by Topic)')
    plt.xlabel('Coverage (max 1.0)')
    plt.ylabel('# of Topics')
    plt.show()

    plt.hist(filter(lambda x: x < 1.0, topic_scores), bins=50)
    plt.title('WGRAP Assignment Quality (by Topic)')
    plt.xlabel('Coverage (max 1.0)')
    plt.ylabel('# of Topics')
    plt.show()

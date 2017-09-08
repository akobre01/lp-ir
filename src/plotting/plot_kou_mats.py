from matplotlib import pyplot as plt
import numpy as np

def showWeights(weights, topic):
    weights = weights.reshape(weights.shape[:2])
    reviewer_order = np.array(sorted(weights, key=lambda row: np.sum(row)))
    paper_order = np.array(sorted(reviewer_order.T, key=lambda row: -np.sum(row))).T
    cMap = plt.get_cmap("Blues")

    reviewer_heatmap = plt.pcolor(paper_order, cmap=cMap, vmin=0.0, vmax=1.0)
    plt.colorbar(reviewer_heatmap)
    plt.title("Topic %d" % topic)
    plt.xlabel("Papers")
    plt.ylabel("Reviewers")

if __name__ == "__main__":
    # rev_tensor = np.load("../../data/train/kou_et_al/kou_rev_tensor_db08.npy")
    # # for i in range(np.size(rev_tensor, axis=2)):
    # for i in range(4):
    #     plt.subplot(2,2, i + 1)
    #     showWeights(rev_tensor[:,:,i+6], i)
    # plt.show()

    score_mat = np.load("../../data/train/kou_et_al/kou_score_mat_db08.npy")
    # for i in range(np.size(rev_tensor, axis=2)):
    plt.subplot(1,1,1)
    showWeights(score_mat, 1)
    plt.show()

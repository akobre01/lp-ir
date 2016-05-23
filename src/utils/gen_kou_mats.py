import numpy as np

def read_pap_profile(f, n_tops, pre):
    paps = {}
    for line in f:
        splits = line.split("\t")
        title, topic, score = "%s-%s" % (pre, splits[0]), int(splits[1]), float(splits[2])
        if title not in paps:
            paps[title] = np.zeros(n_tops)
        paps[title][topic] = score
    return paps


if __name__ == "__main__":
    data_dir = "/Users/akobren/software/repos/git/lp-ir/data/kou_et_al"
    dbs = ["DataMining08", "DataMining09", "Databases08", "Databases09", "Theory08", "Theory09"]
    # dbs = ["DataMining08", "Databases08"]
    papers = "paper-profile"
    reviewers = "reviewer-profile"

    paps = {}
    revs = {}
    for db in dbs:
        f = open("%s/%s/%s" % (data_dir, db, papers),"r")
        paps.update(read_pap_profile(f, 30, db))
        f.close()
        f = open("%s/%s/%s" % (data_dir, db, reviewers),"r")
        revs.update(read_pap_profile(f, 30, db))
        f.close()

    pap_mat = []
    rev_mat = []
    for k,v in paps.iteritems():
        pap_mat.append(v)
    for k,v in revs.iteritems():
        rev_mat.append(v)

    print len(pap_mat)
    print len(rev_mat)
    reviewer_tensor = np.tile(np.array(rev_mat)[:,np.newaxis,:], (1,len(pap_mat),1))
    paper_tensor = np.tile(np.array(pap_mat)[np.newaxis,:,:], (len(rev_mat),1,1))
    score_mat = np.sum(np.minimum(reviewer_tensor, paper_tensor), axis=2)
    np.save("kou_pap_mat", np.array(pap_mat))
    np.save("kou_rev_mat", np.array(rev_mat))
    np.save("kou_pap_tensor", paper_tensor)
    np.save("kou_rev_tensor", reviewer_tensor)
    np.save("kou_score_mat", score_mat)
    # np.save("kou_pap_mat_dbdm", np.array(pap_mat))
    # np.save("kou_rev_mat_dbdm", np.array(rev_mat))
    # np.save("kou_pap_tensor_dbdm", paper_tensor)
    # np.save("kou_rev_tensor_dbdm", reviewer_tensor)
    # np.save("kou_score_mat_dbdm", score_mat)

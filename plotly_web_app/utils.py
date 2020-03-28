import numpy as np
from sklearn.metrics import roc_auc_score


def avg_roc_auc_fed(fm_members_fed, fp_members_fed):
    """ Generate the roc-auc scores for n data sets, their average and std.
    """
    roc_auc_fed = list()
    for fm, fp in zip(fm_members_fed, fp_members_fed):
        roc_auc_fed.append(
            roc_auc_score(
                y_true=np.concatenate((np.ones_like(fp), np.zeros_like(fm))),
                y_score=np.concatenate((fp, fm))
            )
        )
    return roc_auc_fed, np.mean(roc_auc_fed), np.std(roc_auc_fed)

import numpy as np
from sklearn.metrics import roc_auc_score
import seaborn as sns
import matplotlib.pyplot as plt

sns.set(color_codes=True)


def split_members_into_n_groups(
        members,
        similarity_ratio: float = 1.,
        n: int = 4
):
    """ Split the data points into n groups.

    The data points distribution similarity between the groups
    depends on the similarity_ratio.
    """
    n_el = members.shape[0]
    n_identical = int(n_el * similarity_ratio)

    # generate n parts with identical distributions
    identical_parts = members[:n_identical]
    identical_parts = np.split(identical_parts, n)

    # generate n parts with non-identical distributions
    sorted_parts = np.array(sorted(members[n_identical:]))
    sorted_parts = np.split(sorted_parts, n)

    members_fed = [
        np.concatenate((sorted_part, identical_part))
        for sorted_part, identical_part in zip(sorted_parts, identical_parts)
    ]

    return members_fed


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


def plot_fed_distributions(fm_members_fed, fp_members_fed, n=4, fig_size=(7, 4)):
    fig1 = plt.figure(figsize=fig_size)
    with sns.color_palette("GnBu_d", n):
        for fm in fm_members_fed:
            sns.distplot(fm)
        plt.title("Model scores of the members belonging to the negative class for each one of the pods")
        plt.show()

    fig2 = plt.figure(figsize=fig_size)
    with sns.color_palette("YlOrRd", n):
        for fp in fp_members_fed:
            sns.distplot(fp)
        plt.title("Model scores of the members belonging to the positive class for each one of the pods")
        plt.show()

    return fig1, fig2

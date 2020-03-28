import numpy as np


def init_data(
        size: int = 4000,
        seed: int = 15,
        fp_mean: float = 16,
        fp_std: float = 10,
        fm_mean: float = -16,
        fm_std: float = -10
):
    """ Generate the scores that belong to the positive/negative class
    """
    np.random.seed(seed)
    fp_members_ = np.random.randn(size) * fp_std + fp_mean
    fm_members_ = np.random.randn(size) * fm_std + fm_mean

    return fp_members_, fm_members_


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

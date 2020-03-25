import numpy as np


def init_data(size: int = 4000, seed: int = 15):
    np.random.seed(seed)

    fp_mean, fp_std = 16, 10
    fm_mean, fm_std = -16, 20
    fp_members_ = np.random.randn(size) * fp_std + fp_mean
    fm_members_ = np.random.randn(size) * fm_std + fm_mean

    return fp_members_, fm_members_


def split_members_into_n_groups(
        members,
        similarity_ratio: float = 1.,
        n: int = 4
):
    n_el = members.shape[0]

    members_identical_part = members[:int(n_el * similarity_ratio)]
    members_sorted_part = np.array(sorted(members[int(n_el * similarity_ratio):]))

    members_sorted_part = np.split(members_sorted_part, n)
    members_identical_part = np.split(members_identical_part, n)

    members_fed = [
        np.concatenate((sorted_part, identical_part))
        for sorted_part, identical_part in zip(members_sorted_part, members_identical_part)
    ]

    return members_fed

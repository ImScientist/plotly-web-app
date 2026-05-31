from __future__ import annotations

from collections.abc import Sequence

import numpy as np

from .constants import DEFAULT_GROUP_COUNT


def init_data(
        size: int = 4000,
        seed: int = 15,
        fp_mean: float = 16,
        fp_std: float = 10,
        fm_mean: float = -16,
        fm_std: float = 20
):
    """ Generate the scores that belong to the positive/negative class
    """
    rng = np.random.default_rng(seed)
    fp_members_ = rng.normal(loc=fp_mean, scale=fp_std, size=size)
    fm_members_ = rng.normal(loc=fm_mean, scale=fm_std, size=size)

    return fp_members_, fm_members_


def split_members_into_n_groups(
        members: Sequence[float],
        similarity_ratio: float = 1.,
        n: int = DEFAULT_GROUP_COUNT
):
    """ Split the data points into n groups.

    The data points distribution similarity between the groups
    depends on the similarity_ratio.
    """
    if not 0 <= similarity_ratio <= 1:
        raise ValueError('similarity_ratio must be between 0 and 1 inclusive')
    if n <= 0:
        raise ValueError('n must be a positive integer')

    members = np.asarray(members)
    n_el = members.shape[0]
    n_identical = int(n_el * similarity_ratio)

    # generate n parts with identical distributions
    identical_parts = members[:n_identical]
    identical_parts = np.array_split(identical_parts, n)

    # generate n parts with non-identical distributions
    sorted_parts = np.array(sorted(members[n_identical:]))
    sorted_parts = np.array_split(sorted_parts, n)

    members_fed = [
        np.concatenate((sorted_part, identical_part))
        for sorted_part, identical_part in zip(sorted_parts, identical_parts)
    ]

    return members_fed

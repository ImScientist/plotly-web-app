import os
import pickle
import numpy as np

from .constants import RATIOS
from .data import split_members_into_n_groups, init_data
from .utils import avg_roc_auc_fed
from .visualization import (
    build_negative_distribution_figure,
    build_positive_distribution_figure,
    calculate_global_roc_auc,
    format_roc_auc_values,
)


def generate_figures_and_data_splits(ratios, fp_members, fm_members):
    """ Generate all possible data distributions and figures.
    """
    content_p = dict()
    content_m = dict()

    for ratio in ratios:
        fp_members_fed = split_members_into_n_groups(fp_members, similarity_ratio=ratio)
        fm_members_fed = split_members_into_n_groups(fm_members, similarity_ratio=ratio)
        fig_p = build_positive_distribution_figure(fp_members_fed)
        fig_m = build_negative_distribution_figure(fm_members_fed)

        content_p[f"{ratio:.2f}"] = {
            'fig_p': fig_p,
            'data': fp_members_fed
        }

        content_m[f"{ratio:.2f}"] = {
            'fig_m': fig_m,
            'data': fm_members_fed
        }

    return content_p, content_m


def calculate_roc_auc_scores(ratios, content_p, content_m):
    """ Calculate all possible roc-auc scores
    """

    roc_auc_scores = dict()

    for ratio_p in ratios:
        for ratio_m in ratios:
            fm_members_fed = content_m[f"{ratio_m:.2f}"]['data']
            fp_members_fed = content_p[f"{ratio_p:.2f}"]['data']
            roc_auc_fed, roc_auc_mean, _ = avg_roc_auc_fed(fm_members_fed, fp_members_fed)

            roc_auc_scores[f"{ratio_p:.2f}_{ratio_m:.2f}"] = {
                'mean': str(np.round(roc_auc_mean, 3)),
                'values': format_roc_auc_values(roc_auc_fed)
            }

    return roc_auc_scores


def create_content(data_dir: str = 'content',
                   size: int = 4000,
                   seed: int = 15):
    """ Create (and dump) the content needed to generate the interactive visualization.
    """
    fp_members, fm_members = init_data(size, seed)
    score = calculate_global_roc_auc(fp_members, fm_members)

    # create all figures
    ratios = list(RATIOS)
    content_p, content_m = generate_figures_and_data_splits(ratios, fp_members, fm_members)
    roc_auc_scores = calculate_roc_auc_scores(ratios, content_p, content_m)

    content = {
        'ratios': ratios,
        'content_p': content_p,
        'content_m': content_m,
        'roc_auc_scores': roc_auc_scores,
        'score': score
    }

    os.makedirs(data_dir, exist_ok=True)

    with open(os.path.join(data_dir, 'content.pickle'), 'wb') as f:
        pickle.dump(content, f)

    return content


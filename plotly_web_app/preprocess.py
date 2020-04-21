import os
import pickle
import numpy as np
from sklearn.metrics import roc_auc_score

from .data import split_members_into_n_groups, init_data
from .utils import avg_roc_auc_fed

import plotly.express as px
import plotly.figure_factory as ff


def generate_figures_and_data_splits(ratios, fp_members, fm_members):
    """ Generate all possible data distributions and figures.
    """
    content_p = dict()
    content_m = dict()

    for ratio in ratios:
        fp_members_fed = split_members_into_n_groups(fp_members, similarity_ratio=ratio)
        fm_members_fed = split_members_into_n_groups(fm_members, similarity_ratio=ratio)

        labels = [f'pod {i}' for i in range(len(fp_members_fed))]

        fig_p = ff.create_distplot(fp_members_fed,
                                   labels,
                                   show_hist=False,
                                   colors=px.colors.sequential.Sunsetdark[2:])
        fig_m = ff.create_distplot(fm_members_fed,
                                   labels,
                                   show_hist=False,
                                   colors=px.colors.sequential.Teal[2:])

        fig_p.update_traces(opacity=0.8)
        fig_p.update_layout(
            title_text='Scores distribution (positive class)',
            xaxis_title_text='Score',
            bargap=0.85,
            bargroupgap=0
        )

        fig_m.update_traces(opacity=0.8)
        fig_m.update_layout(
            title_text='Scores distribution (negative class)',
            xaxis_title_text='Score',
            bargap=0.85,
            bargroupgap=0
        )

        content_p[ratio] = {
            'fig_p': fig_p,
            'data': fp_members_fed
        }

        content_m[ratio] = {
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
            fm_members_fed = content_m[ratio_m]['data']
            fp_members_fed = content_p[ratio_p]['data']
            roc_auc_fed, roc_auc_mean, _ = avg_roc_auc_fed(fm_members_fed, fp_members_fed)

            roc_auc_scores[f"{ratio_p}_{ratio_m}"] = {
                'mean': str(np.round(roc_auc_mean, 3)),
                'values': list(map(lambda x: str(np.round(x, 3)), roc_auc_fed))
            }

    return roc_auc_scores


def create_content(data_dir: str = 'content',
                   size: int = 4000,
                   seed: int = 15):
    """ Create (and dump) the content needed to generate the interactive visualization.
    """
    fp_members, fm_members = init_data(size, seed)
    score = roc_auc_score(
        y_true=np.concatenate((np.ones_like(fp_members), np.zeros_like(fm_members))),
        y_score=np.concatenate((fp_members, fm_members))
    )

    # create all figures
    ratios = [0.02, 0.2, 0.4, 0.6, 0.8, 1]
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

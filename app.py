import os

import numpy as np

from plotly_web_app.constants import DEFAULT_PORT, RATIOS
from plotly_web_app.data import init_data, split_members_into_n_groups
from plotly_web_app.dashboard import create_dashboard
from plotly_web_app.utils import avg_roc_auc_fed
from plotly_web_app.visualization import (
    build_negative_distribution_figure,
    build_positive_distribution_figure,
    calculate_global_roc_auc,
    format_roc_auc_values,
)

fp_members, fm_members = init_data()
score = calculate_global_roc_auc(fp_members, fm_members)
ratios = list(RATIOS)

def update_fp_fm_dist(ratio_p, ratio_m):
    fp_members_fed = split_members_into_n_groups(fp_members, similarity_ratio=ratio_p)
    fm_members_fed = split_members_into_n_groups(fm_members, similarity_ratio=ratio_m)
    fig_p = build_positive_distribution_figure(fp_members_fed)
    fig_m = build_negative_distribution_figure(fm_members_fed)
    roc_auc_fed, roc_auc_mean, _ = avg_roc_auc_fed(fm_members_fed, fp_members_fed)
    return fig_p, fig_m, format_roc_auc_values(roc_auc_fed), str(np.round(roc_auc_mean, 3))


app = create_dashboard(score=score, ratios=ratios, update_view=update_fp_fm_dist)
server = app.server


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', DEFAULT_PORT)), debug=False)

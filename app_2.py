import os

from plotly_web_app.constants import DEFAULT_PORT
from plotly_web_app.content import load_or_build_precomputed_content
from plotly_web_app.dashboard import create_dashboard

LOAD_GENERATED_DATA = True

if LOAD_GENERATED_DATA is True:
    print('Load generated data.')
    content = load_or_build_precomputed_content()

    ratios = content['ratios']
    content_p = content['content_p']
    content_m = content['content_m']
    roc_auc_scores = content['roc_auc_scores']
    score = content['score']

else:
    print('Generate all possible plots.')
    content = load_or_build_precomputed_content()
    ratios = content['ratios']
    content_p = content['content_p']
    content_m = content['content_m']
    roc_auc_scores = content['roc_auc_scores']
    score = content['score']


def update_fp_fm_dist(ratio_p, ratio_m):
    fig_p = content_p[f"{ratio_p:.2f}"]['fig_p']
    fig_m = content_m[f"{ratio_m:.2f}"]['fig_m']

    print(ratio_p, ratio_m, sep='\t')
    print(roc_auc_scores.keys())

    roc_auc_fed = roc_auc_scores[f"{ratio_p:.2f}_{ratio_m:.2f}"]['values']
    roc_auc_mean = roc_auc_scores[f"{ratio_p:.2f}_{ratio_m:.2f}"]['mean']
    return fig_p, fig_m, roc_auc_fed, roc_auc_mean


app = create_dashboard(score=score, ratios=ratios, update_view=update_fp_fm_dist)
server = app.server


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', DEFAULT_PORT)), debug=False)

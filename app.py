import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
from sklearn.metrics import roc_auc_score

import plotly.figure_factory as ff

from plotly_web_app.data import init_data, split_members_into_n_groups
from plotly_web_app.utils import avg_roc_auc_fed

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

fp_members, fm_members = init_data()
score = roc_auc_score(
    y_true=np.concatenate((np.ones_like(fp_members), np.zeros_like(fm_members))),
    y_score=np.concatenate((fp_members, fm_members))
)

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div([

    # divs levers
    html.Div([
        html.Div([
            dcc.Slider(
                id='fm-slider',
                min=0,
                max=1,
                value=0.3,
                marks={str(i): str(i) for i in np.round(np.linspace(0, 1, 11), 2)},
                step=None
            )], style={'width': '45%', 'display': 'inline-block'}
        ),
        html.Div([
            dcc.Slider(
                id='fp-slider',
                min=0,
                max=1,
                value=0.8,
                marks={str(i): str(i) for i in np.round(np.linspace(0, 1, 11), 2)},
                step=None
            )], style={'width': '45%', 'display': 'inline-block',
                       'float': 'right'}
        )
    ], style={
        'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '10px 5px'
    }),

    # divs with graphs
    html.Div([
        dcc.Graph(
            id='fm_dist'
        )
    ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),

    html.Div([
        dcc.Graph(
            id='fp_dist'
        )
    ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20',
              'float': 'right'}),

    html.Div(id='roc-auc-scores'),
    html.Div(id='roc-auc-mean'),
    html.Div(id='roc-auc', children=f'ROC-AUC {np.round(score, 3)}')
])


@app.callback(
    [dash.dependencies.Output('fp_dist', 'figure'),
     dash.dependencies.Output('fm_dist', 'figure'),
     dash.dependencies.Output('roc-auc-scores', 'children'),
     dash.dependencies.Output('roc-auc-mean', 'children')],
    [dash.dependencies.Input('fp-slider', 'value'),
     dash.dependencies.Input('fm-slider', 'value')])
def update_fp_fm_dist(ratio_p, ratio_m):
    fp_members_fed = split_members_into_n_groups(fp_members, similarity_ratio=ratio_p)
    fm_members_fed = split_members_into_n_groups(fm_members, similarity_ratio=ratio_m)

    labels = [f'pod {i}' for i in range(len(fp_members_fed))]
    fig_p = ff.create_distplot(fp_members_fed, labels)
    fig_m = ff.create_distplot(fm_members_fed, labels)

    roc_auc_fed, roc_auc_mean, _ = avg_roc_auc_fed(fm_members_fed, fp_members_fed)
    roc_auc_fed = list(map(lambda x: str(np.round(x, 3)), roc_auc_fed))
    scores = ', '.join(roc_auc_fed)
    res1 = f"ROC-AUC scores = [{scores}]"
    res2 = f"ROC-AUC mean = {np.round(roc_auc_mean, 3)}"
    return fig_p, fig_m, res1, res2


if __name__ == '__main__':
    server.run(host='0.0.0.0', port=80)
    # app.run_server(port=80)
    # app.run_server(debug=True)
    # app.run(host='0.0.0.0')

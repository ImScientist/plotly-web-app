import os
import pickle
import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
from sklearn.metrics import roc_auc_score

from plotly_web_app.data import init_data
from plotly_web_app.preprocess import generate_figures_and_data_splits, calculate_roc_auc_scores

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

LOAD_GENERATED_DATA = True

if LOAD_GENERATED_DATA is True:
    print('AAA')
    with open(os.path.join('content', 'content.pickle'), 'rb') as f:
        content = pickle.load(f)

    ratios = content['ratios']
    content_p = content['content_p']
    content_m = content['content_m']
    roc_auc_scores = content['roc_auc_scores']
    score = content['score']

else:
    print('BBB')
    fp_members, fm_members = init_data()
    score = roc_auc_score(
        y_true=np.concatenate((np.ones_like(fp_members), np.zeros_like(fm_members))),
        y_score=np.concatenate((fp_members, fm_members))
    )

    ratios = [0.02, 0.2, 0.4, 0.6, 0.8, 1]
    content_p, content_m = generate_figures_and_data_splits(ratios, fp_members, fm_members)
    roc_auc_scores = calculate_roc_auc_scores(ratios, content_p, content_m)

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True
server = app.server

app.layout = html.Div([

    # divs levers
    html.Div([
        html.Div([
            dcc.Slider(
                id='fm-slider',
                min=0,
                max=1,
                value=0.4,
                marks={str(i): str(i) for i in ratios},
                step=None
            )], style={'width': '45%', 'display': 'inline-block'}
        ),
        html.Div([
            dcc.Slider(
                id='fp-slider',
                min=0,
                max=1,
                value=0.8,
                marks={str(i): str(i) for i in ratios},
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
    fig_p = content_p[ratio_p]['fig_p']
    fig_m = content_m[ratio_m]['fig_m']

    roc_auc_fed = roc_auc_scores[f"{ratio_p}_{ratio_m}"]['values']
    roc_auc_mean = roc_auc_scores[f"{ratio_p}_{ratio_m}"]['mean']

    scores = ', '.join(roc_auc_fed)

    res1 = f"ROC-AUC scores = [{scores}]"
    res2 = f"ROC-AUC mean = {roc_auc_mean}"
    return fig_p, fig_m, res1, res2


if __name__ == '__main__':
    server.run(host='0.0.0.0', port=80)
    # app.run_server(port=80)
    # app.run_server(debug=True)
    # app.run(host='0.0.0.0')

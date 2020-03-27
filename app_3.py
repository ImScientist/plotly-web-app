import json
import datetime
from textwrap import dedent as d
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

import os
import pickle
import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
from sklearn.metrics import roc_auc_score

from plotly_web_app.data import init_data
from plotly_web_app.preprocess import generate_figures_and_data_splits, calculate_roc_auc_scores

LOAD_GENERATED_DATA = True

if LOAD_GENERATED_DATA is True:
    print('AAA')
    with open(os.path.join('content_vis', 'content.pickle'), 'rb') as f:
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

df = pd.read_csv(
    ('https://raw.githubusercontent.com/plotly/'
     'datasets/master/1962_2006_walmart_store_openings.csv'),
    parse_dates=[1, 2],
    infer_datetime_format=True
)
future_indices = df['OPENDATE'] > datetime.datetime(year=2050,month=1,day=1)
df.loc[future_indices, 'OPENDATE'] -= datetime.timedelta(days=365.25*100)

app = dash.Dash(__name__)
app.scripts.config.serve_locally = True
app.css.config.serve_locally = True

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

app.layout = html.Div([
    dcc.Graph(
        id='basic-interactions',
        figure={
            'data': [
                {
                    'x': content_p[0.8]['data'][0],
                    'name': 'device 1',
                    'type': 'histogram',
                    'mode': 'lines'
                },
                {
                    'x': content_p[0.8]['data'][1],
                    'name': 'device 2',
                    'type': 'histogram'
                },
                {
                    'x': content_p[0.8]['data'][2],
                    'name': 'device 3',
                    'type': 'histogram'
                },
                {
                    'x': content_p[0.8]['data'][3],
                    'name': 'device 4',
                    'type': 'histogram'
                },
                # {
                #     'x': df['OPENDATE'],
                #     # 'text': df['STRCITY'],
                #     # 'customdata': df['storenum'],
                #     'name': 'Open Date',
                #     'type': 'histogram'
                # },
                # {
                #     'x': df['date_super'],
                #     'text': df['STRCITY'],
                #     'customdata': df['storenum'],
                #     'name': 'Super Date',
                #     'type': 'histogram'
                # }
            ],
            'layout': {}
        }
    ),

    # html.Div(className='row', children=[
    #     html.Div([
    #         dcc.Markdown(d("""
    #             **Hover Data**
    #             Mouse over values in the graph.
    #         """)),
    #         html.Pre(id='hover-data', style=styles['pre'])
    #     ], className='three columns'),
    #
    #     html.Div([
    #         dcc.Markdown(d("""
    #             **Click Data**
    #             Click on points in the graph.
    #         """)),
    #         html.Pre(id='click-data', style=styles['pre']),
    #     ], className='three columns'),
    #
    #     html.Div([
    #         dcc.Markdown(d("""
    #             **Selection Data**
    #             Choose the lasso or rectangle tool in the graph's menu
    #             bar and then select points in the graph.
    #         """)),
    #         html.Pre(id='selected-data', style=styles['pre']),
    #     ], className='three columns'),
    #
    #     html.Div([
    #         dcc.Markdown(d("""
    #             **Zoom and Relayout Data**
    #             Click and drag on the graph to zoom or click on the zoom
    #             buttons in the graph's menu bar.
    #             Clicking on legend items will also fire
    #             this event.
    #         """)),
    #         html.Pre(id='relayout-data', style=styles['pre']),
    #     ], className='three columns')
    # ])
])


# @app.callback(
#     Output('hover-data', 'children'),
#     [Input('basic-interactions', 'hoverData')])
# def display_hover_data(hoverData):
#     return json.dumps(hoverData, indent=2)


# @app.callback(
#     Output('click-data', 'children'),
#     [Input('basic-interactions', 'clickData')])
# def display_click_data(clickData):
#     return json.dumps(clickData, indent=2)


# @app.callback(
#     Output('selected-data', 'children'),
#     [Input('basic-interactions', 'selectedData')])
# def display_selected_data(selectedData):
#     return json.dumps(selectedData, indent=2)


# @app.callback(
#     Output('relayout-data', 'children'),
#     [Input('basic-interactions', 'relayoutData')])
# def display_selected_data(relayoutData):
#     return json.dumps(relayoutData, indent=2)


if __name__ == '__main__':
    app.run_server(debug=True)

import os
from dash import Dash, Input, Output, dcc, html
import plotly.graph_objects as go

from plotly_web_app.constants import DEFAULT_PORT, EXTERNAL_STYLESHEETS
from plotly_web_app.content import load_or_build_precomputed_content

content = load_or_build_precomputed_content()
ratios = content['ratios']
content_p = content['content_p']

app = Dash(__name__, external_stylesheets=EXTERNAL_STYLESHEETS)
server = app.server

app.layout = html.Div([
    html.H3('Positive class pod histogram explorer'),
    dcc.Dropdown(
        id='ratio-selector',
        options=[{'label': f'{ratio:g}', 'value': ratio} for ratio in ratios],
        value=0.8,
        clearable=False,
        style={'maxWidth': '320px'}
    ),
    dcc.Graph(id='basic-interactions')
])


@app.callback(Output('basic-interactions', 'figure'), Input('ratio-selector', 'value'))
def display_histograms(ratio):
    figure = go.Figure()
    for index, pod_data in enumerate(content_p[ratio]['data'], start=1):
        figure.add_histogram(
            x=pod_data,
            name=f'pod {index}',
            opacity=0.65,
            histnorm='probability density',
        )

    figure.update_layout(
        barmode='overlay',
        title=f'Positive class pod distributions for ratio {ratio:g}',
        xaxis_title='Score',
        yaxis_title='Density',
    )
    return figure


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', DEFAULT_PORT)), debug=False)

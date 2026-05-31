from __future__ import annotations

from collections.abc import Callable, Sequence

import numpy as np
from dash import Dash, Input, Output, dcc, html

from .constants import EXTERNAL_STYLESHEETS


UpdateView = Callable[[float, float], tuple[object, object, Sequence[str], str | float]]


def create_dashboard(score: float, ratios: Sequence[float], update_view: UpdateView) -> Dash:
    app = Dash(__name__, external_stylesheets=EXTERNAL_STYLESHEETS)
    server = app.server

    app.layout = html.Div(
        [
            html.Div(
                [
                    html.Div(
                        [
                            dcc.Slider(
                                id="fm-slider",
                                min=min(ratios),
                                max=max(ratios),
                                value=0.4,
                                marks={ratio: f"{ratio:g}" for ratio in ratios},
                                step=None,
                            )
                        ],
                        style={"width": "45%", "display": "inline-block"},
                    ),
                    html.Div(
                        [
                            dcc.Slider(
                                id="fp-slider",
                                min=min(ratios),
                                max=max(ratios),
                                value=0.8,
                                marks={ratio: f"{ratio:g}" for ratio in ratios},
                                step=None,
                            )
                        ],
                        style={"width": "45%", "display": "inline-block", "float": "right"},
                    ),
                ],
                style={
                    "borderBottom": "thin lightgrey solid",
                    "backgroundColor": "rgb(250, 250, 250)",
                    "padding": "10px 5px",
                },
            ),
            html.Div(
                [dcc.Graph(id="fm_dist")],
                style={"width": "49%", "display": "inline-block", "padding": "0 20"},
            ),
            html.Div(
                [dcc.Graph(id="fp_dist")],
                style={"width": "49%", "display": "inline-block", "padding": "0 20", "float": "right"},
            ),
            html.Div(id="roc-auc-scores"),
            html.Div(id="roc-auc-mean"),
            html.Div(id="roc-auc", children=f"ROC-AUC {np.round(score, 3)}"),
        ]
    )

    @app.callback(
        Output("fp_dist", "figure"),
        Output("fm_dist", "figure"),
        Output("roc-auc-scores", "children"),
        Output("roc-auc-mean", "children"),
        Input("fp-slider", "value"),
        Input("fm-slider", "value"),
    )
    def update_figures(ratio_p: float, ratio_m: float):
        positive_figure, negative_figure, roc_auc_values, roc_auc_mean = update_view(ratio_p, ratio_m)
        scores = ", ".join(roc_auc_values)
        return (
            positive_figure,
            negative_figure,
            f"ROC-AUC scores = [{scores}]",
            f"ROC-AUC mean = {roc_auc_mean}",
        )

    app.server = server
    return app


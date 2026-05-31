from __future__ import annotations

from collections.abc import Sequence

import numpy as np
import plotly.express as px
import plotly.figure_factory as ff
from sklearn.metrics import roc_auc_score


def calculate_global_roc_auc(
    positive_members: Sequence[float],
    negative_members: Sequence[float],
) -> float:
    positive_members = np.asarray(positive_members)
    negative_members = np.asarray(negative_members)
    return roc_auc_score(
        y_true=np.concatenate((np.ones_like(positive_members), np.zeros_like(negative_members))),
        y_score=np.concatenate((positive_members, negative_members)),
    )


def build_distribution_figure(member_groups: Sequence[Sequence[float]], title: str, color_scale: Sequence[str]):
    labels = [f"pod {index}" for index in range(len(member_groups))]
    figure = ff.create_distplot(
        list(member_groups),
        labels,
        show_hist=False,
        colors=list(color_scale),
    )
    figure.update_traces(opacity=0.8)
    figure.update_layout(
        title_text=title,
        xaxis_title_text="Score",
        bargap=0.85,
        bargroupgap=0,
    )
    return figure


def build_positive_distribution_figure(member_groups: Sequence[Sequence[float]]):
    return build_distribution_figure(
        member_groups,
        title="Scores distribution (positive class)",
        color_scale=px.colors.sequential.Sunsetdark[2:],
    )


def build_negative_distribution_figure(member_groups: Sequence[Sequence[float]]):
    return build_distribution_figure(
        member_groups,
        title="Scores distribution (negative class)",
        color_scale=px.colors.sequential.Teal[2:],
    )


def format_roc_auc_values(values: Sequence[float]) -> list[str]:
    return [str(np.round(value, 3)) for value in values]


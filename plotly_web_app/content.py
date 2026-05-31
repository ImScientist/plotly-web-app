from __future__ import annotations

import json
import pickle
from pathlib import Path
from typing import Any

from .constants import RATIOS
from .data import init_data, split_members_into_n_groups
from .preprocess import calculate_roc_auc_scores, generate_figures_and_data_splits
from .visualization import calculate_global_roc_auc

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CONTENT_DIR = PROJECT_ROOT / "content"
DEFAULT_CONTENT_FILE = DEFAULT_CONTENT_DIR / "content.pickle"
STATIC_APP_DIR = PROJECT_ROOT / "static_app"
STATIC_DATA_DIR = STATIC_APP_DIR / "data"
STATIC_CONTENT_FILE = STATIC_DATA_DIR / "content.json"


ContentDict = dict[str, Any]


def ratio_to_key(ratio: float) -> str:
    return f"{ratio:.2f}"


def build_precomputed_content(size: int = 4000, seed: int = 15) -> ContentDict:
    fp_members, fm_members = init_data(size=size, seed=seed)
    ratios = list(RATIOS)
    content_p, content_m = generate_figures_and_data_splits(ratios, fp_members, fm_members)
    return {
        "ratios": ratios,
        "content_p": content_p,
        "content_m": content_m,
        "roc_auc_scores": calculate_roc_auc_scores(ratios, content_p, content_m),
        "score": calculate_global_roc_auc(fp_members, fm_members),
    }


def load_precomputed_content(content_file: Path | None = None) -> ContentDict:
    content_file = content_file or DEFAULT_CONTENT_FILE
    with content_file.open("rb") as file_handle:
        return pickle.load(file_handle)


def load_or_build_precomputed_content(content_file: Path | None = None) -> ContentDict:
    content_file = content_file or DEFAULT_CONTENT_FILE
    if content_file.exists():
        return load_precomputed_content(content_file)
    return build_precomputed_content()


def save_precomputed_content(content: ContentDict, content_file: Path | None = None) -> Path:
    content_file = content_file or DEFAULT_CONTENT_FILE
    content_file.parent.mkdir(parents=True, exist_ok=True)
    with content_file.open("wb") as file_handle:
        pickle.dump(content, file_handle)
    return content_file


def build_static_content(size: int = 4000, seed: int = 15) -> ContentDict:
    fp_members, fm_members = init_data(size=size, seed=seed)
    ratio_keys = [ratio_to_key(ratio) for ratio in RATIOS]

    content_p = {
        ratio_key: {"data": split_members_into_n_groups(fp_members, similarity_ratio=ratio)}
        for ratio, ratio_key in zip(RATIOS, ratio_keys)
    }
    content_m = {
        ratio_key: {"data": split_members_into_n_groups(fm_members, similarity_ratio=ratio)}
        for ratio, ratio_key in zip(RATIOS, ratio_keys)
    }

    return {
        "ratios": ratio_keys,
        "defaults": {
            "positive_ratio": ratio_to_key(0.8),
            "negative_ratio": ratio_to_key(0.4),
        },
        "positive_groups": {
            ratio_key: {
                "data": [list(map(float, group)) for group in content_p[ratio_key]["data"]]
            }
            for ratio_key in ratio_keys
        },
        "negative_groups": {
            ratio_key: {
                "data": [list(map(float, group)) for group in content_m[ratio_key]["data"]]
            }
            for ratio_key in ratio_keys
        },
        "roc_auc_scores": calculate_roc_auc_scores(list(RATIOS), content_p, content_m),
        "global_score": round(float(calculate_global_roc_auc(fp_members, fm_members)), 3),
        "metadata": {
            "seed": seed,
            "size": size,
            "pod_count": len(content_p[ratio_keys[0]]["data"]),
        },
    }


def save_static_content(content: ContentDict, content_file: Path | None = None) -> Path:
    content_file = content_file or STATIC_CONTENT_FILE
    content_file.parent.mkdir(parents=True, exist_ok=True)
    with content_file.open("w", encoding="utf-8") as file_handle:
        json.dump(content, file_handle, indent=2)
    return content_file


def export_static_content(
    content_file: Path | None = None,
    size: int = 4000,
    seed: int = 15,
) -> Path:
    return save_static_content(
        build_static_content(size=size, seed=seed),
        content_file=content_file,
    )



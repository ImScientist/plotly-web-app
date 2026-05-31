from __future__ import annotations

import pickle
from pathlib import Path
from typing import Any

from .constants import RATIOS
from .data import init_data
from .preprocess import calculate_roc_auc_scores, generate_figures_and_data_splits
from .visualization import calculate_global_roc_auc

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CONTENT_DIR = PROJECT_ROOT / "content"
DEFAULT_CONTENT_FILE = DEFAULT_CONTENT_DIR / "content.pickle"


ContentDict = dict[str, Any]


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


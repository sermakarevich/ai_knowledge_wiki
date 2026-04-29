"""Sample data: a target task plus a seeded L3 prior-wisdom store.

In the real ML-Master 2.0, L3 is warmed up from 407 Kaggle competitions via
the P2 operator. Here we seed 3 plausible wisdom entries so Context Prefetch
has something to retrieve from.
"""

from __future__ import annotations

import os

from langchain_ollama import OllamaEmbeddings

from src.state import WisdomEntry

EMBED_MODEL_NAME = os.environ.get("OLLAMA_EMBED_MODEL", "nomic-embed-text")


SAMPLE_TASK = (
    "Build a classifier for a small tabular dataset of credit applications "
    "with ~10k rows, 20 numeric + categorical features, and a binary default/no-default label. "
    "Class imbalance is roughly 1:9. The evaluation metric is ROC-AUC on a held-out split."
)


SEED_WISDOM: list[dict] = [
    {
        "descriptor": "small tabular classification | gradient boosting baseline",
        "wisdom_text": (
            "DATA SUMMARY: tabular, low-rank, mixed numeric/categorical with class imbalance. "
            "MODEL SUMMARY: start with gradient-boosted trees (lightgbm/xgboost) with early stopping, "
            "class_weight='balanced', 5-fold stratified CV; avoid deep nets on <50k rows."
        ),
    },
    {
        "descriptor": "image classification small dataset | transfer learning",
        "wisdom_text": (
            "DATA SUMMARY: small labelled image corpus, high inter-class similarity. "
            "MODEL SUMMARY: fine-tune a pretrained CNN backbone with aggressive augmentation; "
            "training from scratch underperforms below 20k images."
        ),
    },
    {
        "descriptor": "imbalanced binary classification | threshold tuning and calibration",
        "wisdom_text": (
            "DATA SUMMARY: binary target with ~10% positive rate, metric is ranking-based. "
            "MODEL SUMMARY: prioritise ROC-AUC via probability calibration (isotonic or Platt), "
            "consider SMOTE only when trees underfit minority; feature interactions often matter more than resampling."
        ),
    },
]


def build_prior_wisdom_store() -> list[WisdomEntry]:
    """Embed each seed entry once so Context Prefetch can cosine-compare."""
    embedder = OllamaEmbeddings(model=EMBED_MODEL_NAME)
    store: list[WisdomEntry] = []
    for entry in SEED_WISDOM:
        vec = embedder.embed_query(entry["descriptor"])
        store.append(
            {
                "descriptor": entry["descriptor"],
                "wisdom_text": entry["wisdom_text"],
                "embedding": vec,
            }
        )
    return store

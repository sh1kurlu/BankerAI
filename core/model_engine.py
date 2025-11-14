"""Core recommendation engine (item-based CF)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Any

import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


@dataclass
class ModelArtifacts:
    R: np.ndarray
    user_to_idx: Dict[str, int]
    idx_to_user: Dict[int, str]
    item_to_idx: Dict[str, int]
    idx_to_item: Dict[int, str]
    item_sim: np.ndarray
    item_meta: Dict[str, Dict[str, Any]]


class RecommenderEngine:
    """Item-based collaborative filtering engine."""

    def __init__(self, artifacts: ModelArtifacts):
        self.artifacts = artifacts

    @classmethod
    def from_dataframe(cls, df: pd.DataFrame, R: np.ndarray, user_to_idx, idx_to_user, item_to_idx, idx_to_item):
        item_norms = np.linalg.norm(R, axis=0, keepdims=True) + 1e-9
        R_norm = R / item_norms
        item_sim = cosine_similarity(R_norm.T)

        meta_df = df.groupby("item_id").agg({
            "item_name": "first",
            "category": "first",
        }).reset_index()
        meta_df["item_id"] = meta_df["item_id"].astype(str)
        item_meta = meta_df.set_index("item_id").to_dict(orient="index")

        arts = ModelArtifacts(
            R=R,
            user_to_idx=user_to_idx,
            idx_to_user=idx_to_user,
            item_to_idx=item_to_idx,
            idx_to_item=idx_to_item,
            item_sim=item_sim,
            item_meta=item_meta,
        )
        return cls(arts)

    def _user_history_indices(self, user_id: str):
        a = self.artifacts
        if user_id not in a.user_to_idx:
            return []
        u = a.user_to_idx[user_id]
        interacted = np.where(a.R[u] > 0)[0]
        return interacted.tolist()

    def recommend(self, user_id: str, k: int = 5) -> List[Dict[str, Any]]:
        a = self.artifacts
        interacted = self._user_history_indices(user_id)

        if not interacted:
            # Use popularity-based recommendations with smoothing
            item_scores = a.R.sum(axis=0)
            # Add small constant to avoid zero scores for cold start
            item_scores = item_scores + 0.1
        else:
            # Combine similarity scores with popularity for better recommendations
            sim_scores = a.item_sim[interacted].sum(axis=0)
            
            # Add popularity component (30% weight) to avoid zero scores
            popularity_scores = a.R.sum(axis=0)
            popularity_scores = (popularity_scores - popularity_scores.min()) / (popularity_scores.max() - popularity_scores.min() + 1e-9)
            
            # Blend similarity and popularity
            item_scores = 0.7 * sim_scores + 0.3 * popularity_scores
            
            # Set interacted items to minimum score instead of extreme negative
            min_score = item_scores.min() - 0.1
            item_scores[interacted] = min_score

        # Filter out interacted items and get top k valid recommendations
        valid_indices = [idx for idx in range(len(item_scores)) if idx not in interacted]
        if not valid_indices:
            # If all items are interacted, return empty list
            return []
            
        valid_scores = item_scores[valid_indices]
        top_valid_indices = np.argsort(-valid_scores)[:k]
        top_indices = [valid_indices[idx] for idx in top_valid_indices]
        
        recs: List[Dict[str, Any]] = []

        for idx in top_indices:
            item_id = a.idx_to_item[idx]
            meta = a.item_meta.get(item_id, {})
            raw_score = float(item_scores[idx])
            
            # Normalize score to 0-100 range for better UX
            normalized_score = max(0, min(100, (raw_score + 1) * 50))
            
            recs.append({
                "item_id": item_id,
                "item_name": meta.get("item_name", f"Item {item_id}"),
                "category": meta.get("category", "unknown"),
                "score": normalized_score,
                "raw_score": raw_score,
            })

        return recs

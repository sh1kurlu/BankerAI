"""Data loading and preprocessing utilities for CustomerAI."""

from __future__ import annotations

from typing import Dict, Tuple
import numpy as np
import pandas as pd


EVENT_WEIGHTS = {
    "view": 1.0,
    "cart": 2.0,
    "purchase": 3.0,
}


def load_events(path: str) -> pd.DataFrame:
    """Load raw events CSV with enhanced data processing.

    Expected columns:
        user_id, item_id, event_type, timestamp, item_name, category
    Optional columns for enhanced recommendations:
        cooking_preference, purchase_history, user_preferences, rating
    """
    df = pd.read_csv(path)
    df = df.dropna(subset=["user_id", "item_id"])
    df["user_id"] = df["user_id"].astype(str)
    df["item_id"] = df["item_id"].astype(str)
    df["event_type"] = df["event_type"].str.lower()
    
    # Process optional columns for enhanced recommendations
    if "cooking_preference" in df.columns:
        df["cooking_preference"] = df["cooking_preference"].fillna("none")
    
    if "rating" in df.columns:
        df["rating"] = pd.to_numeric(df["rating"], errors="coerce").fillna(3.0)
        # Use rating as additional weight factor
        df["rating_weight"] = df["rating"] / 5.0
    else:
        df["rating_weight"] = 1.0
        
    return df


def build_interaction_matrix(df: pd.DataFrame) -> Tuple[np.ndarray, Dict[str, int], Dict[int, str], Dict[str, int], Dict[int, str]]:
    """Build a user-item interaction matrix with enhanced implicit feedback weights."""
    user_ids = df["user_id"].unique()
    item_ids = df["item_id"].unique()

    user_to_idx = {u: i for i, u in enumerate(user_ids)}
    idx_to_user = {i: u for u, i in user_to_idx.items()}
    item_to_idx = {i: j for j, i in enumerate(item_ids)}
    idx_to_item = {j: i for i, j in item_to_idx.items()}

    num_users = len(user_ids)
    num_items = len(item_ids)

    R = np.zeros((num_users, num_items), dtype=np.float32)

    for _, row in df.iterrows():
        u = user_to_idx[row["user_id"]]
        it = item_to_idx[row["item_id"]]
        w = EVENT_WEIGHTS.get(row["event_type"], 1.0)
        
        # Apply rating weight if available
        rating_weight = row.get("rating_weight", 1.0)
        w *= rating_weight
        
        # Add time decay factor (more recent events get higher weight)
        if "timestamp" in row and pd.notna(row["timestamp"]):
            try:
                timestamp = pd.to_datetime(row["timestamp"])
                days_ago = (pd.Timestamp.now() - timestamp).days
                time_decay = max(0.1, 1.0 - (days_ago / 365))  # Decay over a year
                w *= time_decay
            except:
                pass  # If timestamp parsing fails, use original weight
        
        R[u, it] += w

    return R, user_to_idx, idx_to_user, item_to_idx, idx_to_item

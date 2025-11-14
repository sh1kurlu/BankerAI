"""Simple feedback generation (no external API)."""

from __future__ import annotations

from typing import Dict, Any
import pandas as pd


class FeedbackEngine:
    def __init__(self, events_df: pd.DataFrame):
        self.df = events_df.copy()
        self.df["user_id"] = self.df["user_id"].astype(str)

    def generate(self, user_id: str, item: Dict[str, Any]) -> str:
        category = item.get("category", "this category")
        name = item.get("item_name", "this item")

        user_df = self.df[self.df["user_id"] == user_id]
        if user_df.empty:
            return f"We think {name} could be a good starting point for you in {category}."

        same_cat = user_df[user_df["category"] == category]
        if not same_cat.empty:
            past_name = same_cat.iloc[0]["item_name"]
            return (
                f"Since you interacted with '{past_name}' in {category}, "
                f"'{name}' is a natural next suggestion for you."
            )

        return (
            f"Based on your previous behaviour, users like you often enjoy {category} items "
            f"such as '{name}'."
        )

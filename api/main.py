from __future__ import annotations

from typing import List, Dict, Any
import pandas as pd
import numpy as np
from datetime import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from customerai.config.settings import settings
from customerai.core.preprocessor import load_events, build_interaction_matrix
from customerai.core.model_engine import RecommenderEngine
from customerai.core.feedback_engine import FeedbackEngine


app = FastAPI(
    title="CustomerAI API",
    version="0.1.0-fastapi",
    description="Customer behaviour recommendation + feedback API.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load data and initialise engines on startup
events_df = load_events(settings.data_path)
R, user_to_idx, idx_to_user, item_to_idx, idx_to_item = build_interaction_matrix(events_df)
engine = RecommenderEngine.from_dataframe(events_df, R, user_to_idx, idx_to_user, item_to_idx, idx_to_item)
feedback_engine = FeedbackEngine(events_df)


class RecommendRequest(BaseModel):
    user_id: str
    k: int = 5


class Recommendation(BaseModel):
    item_id: str
    item_name: str
    category: str
    score: float
    feedback: str


class RecommendResponse(BaseModel):
    user_id: str
    recommendations: List[Recommendation]


class VisualizationData(BaseModel):
    chart_type: str
    data: Dict[str, Any]
    title: str
    description: str


@app.get("/api/health")
async def health():
    return {"status": "ok"}


@app.post("/api/recommend", response_model=RecommendResponse)
async def recommend(req: RecommendRequest):
    user_id = req.user_id.strip()
    k = req.k

    recs_raw = engine.recommend(user_id, k=k)
    enriched = []
    for r in recs_raw:
        fb = feedback_engine.generate(user_id, r)
        enriched.append(Recommendation(**{**r, "feedback": fb}))

    return RecommendResponse(user_id=user_id, recommendations=enriched)


@app.get("/api/visualization/score-distribution", response_model=VisualizationData)
async def get_score_distribution():
    """Get recommendation score distribution data for visualization."""
    # Get all recommendations for all users to analyze score patterns
    all_scores = []
    categories = []
    
    for user_id in events_df["user_id"].unique()[:10]:  # Sample 10 users for performance
        recs = engine.recommend(user_id, k=20)
        for rec in recs:
            all_scores.append(rec["score"])
            categories.append(rec["category"])
    
    # Create score distribution bins
    score_bins = list(range(0, 101, 10))
    score_counts = pd.cut(all_scores, bins=score_bins).value_counts().sort_index()
    
    return VisualizationData(
        chart_type="histogram",
        data={
            "labels": [f"{int(interval.left)}-{int(interval.right)}" for interval in score_counts.index],
            "values": score_counts.tolist(),
            "categories": list(set(categories))
        },
        title="Recommendation Score Distribution",
        description="Distribution of recommendation scores across all users and items"
    )


@app.get("/api/visualization/category-distribution", response_model=VisualizationData)
async def get_category_distribution():
    """Get category distribution data for visualization."""
    category_counts = events_df["category"].value_counts().to_dict()
    
    return VisualizationData(
        chart_type="pie",
        data={
            "labels": list(category_counts.keys()),
            "values": list(category_counts.values())
        },
        title="Item Category Distribution",
        description="Distribution of items across different categories"
    )


@app.get("/api/visualization/user-preferences/{user_id}", response_model=VisualizationData)
async def get_user_preferences(user_id: str):
    """Get user preference patterns for visualization."""
    user_events = events_df[events_df["user_id"] == user_id]
    
    if user_events.empty:
        return VisualizationData(
            chart_type="bar",
            data={"labels": [], "values": []},
            title=f"User {user_id} Preferences",
            description="No data available for this user"
        )
    
    # Category preferences
    category_activity = user_events["category"].value_counts().to_dict()
    
    # Event type distribution
    event_type_counts = user_events["event_type"].value_counts().to_dict()
    
    # Timeline data
    if "timestamp" in user_events.columns:
        user_events["date"] = pd.to_datetime(user_events["timestamp"]).dt.date
        timeline = user_events.groupby("date").size().to_dict()
        timeline_data = {
            "dates": [str(date) for date in timeline.keys()],
            "counts": list(timeline.values())
        }
    else:
        timeline_data = {"dates": [], "counts": []}
    
    return VisualizationData(
        chart_type="multi",
        data={
            "category_preferences": {
                "labels": list(category_activity.keys()),
                "values": list(category_activity.values())
            },
            "event_types": {
                "labels": list(event_type_counts.keys()),
                "values": list(event_type_counts.values())
            },
            "timeline": timeline_data
        },
        title=f"User {user_id} Activity Patterns",
        description="User interaction patterns over time and across categories"
    )


@app.get("/api/visualization/recommendation-strength", response_model=VisualizationData)
async def get_recommendation_strength():
    """Get recommendation strength analysis for visualization."""
    user_counts = []
    avg_scores = []
    user_ids_sample = events_df["user_id"].unique()[:20]
    
    for user_id in user_ids_sample:
        recs = engine.recommend(user_id, k=10)
        if recs:
            scores = [rec["score"] for rec in recs]
            user_counts.append(len(recs))
            avg_scores.append(np.mean(scores))
        else:
            user_counts.append(0)
            avg_scores.append(0)
    
    return VisualizationData(
        chart_type="scatter",
        data={
            "users": list(user_ids_sample),
            "recommendation_counts": user_counts,
            "average_scores": avg_scores
        },
        title="Recommendation Strength Analysis",
        description="Relationship between number of recommendations and average scores by user"
    )

from __future__ import annotations

from typing import List, Dict, Any, Optional
import pandas as pd
import numpy as np
from datetime import datetime
import asyncio
from collections import defaultdict

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from config.settings import settings
from core.preprocessor import load_events, build_interaction_matrix
from core.model_engine import RecommenderEngine
from core.feedback_engine import FeedbackEngine
from core.ai_behavioral_engine import AIBehavioralEngine


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
ai_behavioral_engine = AIBehavioralEngine(events_df)


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


class AIBehavioralAnalysisRequest(BaseModel):
    user_id: str
    k: int = 5


class AIBehavioralAnalysisResponse(BaseModel):
    user_id: str
    recommendations: List[Dict[str, Any]]
    user_summary: Dict[str, Any]
    predicted_actions: List[Dict[str, Any]]
    persona: Dict[str, Any]
    analytics_data: Dict[str, Any]


class TrackEventRequest(BaseModel):
    user_id: str
    item_id: Optional[str] = None
    event_type: str
    timestamp: str
    time_spent_seconds: Optional[float] = None
    item_name: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    brand: Optional[str] = None
    quantity: Optional[int] = None
    search_query: Optional[str] = None
    results_count: Optional[int] = None
    recommendation_action: Optional[str] = None
    score: Optional[float] = None
    element: Optional[str] = None
    position: Optional[str] = None
    page_url: str
    referrer: Optional[str] = None
    session_id: str
    user_agent: Optional[str] = None
    screen_resolution: Optional[str] = None
    viewport: Optional[str] = None


class TrackEventsBatchRequest(BaseModel):
    events: List[Dict[str, Any]]


class RealtimeInsightsResponse(BaseModel):
    user_id: str
    session_events: int
    last_activity: str
    recent_categories: List[str]
    current_interest: str
    recommendations_ready: bool
    insights_timestamp: str


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


@app.post("/api/ai-behavioral-analysis", response_model=AIBehavioralAnalysisResponse)
async def ai_behavioral_analysis(req: AIBehavioralAnalysisRequest):
    """Get comprehensive AI behavioral analysis for a user."""
    user_id = req.user_id.strip()
    k = req.k
    
    # Generate comprehensive AI analysis
    ai_output = ai_behavioral_engine.get_comprehensive_ai_output(user_id, k)
    
    # Convert numpy types to Python native types for JSON serialization
    import json
    json_str = json.dumps(ai_output, default=str)
    ai_output_clean = json.loads(json_str)
    
    return AIBehavioralAnalysisResponse(**ai_output_clean)


# Real-time tracking endpoints
@app.post("/api/track_event")
async def track_event(event: TrackEventRequest):
    """Track a single user event in real-time."""
    try:
        # Convert to DataFrame row and append to events
        event_dict = event.dict()
        
        # Add to global events dataframe
        global events_df, engine, feedback_engine
        new_row = pd.DataFrame([event_dict])
        events_df = pd.concat([events_df, new_row], ignore_index=True)
        
        # Update engines with new data
        ai_behavioral_engine.events_df = events_df.copy()
        ai_behavioral_engine.events_df['timestamp'] = pd.to_datetime(ai_behavioral_engine.events_df['timestamp'], format='mixed', errors='coerce')
        
        # Rebuild user and item profiles periodically (every 10 events to avoid performance issues)
        # For single events, we'll update incrementally
        if len(events_df) % 10 == 0:
            ai_behavioral_engine.user_profiles = ai_behavioral_engine._build_user_profiles()
            ai_behavioral_engine.item_profiles = ai_behavioral_engine._build_item_profiles()
            
            # Rebuild main recommender engine with updated data
            try:
                R, user_to_idx, idx_to_user, item_to_idx, idx_to_item = build_interaction_matrix(events_df)
                engine = RecommenderEngine.from_dataframe(events_df, R, user_to_idx, idx_to_user, item_to_idx, idx_to_item)
                feedback_engine = FeedbackEngine(events_df)
            except Exception as rebuild_error:
                print(f"Warning: Could not rebuild recommender engine: {rebuild_error}")
        
        return {"status": "success", "message": "Event tracked successfully", "total_events": len(events_df)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error tracking event: {str(e)}")


@app.post("/api/track_events_batch")
async def track_events_batch(batch: TrackEventsBatchRequest):
    """Track multiple user events in batch for better performance."""
    try:
        global events_df, engine, feedback_engine
        
        # Convert batch events to DataFrame
        if batch.events:
            new_rows = pd.DataFrame(batch.events)
            events_df = pd.concat([events_df, new_rows], ignore_index=True)
            
            # Update engines with new data
            ai_behavioral_engine.events_df = events_df.copy()
            ai_behavioral_engine.events_df['timestamp'] = pd.to_datetime(ai_behavioral_engine.events_df['timestamp'], format='mixed', errors='coerce')
            
            # Rebuild profiles if we have enough new data
            if len(batch.events) > 5:
                ai_behavioral_engine.user_profiles = ai_behavioral_engine._build_user_profiles()
                ai_behavioral_engine.item_profiles = ai_behavioral_engine._build_item_profiles()
                
                # Rebuild main recommender engine with updated data
                try:
                    R, user_to_idx, idx_to_user, item_to_idx, idx_to_item = build_interaction_matrix(events_df)
                    engine = RecommenderEngine.from_dataframe(events_df, R, user_to_idx, idx_to_user, item_to_idx, idx_to_item)
                    feedback_engine = FeedbackEngine(events_df)
                except Exception as rebuild_error:
                    print(f"Warning: Could not rebuild recommender engine: {rebuild_error}")
        
        return {
            "status": "success", 
            "message": f"{len(batch.events)} events tracked successfully",
            "total_events": len(events_df)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error tracking batch events: {str(e)}")


@app.get("/api/realtime-insights/{user_id}", response_model=RealtimeInsightsResponse)
async def get_realtime_insights(user_id: str):
    """Get real-time insights for a user based on recent activity."""
    try:
        user_events = events_df[events_df["user_id"] == user_id].copy()
        
        if user_events.empty:
            return RealtimeInsightsResponse(
                user_id=user_id,
                session_events=0,
                last_activity="No activity found",
                recent_categories=[],
                current_interest="Unknown",
                recommendations_ready=False,
                insights_timestamp=datetime.now().isoformat()
            )
        
        # Get recent activity (last 30 minutes)
        recent_cutoff = datetime.now() - pd.Timedelta(minutes=30)
        user_events['timestamp'] = pd.to_datetime(user_events['timestamp'])
        recent_events = user_events[user_events['timestamp'] > recent_cutoff]
        
        # Analyze recent categories
        recent_categories = recent_events['category'].value_counts().head(3).index.tolist() if 'category' in recent_events.columns else []
        
        # Determine current interest
        current_interest = "Browsing" if len(recent_events) < 3 else "Engaged"
        if len(recent_events) > 10:
            current_interest = "Highly Active"
        
        # Check if we have enough data for recommendations
        recommendations_ready = len(user_events) >= 5
        
        # Get last activity time
        if not recent_events.empty:
            last_activity = recent_events['timestamp'].max().strftime("%Y-%m-%d %H:%M:%S")
        else:
            last_activity = user_events['timestamp'].max().strftime("%Y-%m-%d %H:%M:%S") if not user_events.empty else "Unknown"
        
        return RealtimeInsightsResponse(
            user_id=user_id,
            session_events=len(recent_events),
            last_activity=last_activity,
            recent_categories=recent_categories,
            current_interest=current_interest,
            recommendations_ready=recommendations_ready,
            insights_timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting realtime insights: {str(e)}")


@app.get("/api/user/{user_id}/recent-activity")
async def get_user_recent_activity(user_id: str, limit: int = 10):
    """Get recent activity for a specific user."""
    try:
        user_events = events_df[events_df["user_id"] == user_id].copy()
        
        if user_events.empty:
            return {"user_id": user_id, "recent_activity": []}
        
        # Sort by timestamp (newest first)
        user_events['timestamp'] = pd.to_datetime(user_events['timestamp'])
        recent_events = user_events.sort_values('timestamp', ascending=False).head(limit)
        
        # Convert to list of dicts
        activity_list = recent_events.to_dict('records')
        
        return {
            "user_id": user_id,
            "recent_activity": activity_list,
            "total_events": len(user_events)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting user activity: {str(e)}")

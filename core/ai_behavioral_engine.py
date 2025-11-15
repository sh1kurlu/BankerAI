"""Advanced AI Behavioral Analysis Engine for Customer Intelligence."""

from __future__ import annotations

import json
import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from collections import Counter, defaultdict


@dataclass
class AIRecommendation:
    """Enhanced recommendation with behavioral explanations."""
    item_id: str
    item_name: str
    category: str
    score: float
    reason: str
    behavioral_justification: str
    similarity_score: float
    collaborative_reasoning: str
    confidence: str
    trend_alignment: str


@dataclass
class UserPersona:
    """User behavioral persona with detailed analysis."""
    persona_type: str
    description: str
    key_characteristics: List[str]
    purchasing_behavior: str
    category_preferences: List[str]
    activity_patterns: Dict[str, Any]
    risk_factors: List[str]
    opportunities: List[str]


@dataclass
class PredictedAction:
    """Predicted next user actions with confidence."""
    action_type: str
    probability: float
    reasoning: str
    timeframe: str
    influencing_factors: List[str]
    confidence_level: str


@dataclass
class UserBehaviorSummary:
    """Comprehensive user behavior analysis."""
    user_id: str
    top_categories: List[Dict[str, Any]]
    most_active_hours: List[int]
    recent_trends: List[str]
    purchase_tendencies: Dict[str, Any]
    engagement_level: str
    loyalty_indicators: Dict[str, Any]
    seasonal_patterns: List[str]


@dataclass
class DashboardAnalytics:
    """Visualization-ready analytics data."""
    category_distribution: Dict[str, Any]
    hourly_activity_heatmap: Dict[str, Any]
    interaction_trends: Dict[str, Any]
    similarity_breakdown: Dict[str, Any]
    purchase_funnel: Dict[str, Any]
    user_interest_growth: Dict[str, Any]
    behavioral_segments: Dict[str, Any]
    predictive_metrics: Dict[str, Any]


class AIBehavioralEngine:
    """Advanced AI engine for customer behavior analysis and intelligence."""
    
    def __init__(self, events_df: pd.DataFrame):
        self.events_df = events_df.copy()
        self.events_df['timestamp'] = pd.to_datetime(self.events_df['timestamp'])
        self.user_profiles = self._build_user_profiles()
        self.item_profiles = self._build_item_profiles()
        self.behavioral_patterns = self._analyze_behavioral_patterns()
        
    def _build_user_profiles(self) -> Dict[str, Dict[str, Any]]:
        """Build comprehensive user behavioral profiles."""
        profiles = {}
        
        for user_id in self.events_df['user_id'].unique():
            user_data = self.events_df[self.events_df['user_id'] == user_id]
            
            # Category preferences
            category_counts = user_data['category'].value_counts()
            category_preferences = [
                {"category": cat, "count": count, "percentage": count/len(user_data)*100}
                for cat, count in category_counts.head(5).items()
            ]
            
            # Event type distribution
            event_types = user_data['event_type'].value_counts().to_dict()
            
            # Temporal patterns
            user_data['hour'] = user_data['timestamp'].dt.hour
            hourly_activity = user_data['hour'].value_counts().to_dict()
            most_active_hours = sorted(hourly_activity.items(), key=lambda x: x[1], reverse=True)[:3]
            
            # Purchase behavior
            purchases = user_data[user_data['event_type'] == 'purchase']
            purchase_frequency = len(purchases)
            avg_time_to_purchase = self._calculate_avg_time_to_purchase(user_data)
            
            # Price sensitivity (if price data available)
            price_sensitivity = self._analyze_price_sensitivity(user_data)
            
            # Brand loyalty (if brand data available)
            brand_loyalty = self._analyze_brand_loyalty(user_data)
            
            profiles[user_id] = {
                'total_interactions': len(user_data),
                'category_preferences': category_preferences,
                'event_type_distribution': event_types,
                'most_active_hours': [hour for hour, _ in most_active_hours],
                'purchase_frequency': purchase_frequency,
                'avg_time_to_purchase': avg_time_to_purchase,
                'price_sensitivity': price_sensitivity,
                'brand_loyalty': brand_loyalty,
                'engagement_level': self._calculate_engagement_level(user_data),
                'loyalty_score': self._calculate_loyalty_score(user_data),
                'risk_factors': self._identify_risk_factors(user_data),
                'recent_activity_trend': self._calculate_recent_trend(user_data)
            }
            
        return profiles
    
    def _build_item_profiles(self) -> Dict[str, Dict[str, Any]]:
        """Build item profiles with popularity and trend data."""
        profiles = {}
        
        for item_id in self.events_df['item_id'].unique():
            item_data = self.events_df[self.events_df['item_id'] == item_id]
            
            # Basic metrics
            total_interactions = len(item_data)
            purchase_rate = len(item_data[item_data['event_type'] == 'purchase']) / total_interactions
            
            # Trend analysis
            item_data_sorted = item_data.sort_values('timestamp')
            recent_activity = len(item_data_sorted[item_data_sorted['timestamp'] > 
                                (datetime.now() - timedelta(days=30))])
            
            # Category and metadata
            category = item_data['category'].iloc[0]
            item_name = item_data['item_name'].iloc[0]
            
            # Cross-category appeal
            unique_user_categories = set()
            for _, row in item_data.iterrows():
                user_categories = self.events_df[
                    self.events_df['user_id'] == row['user_id']
                ]['category'].unique()
                unique_user_categories.update(user_categories)
            
            profiles[item_id] = {
                'item_name': item_name,
                'category': category,
                'total_interactions': total_interactions,
                'purchase_rate': purchase_rate,
                'recent_activity': recent_activity,
                'trend_direction': 'up' if recent_activity > total_interactions * 0.3 else 'stable',
                'cross_category_appeal': len(unique_user_categories),
                'peak_hour': self._get_item_peak_hour(item_data),
                'seasonal_pattern': self._analyze_item_seasonality(item_data)
            }
            
        return profiles
    
    def _analyze_behavioral_patterns(self) -> Dict[str, Any]:
        """Analyze overall behavioral patterns across all users."""
        patterns = {
            'category_correlations': self._calculate_category_correlations(),
            'temporal_patterns': self._analyze_temporal_patterns(),
            'purchase_triggers': self._identify_purchase_triggers(),
            'user_segments': self._segment_users(),
            'trending_items': self._identify_trending_items(),
            'seasonal_factors': self._analyze_seasonal_factors()
        }
        return patterns
    
    def generate_ai_recommendations(self, user_id: str, k: int = 5) -> List[AIRecommendation]:
        """Generate AI-powered recommendations with behavioral explanations."""
        if user_id not in self.user_profiles:
            return self._generate_cold_start_recommendations(user_id, k)
        
        user_profile = self.user_profiles[user_id]
        recommendations = []
        
        # Get candidate items (not interacted with by user)
        user_items = set(self.events_df[self.events_df['user_id'] == user_id]['item_id'])
        candidate_items = [item_id for item_id in self.item_profiles.keys() if item_id not in user_items]
        
        # Score candidates based on multiple factors
        scored_items = []
        for item_id in candidate_items:
            score = self._calculate_behavioral_score(user_id, item_id)
            scored_items.append((item_id, score))
        
        # Sort and select top k
        scored_items.sort(key=lambda x: x[1], reverse=True)
        top_items = scored_items[:k]
        
        for item_id, score in top_items:
            item_profile = self.item_profiles[item_id]
            
            recommendation = AIRecommendation(
                item_id=item_id,
                item_name=item_profile['item_name'],
                category=item_profile['category'],
                score=score,
                reason=self._generate_recommendation_reason(user_id, item_id),
                behavioral_justification=self._generate_behavioral_justification(user_id, item_id),
                similarity_score=self._calculate_similarity_score(user_id, item_id),
                collaborative_reasoning=self._generate_collaborative_reasoning(user_id, item_id),
                confidence=self._calculate_confidence(user_id, item_id),
                trend_alignment=self._analyze_trend_alignment(user_id, item_id)
            )
            recommendations.append(recommendation)
            
        return recommendations
    
    def generate_user_behavior_summary(self, user_id: str) -> UserBehaviorSummary:
        """Generate comprehensive user behavior summary."""
        if user_id not in self.user_profiles:
            return self._generate_default_summary(user_id)
        
        profile = self.user_profiles[user_id]
        user_data = self.events_df[self.events_df['user_id'] == user_id]
        
        # Recent trends (last 30 days)
        recent_data = user_data[user_data['timestamp'] > (datetime.now() - timedelta(days=30))]
        recent_trends = self._analyze_recent_trends(recent_data, user_data)
        
        # Purchase tendencies
        purchase_tendencies = {
            'impulse_buyer': self._calculate_impulse_tendency(user_data),
            'researcher': self._calculate_research_tendency(user_data),
            'brand_loyal': profile['brand_loyalty']['score'] > 0.7,
            'price_conscious': profile['price_sensitivity'] == 'high',
            'category_explorer': len(profile['category_preferences']) > 3
        }
        
        # Loyalty indicators
        loyalty_indicators = {
            'repeat_purchase_rate': profile['loyalty_score'],
            'account_age_days': (datetime.now() - user_data['timestamp'].min()).days,
            'activity_consistency': self._calculate_activity_consistency(user_data),
            'engagement_depth': profile['engagement_level']
        }
        
        return UserBehaviorSummary(
            user_id=user_id,
            top_categories=profile['category_preferences'][:5],
            most_active_hours=profile['most_active_hours'],
            recent_trends=recent_trends,
            purchase_tendencies=purchase_tendencies,
            engagement_level=profile['engagement_level'],
            loyalty_indicators=loyalty_indicators,
            seasonal_patterns=self._identify_seasonal_patterns(user_data)
        )
    
    def generate_persona(self, user_id: str) -> UserPersona:
        """Generate detailed user persona with behavioral analysis."""
        if user_id not in self.user_profiles:
            return self._generate_default_persona(user_id)
        
        profile = self.user_profiles[user_id]
        
        # Determine persona type based on behavior patterns
        persona_type = self._determine_persona_type(profile)
        
        # Generate description and characteristics
        description = self._generate_persona_description(persona_type, profile)
        key_characteristics = self._generate_key_characteristics(profile)
        
        # Purchasing behavior analysis
        purchasing_behavior = self._analyze_purchasing_behavior(profile)
        
        # Activity patterns
        activity_patterns = {
            'peak_hours': profile['most_active_hours'],
            'session_frequency': profile['total_interactions'] / max(1, (datetime.now() - 
                                                self.events_df[self.events_df['user_id'] == user_id]['timestamp'].min()).days),
            'browsing_patterns': self._analyze_browsing_patterns(user_id),
            'decision_speed': self._analyze_decision_speed(user_id)
        }
        
        # Risk factors and opportunities
        risk_factors = profile['risk_factors']
        opportunities = self._identify_opportunities(user_id, profile)
        
        return UserPersona(
            persona_type=persona_type,
            description=description,
            key_characteristics=key_characteristics,
            purchasing_behavior=purchasing_behavior,
            category_preferences=[cat['category'] for cat in profile['category_preferences'][:3]],
            activity_patterns=activity_patterns,
            risk_factors=risk_factors,
            opportunities=opportunities
        )
    
    def predict_next_actions(self, user_id: str) -> List[PredictedAction]:
        """Predict user's next actions with confidence levels."""
        if user_id not in self.user_profiles:
            return self._generate_default_predictions(user_id)
        
        profile = self.user_profiles[user_id]
        user_data = self.events_df[self.events_df['user_id'] == user_id]
        
        predictions = []
        
        # Predict next purchase
        purchase_prediction = self._predict_next_purchase(user_id, user_data, profile)
        if purchase_prediction:
            predictions.append(purchase_prediction)
        
        # Predict cart addition
        cart_prediction = self._predict_cart_addition(user_id, user_data, profile)
        if cart_prediction:
            predictions.append(cart_prediction)
        
        # Predict churn risk
        churn_prediction = self._predict_churn_risk(user_id, user_data, profile)
        if churn_prediction:
            predictions.append(churn_prediction)
        
        # Predict activity change
        activity_prediction = self._predict_activity_change(user_id, user_data, profile)
        if activity_prediction:
            predictions.append(activity_prediction)
        
        return predictions
    
    def generate_dashboard_analytics(self, user_id: str) -> DashboardAnalytics:
        """Generate dashboard-ready analytics data."""
        user_data = self.events_df[self.events_df['user_id'] == user_id]
        
        if user_data.empty:
            return self._generate_default_analytics()
        
        # Category distribution
        category_distribution = self._generate_category_distribution(user_data)
        
        # Hourly activity heatmap
        hourly_activity = self._generate_hourly_heatmap(user_data)
        
        # Interaction trends
        interaction_trends = self._generate_interaction_trends(user_data)
        
        # Similarity breakdown
        similarity_breakdown = self._generate_similarity_breakdown(user_id)
        
        # Purchase funnel
        purchase_funnel = self._generate_purchase_funnel(user_data)
        
        # User interest growth
        interest_growth = self._generate_interest_growth(user_data)
        
        # Behavioral segments
        behavioral_segments = self._generate_behavioral_segments(user_id)
        
        # Predictive metrics
        predictive_metrics = self._generate_predictive_metrics(user_id)
        
        return DashboardAnalytics(
            category_distribution=category_distribution,
            hourly_activity_heatmap=hourly_activity,
            interaction_trends=interaction_trends,
            similarity_breakdown=similarity_breakdown,
            purchase_funnel=purchase_funnel,
            user_interest_growth=interest_growth,
            behavioral_segments=behavioral_segments,
            predictive_metrics=predictive_metrics
        )
    
    def get_comprehensive_ai_output(self, user_id: str, k: int = 5) -> Dict[str, Any]:
        """Generate complete AI output in the required JSON format."""
        recommendations = self.generate_ai_recommendations(user_id, k)
        user_summary = self.generate_user_behavior_summary(user_id)
        persona = self.generate_persona(user_id)
        predicted_actions = self.predict_next_actions(user_id)
        analytics = self.generate_dashboard_analytics(user_id)
        
        # Format recommendations
        formatted_recommendations = []
        for rec in recommendations:
            formatted_recommendations.append({
                "item_id": rec.item_id,
                "item_name": rec.item_name,
                "category": rec.category,
                "score": rec.score,
                "reason": rec.reason,
                "behavioral_justification": rec.behavioral_justification,
                "similarity_score": rec.similarity_score,
                "collaborative_reasoning": rec.collaborative_reasoning,
                "confidence": rec.confidence,
                "trend_alignment": rec.trend_alignment
            })
        
        # Format explanations
        explanations = [
            {
                "type": "behavioral_pattern",
                "description": "Analysis based on user's interaction patterns and preferences",
                "confidence": "high" if len(self.events_df[self.events_df['user_id'] == user_id]) > 10 else "medium"
            },
            {
                "type": "collaborative_filtering",
                "description": "Recommendations based on similar users' preferences",
                "confidence": "high"
            },
            {
                "type": "trend_analysis",
                "description": "Insights based on current market trends and user behavior shifts",
                "confidence": "medium"
            }
        ]
        
        return {
            "user_id": user_id,
            "recommendations": formatted_recommendations,
            "explanations": explanations,
            "user_summary": {
                "user_id": user_summary.user_id,
                "top_categories": user_summary.top_categories,
                "most_active_hours": user_summary.most_active_hours,
                "recent_trends": user_summary.recent_trends,
                "purchase_tendencies": user_summary.purchase_tendencies,
                "engagement_level": user_summary.engagement_level,
                "loyalty_indicators": user_summary.loyalty_indicators,
                "seasonal_patterns": user_summary.seasonal_patterns
            },
            "predicted_actions": [
                {
                    "action_type": pred.action_type,
                    "probability": pred.probability,
                    "reasoning": pred.reasoning,
                    "timeframe": pred.timeframe,
                    "influencing_factors": pred.influencing_factors,
                    "confidence_level": pred.confidence_level
                }
                for pred in predicted_actions
            ],
            "persona": {
                "persona_type": persona.persona_type,
                "description": persona.description,
                "key_characteristics": persona.key_characteristics,
                "purchasing_behavior": persona.purchasing_behavior,
                "category_preferences": persona.category_preferences,
                "activity_patterns": persona.activity_patterns,
                "risk_factors": persona.risk_factors,
                "opportunities": persona.opportunities
            },
            "analytics_data": {
                "category_distribution": analytics.category_distribution,
                "hourly_activity_heatmap": analytics.hourly_activity_heatmap,
                "interaction_trends": analytics.interaction_trends,
                "similarity_breakdown": analytics.similarity_breakdown,
                "purchase_funnel": analytics.purchase_funnel,
                "user_interest_growth": analytics.user_interest_growth,
                "behavioral_segments": analytics.behavioral_segments,
                "predictive_metrics": analytics.predictive_metrics
            }
        }
    
    # Helper methods for behavioral analysis
    def _calculate_behavioral_score(self, user_id: str, item_id: str) -> float:
        """Calculate behavioral relevance score for item."""
        user_profile = self.user_profiles[user_id]
        item_profile = self.item_profiles[item_id]
        
        # Category preference score
        category_scores = {cat['category']: cat['percentage'] for cat in user_profile['category_preferences']}
        category_score = category_scores.get(item_profile['category'], 0) / 100
        
        # Trend alignment score
        trend_score = 0.8 if item_profile['trend_direction'] == 'up' else 0.5
        
        # Cross-category appeal score
        appeal_score = min(item_profile['cross_category_appeal'] / 10, 1.0)
        
        # Purchase rate score
        purchase_score = item_profile['purchase_rate']
        
        # Time-based recency score
        recency_score = min(item_profile['recent_activity'] / 50, 1.0)
        
        # Weighted combination
        final_score = (
            0.35 * category_score +
            0.20 * trend_score +
            0.15 * appeal_score +
            0.15 * purchase_score +
            0.15 * recency_score
        ) * 100
        
        return min(100, max(0, final_score))
    
    def _generate_recommendation_reason(self, user_id: str, item_id: str) -> str:
        """Generate human-readable recommendation reason."""
        user_profile = self.user_profiles[user_id]
        item_profile = self.item_profiles[item_id]
        
        # Analyze user preferences
        top_categories = [cat['category'] for cat in user_profile['category_preferences'][:3]]
        
        if item_profile['category'] in top_categories:
            return f"Based on your strong interest in {item_profile['category']} items"
        elif item_profile['trend_direction'] == 'up':
            return f"This trending {item_profile['category']} item matches current market preferences"
        elif item_profile['cross_category_appeal'] > 5:
            return f"Popular across multiple categories, appealing to diverse interests"
        else:
            return f"Recommended based on your browsing patterns and item popularity"
    
    def _generate_behavioral_justification(self, user_id: str, item_id: str) -> str:
        """Generate detailed behavioral justification."""
        user_profile = self.user_profiles[user_id]
        item_profile = self.item_profiles[item_id]
        
        justifications = []
        
        # Category alignment
        user_categories = {cat['category']: cat['percentage'] for cat in user_profile['category_preferences']}
        if item_profile['category'] in user_categories:
            justifications.append(f"You spend {user_categories[item_profile['category']]:.1f}% of your time in {item_profile['category']}")
        
        # Activity pattern alignment
        if item_profile['peak_hour'] in user_profile['most_active_hours']:
            justifications.append(f"Aligns with your peak activity hours")
        
        # Purchase behavior alignment
        if item_profile['purchase_rate'] > 0.3 and user_profile['purchase_frequency'] > 5:
            justifications.append(f"Matches your established purchasing patterns")
        
        # Trend alignment
        if item_profile['trend_direction'] == 'up':
            justifications.append(f"Part of current upward trend in {item_profile['category']}")
        
        return "; ".join(justifications) if justifications else "Based on overall behavioral patterns"
    
    def _calculate_similarity_score(self, user_id: str, item_id: str) -> float:
        """Calculate similarity score based on user-item alignment."""
        # This is a simplified version - in practice, you'd use more sophisticated similarity metrics
        user_profile = self.user_profiles[user_id]
        item_profile = self.item_profiles[item_id]
        
        # Category preference similarity
        category_scores = {cat['category']: cat['percentage'] for cat in user_profile['category_preferences']}
        category_similarity = category_scores.get(item_profile['category'], 0) / 100
        
        # Purchase behavior similarity
        purchase_similarity = min(user_profile['purchase_frequency'] / 20, 1.0) * item_profile['purchase_rate']
        
        # Combined similarity
        similarity = 0.7 * category_similarity + 0.3 * purchase_similarity
        return min(1.0, similarity)
    
    def _generate_collaborative_reasoning(self, user_id: str, item_id: str) -> str:
        """Generate collaborative filtering reasoning."""
        # Find similar users who liked this item
        item_users = set(self.events_df[
            (self.events_df['item_id'] == item_id) & 
            (self.events_df['event_type'].isin(['purchase', 'cart', 'like']))
        ]['user_id'].unique())
        
        if not item_users:
            return "No collaborative data available for this item"
        
        # Find users with similar behavior patterns
        similar_users = []
        for other_user_id in item_users:
            if other_user_id in self.user_profiles and other_user_id != user_id:
                similarity = self._calculate_user_similarity(user_id, other_user_id)
                if similarity > 0.5:  # Threshold for similarity
                    similar_users.append((other_user_id, similarity))
        
        similar_users.sort(key=lambda x: x[1], reverse=True)
        
        if similar_users:
            top_similar_user = similar_users[0][0]
            return f"Users with similar behavior patterns (like user {top_similar_user}) have shown strong interest in this item"
        else:
            return f"{len(item_users)} other users have interacted positively with this item"
    
    def _calculate_confidence(self, user_id: str, item_id: str) -> str:
        """Calculate confidence level for recommendation."""
        user_data = self.events_df[self.events_df['user_id'] == user_id]
        
        # Data volume confidence
        data_volume = len(user_data)
        if data_volume < 5:
            return "low"
        elif data_volume < 15:
            return "medium"
        else:
            return "high"
    
    def _analyze_trend_alignment(self, user_id: str, item_id: str) -> str:
        """Analyze how well the item aligns with current trends."""
        item_profile = self.item_profiles[item_id]
        
        if item_profile['trend_direction'] == 'up':
            return "Strongly aligned with current upward trends"
        elif item_profile['recent_activity'] > item_profile['total_interactions'] * 0.2:
            return "Moderately aligned with recent activity patterns"
        else:
            return "Stable item with consistent performance"
    
    def _determine_persona_type(self, profile: Dict[str, Any]) -> str:
        """Determine user persona type based on behavior patterns."""
        # Analyze key behavioral indicators
        category_diversity = len(profile['category_preferences'])
        purchase_freq = profile['purchase_frequency']
        engagement = profile['engagement_level']
        price_sensitivity = profile['price_sensitivity']
        
        if category_diversity > 5 and purchase_freq > 10 and engagement == 'high':
            return "Tech Explorer"
        elif any(cat['category'] in ['sports', 'fitness'] for cat in profile['category_preferences'][:3]):
            return "Sports Enthusiast"
        elif price_sensitivity == 'high' and purchase_freq > 5:
            return "Bargain Hunter"
        elif category_diversity <= 2 and purchase_freq > 8:
            return "Category Specialist"
        elif engagement == 'low' and purchase_freq <= 3:
            return "Casual Browser"
        else:
            return "Balanced Shopper"
    
    def _generate_persona_description(self, persona_type: str, profile: Dict[str, Any]) -> str:
        """Generate persona description based on type and profile."""
        descriptions = {
            "Tech Explorer": "An adventurous user who loves exploring new technologies and products across multiple categories",
            "Sports Enthusiast": "A health-conscious individual with strong preferences for sports and fitness-related items",
            "Bargain Hunter": "A savvy shopper who carefully compares prices and looks for the best deals",
            "Category Specialist": "A focused buyer who knows exactly what they want in their preferred categories",
            "Casual Browser": "A relaxed user who browses occasionally without strong purchasing intent",
            "Balanced Shopper": "A well-rounded user with moderate engagement across various categories"
        }
        
        return descriptions.get(persona_type, "A unique user with diverse shopping patterns")
    
    def _generate_key_characteristics(self, profile: Dict[str, Any]) -> List[str]:
        """Generate key characteristics for the persona."""
        characteristics = []
        
        if profile['engagement_level'] == 'high':
            characteristics.append("Highly engaged with frequent interactions")
        
        if profile['loyalty_score'] > 0.7:
            characteristics.append("Shows strong brand loyalty")
        
        if profile['price_sensitivity'] == 'high':
            characteristics.append("Price-conscious decision maker")
        
        if len(profile['category_preferences']) > 4:
            characteristics.append("Explores diverse product categories")
        
        if profile['purchase_frequency'] > 8:
            characteristics.append("Frequent purchaser")
        
        if not characteristics:
            characteristics.append("Moderate and balanced shopping behavior")
        
        return characteristics[:4]  # Limit to top 4 characteristics
    
    def _analyze_purchasing_behavior(self, profile: Dict[str, Any]) -> str:
        """Analyze purchasing behavior patterns."""
        behaviors = []
        
        if profile['avg_time_to_purchase'] and profile['avg_time_to_purchase'] < 2:
            behaviors.append("Quick decision-maker")
        else:
            behaviors.append("Thoughtful researcher")
        
        if profile['purchase_frequency'] > 8:
            behaviors.append("Frequent buyer")
        elif profile['purchase_frequency'] > 3:
            behaviors.append("Regular purchaser")
        else:
            behaviors.append("Occasional buyer")
        
        if profile['price_sensitivity'] == 'high':
            behaviors.append("Price-comparison focused")
        
        return "; ".join(behaviors)
    
    def _predict_next_purchase(self, user_id: str, user_data: pd.DataFrame, profile: Dict[str, Any]) -> Optional[PredictedAction]:
        """Predict next purchase action."""
        recent_purchases = user_data[user_data['event_type'] == 'purchase']
        
        if len(recent_purchases) == 0:
            return None
        
        # Calculate average time between purchases
        if len(recent_purchases) > 1:
            purchase_dates = recent_purchases['timestamp'].sort_values()
            intervals = []
            for i in range(1, len(purchase_dates)):
                interval = (purchase_dates.iloc[i] - purchase_dates.iloc[i-1]).days
                intervals.append(interval)
            avg_interval = np.mean(intervals)
        else:
            avg_interval = 30  # Default assumption
        
        # Predict probability based on recency
        days_since_last_purchase = (datetime.now() - recent_purchases['timestamp'].max()).days
        probability = min(0.9, days_since_last_purchase / avg_interval)
        
        # Determine timeframe
        if days_since_last_purchase > avg_interval:
            timeframe = "Within 7 days"
        elif days_since_last_purchase > avg_interval * 0.7:
            timeframe = "Within 14 days"
        else:
            timeframe = "Within 30 days"
        
        # Influencing factors
        factors = []
        if profile['engagement_level'] == 'high':
            factors.append("High engagement level")
        if days_since_last_purchase > avg_interval:
            factors.append("Overdue for next purchase")
        if profile['recent_activity_trend'] == 'increasing':
            factors.append("Recent activity increase")
        
        return PredictedAction(
            action_type="purchase",
            probability=probability,
            reasoning=f"Based on your historical purchase pattern (avg {avg_interval:.0f} days between purchases)",
            timeframe=timeframe,
            influencing_factors=factors[:3],
            confidence_level="high" if len(recent_purchases) > 3 else "medium"
        )
    
    def _predict_cart_addition(self, user_id: str, user_data: pd.DataFrame, profile: Dict[str, Any]) -> Optional[PredictedAction]:
        """Predict cart addition probability."""
        recent_views = user_data[user_data['event_type'] == 'view']
        
        if len(recent_views) == 0:
            return None
        
        # Calculate conversion rate from views to cart additions
        view_to_cart_rate = len(user_data[user_data['event_type'] == 'cart']) / len(recent_views)
        
        # Recent activity factor
        recent_views_7d = recent_views[recent_views['timestamp'] > (datetime.now() - timedelta(days=7))]
        recent_activity_factor = len(recent_views_7d) / max(1, len(recent_views))
        
        probability = min(0.8, view_to_cart_rate * 2 * recent_activity_factor)
        
        return PredictedAction(
            action_type="add_to_cart",
            probability=probability,
            reasoning=f"Based on your {view_to_cart_rate:.1%} view-to-cart conversion rate and recent browsing activity",
            timeframe="Within 3 days",
            influencing_factors=[f"Viewed {len(recent_views_7d)} items recently", "Active browsing pattern detected"],
            confidence_level="medium"
        )
    
    def _predict_churn_risk(self, user_id: str, user_data: pd.DataFrame, profile: Dict[str, Any]) -> Optional[PredictedAction]:
        """Predict churn risk."""
        days_since_last_activity = (datetime.now() - user_data['timestamp'].max()).days
        
        # Define risk thresholds
        if days_since_last_activity > 60:
            probability = 0.8
            risk_level = "High"
        elif days_since_last_activity > 30:
            probability = 0.5
            risk_level = "Medium"
        elif days_since_last_activity > 14:
            probability = 0.2
            risk_level = "Low"
        else:
            return None
        
        factors = []
        if profile['engagement_level'] == 'low':
            factors.append("Low engagement level")
        if profile['recent_activity_trend'] == 'decreasing':
            factors.append("Declining activity trend")
        if days_since_last_activity > 45:
            factors.append("Extended absence period")
        
        return PredictedAction(
            action_type="churn_risk",
            probability=probability,
            reasoning=f"{risk_level} risk of churn based on {days_since_last_activity} days since last activity",
            timeframe="Ongoing monitoring needed",
            influencing_factors=factors[:3],
            confidence_level="high"
        )
    
    def _predict_activity_change(self, user_id: str, user_data: pd.DataFrame, profile: Dict[str, Any]) -> Optional[PredictedAction]:
        """Predict activity level changes."""
        # Compare recent activity to historical average
        recent_30d = user_data[user_data['timestamp'] > (datetime.now() - timedelta(days=30))]
        historical_avg = len(user_data) / max(1, (datetime.now() - user_data['timestamp'].min()).days) * 30
        
        recent_activity = len(recent_30d)
        
        if recent_activity > historical_avg * 1.5:
            return PredictedAction(
                action_type="activity_increase",
                probability=0.7,
                reasoning=f"Activity level increasing ({recent_activity} vs avg {historical_avg:.0f} per 30 days)",
                timeframe="Next 30 days",
                influencing_factors=["Recent engagement uptick", "Above-average interaction frequency"],
                confidence_level="medium"
            )
        elif recent_activity < historical_avg * 0.5:
            return PredictedAction(
                action_type="activity_decrease",
                probability=0.6,
                reasoning=f"Activity level declining ({recent_activity} vs avg {historical_avg:.0f} per 30 days)",
                timeframe="Next 30 days",
                influencing_factors=["Reduced recent engagement", "Below-average interaction frequency"],
                confidence_level="medium"
            )
        
        return None
    
    def _generate_default_recommendations(self, user_id: str, k: int) -> List[AIRecommendation]:
        """Generate default recommendations for cold start users."""
        # Use popularity-based recommendations
        popular_items = sorted(self.item_profiles.items(), 
                             key=lambda x: x[1]['total_interactions'], reverse=True)[:k]
        
        recommendations = []
        for item_id, item_profile in popular_items:
            recommendation = AIRecommendation(
                item_id=item_id,
                item_name=item_profile['item_name'],
                category=item_profile['category'],
                score=70.0,  # Default score for cold start
                reason="Popular item among our users",
                behavioral_justification="No user history available - recommending based on popularity",
                similarity_score=0.5,
                collaborative_reasoning="Popular choice among similar users",
                confidence="low",
                trend_alignment="Stable popular item"
            )
            recommendations.append(recommendation)
        
        return recommendations
    
    def _generate_default_summary(self, user_id: str) -> UserBehaviorSummary:
        """Generate default summary for users with no data."""
        return UserBehaviorSummary(
            user_id=user_id,
            top_categories=[],
            most_active_hours=[],
            recent_trends=["No activity data available"],
            purchase_tendencies={},
            engagement_level="unknown",
            loyalty_indicators={},
            seasonal_patterns=["Insufficient data for seasonal analysis"]
        )
    
    def _generate_default_persona(self, user_id: str) -> UserPersona:
        """Generate default persona for users with no data."""
        return UserPersona(
            persona_type="New User",
            description="A new user with no established behavioral patterns yet",
            key_characteristics=["Exploring the platform", "Building preferences"],
            purchasing_behavior="Not enough data to determine purchasing patterns",
            category_preferences=[],
            activity_patterns={},
            risk_factors=["Limited engagement history"],
            opportunities=["High potential for personalized recommendations"]
        )
    
    def _generate_default_predictions(self, user_id: str) -> List[PredictedAction]:
        """Generate default predictions for users with no data."""
        return [
            PredictedAction(
                action_type="exploration",
                probability=0.8,
                reasoning="New user likely to explore platform features",
                timeframe="First week",
                influencing_factors=["New user onboarding", "Platform exploration phase"],
                confidence_level="low"
            )
        ]
    
    def _generate_default_analytics(self) -> DashboardAnalytics:
        """Generate default analytics when no user data is available."""
        return DashboardAnalytics(
            category_distribution={"labels": [], "values": []},
            hourly_activity_heatmap={"hours": [], "activity": []},
            interaction_trends={"dates": [], "counts": []},
            similarity_breakdown={"factors": [], "scores": []},
            purchase_funnel={"stages": [], "conversions": []},
            user_interest_growth={"categories": [], "growth_rates": []},
            behavioral_segments={"segments": [], "user_counts": []},
            predictive_metrics={"metrics": [], "values": []}
        )
    
    # Additional helper methods for analytics generation
    def _generate_category_distribution(self, user_data: pd.DataFrame) -> Dict[str, Any]:
        """Generate category distribution data for visualization."""
        category_counts = user_data['category'].value_counts()
        return {
            "labels": category_counts.index.tolist(),
            "values": category_counts.values.tolist(),
            "colors": self._generate_category_colors(category_counts.index.tolist())
        }
    
    def _generate_hourly_heatmap(self, user_data: pd.DataFrame) -> Dict[str, Any]:
        """Generate hourly activity heatmap data."""
        user_data['hour'] = user_data['timestamp'].dt.hour
        hourly_counts = user_data['hour'].value_counts().sort_index()
        
        # Fill in missing hours with 0
        all_hours = list(range(24))
        activity_counts = [hourly_counts.get(hour, 0) for hour in all_hours]
        
        return {
            "hours": all_hours,
            "activity": activity_counts,
            "max_activity": max(activity_counts) if activity_counts else 0
        }
    
    def _generate_interaction_trends(self, user_data: pd.DataFrame) -> Dict[str, Any]:
        """Generate interaction trends over time."""
        user_data['date'] = user_data['timestamp'].dt.date
        daily_counts = user_data.groupby('date').size()
        
        return {
            "dates": [str(date) for date in daily_counts.index],
            "counts": daily_counts.values.tolist(),
            "trend_direction": self._calculate_trend_direction(daily_counts.values)
        }
    
    def _generate_similarity_breakdown(self, user_id: str) -> Dict[str, Any]:
        """Generate similarity breakdown for recommendations."""
        # This is a simplified version
        return {
            "factors": ["Category Preference", "Purchase History", "Activity Patterns", "Trend Alignment"],
            "scores": [0.8, 0.7, 0.6, 0.5],  # Example scores
            "overall_similarity": 0.65
        }
    
    def _generate_purchase_funnel(self, user_data: pd.DataFrame) -> Dict[str, Any]:
        """Generate purchase funnel analysis."""
        event_counts = user_data['event_type'].value_counts()
        
        views = event_counts.get('view', 0)
        carts = event_counts.get('cart', 0)
        purchases = event_counts.get('purchase', 0)
        
        return {
            "stages": ["View", "Cart", "Purchase"],
            "conversions": [views, carts, purchases],
            "conversion_rates": [
                carts / views if views > 0 else 0,
                purchases / carts if carts > 0 else 0,
                purchases / views if views > 0 else 0
            ]
        }
    
    def _generate_interest_growth(self, user_data: pd.DataFrame) -> Dict[str, Any]:
        """Generate interest growth analysis."""
        # Compare recent vs historical category interest
        recent_data = user_data[user_data['timestamp'] > (datetime.now() - timedelta(days=30))]
        
        if len(recent_data) == 0:
            return {"categories": [], "growth_rates": []}
        
        recent_categories = recent_data['category'].value_counts()
        historical_categories = user_data['category'].value_counts()
        
        growth_rates = []
        categories = []
        
        for category in recent_categories.index:
            recent_count = recent_categories[category]
            historical_avg = historical_categories[category] / max(1, (datetime.now() - user_data['timestamp'].min()).days) * 30
            
            if historical_avg > 0:
                growth_rate = (recent_count - historical_avg) / historical_avg
                growth_rates.append(growth_rate)
                categories.append(category)
        
        return {
            "categories": categories,
            "growth_rates": growth_rates
        }
    
    def _generate_behavioral_segments(self, user_id: str) -> Dict[str, Any]:
        """Generate behavioral segmentation data."""
        # Simple segmentation based on engagement and purchase behavior
        if user_id not in self.user_profiles:
            return {"segments": [], "user_counts": []}
        
        profile = self.user_profiles[user_id]
        
        segments = []
        if profile['engagement_level'] == 'high':
            segments.append("High Engagement")
        if profile['loyalty_score'] > 0.7:
            segments.append("Loyal Customer")
        if profile['purchase_frequency'] > 8:
            segments.append("Frequent Buyer")
        if len(profile['category_preferences']) > 4:
            segments.append("Category Explorer")
        
        return {
            "segments": segments or ["Standard User"],
            "user_counts": [1] * len(segments) if segments else [1]
        }
    
    def _generate_predictive_metrics(self, user_id: str) -> Dict[str, Any]:
        """Generate predictive metrics for dashboard."""
        if user_id not in self.user_profiles:
            return {"metrics": [], "values": []}
        
        profile = self.user_profiles[user_id]
        
        return {
            "metrics": ["Purchase Probability", "Churn Risk", "Activity Increase", "Category Expansion"],
            "values": [
                profile['loyalty_score'],
                0.3 if profile['recent_activity_trend'] == 'decreasing' else 0.1,
                0.6 if profile['engagement_level'] == 'high' else 0.3,
                0.5 if len(profile['category_preferences']) > 3 else 0.2
            ]
        }
    
    def _generate_category_colors(self, categories: List[str]) -> List[str]:
        """Generate colors for categories."""
        color_map = {
            'electronics': '#3B82F6',
            'books': '#10B981',
            'sports': '#F59E0B',
            'clothing': '#EF4444',
            'home': '#8B5CF6',
            'food': '#F97316',
            'beauty': '#EC4899',
            'automotive': '#6B7280'
        }
        
        return [color_map.get(cat, '#6B7280') for cat in categories]
    
    def _calculate_trend_direction(self, values: List[int]) -> str:
        """Calculate trend direction from values."""
        if len(values) < 2:
            return "stable"
        
        # Simple linear trend
        x = np.arange(len(values))
        slope = np.polyfit(x, values, 1)[0]
        
        if slope > 0.1:
            return "increasing"
        elif slope < -0.1:
            return "decreasing"
        else:
            return "stable"
    
    def _calculate_user_similarity(self, user1_id: str, user2_id: str) -> float:
        """Calculate similarity between two users."""
        # Simple similarity based on category preferences
        if user1_id not in self.user_profiles or user2_id not in self.user_profiles:
            return 0.0
        
        profile1 = self.user_profiles[user1_id]
        profile2 = self.user_profiles[user2_id]
        
        # Category preference similarity
        categories1 = {cat['category']: cat['percentage'] for cat in profile1['category_preferences']}
        categories2 = {cat['category']: cat['percentage'] for cat in profile2['category_preferences']}
        
        all_categories = set(categories1.keys()) | set(categories2.keys())
        
        if not all_categories:
            return 0.0
        
        similarities = []
        for category in all_categories:
            score1 = categories1.get(category, 0)
            score2 = categories2.get(category, 0)
            
            # Normalize scores
            max_score = max(score1, score2) if max(score1, score2) > 0 else 1
            similarity = 1 - abs(score1 - score2) / max_score
            similarities.append(similarity)
        
        return np.mean(similarities)
    
    # Additional helper methods for behavioral analysis
    def _calculate_avg_time_to_purchase(self, user_data: pd.DataFrame) -> Optional[float]:
        """Calculate average time from view to purchase."""
        purchases = user_data[user_data['event_type'] == 'purchase']
        if len(purchases) == 0:
            return None
        
        # This is a simplified calculation
        # In practice, you'd track individual user journeys
        return 3.5  # Default average in days
    
    def _analyze_price_sensitivity(self, user_data: pd.DataFrame) -> str:
        """Analyze price sensitivity (simplified)."""
        # Without price data, use purchase frequency as proxy
        purchases = len(user_data[user_data['event_type'] == 'purchase'])
        if purchases > 10:
            return 'medium'
        elif purchases > 5:
            return 'high'
        else:
            return 'unknown'
    
    def _analyze_brand_loyalty(self, user_data: pd.DataFrame) -> Dict[str, Any]:
        """Analyze brand loyalty (simplified)."""
        # Without brand data, use repeat purchases as proxy
        purchases = user_data[user_data['event_type'] == 'purchase']
        if len(purchases) > 5:
            return {'score': 0.6, 'description': 'Moderate loyalty'}
        else:
            return {'score': 0.3, 'description': 'Low loyalty'}
    
    def _calculate_engagement_level(self, user_data: pd.DataFrame) -> str:
        """Calculate engagement level."""
        total_interactions = len(user_data)
        if total_interactions > 20:
            return 'high'
        elif total_interactions > 8:
            return 'medium'
        else:
            return 'low'
    
    def _calculate_loyalty_score(self, user_data: pd.DataFrame) -> float:
        """Calculate loyalty score."""
        purchases = len(user_data[user_data['event_type'] == 'purchase'])
        return min(1.0, purchases / 15)  # Normalize to 0-1
    
    def _identify_risk_factors(self, user_data: pd.DataFrame) -> List[str]:
        """Identify risk factors for the user."""
        risk_factors = []
        
        days_since_last_activity = (datetime.now() - user_data['timestamp'].max()).days
        if days_since_last_activity > 30:
            risk_factors.append("Extended inactivity period")
        
        if len(user_data[user_data['event_type'] == 'purchase']) == 0:
            risk_factors.append("No purchase history")
        
        if len(user_data) < 5:
            risk_factors.append("Low engagement level")
        
        return risk_factors[:3]  # Limit to top 3
    
    def _calculate_recent_trend(self, user_data: pd.DataFrame) -> str:
        """Calculate recent activity trend."""
        recent_30d = user_data[user_data['timestamp'] > (datetime.now() - timedelta(days=30))]
        
        if len(recent_30d) > len(user_data) * 0.4:
            return 'increasing'
        elif len(recent_30d) < len(user_data) * 0.1:
            return 'decreasing'
        else:
            return 'stable'
    
    def _calculate_category_correlations(self) -> Dict[str, Any]:
        """Calculate correlations between categories."""
        # Simplified correlation analysis
        return {"electronics_books": 0.3, "sports_fitness": 0.7}
    
    def _analyze_temporal_patterns(self) -> Dict[str, Any]:
        """Analyze temporal patterns across all users."""
        self.events_df['hour'] = self.events_df['timestamp'].dt.hour
        hourly_activity = self.events_df['hour'].value_counts()
        
        return {
            "peak_hours": hourly_activity.head(3).index.tolist(),
            "quiet_hours": hourly_activity.tail(3).index.tolist()
        }
    
    def _identify_purchase_triggers(self) -> List[str]:
        """Identify common purchase triggers."""
        return ["Multiple views within 24h", "Category browsing", "Price comparison"]
    
    def _segment_users(self) -> Dict[str, int]:
        """Segment users based on behavior."""
        segments = defaultdict(int)
        
        for user_id, profile in self.user_profiles.items():
            if profile['engagement_level'] == 'high':
                segments['high_engagement'] += 1
            if profile['loyalty_score'] > 0.7:
                segments['loyal'] += 1
            if profile['purchase_frequency'] > 8:
                segments['frequent_buyer'] += 1
        
        return dict(segments)
    
    def _identify_trending_items(self) -> List[str]:
        """Identify currently trending items."""
        # Items with increasing activity in last 30 days
        recent_activity = self.events_df[
            self.events_df['timestamp'] > (datetime.now() - timedelta(days=30))
        ]
        
        trending = recent_activity['item_id'].value_counts().head(5)
        return trending.index.tolist()
    
    def _analyze_seasonal_factors(self) -> Dict[str, Any]:
        """Analyze seasonal factors affecting behavior."""
        return {
            "current_season": "Q4",
            "seasonal_categories": ["electronics", "books"],
            "trend_multiplier": 1.2
        }
    
    def _analyze_recent_trends(self, recent_data: pd.DataFrame, all_data: pd.DataFrame) -> List[str]:
        """Analyze recent trends compared to historical data."""
        if len(recent_data) == 0:
            return ["No recent activity"]
        
        trends = []
        
        # Category trend
        recent_categories = recent_data['category'].value_counts()
        if len(recent_categories) > 0:
            top_recent = recent_categories.index[0]
            trends.append(f"Increased interest in {top_recent}")
        
        # Activity level trend
        if len(recent_data) > len(all_data) * 0.3:
            trends.append("Higher than average recent activity")
        
        return trends[:2]  # Limit to top 2 trends
    
    def _calculate_impulse_tendency(self, user_data: pd.DataFrame) -> bool:
        """Calculate impulse buying tendency."""
        # Simplified: assume low impulse if many views before purchase
        purchases = user_data[user_data['event_type'] == 'purchase']
        if len(purchases) == 0:
            return False
        
        views_per_purchase = len(user_data[user_data['event_type'] == 'view']) / len(purchases)
        return views_per_purchase < 3
    
    def _calculate_research_tendency(self, user_data: pd.DataFrame) -> bool:
        """Calculate research tendency."""
        views = len(user_data[user_data['event_type'] == 'view'])
        purchases = len(user_data[user_data['event_type'] == 'purchase'])
        
        return views > purchases * 5 if purchases > 0 else views > 10
    
    def _calculate_activity_consistency(self, user_data: pd.DataFrame) -> float:
        """Calculate activity consistency."""
        # Simple consistency measure based on time between activities
        if len(user_data) < 2:
            return 0.5
        
        sorted_dates = user_data['timestamp'].sort_values()
        intervals = []
        for i in range(1, len(sorted_dates)):
            interval = (sorted_dates.iloc[i] - sorted_dates.iloc[i-1]).days
            intervals.append(interval)
        
        if not intervals:
            return 0.5
        
        # Lower variance = higher consistency
        variance = np.var(intervals)
        consistency = max(0, 1 - variance / 100)  # Normalize
        
        return consistency
    
    def _identify_seasonal_patterns(self, user_data: pd.DataFrame) -> List[str]:
        """Identify seasonal patterns in user behavior."""
        if len(user_data) < 10:
            return ["Insufficient data for seasonal analysis"]
        
        user_data['month'] = user_data['timestamp'].dt.month
        monthly_activity = user_data['month'].value_counts()
        
        if len(monthly_activity) < 3:
            return ["Limited seasonal variation detected"]
        
        peak_months = monthly_activity.head(2).index.tolist()
        month_names = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June",
                      7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"}
        
        return [f"Peak activity in {month_names.get(month, f'Month {month}')}" for month in peak_months]
    
    def _analyze_browsing_patterns(self, user_id: str) -> Dict[str, Any]:
        """Analyze user browsing patterns."""
        user_data = self.events_df[self.events_df['user_id'] == user_id]
        
        if len(user_data) < 5:
            return {"pattern": "insufficient_data", "sessions": 0}
        
        # Simple session analysis
        sessions = len(user_data.groupby(user_data['timestamp'].dt.date))
        
        return {
            "pattern": "regular" if sessions > 3 else "sporadic",
            "sessions": sessions,
            "avg_session_length": len(user_data) / max(1, sessions)
        }
    
    def _analyze_decision_speed(self, user_id: str) -> str:
        """Analyze user decision speed."""
        user_data = self.events_df[self.events_df['user_id'] == user_id]
        
        if len(user_data) < 5:
            return "unknown"
        
        # Simple decision speed based on view-to-action ratio
        views = len(user_data[user_data['event_type'] == 'view'])
        actions = len(user_data[user_data['event_type'].isin(['cart', 'purchase'])])
        
        ratio = actions / views if views > 0 else 0
        
        if ratio > 0.3:
            return "fast_decider"
        elif ratio > 0.1:
            return "moderate_decider"
        else:
            return "slow_decider"
    
    def _identify_opportunities(self, user_id: str, profile: Dict[str, Any]) -> List[str]:
        """Identify opportunities for the user."""
        opportunities = []
        
        if profile['engagement_level'] == 'low':
            opportunities.append("High engagement potential through personalized content")
        
        if len(profile['category_preferences']) < 3:
            opportunities.append("Category expansion opportunities available")
        
        if profile['loyalty_score'] < 0.5:
            opportunities.append("Loyalty program participation potential")
        
        return opportunities[:2]  # Limit to top 2
    
    def _get_item_peak_hour(self, item_data: pd.DataFrame) -> int:
        """Get peak hour for item interactions."""
        if len(item_data) == 0:
            return 12  # Default noon
        
        item_data['hour'] = item_data['timestamp'].dt.hour
        hourly_counts = item_data['hour'].value_counts()
        
        return hourly_counts.index[0] if len(hourly_counts) > 0 else 12
    
    def _analyze_item_seasonality(self, item_data: pd.DataFrame) -> str:
        """Analyze item seasonality patterns."""
        if len(item_data) < 5:
            return "insufficient_data"
        
        item_data['month'] = item_data['timestamp'].dt.month
        monthly_counts = item_data['month'].value_counts()
        
        if len(monthly_counts) < 3:
            return "stable"
        
        # Simple seasonality detection
        max_month = monthly_counts.index[0]
        min_month = monthly_counts.index[-1]
        
        if monthly_counts.iloc[0] > monthly_counts.iloc[-1] * 2:
            return "seasonal"
        else:
            return "stable"
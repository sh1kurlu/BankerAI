"""
Streamlit Dashboard for Customer Behavior Analytics System
Comprehensive AI-powered business intelligence platform
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.customer_analytics_engine import CustomerAnalyticsEngine
from core.ai_behavioral_engine import AIBehavioralEngine
from core.preprocessor import load_events, build_interaction_matrix
from core.model_engine import RecommenderEngine
from core.feedback_engine import FeedbackEngine

# Page configuration
st.set_page_config(
    page_title="Customer Behavior Analytics",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .persona-card {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
    }
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_customer_data():
    """Load customer data"""
    try:
        df = pd.read_csv('data/customer.csv')
        return df
    except Exception as e:
        st.error(f"Error loading customer data: {e}")
        return None

@st.cache_data
def load_events_data():
    """Load events data if available"""
    try:
        if os.path.exists('data/events.csv'):
            return load_events('data/events.csv')
        return None
    except Exception as e:
        return None

@st.cache_resource
def initialize_engines():
    """Initialize analytics engines"""
    customer_df = load_customer_data()
    if customer_df is None:
        return None, None, None, None
    
    # Initialize Customer Analytics Engine
    customer_engine = CustomerAnalyticsEngine(customer_df)
    
    # Try to initialize AI Behavioral Engine if events data exists
    events_df = load_events_data()
    ai_engine = None
    recommender_engine = None
    feedback_engine = None
    
    if events_df is not None and len(events_df) > 0:
        try:
            ai_engine = AIBehavioralEngine(events_df)
            R, user_to_idx, idx_to_user, item_to_idx, idx_to_item = build_interaction_matrix(events_df)
            recommender_engine = RecommenderEngine.from_dataframe(events_df, R, user_to_idx, idx_to_user, item_to_idx, idx_to_item)
            feedback_engine = FeedbackEngine(events_df)
        except Exception as e:
            st.warning(f"Could not initialize AI engines: {e}")
    
    return customer_engine, ai_engine, recommender_engine, feedback_engine

def display_persona_card(persona_data):
    """Display customer persona card"""
    st.markdown(f"""
        <div class="persona-card">
            <h2>👤 {persona_data['label']}</h2>
            <p>{persona_data['description']}</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Key Traits")
    for trait in persona_data['traits']:
        st.markdown(f"• {trait}")

def display_metrics(analytics_data):
    """Display key metrics"""
    pred = analytics_data.get('predictive_analytics', {})
    visual = analytics_data.get('visual_data', {})
    clv = visual.get('lifetime_value_estimate', {})
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Purchase Probability",
            f"{pred.get('purchase_probability_percent', 0)}%",
            delta=f"{pred.get('purchase_probability_percent', 0) - 50}%"
        )
    
    with col2:
        st.metric(
            "Churn Risk",
            f"{pred.get('churn_risk_percent', 0)}%",
            delta=f"{pred.get('churn_risk_percent', 0) - 30}%",
            delta_color="inverse"
        )
    
    with col3:
        current_val = clv.get('current_value', 0)
        st.metric(
            "Current Value",
            f"${current_val:,.2f}",
            delta=f"${current_val * 0.1:,.2f}"
        )
    
    with col4:
        estimated_clv = clv.get('estimated_clv', 0)
        st.metric(
            "Estimated CLV",
            f"${estimated_clv:,.2f}",
            delta=f"${estimated_clv * 0.05:,.2f}"
        )

def create_category_distribution_chart(category_data):
    """Create category distribution pie chart"""
    if not category_data:
        return None
    
    categories = [item['category'] for item in category_data]
    values = [item['value'] for item in category_data]
    
    fig = px.pie(
        values=values,
        names=categories,
        title="Category Distribution",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig

def create_hourly_activity_chart(activity_data):
    """Create hourly activity heatmap"""
    if not activity_data:
        return None
    
    hours = [item['hour'] for item in activity_data]
    activities = [item['activity'] for item in activity_data]
    
    fig = go.Figure(data=go.Scatter(
        x=hours,
        y=activities,
        mode='lines+markers',
        fill='tozeroy',
        line=dict(color='#667eea', width=3),
        marker=dict(size=8, color='#764ba2')
    ))
    
    fig.update_layout(
        title="Hourly Activity Pattern (24 Hours)",
        xaxis_title="Hour of Day",
        yaxis_title="Activity Level",
        template="plotly_white",
        height=400
    )
    
    return fig

def create_interest_trend_chart(trend_data):
    """Create interest trend line chart"""
    if not trend_data:
        return None
    
    dates = [item['date'] for item in trend_data]
    scores = [item['interest_score'] for item in trend_data]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates,
        y=scores,
        mode='lines+markers',
        name='Interest Score',
        line=dict(color='#f093fb', width=3),
        fill='tonexty',
        fillcolor='rgba(240, 147, 251, 0.2)'
    ))
    
    fig.update_layout(
        title="Interest Trend (30 Days)",
        xaxis_title="Date",
        yaxis_title="Interest Score",
        template="plotly_white",
        height=400
    )
    
    return fig

def create_conversion_funnel_chart(funnel_data):
    """Create conversion funnel chart"""
    if not funnel_data:
        return None
    
    stages = [item['stage'] for item in funnel_data]
    counts = [item['count'] for item in funnel_data]
    
    fig = go.Figure(go.Funnel(
        y=stages,
        x=counts,
        textposition="inside",
        textinfo="value+percent initial",
        marker=dict(
            color=["#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0"]
        )
    ))
    
    fig.update_layout(
        title="Conversion Funnel",
        template="plotly_white",
        height=400
    )
    
    return fig

def create_retention_curve_chart(retention_data):
    """Create retention curve chart"""
    if not retention_data:
        return None
    
    months = [item['month'] for item in retention_data]
    rates = [item['retention_rate'] for item in retention_data]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=months,
        y=rates,
        mode='lines+markers',
        name='Retention Rate',
        line=dict(color='#10B981', width=3),
        fill='tozeroy',
        fillcolor='rgba(16, 185, 129, 0.2)'
    ))
    
    fig.update_layout(
        title="Customer Retention Curve (12 Months)",
        xaxis_title="Month",
        yaxis_title="Retention Rate",
        template="plotly_white",
        height=400
    )
    
    return fig

def display_recommendations(recommendations):
    """Display business recommendations"""
    if not recommendations:
        st.info("No recommendations available for this customer.")
        return
    
    for i, rec in enumerate(recommendations, 1):
        priority_color = {
            "Critical": "🔴",
            "High": "🟠",
            "Medium": "🟡",
            "Low": "🟢"
        }
        
        with st.expander(f"{priority_color.get(rec.get('priority', 'Medium'), '🟡')} {rec.get('type', 'General')}: {rec.get('action', 'N/A')}"):
            st.markdown(f"**Priority:** {rec.get('priority', 'N/A')}")
            st.markdown(f"**Description:** {rec.get('description', 'N/A')}")

def display_ai_recommendations(ai_recommendations):
    """Display AI-powered product recommendations"""
    if not ai_recommendations:
        st.info("No AI recommendations available.")
        return
    
    st.markdown("### 🎯 AI-Powered Recommendations")
    
    for i, rec in enumerate(ai_recommendations, 1):
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            st.markdown(f"**{rec.get('item_name', 'Unknown Item')}**")
            st.markdown(f"*{rec.get('category', 'Unknown Category')}*")
            st.markdown(f"💡 {rec.get('reason', 'Recommended for you')}")
            if rec.get('behavioral_justification'):
                st.caption(f"📊 {rec.get('behavioral_justification')}")
        
        with col2:
            score = rec.get('score', 0)
            st.metric("Score", f"{score:.1f}")
        
        with col3:
            confidence = rec.get('confidence', 'medium')
            st.metric("Confidence", confidence.title())
        
        if i < len(ai_recommendations):
            st.divider()

def main():
    # Header
    st.markdown('<h1 class="main-header">🧠 Customer Behavior Analytics Dashboard</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">AI-Powered Business Intelligence for Customer Insights</p>', unsafe_allow_html=True)
    
    # Initialize engines
    customer_engine, ai_engine, recommender_engine, feedback_engine = initialize_engines()
    
    if customer_engine is None:
        st.error("Failed to load customer data. Please check data/customer.csv exists.")
        return
    
    # Sidebar
    st.sidebar.header("🔍 Customer Analysis")
    
    # Get customer list
    customer_df = load_customer_data()
    customer_ids = sorted(customer_df['Customer ID'].unique().astype(str))
    
    selected_customer = st.sidebar.selectbox(
        "Select Customer ID",
        customer_ids,
        index=0 if customer_ids else None
    )
    
    analysis_type = st.sidebar.selectbox(
        "Analysis Type",
        ["Comprehensive", "Persona Only", "Behavior Only", "Predictive Only", "Recommendations Only"]
    )
    
    num_recommendations = st.sidebar.slider(
        "Number of Recommendations",
        min_value=3,
        max_value=20,
        value=5
    )
    
    if st.sidebar.button("🚀 Analyze Customer", type="primary"):
        st.session_state.analyze = True
        st.session_state.customer_id = selected_customer
    
    # Main content
    if st.session_state.get('analyze', False) and st.session_state.get('customer_id'):
        customer_id = st.session_state.customer_id
        
        with st.spinner("🔄 Analyzing customer data... Please wait."):
            # Analyze customer
            analytics = customer_engine.analyze_customer(customer_id)
            
            if "error" in analytics:
                st.error(analytics["error"])
                return
            
            # Display metrics
            st.markdown("---")
            display_metrics(analytics)
            st.markdown("---")
            
            # Main tabs
            tab1, tab2, tab3, tab4, tab5 = st.tabs([
                "📊 Overview", 
                "👤 Persona & Behavior", 
                "🔮 Predictive Analytics",
                "💡 Recommendations",
                "📈 Visualizations"
            ])
            
            with tab1:
                st.header("Customer Overview")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    display_persona_card(analytics['persona'])
                
                with col2:
                    st.markdown("### Behavior Summary")
                    behavior = analytics['behavior_summary']
                    
                    st.markdown(f"**Top Categories:** {', '.join(behavior.get('top_categories', []))}")
                    st.markdown(f"**Price Range:** {behavior.get('preferred_price_range', 'N/A')}")
                    st.markdown(f"**Active Time:** {behavior.get('most_active_time_window', 'N/A')}")
                    st.markdown(f"**Time Spent:** {behavior.get('time_spent_patterns', 'N/A')}")
                    st.markdown(f"**Activity Trend:** {behavior.get('activity_trend', 'N/A')}")
                    st.markdown(f"**Purchase Pattern:** {behavior.get('purchase_browse_pattern', 'N/A')}")
                    st.markdown(f"**Price Sensitivity:** {behavior.get('price_sensitivity_level', 'N/A')}")
                    st.markdown(f"**Engagement Level:** {behavior.get('engagement_level', 'N/A')}")
            
            with tab2:
                st.header("Customer Persona & Behavior Analysis")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("### 👤 Customer Persona")
                    display_persona_card(analytics['persona'])
                
                with col2:
                    st.markdown("### 📊 Detailed Behavior Analysis")
                    behavior = analytics['behavior_summary']
                    
                    behavior_dict = {
                        "Top Categories": ', '.join(behavior.get('top_categories', [])),
                        "Preferred Price Range": behavior.get('preferred_price_range', 'N/A'),
                        "Most Active Time": behavior.get('most_active_time_window', 'N/A'),
                        "Time Spent Patterns": behavior.get('time_spent_patterns', 'N/A'),
                        "Activity Trend": behavior.get('activity_trend', 'N/A'),
                        "Purchase Pattern": behavior.get('purchase_browse_pattern', 'N/A'),
                        "Price Sensitivity": behavior.get('price_sensitivity_level', 'N/A'),
                        "Engagement Level": behavior.get('engagement_level', 'N/A')
                    }
                    
                    for key, value in behavior_dict.items():
                        st.markdown(f"**{key}:** {value}")
            
            with tab3:
                st.header("🔮 Predictive Analytics")
                
                pred = analytics['predictive_analytics']
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown("### Next Likely Action")
                    st.markdown(f"## {pred.get('next_likely_action', 'N/A')}")
                    st.markdown(f"**Probability:** {pred.get('purchase_probability_percent', 0)}%")
                
                with col2:
                    st.markdown("### Category Shift Prediction")
                    st.markdown(f"## {pred.get('category_shift_prediction', 'N/A')}")
                
                with col3:
                    st.markdown("### Revenue Potential")
                    st.markdown(f"## {pred.get('revenue_potential', 'N/A')}")
                
                st.markdown("---")
                
                # Churn risk visualization
                churn_risk = pred.get('churn_risk_percent', 0)
                st.markdown("### Churn Risk Assessment")
                
                if churn_risk < 30:
                    risk_level = "Low"
                    risk_color = "green"
                elif churn_risk < 60:
                    risk_level = "Medium"
                    risk_color = "orange"
                else:
                    risk_level = "High"
                    risk_color = "red"
                
                st.progress(churn_risk / 100)
                st.markdown(f"**Risk Level:** <span style='color: {risk_color}; font-weight: bold;'>{risk_level}</span> ({churn_risk}%)", unsafe_allow_html=True)
            
            with tab4:
                st.header("💡 Business Recommendations")
                
                recommendations = analytics.get('business_recommendations', [])
                display_recommendations(recommendations)
                
                # AI Recommendations if available
                if ai_engine and recommender_engine:
                    st.markdown("---")
                    st.markdown("### 🎯 AI-Powered Product Recommendations")
                    
                    try:
                        ai_recs = ai_engine.generate_ai_recommendations(customer_id, k=num_recommendations)
                        
                        if ai_recs:
                            for i, rec in enumerate(ai_recs, 1):
                                col1, col2, col3 = st.columns([3, 1, 1])
                                
                                with col1:
                                    st.markdown(f"**{i}. {rec.item_name}**")
                                    st.markdown(f"*Category: {rec.category}*")
                                    st.markdown(f"💡 **Reason:** {rec.reason}")
                                    if rec.behavioral_justification:
                                        st.caption(f"📊 {rec.behavioral_justification}")
                                    if rec.collaborative_reasoning:
                                        st.caption(f"👥 {rec.collaborative_reasoning}")
                                
                                with col2:
                                    st.metric("Score", f"{rec.score:.1f}")
                                
                                with col3:
                                    st.metric("Confidence", rec.confidence.title())
                                
                                if i < len(ai_recs):
                                    st.divider()
                        else:
                            st.info("No AI recommendations available for this customer.")
                    except Exception as e:
                        st.warning(f"Could not generate AI recommendations: {e}")
                
                # Standard recommendations if AI not available
                elif recommender_engine:
                    try:
                        recs = recommender_engine.recommend(customer_id, k=num_recommendations)
                        if recs:
                            st.markdown("### Product Recommendations")
                            for i, rec in enumerate(recs, 1):
                                feedback = feedback_engine.generate(customer_id, rec) if feedback_engine else "Recommended for you"
                                col1, col2 = st.columns([3, 1])
                                with col1:
                                    st.markdown(f"**{i}. {rec['item_name']}**")
                                    st.markdown(f"*{rec['category']}*")
                                    st.caption(f"💡 {feedback}")
                                with col2:
                                    st.metric("Score", f"{rec['score']:.1f}")
                                if i < len(recs):
                                    st.divider()
                    except Exception as e:
                        st.warning(f"Could not generate recommendations: {e}")
            
            with tab5:
                st.header("📈 Data Visualizations")
                
                visual_data = analytics.get('visual_data', {})
                
                # Category Distribution
                col1, col2 = st.columns(2)
                
                with col1:
                    category_chart = create_category_distribution_chart(
                        visual_data.get('category_distribution', [])
                    )
                    if category_chart:
                        st.plotly_chart(category_chart, use_container_width=True)
                
                with col2:
                    funnel_chart = create_conversion_funnel_chart(
                        visual_data.get('conversion_funnel', [])
                    )
                    if funnel_chart:
                        st.plotly_chart(funnel_chart, use_container_width=True)
                
                # Hourly Activity
                activity_chart = create_hourly_activity_chart(
                    visual_data.get('hourly_activity_heatmap', [])
                )
                if activity_chart:
                    st.plotly_chart(activity_chart, use_container_width=True)
                
                # Interest Trend
                col3, col4 = st.columns(2)
                
                with col3:
                    trend_chart = create_interest_trend_chart(
                        visual_data.get('interest_trend', [])
                    )
                    if trend_chart:
                        st.plotly_chart(trend_chart, use_container_width=True)
                
                with col4:
                    retention_chart = create_retention_curve_chart(
                        visual_data.get('retention_curve', [])
                    )
                    if retention_chart:
                        st.plotly_chart(retention_chart, use_container_width=True)
                
                # Lifetime Value Details
                clv = visual_data.get('lifetime_value_estimate', {})
                if clv:
                    st.markdown("### Customer Lifetime Value Details")
                    clv_col1, clv_col2, clv_col3, clv_col4 = st.columns(4)
                    
                    with clv_col1:
                        st.metric("Current Value", f"${clv.get('current_value', 0):,.2f}")
                    with clv_col2:
                        st.metric("Estimated CLV", f"${clv.get('estimated_clv', 0):,.2f}")
                    with clv_col3:
                        st.metric("Remaining Years", f"{clv.get('remaining_years', 0):.1f}")
                    with clv_col4:
                        st.metric("Annual Projected", f"${clv.get('annual_projected_value', 0):,.2f}")
    
    else:
        # Welcome screen
        st.info("👈 Select a customer ID from the sidebar and click 'Analyze Customer' to get started!")
        
        # Show summary statistics
        st.markdown("### 📊 Dataset Overview")
        customer_df = load_customer_data()
        if customer_df is not None:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Customers", len(customer_df))
            
            with col2:
                avg_purchase = customer_df['Purchase Amount (USD)'].mean()
                st.metric("Avg Purchase Amount", f"${avg_purchase:.2f}")
            
            with col3:
                avg_rating = customer_df['Review Rating'].mean()
                st.metric("Avg Review Rating", f"{avg_rating:.2f}")
            
            with col4:
                subscription_rate = (customer_df['Subscription Status'] == 'Yes').mean() * 100
                st.metric("Subscription Rate", f"{subscription_rate:.1f}%")

if __name__ == "__main__":
    main()


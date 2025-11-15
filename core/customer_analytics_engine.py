"""
Customer Behavior Analytics Engine
Analyzes customer data to provide business insights, personas, and predictive analytics
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from collections import Counter
import json
from typing import Dict, List, Any, Optional

class CustomerAnalyticsEngine:
    def __init__(self, data_source):
        """Initialize the analytics engine with customer data"""
        if isinstance(data_source, str):
            # If it's a file path, read the CSV
            self.df = pd.read_csv(data_source)
            self.df.columns = [col.strip() for col in self.df.columns]
        elif isinstance(data_source, pd.DataFrame):
            # If it's already a DataFrame, use it directly
            self.df = data_source.copy()
            self.df.columns = [col.strip() for col in self.df.columns]
        else:
            raise ValueError("data_source must be either a file path string or a pandas DataFrame")
        
        self.preprocess_data()
        
    def preprocess_data(self):
        """Clean and preprocess the customer data"""
        # Convert categorical columns
        self.df['Age'] = pd.to_numeric(self.df['Age'], errors='coerce')
        self.df['Purchase Amount (USD)'] = pd.to_numeric(self.df['Purchase Amount (USD)'], errors='coerce')
        self.df['Review Rating'] = pd.to_numeric(self.df['Review Rating'], errors='coerce')
        self.df['Previous Purchases'] = pd.to_numeric(self.df['Previous Purchases'], errors='coerce')
        
        # Create derived features
        self.df['Customer_Value'] = self.df['Purchase Amount (USD)'] * self.df['Previous Purchases']
        self.df['Price_Sensitivity'] = self.df['Discount Applied'].map({'Yes': 1, 'No': 0})
        self.df['Subscription_Loyalty'] = self.df['Subscription Status'].map({'Yes': 1, 'No': 0})
        
        # Map frequency to numeric
        frequency_map = {
            'Weekly': 52, 'Bi-Weekly': 26, 'Fortnightly': 26,
            'Monthly': 12, 'Quarterly': 4, 'Every 3 Months': 4,
            'Annually': 1
        }
        self.df['Purchase_Frequency_Numeric'] = self.df['Frequency of Purchases'].map(frequency_map)
        
    def analyze_customer(self, customer_id: str) -> Dict[str, Any]:
        """Analyze a specific customer and return comprehensive insights"""
        customer_data = self.df[self.df['Customer ID'] == int(customer_id)]
        
        if customer_data.empty:
            return {"error": "Customer not found"}
        
        # Get customer profile
        customer = customer_data.iloc[0]
        
        # Generate persona
        persona = self.generate_persona(customer, customer_data)
        
        # Generate behavior summary
        behavior_summary = self.generate_behavior_summary(customer, customer_data)
        
        # Generate predictive analytics
        predictive_analytics = self.generate_predictive_analytics(customer, customer_data)
        
        # Generate visual data
        visual_data = self.generate_visual_data(customer, customer_data)
        
        # Generate business recommendations
        business_recommendations = self.generate_business_recommendations(customer, customer_data)
        
        # Convert numpy/pandas types to native Python types for JSON serialization
        return {
            "user_id": str(customer_id),
            "persona": persona,
            "behavior_summary": behavior_summary,
            "predictive_analytics": predictive_analytics,
            "visual_data": visual_data,
            "business_recommendations": business_recommendations
        }
    
    def generate_persona(self, customer: pd.Series, customer_data: pd.DataFrame) -> Dict[str, Any]:
        """Generate customer persona based on behavior patterns using actual customer data"""
        
        # Get actual customer data
        purchase_amount = float(customer['Purchase Amount (USD)'])
        frequency = float(customer['Purchase_Frequency_Numeric'])
        review_rating = float(customer['Review Rating'])
        previous_purchases = int(customer['Previous Purchases'])
        subscription = customer['Subscription Status']
        discount_usage = customer['Discount Applied']
        age = int(customer['Age'])
        category = customer['Category']
        location = customer['Location']
        
        # Enhanced persona classification with unique combinations
        if purchase_amount >= 90 and frequency >= 20 and review_rating >= 4.5:
            persona_label = "Ultra Premium Advocate"
            description = f"Exceptional customer from {location} - highest value with {previous_purchases} purchases and {review_rating} rating"
        elif purchase_amount >= 80 and frequency >= 12 and subscription == 'Yes' and review_rating >= 4.0:
            persona_label = "Premium Loyalist"
            description = f"High-value {category} enthusiast from {location} with strong brand loyalty and {frequency} annual purchases"
        elif purchase_amount >= 70 and previous_purchases >= 30:
            persona_label = "Experienced High-Value"
            description = f"Mature customer from {location} with {previous_purchases} purchases, prefers premium {category} items"
        elif discount_usage == 'Yes' and purchase_amount <= 35 and frequency >= 12:
            persona_label = "Deal Seeker Regular"
            description = f"Price-sensitive regular from {location} - shops frequently but seeks discounts on {category}"
        elif review_rating <= 3.0 and previous_purchases >= 20:
            persona_label = "Critical Long-term"
            description = f"Experienced but critical customer from {location} - {previous_purchases} purchases but {review_rating} rating indicates quality concerns"
        elif frequency >= 26 and purchase_amount >= 50:
            persona_label = "Frequent Quality Buyer"
            description = f"Regular purchaser from {location} - shops {frequency} times yearly, invests in quality {category}"
        elif age >= 60 and purchase_amount >= 60:
            persona_label = "Mature Premium"
            description = f"Mature customer from {location} - prefers premium {category} items with ${purchase_amount} average spend"
        elif age <= 25 and frequency >= 12:
            persona_label = "Young Active Shopper"
            description = f"Young customer from {location} - highly active with {frequency} annual purchases, trendy {category} preferences"
        elif purchase_amount >= 80:
            persona_label = "High-Value Occasional"
            description = f"Occasional but high-value customer from {location} - spends ${purchase_amount} on premium {category}"
        elif review_rating >= 4.5 and previous_purchases >= 15:
            persona_label = "Satisfied Advocate"
            description = f"Highly satisfied customer from {location} - {review_rating} rating with {previous_purchases} purchases, potential brand advocate"
        else:
            persona_label = "Casual Explorer"
            description = f"Moderate engagement customer from {location} - explores {category} with occasional ${purchase_amount} purchases"
        
        # Generate personalized behavioral traits based on actual data
        traits = []
        
        # Review-based traits
        if review_rating >= 4.5:
            traits.append(f"Exceptionally satisfied ({review_rating}/5) - potential brand advocate")
        elif review_rating >= 4.0:
            traits.append(f"Highly satisfied ({review_rating}/5) with product quality")
        elif review_rating <= 2.5:
            traits.append(f"Critical of product quality ({review_rating}/5) - needs attention")
        elif review_rating <= 3.5:
            traits.append(f"Moderately satisfied ({review_rating}/5) - room for improvement")
        
        # Subscription and loyalty traits
        if subscription == 'Yes':
            traits.append("Values loyalty programs and exclusive benefits")
        
        # Price sensitivity traits
        if discount_usage == 'Yes' and purchase_amount >= 60:
            traits.append(f"Deal-seeking premium buyer - spends ${purchase_amount} with discounts")
        elif discount_usage == 'Yes':
            traits.append(f"Price-conscious shopper - seeks deals on ${purchase_amount} purchases")
        elif purchase_amount >= 80:
            traits.append(f"Premium buyer - pays full price for quality ${purchase_amount} items")
        
        # Purchase behavior traits
        if frequency >= 26:
            traits.append(f"Very frequent buyer - shops {frequency} times per year")
        elif frequency >= 12:
            traits.append(f"Regular purchaser - shops {frequency} times per year")
        elif frequency <= 4:
            traits.append(f"Occasional buyer - shops only {frequency} times per year")
        
        # Experience traits
        if previous_purchases >= 40:
            traits.append(f"Highly experienced - {previous_purchases} previous purchases")
        elif previous_purchases >= 20:
            traits.append(f"Established customer - {previous_purchases} previous purchases")
        elif previous_purchases <= 5:
            traits.append(f"New customer - only {previous_purchases} previous purchases")
        
        # Category-specific traits
        if category == 'Clothing':
            traits.append(f"Fashion-focused - prefers {category} items")
        elif category == 'Accessories':
            traits.append(f"Style-conscious - shops {category} to complete looks")
        elif category == 'Footwear':
            traits.append(f"Quality-focused - invests in {category}")
        elif category == 'Outerwear':
            traits.append(f"Practical buyer - purchases {category} for function")
        
        # Age and demographic traits
        if age >= 60:
            traits.append(f"Mature buyer ({age}) - established preferences and loyal")
        elif age <= 25:
            traits.append(f"Young shopper ({age}) - trend-conscious and experimental")
        elif age >= 40:
            traits.append(f"Middle-aged buyer ({age}) - quality and value focused")
        
        # Location-based insights
        if location in ['New York', 'California', 'Massachusetts']:
            traits.append(f"Metropolitan buyer from {location} - likely trend-conscious")
        elif location in ['Texas', 'Florida', 'Georgia']:
            traits.append(f"Southern customer from {location} - traditional preferences")
        elif location in ['Montana', 'Wyoming', 'North Dakota']:
            traits.append(f"Rural customer from {location} - practical and value-focused")
        
        return {
            "label": persona_label,
            "description": description,
            "traits": traits[:6]  # Limit to 6 traits
        }
    
    def generate_behavior_summary(self, customer: pd.Series, customer_data: pd.DataFrame) -> Dict[str, Any]:
        """Generate comprehensive behavior summary using actual customer data"""
        
        # Get actual customer data
        category = customer['Category']
        purchase_amount = float(customer['Purchase Amount (USD)'])
        frequency = float(customer['Purchase_Frequency_Numeric'])
        review_rating = float(customer['Review Rating'])
        previous_purchases = int(customer['Previous Purchases'])
        discount_usage = customer['Discount Applied']
        subscription = customer['Subscription Status']
        location = customer['Location']
        season = customer['Season']
        shipping_type = customer['Shipping Type']
        
        # Personalized top categories based on actual purchase
        top_categories = [category]
        
        # Dynamic price range based on actual spending
        if purchase_amount >= 90:
            price_range = f"Ultra Premium (${purchase_amount}+)"
        elif purchase_amount >= 70:
            price_range = f"Premium ($70-${purchase_amount})"
        elif purchase_amount >= 50:
            price_range = f"Mid-range ($50-${purchase_amount})"
        elif purchase_amount >= 30:
            price_range = f"Budget ($30-${purchase_amount})"
        else:
            price_range = f"Value Seeker (<$30) - Current: ${purchase_amount}"
        
        # Personalized time preferences based on demographics and behavior
        preferred_hours = self.get_personalized_shopping_hours(customer)
        
        # Personalized time spent based on engagement
        time_spent = self.estimate_personalized_time_spent(customer)
        
        # Activity trend based on actual frequency and purchase history
        if frequency >= 26:
            activity_trend = f"Very High Activity - {frequency} purchases/year"
        elif frequency >= 16:
            activity_trend = f"High Activity - {frequency} purchases/year"
        elif frequency >= 8:
            activity_trend = f"Moderate Activity - {frequency} purchases/year"
        elif frequency >= 4:
            activity_trend = f"Low Activity - {frequency} purchases/year"
        else:
            activity_trend = f"Minimal Activity - {frequency} purchases/year"
        
        # Purchase pattern based on frequency vs previous purchases
        purchase_pattern = self.analyze_personalized_purchase_pattern(customer)
        
        # Price sensitivity based on discount usage and spending
        if discount_usage == 'Yes' and purchase_amount >= 60:
            price_sensitivity = f"Deal-Seeking Premium (uses discounts on ${purchase_amount} items)"
        elif discount_usage == 'Yes':
            price_sensitivity = f"Price Sensitive (uses discounts on ${purchase_amount} items)"
        elif purchase_amount >= 80:
            price_sensitivity = f"Premium Buyer (pays full ${purchase_amount} for quality)"
        else:
            price_sensitivity = f"Value Conscious (spends ${purchase_amount} without discounts)"
        
        # Engagement level based on multiple factors
        if review_rating >= 4.5 and previous_purchases >= 30 and subscription == 'Yes':
            engagement_level = f"Exceptionally High - {review_rating}/5 rating, {previous_purchases} purchases, subscriber"
        elif review_rating >= 4.0 and previous_purchases >= 20:
            engagement_level = f"High - {review_rating}/5 rating, {previous_purchases} purchases"
        elif review_rating >= 3.5 and previous_purchases >= 10:
            engagement_level = f"Medium - {review_rating}/5 rating, {previous_purchases} purchases"
        elif review_rating <= 3.0:
            engagement_level = f"Low - {review_rating}/5 rating indicates dissatisfaction"
        else:
            engagement_level = f"Developing - {review_rating}/5 rating, {previous_purchases} purchases"
        
        return {
            "top_categories": top_categories,
            "preferred_price_range": price_range,
            "most_active_time_window": preferred_hours,
            "time_spent_patterns": time_spent,
            "activity_trend": activity_trend,
            "purchase_browse_pattern": purchase_pattern,
            "price_sensitivity_level": price_sensitivity,
            "engagement_level": engagement_level
        }
    
    def generate_predictive_analytics(self, customer: pd.Series, customer_data: pd.DataFrame) -> Dict[str, Any]:
        """Generate personalized predictive analytics using actual customer data"""
        
        # Get actual customer data
        frequency = float(customer['Purchase_Frequency_Numeric'])
        review_rating = float(customer['Review Rating'])
        subscription = customer['Subscription Status']
        purchase_amount = float(customer['Purchase Amount (USD)'])
        previous_purchases = int(customer['Previous Purchases'])
        discount_usage = customer['Discount Applied']
        age = int(customer['Age'])
        category = customer['Category']
        
        # Personalized next action prediction
        if frequency >= 20 and review_rating >= 4.5 and purchase_amount >= 80:
            next_action = "High-Value Purchase"
            purchase_probability = 95
        elif frequency >= 16 and review_rating >= 4.0 and subscription == 'Yes':
            next_action = "Premium Purchase"
            purchase_probability = 88
        elif frequency >= 12 and review_rating >= 4.0:
            next_action = "Regular Purchase"
            purchase_probability = 85
        elif frequency >= 8 and review_rating >= 3.5:
            next_action = "Considered Purchase"
            purchase_probability = 70
        elif review_rating >= 3.0 and previous_purchases >= 10:
            next_action = "Browse with Intent"
            purchase_probability = 50
        elif review_rating <= 2.5 and previous_purchases >= 15:
            next_action = "Churn Risk - Quality Concern"
            purchase_probability = 25
        else:
            next_action = "Churn Risk"
            purchase_probability = 15
        
        # Personalized category shift prediction
        current_category = customer['Category']
        category_shift = self.predict_personalized_category_shift(current_category, customer)
        
        # Personalized churn risk calculation
        churn_risk = self.calculate_personalized_churn_risk(customer)
        
        # Personalized revenue potential
        customer_value = float(customer['Customer_Value'])
        if customer_value >= 4000 and review_rating >= 4.5:
            revenue_potential = "Exceptional"
        elif customer_value >= 2500 and review_rating >= 4.0:
            revenue_potential = "High"
        elif customer_value >= 1500:
            revenue_potential = "Medium"
        elif customer_value >= 500:
            revenue_potential = "Developing"
        else:
            revenue_potential = "Low"
        
        return {
            "next_likely_action": next_action,
            "purchase_probability_percent": int(purchase_probability),
            "category_shift_prediction": category_shift,
            "churn_risk_percent": churn_risk,
            "revenue_potential": revenue_potential
        }
    
    def generate_visual_data(self, customer: pd.Series, customer_data: pd.DataFrame) -> Dict[str, Any]:
        """Generate data for visualizations"""
        
        # Category distribution (for this customer)
        category_dist = self.get_category_distribution(customer)
        
        # Hourly activity heatmap (simulated)
        hourly_activity = self.generate_hourly_activity_heatmap(customer)
        
        # Interest trend (based on purchase frequency and amount)
        interest_trend = self.generate_interest_trend(customer)
        
        # Conversion funnel
        conversion_funnel = self.generate_conversion_funnel(customer)
        
        # Retention curve (based on previous purchases)
        retention_curve = self.generate_retention_curve(customer)
        
        # Lifetime value estimate
        lifetime_value = self.estimate_lifetime_value(customer)
        
        return {
            "category_distribution": category_dist,
            "hourly_activity_heatmap": hourly_activity,
            "interest_trend": interest_trend,
            "conversion_funnel": conversion_funnel,
            "retention_curve": retention_curve,
            "lifetime_value_estimate": lifetime_value
        }
    
    def generate_business_recommendations(self, customer: pd.Series, customer_data: pd.DataFrame) -> List[Dict[str, Any]]:
        """Generate personalized actionable business recommendations based on actual customer data"""
        
        recommendations = []
        
        # Get actual customer characteristics
        persona = self.generate_persona(customer, customer_data)
        purchase_amount = float(customer['Purchase Amount (USD)'])
        frequency = float(customer['Purchase_Frequency_Numeric'])
        review_rating = float(customer['Review Rating'])
        subscription = customer['Subscription Status']
        discount_usage = customer['Discount Applied']
        previous_purchases = int(customer['Previous Purchases'])
        age = int(customer['Age'])
        category = customer['Category']
        location = customer['Location']
        season = customer['Season']
        shipping_type = customer['Shipping Type']
        
        # Personalized marketing recommendations
        if review_rating <= 2.0:
            recommendations.append({
                "type": "Marketing",
                "priority": "Critical",
                "action": f"Immediate Quality Intervention for {category}",
                "description": f"Customer extremely dissatisfied ({review_rating}/5) with {category}. Personal follow-up call, quality replacement, and satisfaction survey required."
            })
        elif review_rating <= 3.0:
            recommendations.append({
                "type": "Marketing",
                "priority": "High", 
                "action": f"Quality Improvement Focus for {category}",
                "description": f"Customer shows dissatisfaction ({review_rating}/5) with {category}. Send quality survey, offer exchange, and provide {location}-specific customer service."
            })
        
        if discount_usage == 'Yes' and purchase_amount >= 70:
            recommendations.append({
                "type": "Marketing", 
                "priority": "Medium",
                "action": f"Premium Deal Strategy for {category}",
                "description": f"Deal-seeking premium customer spends ${purchase_amount} on {category}. Offer exclusive member discounts, bundle deals, and early access to sales."
            })
        elif discount_usage == 'Yes' and purchase_amount <= 35:
            recommendations.append({
                "type": "Marketing", 
                "priority": "High",
                "action": f"Value-Based Promotions for {category}",
                "description": f"Price-sensitive customer seeks deals on ${purchase_amount} {category} purchases. Target with clearance sales, seasonal promotions, and value-focused campaigns in {location}."
            })
        
        # Personalized retention strategies
        if frequency <= 3 and previous_purchases >= 10:
            recommendations.append({
                "type": "Retention",
                "priority": "Critical",
                "action": f"Urgent Re-engagement for {category}",
                "description": f"Experienced customer ({previous_purchases} purchases) with declining activity ({frequency} freq). Immediate intervention with personalized offers, feedback survey, and {category} recommendations."
            })
        elif frequency <= 6 and previous_purchases >= 20:
            recommendations.append({
                "type": "Retention",
                "priority": "High",
                "action": f"VIP Re-engagement Campaign for {category}",
                "description": f"Valuable customer ({previous_purchases} purchases) showing reduced activity ({frequency} freq). Launch targeted email campaigns, loyalty incentives, and exclusive {category} previews."
            })
        
        if subscription == 'No' and purchase_amount >= 60 and review_rating >= 4.0:
            recommendations.append({
                "type": "Retention",
                "priority": "High", 
                "action": f"Premium Subscription Upsell for {category}",
                "description": f"High-value customer (${purchase_amount} avg) without subscription. Promote premium membership benefits, exclusive {category} access, and personalized shopping assistance in {location}."
            })
        
        # Personalized upsell/cross-sell opportunities
        if purchase_amount >= 90 and review_rating >= 4.0:
            recommendations.append({
                "type": "Upsell",
                "priority": "High",
                "action": f"Luxury {category} Recommendations",
                "description": f"Ultra-premium customer (${purchase_amount} avg) with high satisfaction. Recommend luxury {category} collections, limited editions, and exclusive designer collaborations."
            })
        elif purchase_amount >= 70:
            recommendations.append({
                "type": "Upsell",
                "priority": "Medium",
                "action": f"Premium {category} Upgrade", 
                "description": f"Premium customer (${purchase_amount} avg). Recommend higher-end {category} products, exclusive collections, and premium brand partnerships."
            })
        
        if previous_purchases >= 35:
            recommendations.append({
                "type": "Cross-sell",
                "priority": "High",
                "action": f"Advanced Category Expansion beyond {category}",
                "description": f"Highly experienced customer ({previous_purchases} purchases). Introduce complementary categories, lifestyle bundles, and complete outfit solutions beyond {category}."
            })
        elif previous_purchases >= 20:
            recommendations.append({
                "type": "Cross-sell",
                "priority": "Medium",
                "action": f"Complementary {category} Categories",
                "description": f"Established customer ({previous_purchases} purchases). Introduce complementary categories that pair well with {category} based on {location} preferences."
            })
        
        # Personalized product-level actions
        if review_rating >= 4.5 and previous_purchases >= 25:
            recommendations.append({
                "type": "Product",
                "priority": "Medium",
                "action": f"Brand Advocate Program for {category}",
                "description": f"Highly satisfied customer ({review_rating}/5) with extensive history ({previous_purchases} purchases). Encourage reviews, referrals, user-generated content, and {category} testimonials."
            })
        elif review_rating >= 4.0:
            recommendations.append({
                "type": "Product",
                "priority": "Low",
                "action": f"Satisfaction Leverage for {category}",
                "description": f"Satisfied customer ({review_rating}/5) with {category} purchases. Request reviews, offer referral incentives, and showcase their {category} preferences."
            })
        
        # Personalized segment-level strategies
        if "Bargain Hunter" in persona['label']:
            recommendations.append({
                "type": "Segment",
                "priority": "High",
                "action": f"Deal-Focused {category} Campaigns",
                "description": f"Price-sensitive {category} buyer. Target with flash sales, clearance events, seasonal promotions, and discount-focused messaging for {location} market."
            })
        elif "Premium Loyalist" in persona['label']:
            recommendations.append({
                "type": "Segment",
                "priority": "High",
                "action": f"VIP {category} Treatment",
                "description": f"Premium {category} customer from {location}. Offer exclusive access, personal shopping assistance, premium customer service, and early access to new {category} collections."
            })
        elif "Ultra Premium Advocate" in persona['label']:
            recommendations.append({
                "type": "Segment",
                "priority": "Critical",
                "action": f"Ultra-Premium {category} Experience",
                "description": f"Exceptional customer for {category}. Provide white-glove service, exclusive previews, personal stylist for {category}, and invitation-only events in {location}."
            })
        
        # Location-specific recommendations
        if location in ['New York', 'California', 'Massachusetts']:
            recommendations.append({
                "type": "Geographic",
                "priority": "Medium",
                "action": f"Metropolitan {category} Strategy",
                "description": f"Trend-conscious {location} customer. Focus on latest {category} trends, fast shipping, urban lifestyle marketing, and tech-savvy shopping experience."
            })
        elif location in ['Texas', 'Florida', 'Georgia']:
            recommendations.append({
                "type": "Geographic", 
                "priority": "Medium",
                "action": f"Southern {category} Approach",
                "description": f"Traditional {location} customer. Emphasize quality, value, traditional styles, family-oriented marketing, and community engagement for {category}."
            })
        
        return recommendations
    
    # Helper methods
    def get_personalized_shopping_hours(self, customer: pd.Series) -> str:
        """Generate personalized shopping hours based on actual customer data"""
        age = int(customer['Age'])
        frequency = float(customer['Purchase_Frequency_Numeric'])
        location = customer['Location']
        category = customer['Category']
        
        # Metropolitan areas - more flexible hours
        metro_locations = ['New York', 'California', 'Massachusetts', 'Texas', 'Florida']
        
        if location in metro_locations:
            if age <= 30:
                return f"Late Evening (8PM-11PM) - Young {category} shopper in {location}"
            elif age >= 60:
                return f"Early Morning (7AM-10AM) - Mature {category} buyer in {location}"
            else:
                return f"Lunch Hours (12PM-3PM) - Working professional in {location}"
        else:
            # Rural/suburban areas - traditional hours
            if age >= 50:
                return f"Morning (9AM-12PM) - Traditional {category} shopper from {location}"
            elif age <= 25:
                return f"Afternoon (3PM-6PM) - Student {category} buyer from {location}"
            else:
                return f"Evening (5PM-8PM) - After-work {category} shopper from {location}"
    
    def estimate_personalized_time_spent(self, customer: pd.Series) -> str:
        """Estimate personalized time spent based on actual engagement data"""
        review_rating = float(customer['Review Rating'])
        previous_purchases = int(customer['Previous Purchases'])
        frequency = float(customer['Purchase_Frequency_Numeric'])
        category = customer['Category']
        
        # Calculate engagement score
        engagement_score = (review_rating * 20) + (previous_purchases * 0.5) + (frequency * 2)
        
        if engagement_score >= 120:
            return f"Very High (15-20 min) - Deep {category} research, reads reviews, compares options"
        elif engagement_score >= 80:
            return f"High (10-15 min) - Thoughtful {category} selection, quality focused"
        elif engagement_score >= 50:
            return f"Medium (5-10 min) - Efficient {category} shopping, knows what they want"
        else:
            return f"Quick (<5 min) - Fast {category} decisions, impulse or urgent needs"
    
    def estimate_time_spent(self, customer: pd.Series) -> str:
        """Estimate time spent based on engagement level"""
        review_rating = customer['Review Rating']
        if review_rating >= 4.0:
            return "High (10-15 minutes per session)"
        elif review_rating >= 3.5:
            return "Medium (5-10 minutes per session)"
        else:
            return "Low (<5 minutes per session)"
    
    def analyze_personalized_purchase_pattern(self, customer: pd.Series) -> str:
        """Analyze personalized purchase vs browse pattern based on actual data"""
        frequency = float(customer['Purchase_Frequency_Numeric'])
        previous_purchases = int(customer['Previous Purchases'])
        review_rating = float(customer['Review Rating'])
        category = customer['Category']
        
        # Calculate conversion likelihood based on multiple factors
        conversion_score = (frequency * 2) + (previous_purchases * 0.3) + (review_rating * 5)
        
        if conversion_score >= 80:
            return f"Purchase-Driven - High conversion for {category} ({frequency} freq, {previous_purchases} prev)"
        elif conversion_score >= 50:
            return f"Balanced Shopper - Researches then buys {category} ({frequency} freq, {review_rating} rating)"
        elif conversion_score >= 30:
            return f"Considered Buyer - Takes time before {category} purchases ({previous_purchases} experience)"
        else:
            return f"Browse-Heavy - Explores {category} but buys infrequently ({frequency} low freq)"
    
    def analyze_purchase_pattern(self, customer: pd.Series) -> str:
        """Analyze purchase vs browse pattern"""
        frequency = customer['Purchase_Frequency_Numeric']
        if frequency >= 20:
            return "Purchase-focused (high conversion)"
        elif frequency >= 8:
            return "Balanced browse and purchase"
        else:
            return "Browse-focused (low conversion)"
    
    def predict_personalized_category_shift(self, current_category: str, customer: pd.Series) -> str:
        """Predict personalized category shifts based on actual customer behavior"""
        purchase_amount = float(customer['Purchase Amount (USD)'])
        review_rating = float(customer['Review Rating'])
        previous_purchases = int(customer['Previous Purchases'])
        age = int(customer['Age'])
        
        # Personalized category predictions based on customer profile
        if purchase_amount >= 80 and review_rating >= 4.0:
            # High-value satisfied customer
            premium_shifts = {
                'Clothing': 'Premium Accessories or Luxury Footwear',
                'Footwear': 'Designer Clothing or Premium Accessories', 
                'Accessories': 'High-end Clothing or Premium Footwear',
                'Outerwear': 'Premium Clothing or Designer Accessories'
            }
            return premium_shifts.get(current_category, 'Premium cross-category exploration')
        elif purchase_amount <= 40:
            # Budget-conscious customer
            budget_shifts = {
                'Clothing': 'Basic Accessories or Sale Footwear',
                'Footwear': 'Discount Clothing or Value Accessories', 
                'Accessories': 'Affordable Clothing or Budget Footwear',
                'Outerwear': 'Seasonal Clothing or Practical Accessories'
            }
            return budget_shifts.get(current_category, 'Value-focused cross-category exploration')
        elif age >= 50:
            # Mature customer preferences
            mature_shifts = {
                'Clothing': 'Classic Accessories or Comfort Footwear',
                'Footwear': 'Quality Clothing or Functional Accessories', 
                'Accessories': 'Timeless Clothing or Reliable Footwear',
                'Outerwear': 'Practical Clothing or Weather Accessories'
            }
            return mature_shifts.get(current_category, 'Quality-focused cross-category exploration')
        elif age <= 25:
            # Young customer preferences
            young_shifts = {
                'Clothing': 'Trendy Accessories or Fashion Footwear',
                'Footwear': 'Stylish Clothing or Statement Accessories', 
                'Accessories': 'Fashion-forward Clothing or Trendy Footwear',
                'Outerwear': 'Contemporary Clothing or Urban Accessories'
            }
            return young_shifts.get(current_category, 'Trend-focused cross-category exploration')
        else:
            # Default based on current category
            category_shifts = {
                'Clothing': 'Footwear or Accessories',
                'Footwear': 'Clothing or Accessories', 
                'Accessories': 'Clothing or Footwear',
                'Outerwear': 'Clothing or Accessories'
            }
            return category_shifts.get(current_category, 'Cross-category exploration')
    
    def predict_category_shift(self, current_category: str, customer: pd.Series) -> str:
        """Predict potential category shifts based on behavior"""
        # Simplified prediction based on current category and customer behavior
        category_shifts = {
            'Clothing': 'Footwear or Accessories',
            'Footwear': 'Clothing or Accessories', 
            'Accessories': 'Clothing or Footwear',
            'Outerwear': 'Clothing or Accessories'
        }
        return category_shifts.get(current_category, 'Cross-category exploration')
    
    def calculate_personalized_churn_risk(self, customer: pd.Series) -> int:
        """Calculate personalized churn risk percentage based on actual customer data"""
        frequency = float(customer['Purchase_Frequency_Numeric'])
        review_rating = float(customer['Review Rating'])
        subscription = customer['Subscription Status']
        purchase_amount = float(customer['Purchase Amount (USD)'])
        previous_purchases = int(customer['Previous Purchases'])
        discount_usage = customer['Discount Applied']
        age = int(customer['Age'])
        
        risk_score = 0
        
        # Frequency-based risk (most important factor)
        if frequency <= 2:
            risk_score += 50  # Very high risk for minimal activity
        elif frequency <= 4:
            risk_score += 35  # High risk for low activity
        elif frequency <= 8:
            risk_score += 20  # Medium risk for moderate activity
        elif frequency >= 20:
            risk_score -= 10  # Low risk for very high activity
        
        # Review rating risk
        if review_rating <= 2.0:
            risk_score += 40  # Critical satisfaction issues
        elif review_rating <= 2.5:
            risk_score += 30  # Major satisfaction concerns
        elif review_rating <= 3.0:
            risk_score += 20  # Moderate dissatisfaction
        elif review_rating <= 3.5:
            risk_score += 10  # Minor concerns
        elif review_rating >= 4.5:
            risk_score -= 15  # Very satisfied, low risk
        
        # Purchase amount risk (value-based)
        if purchase_amount <= 20 and previous_purchases <= 5:
            risk_score += 15  # Low-value, new customer
        elif purchase_amount >= 80 and previous_purchases >= 20:
            risk_score -= 10  # High-value, experienced customer
        
        # Subscription impact
        if subscription == 'No':
            risk_score += 10  # No loyalty program
        else:
            risk_score -= 5   # Has loyalty program
        
        # Age-based adjustments
        if age >= 65 and frequency <= 6:
            risk_score += 10  # Older customers with low frequency
        elif age <= 25 and review_rating <= 3.0:
            risk_score += 15  # Young customers with poor satisfaction
        
        # Previous purchase history
        if previous_purchases <= 3:
            risk_score += 15  # Very new customer
        elif previous_purchases >= 40:
            risk_score -= 15  # Very experienced customer
        
        return int(max(0, min(risk_score, 95)))  # Cap between 0-95%
    
    def calculate_churn_risk(self, customer: pd.Series) -> int:
        """Calculate churn risk percentage"""
        frequency = float(customer['Purchase_Frequency_Numeric'])
        review_rating = float(customer['Review Rating'])
        subscription = customer['Subscription Status']
        
        risk_score = 0
        
        if frequency <= 4:
            risk_score += 40
        elif frequency <= 8:
            risk_score += 20
        
        if review_rating <= 3.0:
            risk_score += 30
        elif review_rating <= 3.5:
            risk_score += 15
        
        if subscription == 'No':
            risk_score += 10
        
        return int(min(risk_score, 90))  # Cap at 90% and convert to int
    
    def get_category_distribution(self, customer: pd.Series) -> List[Dict[str, Any]]:
        """Generate category distribution data for pie chart"""
        current_category = customer['Category']
        # Simulate distribution based on customer behavior
        categories = ['Clothing', 'Footwear', 'Accessories', 'Outerwear']
        values = [40, 25, 20, 15]  # Base distribution
        
        # Adjust based on current category
        category_index = categories.index(current_category) if current_category in categories else 0
        values[category_index] += 20  # Boost current category
        
        # Normalize to 100%
        total = sum(values)
        values = [v/total*100 for v in values]
        
        return [
            {"category": cat, "value": round(val, 1), "percentage": round(val, 1)}
            for cat, val in zip(categories, values)
        ]
    
    def generate_hourly_activity_heatmap(self, customer: pd.Series) -> List[Dict[str, Any]]:
        """Generate hourly activity data for heatmap"""
        age = customer['Age']
        
        # Generate activity pattern based on age group
        if age >= 50:
            activity_pattern = [0.1, 0.1, 0.1, 0.1, 0.2, 0.4, 0.7, 0.8, 0.9, 0.8, 0.6, 0.5,
                               0.4, 0.3, 0.3, 0.2, 0.2, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]
        elif age <= 30:
            activity_pattern = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7,
                               0.8, 0.7, 0.6, 0.5, 0.6, 0.8, 0.9, 0.8, 0.6, 0.4, 0.2, 0.1]
        else:
            activity_pattern = [0.1, 0.1, 0.1, 0.1, 0.1, 0.2, 0.3, 0.5, 0.7, 0.8, 0.9, 0.8,
                               0.7, 0.6, 0.5, 0.4, 0.5, 0.6, 0.7, 0.6, 0.4, 0.3, 0.2, 0.1]
        
        return [
            {"hour": i, "activity": round(activity_pattern[i], 2)}
            for i in range(24)
        ]
    
    def generate_interest_trend(self, customer: pd.Series) -> List[Dict[str, Any]]:
        """Generate interest trend data for line chart"""
        # Simulate 30-day trend
        base_interest = customer['Purchase_Frequency_Numeric'] / 52  # Normalize
        
        trend_data = []
        for day in range(30):
            # Add some noise and trend
            trend_factor = 1 + (day * 0.01)  # Slight upward trend
            noise = np.random.normal(0, 0.1)
            interest = max(0, base_interest * trend_factor + noise)
            
            trend_data.append({
                "date": f"Day {day+1}",
                "interest_score": round(interest, 2)
            })
        
        return trend_data
    
    def generate_conversion_funnel(self, customer: pd.Series) -> List[Dict[str, Any]]:
        """Generate conversion funnel data"""
        # Simulate funnel based on customer behavior
        engagement_level = customer['Review Rating'] / 5.0
        frequency_factor = customer['Purchase_Frequency_Numeric'] / 52
        
        views = 100
        engagement = views * (0.3 + engagement_level * 0.4)
        cart_adds = engagement * (0.2 + frequency_factor * 0.3)
        purchases = cart_adds * (0.4 + engagement_level * 0.3)
        
        return [
            {"stage": "Product Views", "count": int(views), "percentage": 100},
            {"stage": "Engagement", "count": int(engagement), "percentage": int(engagement/views*100)},
            {"stage": "Cart Adds", "count": int(cart_adds), "percentage": int(cart_adds/views*100)},
            {"stage": "Purchases", "count": int(purchases), "percentage": int(purchases/views*100)}
        ]
    
    def generate_retention_curve(self, customer: pd.Series) -> List[Dict[str, Any]]:
        """Generate retention curve data"""
        previous_purchases = customer['Previous Purchases']
        frequency = customer['Purchase_Frequency_Numeric']
        
        # Simulate retention based on purchase history
        months = list(range(1, 13))
        base_retention = min(0.9, previous_purchases / 100)
        
        retention_data = []
        for month in months:
            # Retention decreases over time but is boosted by frequency
            decay_factor = 0.95 ** month
            frequency_boost = (frequency / 52) * 0.1
            retention = max(0.1, base_retention * decay_factor + frequency_boost)
            
            retention_data.append({
                "month": month,
                "retention_rate": round(retention, 3)
            })
        
        return retention_data
    
    def estimate_lifetime_value(self, customer: pd.Series) -> Dict[str, Any]:
        """Estimate customer lifetime value"""
        current_value = float(customer['Customer_Value'])
        frequency = float(customer['Purchase_Frequency_Numeric'])
        subscription = customer['Subscription Status']
        age = float(customer['Age'])
        
        # Estimate remaining customer lifespan (simplified)
        remaining_years = max(2.0, 5.0 - (age - 30.0) / 10.0)  # Younger customers have longer lifespan
        
        # Calculate CLV
        annual_value = current_value * frequency
        subscription_multiplier = 1.2 if subscription == 'Yes' else 1.0
        clv = annual_value * remaining_years * subscription_multiplier
        
        return {
            "current_value": round(current_value, 2),
            "estimated_clv": round(clv, 2),
            "remaining_years": round(remaining_years, 1),
            "annual_projected_value": round(annual_value * subscription_multiplier, 2)
        }
    
    def get_all_customers_summary(self) -> Dict[str, Any]:
        """Get summary statistics for all customers"""
        return {
            "total_customers": len(self.df),
            "average_purchase_amount": round(self.df['Purchase Amount (USD)'].mean(), 2),
            "average_review_rating": round(self.df['Review Rating'].mean(), 2),
            "subscription_rate": round((self.df['Subscription Status'] == 'Yes').mean() * 100, 1),
            "average_previous_purchases": round(self.df['Previous Purchases'].mean(), 1)
        }
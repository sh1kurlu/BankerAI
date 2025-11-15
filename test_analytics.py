#!/usr/bin/env python3
"""
Test script for Customer Analytics Engine
Demonstrates the analytics capabilities on sample customer data
"""

import pandas as pd
import json
from core.customer_analytics_engine import CustomerAnalyticsEngine

def test_analytics_engine():
    """Test the analytics engine with sample customer data"""
    print("🚀 Loading customer data...")
    
    # Load customer data
    df = pd.read_csv('/Users/meh2/CustomerAI/BankerAI/data/customer.csv')
    print(f"📊 Loaded {len(df)} customer records")
    
    # Initialize analytics engine
    engine = CustomerAnalyticsEngine(df)
    print("🔧 Analytics engine initialized")
    
    # Test with a specific customer
    sample_customer = df.iloc[100]  # Customer at index 100
    customer_id = sample_customer['Customer ID']
    
    print(f"\n🎯 Analyzing Customer ID: {customer_id}")
    print(f"Sample customer data:")
    for key, value in sample_customer.items():
        print(f"  {key}: {value}")
    
    # Generate comprehensive analytics
    print("\n🧠 Generating business insights...")
    analytics_result = engine.analyze_customer(customer_id)
    
    # Display results in formatted JSON
    print("\n" + "="*60)
    print("📈 BUSINESS INSIGHTS REPORT")
    print("="*60)
    print(json.dumps(analytics_result, indent=2, ensure_ascii=False))
    
    # Save results to file
    output_file = '/Users/meh2/CustomerAI/BankerAI/analytics_output.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(analytics_result, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Analytics results saved to: {output_file}")
    
    # Generate insights for multiple customers
    print("\n🔍 Generating batch analytics for top customers...")
    top_customers = df.nlargest(5, 'Purchase Amount (USD)')
    
    batch_results = []
    for _, customer in top_customers.iterrows():
        customer_analytics = engine.analyze_customer(customer['Customer ID'])
        batch_results.append({
            'customer_id': customer['Customer ID'],
            'purchase_amount': customer['Purchase Amount (USD)'],
            'analytics': customer_analytics
        })
    
    # Save batch results
    batch_file = '/Users/meh2/CustomerAI/BankerAI/batch_analytics.json'
    with open(batch_file, 'w', encoding='utf-8') as f:
        json.dump(batch_results, f, indent=2, ensure_ascii=False)
    
    print(f"📋 Batch analytics saved to: {batch_file}")
    
    # Generate summary statistics
    print("\n📊 GENERATING BUSINESS SUMMARY")
    print("-" * 40)
    
    total_customers = len(df)
    total_revenue = df['Purchase Amount (USD)'].sum()
    avg_purchase = df['Purchase Amount (USD)'].mean()
    high_value_customers = len(df[df['Purchase Amount (USD)'] > avg_purchase * 2])
    churn_risk_customers = len(df[df['Purchase Amount (USD)'] < df['Purchase Amount (USD)'].quantile(0.25)])
    
    print(f"Total Customers: {total_customers:,}")
    print(f"Total Revenue: ${total_revenue:,.2f}")
    print(f"Average Purchase: ${avg_purchase:.2f}")
    print(f"High-Value Customers: {high_value_customers:,}")
    print(f"Churn Risk Customers: {churn_risk_customers:,}")
    
    # Category analysis
    print(f"\n🏷️  TOP CATEGORIES BY REVENUE")
    print("-" * 30)
    category_revenue = df.groupby('Category')['Purchase Amount (USD)'].sum().sort_values(ascending=False)
    for category, revenue in category_revenue.head().items():
        print(f"{category}: ${revenue:,.2f}")
    
    print(f"\n✅ Analytics engine test completed successfully!")

if __name__ == "__main__":
    test_analytics_engine()
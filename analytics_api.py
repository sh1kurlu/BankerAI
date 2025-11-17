#!/usr/bin/env python3
"""
Customer Analytics API Server
Provides REST API endpoints for customer behavior analytics
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import json
from core.customer_analytics_engine import CustomerAnalyticsEngine
import os

app = Flask(__name__)
CORS(app)

# Global analytics engine instance
analytics_engine = None

def initialize_engine():
    """Initialize the analytics engine with customer data"""
    global analytics_engine
    try:
        # Load customer data using relative path
        base_dir = os.path.dirname(os.path.abspath(__file__))
        data_path = os.path.join(base_dir, 'data', 'customer.csv')
        df = pd.read_csv(data_path)
        analytics_engine = CustomerAnalyticsEngine(df)
        print("✅ Analytics engine initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to initialize analytics engine: {e}")
        return False

@app.route('/api/analyze/<customer_id>', methods=['GET'])
def analyze_customer(customer_id):
    """Analyze a specific customer and return comprehensive insights"""
    try:
        if not analytics_engine:
            return jsonify({"error": "Analytics engine not initialized"}), 500
        
        analysis_type = request.args.get('type', 'comprehensive')
        
        # Generate analytics
        result = analytics_engine.analyze_customer(customer_id)
        
        if "error" in result:
            return jsonify(result), 404
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": f"Analysis failed: {str(e)}"}), 500

@app.route('/api/customers', methods=['GET'])
def get_customers():
    """Get list of all customers with basic info"""
    try:
        if not analytics_engine:
            return jsonify({"error": "Analytics engine not initialized"}), 500
        
        # Get summary statistics
        summary = analytics_engine.get_all_customers_summary()
        
        # Get sample of customers
        df_sample = analytics_engine.df.head(50)
        customers = []
        
        for _, customer in df_sample.iterrows():
            customers.append({
                "customer_id": str(customer['Customer ID']),
                "age": int(customer['Age']),
                "gender": customer['Gender'],
                "category": customer['Category'],
                "purchase_amount": float(customer['Purchase Amount (USD)']),
                "review_rating": float(customer['Review Rating']),
                "subscription_status": customer['Subscription Status'],
                "previous_purchases": int(customer['Previous Purchases'])
            })
        
        return jsonify({
            "summary": summary,
            "customers": customers,
            "total_count": len(analytics_engine.df)
        })
        
    except Exception as e:
        return jsonify({"error": f"Failed to get customers: {str(e)}"}), 500

@app.route('/api/batch-analyze', methods=['POST'])
def batch_analyze():
    """Analyze multiple customers in batch"""
    try:
        if not analytics_engine:
            return jsonify({"error": "Analytics engine not initialized"}), 500
        
        data = request.get_json()
        customer_ids = data.get('customer_ids', [])
        
        if not customer_ids:
            return jsonify({"error": "No customer IDs provided"}), 400
        
        results = []
        for customer_id in customer_ids:
            result = analytics_engine.analyze_customer(customer_id)
            if "error" not in result:
                results.append(result)
        
        return jsonify({
            "analyzed_count": len(results),
            "results": results
        })
        
    except Exception as e:
        return jsonify({"error": f"Batch analysis failed: {str(e)}"}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "engine_initialized": analytics_engine is not None,
        "data_loaded": analytics_engine is not None and hasattr(analytics_engine, 'df')
    })

@app.route('/', methods=['GET'])
def index():
    """Root endpoint with API information"""
    return jsonify({
        "message": "Customer Behavior Analytics API",
        "version": "1.0.0",
        "endpoints": {
            "analyze_customer": "/api/analyze/<customer_id>",
            "get_customers": "/api/customers",
            "batch_analyze": "/api/batch-analyze",
            "health_check": "/api/health"
        },
        "engine_status": "initialized" if analytics_engine else "not_initialized"
    })

if __name__ == '__main__':
    print("🚀 Starting Customer Analytics API Server...")
    
    # Initialize the analytics engine
    if initialize_engine():
        print("🎯 Analytics API ready!")
        print("📊 Available endpoints:")
        print("   - GET /api/analyze/<customer_id>")
        print("   - GET /api/customers") 
        print("   - POST /api/batch-analyze")
        print("   - GET /api/health")
        print("\n🌐 Starting Flask server on port 5001...")
        
        app.run(host='0.0.0.0', port=5001, debug=True)
    else:
        print("❌ Failed to start server - could not initialize analytics engine")
        exit(1)
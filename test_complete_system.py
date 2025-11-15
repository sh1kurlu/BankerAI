#!/usr/bin/env python3
"""
Complete system test for Customer Analytics
Verifies unique results, API functionality, and dashboard integration
"""

import requests
import json
import time

def test_api_endpoint(customer_id, expected_uniqueness=None):
    """Test API endpoint and verify unique results"""
    print(f"\n🎯 Testing Customer ID: {customer_id}")
    
    try:
        response = requests.get(f"http://localhost:5001/api/analyze/{customer_id}")
        
        if response.status_code == 200:
            data = response.json()
            
            # Extract key unique identifiers
            persona = data.get('persona', {})
            behavior = data.get('behavior_summary', {})
            
            print(f"✅ API Response Successful")
            print(f"   Persona: {persona.get('label', 'N/A')}")
            print(f"   Description: {persona.get('description', 'N/A')[:80]}...")
            print(f"   Price Range: {behavior.get('preferred_price_range', 'N/A')}")
            print(f"   Top Category: {behavior.get('top_categories', ['N/A'])[0]}")
            
            # Check for uniqueness markers
            traits = persona.get('traits', [])
            if traits:
                print(f"   Key Trait: {traits[0]}")
            
            return data
        else:
            print(f"❌ API Error: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ API Connection Error: {e}")
        return None

def test_dashboard_integration():
    """Test dashboard accessibility"""
    print(f"\n🌐 Testing Dashboard Integration")
    
    try:
        # Test dashboard accessibility
        response = requests.get("http://localhost:8080/analytics_dashboard.html")
        
        if response.status_code == 200:
            print(f"✅ Dashboard Accessible at http://localhost:8080/analytics_dashboard.html")
            return True
        else:
            print(f"❌ Dashboard Error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Dashboard Connection Error: {e}")
        return False

def compare_customer_uniqueness(customer_ids):
    """Compare multiple customers to verify uniqueness"""
    print(f"\n🔍 Comparing Customer Uniqueness")
    
    results = {}
    for customer_id in customer_ids:
        data = test_api_endpoint(customer_id)
        if data:
            results[customer_id] = {
                'persona_label': data.get('persona', {}).get('label'),
                'description': data.get('persona', {}).get('description'),
                'price_range': data.get('behavior_summary', {}).get('preferred_price_range'),
                'top_category': data.get('behavior_summary', {}).get('top_categories', ['N/A'])[0],
                'rating': data.get('persona', {}).get('traits', ['N/A'])[0] if data.get('persona', {}).get('traits') else 'N/A'
            }
    
    # Compare uniqueness
    if len(results) > 1:
        personas = [results[cid]['persona_label'] for cid in results]
        descriptions = [results[cid]['description'] for cid in results]
        categories = [results[cid]['top_category'] for cid in results]
        
        unique_personas = len(set(personas))
        unique_descriptions = len(set(descriptions))
        unique_categories = len(set(categories))
        
        print(f"\n📊 Uniqueness Analysis:")
        print(f"   Unique Personas: {unique_personas}/{len(personas)}")
        print(f"   Unique Descriptions: {unique_descriptions}/{len(descriptions)}")
        print(f"   Unique Categories: {unique_categories}/{len(categories)}")
        
        if unique_personas == len(personas) and unique_descriptions == len(descriptions):
            print(f"✅ All customers have unique profiles!")
            return True
        else:
            print(f"⚠️  Some customers have similar profiles")
            return False
    
    return False

def main():
    """Run complete system test"""
    print("🚀 Starting Complete Customer Analytics System Test")
    print("=" * 60)
    
    # Wait for servers to be ready
    print("⏳ Waiting for servers to initialize...")
    time.sleep(2)
    
    # Test dashboard integration
    dashboard_ok = test_dashboard_integration()
    
    # Test multiple customers for uniqueness
    test_customers = [101, 205, 500, 750, 1000]
    uniqueness_ok = compare_customer_uniqueness(test_customers)
    
    # Test API health
    try:
        health_response = requests.get("http://localhost:5001/api/health")
        if health_response.status_code == 200:
            health_data = health_response.json()
            print(f"\n🏥 API Health: {health_data.get('status', 'Unknown')}")
            print(f"   Engine Initialized: {health_data.get('engine_initialized', False)}")
            print(f"   Data Loaded: {health_data.get('data_loaded', False)}")
            health_ok = True
        else:
            print(f"❌ Health Check Failed: {health_response.status_code}")
            health_ok = False
    except Exception as e:
        print(f"❌ Health Check Error: {e}")
        health_ok = False
    
    # Final summary
    print("\n" + "=" * 60)
    print("📋 TEST SUMMARY")
    print("=" * 60)
    print(f"Dashboard Integration: {'✅ PASS' if dashboard_ok else '❌ FAIL'}")
    print(f"Customer Uniqueness: {'✅ PASS' if uniqueness_ok else '❌ FAIL'}")
    print(f"API Health: {'✅ PASS' if health_ok else '❌ FAIL'}")
    
    if dashboard_ok and uniqueness_ok and health_ok:
        print(f"\n🎉 ALL TESTS PASSED! System is working correctly.")
        print(f"\n🌐 Access your dashboard at: http://localhost:8080/analytics_dashboard.html")
        print(f"📊 API Documentation: http://localhost:5001/api/")
    else:
        print(f"\n⚠️  Some tests failed. Please check the errors above.")

if __name__ == "__main__":
    main()
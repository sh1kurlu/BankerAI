from core.customer_analytics_engine import CustomerAnalyticsEngine
import pandas as pd

# Load customer data
df = pd.read_csv('data/customer.csv')
engine = CustomerAnalyticsEngine(df)

# Test customer ID 205 (different from 101)
result = engine.analyze_customer(205)
print('🎯 Customer 205 Analysis:')
print(f'Persona: {result["persona"]["label"]}')
print(f'Description: {result["persona"]["description"]}')
print(f'Purchase Amount: {result["behavior_summary"]["preferred_price_range"]}')
print(f'Rating: {result["persona"]["traits"][0]}')

# Test customer ID 101 for comparison
result2 = engine.analyze_customer(101)
print('\n🎯 Customer 101 Analysis:')
print(f'Persona: {result2["persona"]["label"]}')
print(f'Description: {result2["persona"]["description"]}')
print(f'Purchase Amount: {result2["behavior_summary"]["preferred_price_range"]}')
print(f'Rating: {result2["persona"]["traits"][0]}')

# Test customer ID 500 (another different one)
result3 = engine.analyze_customer(500)
print('\n🎯 Customer 500 Analysis:')
print(f'Persona: {result3["persona"]["label"]}')
print(f'Description: {result3["persona"]["description"]}')
print(f'Purchase Amount: {result3["behavior_summary"]["preferred_price_range"]}')
print(f'Rating: {result3["persona"]["traits"][0]}')
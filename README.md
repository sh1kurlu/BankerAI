# 🧠 Customer Behavior Analytics System

An AI-powered business intelligence platform that analyzes customer data to provide comprehensive behavioral insights, predictive analytics, and actionable business recommendations.

## 🎯 Key Features

### Customer Persona Development
- **Automated Persona Classification**: Identifies customer segments like "Premium Loyalist", "Bargain Hunter", "Quality Seeker", etc.
- **Behavioral Trait Analysis**: Generates detailed customer characteristics based on purchase patterns
- **Demographic Integration**: Incorporates age, gender, and location data into persona development

### Predictive Analytics
- **Next Action Prediction**: Forecasts customer behavior (Purchase, Browse, Churn Risk)
- **Purchase Probability**: Calculates likelihood of conversion with percentage confidence
- **Churn Risk Assessment**: Identifies customers at risk of leaving with risk percentages
- **Category Shift Prediction**: Anticipates future product category interests

### Business Intelligence Dashboard
- **Interactive Visualizations**: Charts.js powered charts for category distribution, activity patterns, and conversion funnels
- **Real-time Analytics**: Live customer behavior tracking and analysis
- **Mobile Responsive**: Optimized for desktop, tablet, and mobile viewing

### Actionable Recommendations
- **Marketing Strategies**: Targeted campaign recommendations based on customer segments
- **Retention Tactics**: Specific actions to reduce churn risk
- **Upsell/Cross-sell Opportunities**: Product recommendations for revenue growth
- **Priority-based Actions**: High, Medium, and Low priority business recommendations

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- pip package manager

### Installation

1. **Clone or download the project**
```bash
cd /Users/meh2/Applications/BankerAI/BankerAI
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

### Running with Streamlit (Recommended)

**Streamlit provides a modern, interactive web interface with all features and visualizations:**

1. **Run the Streamlit app**
```bash
streamlit run streamlit_app.py
```

Or use the helper script:
```bash
python run_streamlit.py
```

2. **Access the dashboard**
The app will automatically open in your browser at `http://localhost:8501`

**Streamlit Features:**
- ✅ Interactive customer analysis
- ✅ Beautiful visualizations (Plotly charts)
- ✅ Customer persona analysis
- ✅ Predictive analytics
- ✅ AI-powered recommendations
- ✅ Business recommendations
- ✅ Real-time data processing
- ✅ Responsive design

### Alternative: Running with Flask/HTML Dashboard

1. **Start the complete system**
```bash
python start_analytics.py
```

2. **Access the dashboard**
Open your browser and navigate to: `http://localhost:8080/analytics_dashboard.html`

## 📊 Data Structure

The system analyzes customer data with the following fields:

- **Customer ID**: Unique identifier
- **Age**: Customer age
- **Gender**: Customer gender
- **Item Purchased**: Product name
- **Category**: Product category (Clothing, Footwear, Accessories, Outerwear)
- **Purchase Amount**: Transaction value in USD
- **Location**: Customer location
- **Size**: Product size
- **Color**: Product color
- **Season**: Purchase season
- **Review Rating**: Customer satisfaction (1-5)
- **Subscription Status**: Loyalty program membership
- **Shipping Type**: Delivery preference
- **Discount Applied**: Price sensitivity indicator
- **Promo Code Used**: Marketing response
- **Previous Purchases**: Purchase history count
- **Payment Method**: Payment preference
- **Frequency of Purchases**: Purchase frequency

## 🎨 Dashboard Features

### Customer Analysis Interface
- **Customer ID Input**: Analyze any customer by ID (1-3900)
- **Analysis Type Selection**: Choose comprehensive or focused analysis
- **Real-time Processing**: Instant analytics generation

### Visual Analytics
- **Category Distribution**: Pie chart showing product category preferences
- **Hourly Activity Heatmap**: 24-hour customer activity patterns
- **Interest Trend Line**: 30-day engagement tracking
- **Conversion Funnel**: Purchase journey visualization

### Business Metrics
- **Purchase Probability**: Conversion likelihood percentage
- **Churn Risk**: Customer retention risk assessment
- **Current Value**: Customer's current spending value
- **Estimated CLV**: Customer Lifetime Value projection

## 🔧 API Endpoints

### Core Analytics
- `GET /api/analyze/<customer_id>` - Analyze specific customer
- `GET /api/customers` - Get customer list with basic info
- `POST /api/batch-analyze` - Analyze multiple customers
- `GET /api/health` - System health check

### Example API Usage

```python
import requests

# Analyze a customer
response = requests.get('http://localhost:5000/api/analyze/101')
analytics = response.json()

# Get customer list
response = requests.get('http://localhost:5000/api/customers')
customers = response.json()

# Batch analyze multiple customers
response = requests.post('http://localhost:5000/api/batch-analyze', 
                        json={'customer_ids': [101, 102, 103]})
results = response.json()
```

## 📈 Sample Analytics Output

```json
{
  "user_id": "101",
  "persona": {
    "label": "Premium Loyalist",
    "description": "High-value customer with strong brand loyalty",
    "traits": ["Quality-focused", "Subscription member", "Regular purchaser"]
  },
  "behavior_summary": {
    "top_categories": ["Accessories"],
    "preferred_price_range": "Premium ($80+)",
    "activity_trend": "Highly Active",
    "engagement_level": "High"
  },
  "predictive_analytics": {
    "next_likely_action": "Purchase",
    "purchase_probability_percent": 85,
    "churn_risk_percent": 15,
    "revenue_potential": "High"
  },
  "visual_data": {
    "category_distribution": [...],
    "hourly_activity_heatmap": [...],
    "interest_trend": [...],
    "conversion_funnel": [...],
    "lifetime_value_estimate": {...}
  },
  "business_recommendations": [
    {
      "type": "Marketing",
      "priority": "High",
      "action": "VIP Treatment",
      "description": "Offer exclusive access and premium service"
    }
  ]
}
```

## 🎨 Customization

### Adding New Personas
Edit the persona classification logic in `core/customer_analytics_engine.py`:

```python
# Add new persona conditions
if purchase_amount >= 100 and subscription == 'Yes':
    persona_label = "Ultra Premium"
    description = "Highest value customers with premium subscriptions"
```

### Modifying Predictive Models
Adjust prediction algorithms in the `generate_predictive_analytics()` method:

```python
# Customize prediction logic
if frequency >= 20 and review_rating >= 4.5:
    next_action = "High-Value Purchase"
    purchase_probability = 95
```

### Adding New Visualizations
Extend the dashboard by adding new Chart.js configurations:

```javascript
// Add new chart types in the displayCharts function
const newChart = new Chart(ctx, {
    type: 'radar',
    data: newChartData,
    options: newChartOptions
});
```

## 📋 Business Use Cases

### Marketing Teams
- **Campaign Targeting**: Identify high-value customers for premium campaigns
- **Churn Prevention**: Proactively reach out to at-risk customers
- **Product Recommendations**: Suggest relevant products based on behavior

### Sales Teams
- **Lead Prioritization**: Focus on customers with high purchase probability
- **Upsell Opportunities**: Identify customers ready for premium products
- **Customer Segmentation**: Group customers for targeted sales approaches

### Product Teams
- **Feature Development**: Understand customer preferences for new features
- **User Experience**: Optimize based on engagement patterns
- **Category Expansion**: Identify opportunities for new product lines

### Executive Teams
- **Revenue Forecasting**: Use CLV estimates for financial planning
- **Customer Retention**: Monitor churn risk across customer base
- **Strategic Planning**: Make data-driven decisions about market focus

## 🔒 Security & Privacy

- **Local Processing**: All analytics run locally on your machine
- **No External APIs**: No data sent to external services
- **Data Anonymization**: Customer IDs can be anonymized for privacy
- **Secure API**: CORS-enabled for controlled access

## 🐛 Troubleshooting

### Common Issues

**API Server Won't Start**
- Check Python dependencies: `pip install flask flask-cors pandas numpy`
- Verify port 5000 is available: `lsof -i :5000`

**Dashboard Not Loading**
- Ensure port 8080 is available: `lsof -i :8080`
- Check browser console for JavaScript errors

**Analytics Not Generating**
- Verify customer.csv file exists in data/ directory
- Check customer ID is within valid range (1-3900)

**Charts Not Displaying**
- Ensure Chart.js library loads properly
- Check browser developer console for errors

### Performance Optimization
- For large datasets (>10k customers), consider implementing pagination
- Use batch processing for multiple customer analysis
- Implement caching for frequently accessed customer profiles

## 🤝 Contributing

This system is designed for business intelligence and customer analytics. To extend functionality:

1. **Add New Data Sources**: Integrate additional customer data streams
2. **Enhance ML Models**: Implement more sophisticated prediction algorithms
3. **Extend Visualizations**: Add new chart types and interactive features
4. **Improve Recommendations**: Develop more targeted business strategies

## 📞 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the API endpoints and error messages
3. Examine the browser console for frontend issues
4. Check the Python console for backend errors

---

**🎯 Ready to unlock customer insights? Start analyzing your customer data today!**

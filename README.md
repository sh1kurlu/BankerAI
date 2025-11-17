# 🧠 CustomerAI - Customer Behavior Analytics Platform

A comprehensive AI-powered business intelligence platform that analyzes customer data to provide behavioral insights, predictive analytics, product recommendations, and actionable business recommendations. Built with FastAPI, Streamlit, Flask, and modern web technologies.

## 🎯 Overview

CustomerAI is a multi-component customer analytics system that combines:
- **Customer Analytics Engine**: Deep behavioral analysis and persona classification
- **AI Behavioral Engine**: Advanced ML-powered customer intelligence
- **Recommendation System**: Collaborative filtering and AI-powered product recommendations
- **Real-time Tracking**: Event tracking and live analytics
- **Interactive Dashboards**: Streamlit and web-based visualization interfaces
- **Marketplace Frontend**: E-commerce demo with AI recommendations

## ✨ Key Features

### 🎭 Customer Persona Development
- **Automated Persona Classification**: Identifies customer segments (Premium Loyalist, Bargain Hunter, Quality Seeker, etc.)
- **Behavioral Trait Analysis**: Generates detailed customer characteristics based on purchase patterns
- **Demographic Integration**: Incorporates age, gender, and location data into persona development

### 🔮 Predictive Analytics
- **Next Action Prediction**: Forecasts customer behavior (Purchase, Browse, Churn Risk)
- **Purchase Probability**: Calculates likelihood of conversion with percentage confidence
- **Churn Risk Assessment**: Identifies customers at risk of leaving with risk percentages
- **Category Shift Prediction**: Anticipates future product category interests
- **Customer Lifetime Value (CLV)**: Estimates long-term customer value

### 🤖 AI-Powered Recommendations
- **Collaborative Filtering**: User-based and item-based recommendation algorithms
- **Behavioral Analysis**: Recommendations based on user behavior patterns
- **Real-time Personalization**: Dynamic recommendations that update with user activity
- **Feedback Integration**: Learning from user interactions to improve recommendations

### 📊 Interactive Dashboards
- **Streamlit Dashboard**: Modern, interactive web interface with Plotly visualizations
- **HTML Dashboard**: Lightweight web-based analytics dashboard
- **Real-time Analytics**: Live customer behavior tracking and analysis
- **Mobile Responsive**: Optimized for desktop, tablet, and mobile viewing

### 🛒 Marketplace Demo
- **E-commerce Frontend**: Full-featured marketplace with product browsing
- **AI Recommendations**: Real-time product recommendations integrated into shopping experience
- **Event Tracking**: Comprehensive user interaction tracking
- **Multi-language Support**: Internationalization (i18n) capabilities
- **Theme Support**: Light/dark mode themes

## 🏗️ Architecture

```
CustomerAI/
├── api/                    # FastAPI backend server
│   └── main.py            # Main API endpoints
├── core/                   # Core analytics engines
│   ├── customer_analytics_engine.py    # Customer behavior analysis
│   ├── ai_behavioral_engine.py        # AI-powered behavioral analysis
│   ├── model_engine.py                # Recommendation models
│   ├── feedback_engine.py             # Recommendation feedback
│   └── preprocessor.py                # Data preprocessing
├── config/                 # Configuration
│   └── settings.py        # Application settings
├── data/                   # Data files
│   ├── customer.csv       # Customer dataset
│   └── events.csv         # User interaction events
├── frontend/               # Frontend applications
│   ├── app.js             # Frontend JavaScript
│   ├── index.html         # Frontend HTML
│   └── src/               # React/TypeScript source
├── marketplace/            # E-commerce marketplace demo
│   ├── index.html         # Marketplace homepage
│   ├── js/                # Marketplace JavaScript
│   └── data/              # Product data
├── analytics_api.py        # Flask-based analytics API
├── streamlit_app.py        # Streamlit dashboard
└── requirements.txt        # Python dependencies
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.7+**
- **pip** package manager
- **Node.js** (optional, for frontend development)

### Installation

1. **Clone or navigate to the project directory**
```bash
cd CustomerAI
```

2. **Install Python dependencies**
```bash
pip install -r requirements.txt
```

3. **Verify data files exist**
   - Ensure `data/customer.csv` exists for customer analytics
   - Ensure `data/events.csv` exists for recommendation system (optional)

## 🎮 Usage

### Option 1: Streamlit Dashboard (Recommended)

The Streamlit dashboard provides a modern, interactive interface with all analytics features:

```bash
streamlit run streamlit_app.py
```

Or use the helper script:
```bash
python run_streamlit.py
```

**Features:**
- ✅ Interactive customer analysis
- ✅ Beautiful visualizations (Plotly charts)
- ✅ Customer persona analysis
- ✅ Predictive analytics
- ✅ AI-powered recommendations
- ✅ Business recommendations
- ✅ Real-time data processing
- ✅ Responsive design

Access at: `http://localhost:8501`

### Option 2: FastAPI Backend Server

Run the FastAPI server for API access and marketplace integration:

```bash
uvicorn api.main:app --reload --port 8000
```

**API Documentation:**
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

**Key Endpoints:**
- `POST /api/recommend` - Get product recommendations
- `POST /api/ai-behavioral-analysis` - Comprehensive AI behavioral analysis
- `POST /api/track_event` - Track user events in real-time
- `GET /api/realtime-insights/{user_id}` - Get real-time user insights
- `GET /api/visualization/*` - Visualization data endpoints

### Option 3: Flask Analytics API

Run the Flask-based analytics API server:

```bash
python analytics_api.py
```

Access at: `http://localhost:5001`

**Endpoints:**
- `GET /api/analyze/<customer_id>` - Analyze specific customer
- `GET /api/customers` - Get customer list
- `POST /api/batch-analyze` - Analyze multiple customers
- `GET /api/health` - Health check

### Option 4: Complete System (Flask + Dashboard)

Run both the analytics API and web dashboard:

```bash
python start_analytics.py
```

Access dashboard at: `http://localhost:8080/analytics_dashboard.html`

### Option 5: Marketplace Frontend

Open the marketplace demo in your browser:

```bash
# Serve the marketplace directory
cd marketplace
python -m http.server 8080
```

Or open `marketplace/index.html` directly in your browser.

**Marketplace Features:**
- Product browsing and search
- AI-powered recommendations
- Shopping cart functionality
- Real-time event tracking
- Multi-language support
- Theme customization

## 📊 Data Structure

### Customer Data (`data/customer.csv`)

Required fields:
- **Customer ID**: Unique identifier
- **Age**: Customer age
- **Gender**: Customer gender
- **Item Purchased**: Product name
- **Category**: Product category
- **Purchase Amount (USD)**: Transaction value
- **Location**: Customer location
- **Review Rating**: Customer satisfaction (1-5)
- **Subscription Status**: Loyalty program membership
- **Previous Purchases**: Purchase history count
- **Frequency of Purchases**: Purchase frequency
- **Discount Applied**: Price sensitivity indicator

### Events Data (`data/events.csv`)

Required fields for recommendation system:
- **user_id**: User identifier
- **item_id**: Product identifier
- **item_name**: Product name
- **category**: Product category
- **event_type**: Type of interaction (view, cart, purchase, etc.)
- **timestamp**: Event timestamp
- **time_spent_seconds**: Time spent on item (optional)
- **price**: Product price (optional)

## 🔌 API Documentation

### FastAPI Endpoints

#### Get Recommendations
```python
POST /api/recommend
{
    "user_id": "user123",
    "k": 5
}

Response:
{
    "user_id": "user123",
    "recommendations": [
        {
            "item_id": "item1",
            "item_name": "Product Name",
            "category": "Electronics",
            "score": 85.5,
            "feedback": "Based on your browsing history"
        }
    ]
}
```

#### AI Behavioral Analysis
```python
POST /api/ai-behavioral-analysis
{
    "user_id": "user123",
    "k": 5
}

Response:
{
    "user_id": "user123",
    "recommendations": [...],
    "user_summary": {...},
    "predicted_actions": [...],
    "persona": {...},
    "analytics_data": {...}
}
```

#### Track Event
```python
POST /api/track_event
{
    "user_id": "user123",
    "item_id": "item1",
    "event_type": "view",
    "timestamp": "2024-01-01T12:00:00",
    "page_url": "/product/item1",
    "session_id": "session123"
}
```

#### Real-time Insights
```python
GET /api/realtime-insights/{user_id}

Response:
{
    "user_id": "user123",
    "session_events": 15,
    "last_activity": "2024-01-01 12:00:00",
    "recent_categories": ["Electronics", "Books"],
    "current_interest": "Highly Active",
    "recommendations_ready": true
}
```

### Flask Analytics API Endpoints

#### Analyze Customer
```python
GET /api/analyze/<customer_id>?type=comprehensive

Response:
{
    "user_id": "101",
    "persona": {
        "label": "Premium Loyalist",
        "description": "High-value customer...",
        "traits": [...]
    },
    "behavior_summary": {...},
    "predictive_analytics": {...},
    "visual_data": {...},
    "business_recommendations": [...]
}
```

#### Batch Analyze
```python
POST /api/batch-analyze
{
    "customer_ids": ["101", "102", "103"]
}
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
    "top_categories": ["Accessories", "Electronics"],
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
    "lifetime_value_estimate": {
      "current_value": 1250.00,
      "estimated_clv": 5000.00,
      "remaining_years": 4.0
    }
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

## 🎨 Dashboard Features

### Streamlit Dashboard

**Tabs:**
1. **Overview**: Customer summary and persona
2. **Persona & Behavior**: Detailed behavioral analysis
3. **Predictive Analytics**: Churn risk, purchase probability, CLV
4. **Recommendations**: Business and AI product recommendations
5. **Visualizations**: Interactive charts and graphs

**Visualizations:**
- Category distribution (pie chart)
- Hourly activity patterns (line chart)
- Interest trends (time series)
- Conversion funnel
- Retention curve
- Customer lifetime value metrics

### HTML Dashboard

- Customer ID input and analysis
- Real-time analytics generation
- Interactive Chart.js visualizations
- Business recommendations display
- Mobile-responsive design

## 🛠️ Development

### Project Structure

- **Core Engines**: Analytics and ML models in `core/`
- **API Layer**: FastAPI and Flask APIs in `api/` and root
- **Frontend**: Streamlit app and HTML dashboards
- **Marketplace**: E-commerce demo with tracking

### Adding New Features

#### Custom Personas
Edit `core/customer_analytics_engine.py`:
```python
# Add new persona classification logic
if purchase_amount >= 100 and subscription == 'Yes':
    persona_label = "Ultra Premium"
    description = "Highest value customers"
```

#### Custom Recommendations
Extend `core/model_engine.py`:
```python
# Add new recommendation algorithms
def custom_recommend(self, user_id, k=5):
    # Your custom logic
    return recommendations
```

#### New API Endpoints
Add to `api/main.py`:
```python
@app.get("/api/custom-endpoint")
async def custom_endpoint():
    return {"message": "Custom endpoint"}
```

## 📋 Business Use Cases

### Marketing Teams
- **Campaign Targeting**: Identify high-value customers for premium campaigns
- **Churn Prevention**: Proactively reach out to at-risk customers
- **Product Recommendations**: Suggest relevant products based on behavior
- **Segmentation**: Group customers for targeted marketing

### Sales Teams
- **Lead Prioritization**: Focus on customers with high purchase probability
- **Upsell Opportunities**: Identify customers ready for premium products
- **Customer Segmentation**: Group customers for targeted sales approaches
- **Real-time Insights**: Get live customer activity data

### Product Teams
- **Feature Development**: Understand customer preferences for new features
- **User Experience**: Optimize based on engagement patterns
- **Category Expansion**: Identify opportunities for new product lines
- **A/B Testing**: Use analytics to measure feature impact

### Executive Teams
- **Revenue Forecasting**: Use CLV estimates for financial planning
- **Customer Retention**: Monitor churn risk across customer base
- **Strategic Planning**: Make data-driven decisions about market focus
- **Performance Metrics**: Track key business indicators

## 🔒 Security & Privacy

- **Local Processing**: All analytics run locally on your machine
- **No External APIs**: No data sent to external services (unless configured)
- **Data Anonymization**: Customer IDs can be anonymized for privacy
- **CORS Configuration**: Controlled API access via CORS settings
- **Secure Endpoints**: API endpoints can be secured with authentication

## 🐛 Troubleshooting

### Common Issues

**API Server Won't Start**
- Check Python dependencies: `pip install -r requirements.txt`
- Verify ports are available: `lsof -i :8000` or `lsof -i :5001`
- Check for missing data files in `data/` directory

**Streamlit Dashboard Not Loading**
- Ensure Streamlit is installed: `pip install streamlit`
- Check data file paths are correct
- Review console for error messages

**Recommendations Not Working**
- Verify `data/events.csv` exists and has valid data
- Check user_id exists in events data
- Ensure preprocessor can load events file

**Charts Not Displaying**
- Check browser console for JavaScript errors
- Verify Plotly/Chart.js libraries load properly
- Ensure data format matches expected structure

### Performance Optimization

- For large datasets (>10k customers), consider implementing pagination
- Use batch processing for multiple customer analysis
- Implement caching for frequently accessed customer profiles
- Use async endpoints for better concurrency (FastAPI)

## 📦 Dependencies

### Python Packages
- `fastapi==0.115.0` - Modern API framework
- `uvicorn==0.30.0` - ASGI server
- `pandas==2.1.0` - Data manipulation
- `numpy==1.25.0` - Numerical computing
- `scikit-learn==1.3.0` - Machine learning
- `streamlit>=1.28.0` - Interactive dashboards
- `plotly>=5.17.0` - Interactive visualizations
- `flask` - Flask API (if using analytics_api.py)
- `flask-cors` - CORS support for Flask

### Frontend Libraries
- Chart.js - Data visualization
- Plotly - Interactive charts (Streamlit)
- Modern JavaScript (ES6+)

## 🤝 Contributing

To extend functionality:

1. **Add New Data Sources**: Integrate additional customer data streams
2. **Enhance ML Models**: Implement more sophisticated prediction algorithms
3. **Extend Visualizations**: Add new chart types and interactive features
4. **Improve Recommendations**: Develop more targeted business strategies
5. **Add API Endpoints**: Extend API functionality for new use cases
6. **Enhance Marketplace**: Add new features to the e-commerce demo

## 📞 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review API documentation at `/docs` (FastAPI) or `/api/health`
3. Examine browser console for frontend issues
4. Check Python console/logs for backend errors
5. Review `backend.log` for detailed error information

## 📄 License

This project is designed for business intelligence and customer analytics. Use responsibly and in accordance with data privacy regulations.

---

**🎯 Ready to unlock customer insights? Start analyzing your customer data today!**

For the best experience, start with the **Streamlit Dashboard**:
```bash
streamlit run streamlit_app.py
```

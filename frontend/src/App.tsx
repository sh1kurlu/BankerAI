import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, 
         PieChart, Pie, Cell, BarChart, Bar, ScatterChart, Scatter, Area, AreaChart } from 'recharts';
import { Brain, TrendingUp, Users, ShoppingCart, Clock, Target, AlertTriangle, CheckCircle } from 'lucide-react';
import './App.css';

// Types for AI-generated data
interface AIRecommendation {
  item_id: string;
  item_name: string;
  category: string;
  score: number;
  reason: string;
  behavioral_justification: string;
  similarity_score: number;
  collaborative_reasoning: string;
  confidence: string;
  trend_alignment: string;
}

interface UserPersona {
  persona_type: string;
  description: string;
  key_characteristics: string[];
  purchasing_behavior: string;
  category_preferences: string[];
  activity_patterns: {
    peak_hours: number[];
    session_frequency: number;
    browsing_patterns: {
      pattern: string;
      sessions: number;
      avg_session_length: number;
    };
    decision_speed: string;
  };
  risk_factors: string[];
  opportunities: string[];
}

interface PredictedAction {
  action_type: string;
  probability: number;
  reasoning: string;
  timeframe: string;
  influencing_factors: string[];
  confidence_level: string;
}

interface UserBehaviorSummary {
  user_id: string;
  top_categories: Array<{
    category: string;
    count: number;
    percentage: number;
  }>;
  most_active_hours: number[];
  recent_trends: string[];
  purchase_tendencies: {
    impulse_buyer: boolean;
    researcher: boolean;
    brand_loyal: boolean;
    price_conscious: boolean;
    category_explorer: boolean;
  };
  engagement_level: string;
  loyalty_indicators: {
    repeat_purchase_rate: number;
    account_age_days: number;
    activity_consistency: number;
    engagement_depth: string;
  };
  seasonal_patterns: string[];
}

interface Explanation {
  type: string;
  description: string;
  confidence: string;
}

interface DashboardAnalytics {
  category_distribution: {
    labels: string[];
    values: number[];
    colors: string[];
  };
  hourly_activity_heatmap: {
    hours: number[];
    activity: number[];
    max_activity: number;
  };
  interaction_trends: {
    dates: string[];
    counts: number[];
    trend_direction: string;
  };
  similarity_breakdown: {
    factors: string[];
    scores: number[];
    overall_similarity: number;
  };
  purchase_funnel: {
    stages: string[];
    conversions: number[];
    conversion_rates: number[];
  };
  user_interest_growth: {
    categories: string[];
    growth_rates: number[];
  };
}

interface ComprehensiveAIOutput {
  recommendations: AIRecommendation[];
  explanations: Explanation[];
  user_summary: UserBehaviorSummary;
  predicted_actions: PredictedAction[];
  persona: UserPersona;
  analytics_data: DashboardAnalytics;
}

const API_BASE = 'http://localhost:8000';

function App() {
  const [userId, setUserId] = useState<string>('');
  const [k, setK] = useState<number>(5);
  const [aiData, setAiData] = useState<ComprehensiveAIOutput | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>('');
  const [activeTab, setActiveTab] = useState<string>('recommendations');

  const fetchAIRecommendations = async () => {
    if (!userId.trim()) {
      setError('Please enter a user ID');
      return;
    }

    setLoading(true);
    setError('');

    try {
      // Use the new AI behavioral analysis endpoint
      const aiAnalysisRes = await fetch(`${API_BASE}/api/ai-behavioral-analysis`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: userId, k })
      });

      if (!aiAnalysisRes.ok) {
        throw new Error(`AI Behavioral Analysis API error: ${aiAnalysisRes.status}`);
      }

      const aiData = await aiAnalysisRes.json();
      
      // Transform the API response to match our frontend structure
      const transformedData: ComprehensiveAIOutput = {
        recommendations: aiData.recommendations,
        explanations: [
          {
            type: 'behavioral_pattern',
            description: 'Analysis based on user interaction patterns and preferences',
            confidence: 'high'
          },
          {
            type: 'collaborative_filtering',
            description: 'Recommendations based on similar user preferences',
            confidence: 'high'
          },
          {
            type: 'trend_analysis',
            description: 'Incorporating current market trends and seasonality',
            confidence: 'medium'
          }
        ],
        user_summary: aiData.user_summary,
        predicted_actions: aiData.predicted_actions,
        persona: aiData.persona,
        analytics_data: aiData.analytics_data
      };

      setAiData(transformedData);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  const getConfidenceColor = (confidence: string) => {
    switch (confidence) {
      case 'high': return 'text-green-600';
      case 'medium': return 'text-yellow-600';
      case 'low': return 'text-red-600';
      default: return 'text-gray-600';
    }
  };

  const getActionIcon = (actionType: string) => {
    switch (actionType) {
      case 'purchase': return <ShoppingCart className="w-4 h-4" />;
      case 'add_to_cart': return <ShoppingCart className="w-4 h-4" />;
      case 'churn': return <AlertTriangle className="w-4 h-4" />;
      default: return <Target className="w-4 h-4" />;
    }
  };

  const COLORS = ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#06B6D4'];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-3">
              <Brain className="w-8 h-8 text-blue-600" />
              <h1 className="text-2xl font-bold text-gray-900">CustomerAI Dashboard</h1>
            </div>
            <div className="flex items-center space-x-4">
              <input
                type="text"
                placeholder="Enter User ID"
                value={userId}
                onChange={(e) => setUserId(e.target.value)}
                className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
              <input
                type="number"
                placeholder="Recommendations (k)"
                value={k}
                onChange={(e) => setK(parseInt(e.target.value) || 5)}
                min="1"
                max="20"
                className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent w-32"
              />
              <button
                onClick={fetchAIRecommendations}
                disabled={loading}
                className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
              >
                {loading ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                    <span>Analyzing...</span>
                  </>
                ) : (
                  <>
                    <Brain className="w-4 h-4" />
                    <span>Analyze User</span>
                  </>
                )}
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Error Message */}
      {error && (
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-4">
          <div className="bg-red-50 border border-red-200 rounded-lg p-4">
            <div className="flex items-center space-x-2">
              <AlertTriangle className="w-5 h-5 text-red-500" />
              <span className="text-red-800">{error}</span>
            </div>
          </div>
        </div>
      )}

      {/* Main Content */}
      {aiData && (
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {/* Tab Navigation */}
          <div className="mb-8">
            <nav className="flex space-x-8 border-b border-gray-200">
              {[
                { id: 'recommendations', label: 'AI Recommendations', icon: Brain },
                { id: 'persona', label: 'User Persona', icon: Users },
                { id: 'predictions', label: 'Predicted Actions', icon: TrendingUp },
                { id: 'analytics', label: 'Analytics Dashboard', icon: Target }
              ].map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center space-x-2 py-4 px-1 border-b-2 font-medium text-sm ${
                    activeTab === tab.id
                      ? 'border-blue-500 text-blue-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  <tab.icon className="w-5 h-5" />
                  <span>{tab.label}</span>
                </button>
              ))}
            </nav>
          </div>

          {/* Tab Content */}
          <div className="space-y-8">
            {activeTab === 'recommendations' && (
              <div className="space-y-6">
                <div className="bg-white rounded-lg shadow-sm border p-6">
                  <h2 className="text-xl font-semibold text-gray-900 mb-4">AI-Powered Recommendations</h2>
                  <div className="grid gap-4">
                    {aiData.recommendations.map((rec, index) => (
                      <div key={index} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
                        <div className="flex items-start justify-between mb-3">
                          <div>
                            <h3 className="font-semibold text-gray-900">{rec.item_name}</h3>
                            <p className="text-sm text-gray-600">{rec.category}</p>
                          </div>
                          <div className="text-right">
                            <div className="text-lg font-bold text-blue-600">{rec.score.toFixed(1)}</div>
                            <div className={`text-xs font-medium ${getConfidenceColor(rec.confidence)}`}>
                              {rec.confidence} confidence
                            </div>
                          </div>
                        </div>
                        
                        <div className="space-y-2 text-sm">
                          <div>
                            <span className="font-medium text-gray-700">Reason: </span>
                            <span className="text-gray-600">{rec.reason}</span>
                          </div>
                          <div>
                            <span className="font-medium text-gray-700">Behavioral Justification: </span>
                            <span className="text-gray-600">{rec.behavioral_justification}</span>
                          </div>
                          <div>
                            <span className="font-medium text-gray-700">Collaborative Reasoning: </span>
                            <span className="text-gray-600">{rec.collaborative_reasoning}</span>
                          </div>
                          <div className="flex items-center space-x-4 text-xs text-gray-500">
                            <span>Similarity: {(rec.similarity_score * 100).toFixed(1)}%</span>
                            <span>Trend: {rec.trend_alignment}</span>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Explanations */}
                <div className="bg-white rounded-lg shadow-sm border p-6">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">AI Analysis Explanations</h3>
                  <div className="grid gap-4">
                    {aiData.explanations.map((exp, index) => (
                      <div key={index} className="flex items-start space-x-3">
                        <CheckCircle className={`w-5 h-5 mt-0.5 ${getConfidenceColor(exp.confidence)}`} />
                        <div>
                          <h4 className="font-medium text-gray-900 capitalize">{exp.type.replace('_', ' ')}</h4>
                          <p className="text-sm text-gray-600">{exp.description}</p>
                          <div className={`text-xs font-medium ${getConfidenceColor(exp.confidence)} mt-1`}>
                            Confidence: {exp.confidence}
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            )}

            {activeTab === 'persona' && (
              <div className="space-y-6">
                <div className="bg-white rounded-lg shadow-sm border p-6">
                  <div className="flex items-center space-x-3 mb-6">
                    <Users className="w-6 h-6 text-blue-600" />
                    <h2 className="text-xl font-semibold text-gray-900">User Persona Analysis</h2>
                  </div>
                  
                  <div className="grid md:grid-cols-2 gap-6">
                    <div className="space-y-4">
                      <div>
                        <h3 className="font-semibold text-gray-900 mb-2">Persona Type</h3>
                        <p className="text-lg text-blue-600 font-medium">{aiData.persona.persona_type}</p>
                      </div>
                      
                      <div>
                        <h3 className="font-semibold text-gray-900 mb-2">Description</h3>
                        <p className="text-gray-600">{aiData.persona.description}</p>
                      </div>
                      
                      <div>
                        <h3 className="font-semibold text-gray-900 mb-2">Key Characteristics</h3>
                        <ul className="space-y-1">
                          {aiData.persona.key_characteristics.map((char, index) => (
                            <li key={index} className="flex items-center space-x-2">
                              <CheckCircle className="w-4 h-4 text-green-500" />
                              <span className="text-gray-600">{char}</span>
                            </li>
                          ))}
                        </ul>
                      </div>
                    </div>
                    
                    <div className="space-y-4">
                      <div>
                        <h3 className="font-semibold text-gray-900 mb-2">Purchasing Behavior</h3>
                        <p className="text-gray-600">{aiData.persona.purchasing_behavior}</p>
                      </div>
                      
                      <div>
                        <h3 className="font-semibold text-gray-900 mb-2">Category Preferences</h3>
                        <div className="flex flex-wrap gap-2">
                          {aiData.persona.category_preferences.map((cat, index) => (
                            <span key={index} className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm">
                              {cat}
                            </span>
                          ))}
                        </div>
                      </div>
                      
                      <div>
                        <h3 className="font-semibold text-gray-900 mb-2">Activity Patterns</h3>
                        <div className="space-y-2 text-sm">
                          <div className="flex justify-between">
                            <span className="text-gray-600">Peak Hours:</span>
                            <span className="text-gray-900">{aiData.persona.activity_patterns.peak_hours.join(', ')}</span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-gray-600">Session Frequency:</span>
                            <span className="text-gray-900">{aiData.persona.activity_patterns.session_frequency}/day</span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-gray-600">Decision Speed:</span>
                            <span className="text-gray-900 capitalize">{aiData.persona.activity_patterns.decision_speed.replace('_', ' ')}</span>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  {aiData.persona.risk_factors.length > 0 && (
                    <div className="mt-6 p-4 bg-yellow-50 rounded-lg">
                      <h3 className="font-semibold text-yellow-800 mb-2 flex items-center space-x-2">
                        <AlertTriangle className="w-5 h-5" />
                        <span>Risk Factors</span>
                      </h3>
                      <ul className="space-y-1">
                        {aiData.persona.risk_factors.map((risk, index) => (
                          <li key={index} className="text-yellow-700">• {risk}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                  
                  {aiData.persona.opportunities.length > 0 && (
                    <div className="mt-4 p-4 bg-green-50 rounded-lg">
                      <h3 className="font-semibold text-green-800 mb-2 flex items-center space-x-2">
                        <CheckCircle className="w-5 h-5" />
                        <span>Opportunities</span>
                      </h3>
                      <ul className="space-y-1">
                        {aiData.persona.opportunities.map((opp, index) => (
                          <li key={index} className="text-green-700">• {opp}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              </div>
            )}

            {activeTab === 'predictions' && (
              <div className="space-y-6">
                <div className="bg-white rounded-lg shadow-sm border p-6">
                  <div className="flex items-center space-x-3 mb-6">
                    <TrendingUp className="w-6 h-6 text-blue-600" />
                    <h2 className="text-xl font-semibold text-gray-900">Predicted Next Actions</h2>
                  </div>
                  
                  <div className="grid gap-4">
                    {aiData.predicted_actions.map((action, index) => (
                      <div key={index} className="border border-gray-200 rounded-lg p-4">
                        <div className="flex items-center justify-between mb-3">
                          <div className="flex items-center space-x-3">
                            {getActionIcon(action.action_type)}
                            <h3 className="font-semibold text-gray-900 capitalize">{action.action_type.replace('_', ' ')}</h3>
                          </div>
                          <div className="text-right">
                            <div className="text-lg font-bold text-blue-600">{(action.probability * 100).toFixed(1)}%</div>
                            <div className={`text-xs font-medium ${getConfidenceColor(action.confidence_level)}`}>
                              {action.confidence_level} confidence
                            </div>
                          </div>
                        </div>
                        
                        <div className="space-y-2 text-sm">
                          <div>
                            <span className="font-medium text-gray-700">Reasoning: </span>
                            <span className="text-gray-600">{action.reasoning}</span>
                          </div>
                          <div>
                            <span className="font-medium text-gray-700">Timeframe: </span>
                            <span className="text-gray-600">{action.timeframe}</span>
                          </div>
                          <div>
                            <span className="font-medium text-gray-700">Influencing Factors: </span>
                            <div className="flex flex-wrap gap-2 mt-1">
                              {action.influencing_factors.map((factor, idx) => (
                                <span key={idx} className="px-2 py-1 bg-gray-100 text-gray-700 rounded text-xs">
                                  {factor}
                                </span>
                              ))}
                            </div>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            )}

            {activeTab === 'analytics' && (
              <div className="space-y-6">
                <div className="bg-white rounded-lg shadow-sm border p-6">
                  <div className="flex items-center space-x-3 mb-6">
                    <Target className="w-6 h-6 text-blue-600" />
                    <h2 className="text-xl font-semibold text-gray-900">Analytics Dashboard</h2>
                  </div>
                  
                  {/* Category Distribution */}
                  <div className="mb-8">
                    <h3 className="text-lg font-semibold text-gray-900 mb-4">Category Distribution</h3>
                    <div className="h-64">
                      <ResponsiveContainer width="100%" height="100%">
                        <PieChart>
                          <Pie
                            data={aiData.analytics_data.category_distribution.labels.map((label, index) => ({
                              name: label,
                              value: aiData.analytics_data.category_distribution.values[index],
                              fill: aiData.analytics_data.category_distribution.colors[index]
                            }))}
                            cx="50%"
                            cy="50%"
                            outerRadius={80}
                            dataKey="value"
                            label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                          />
                          <Tooltip />
                        </PieChart>
                      </ResponsiveContainer>
                    </div>
                  </div>

                  {/* Hourly Activity */}
                  <div className="mb-8">
                    <h3 className="text-lg font-semibold text-gray-900 mb-4">Hourly Activity Pattern</h3>
                    <div className="h-64">
                      <ResponsiveContainer width="100%" height="100%">
                        <BarChart
                          data={aiData.analytics_data.hourly_activity_heatmap.hours.map((hour, index) => ({
                            hour: `${hour}:00`,
                            activity: aiData.analytics_data.hourly_activity_heatmap.activity[index]
                          }))}
                        >
                          <CartesianGrid strokeDasharray="3 3" />
                          <XAxis dataKey="hour" />
                          <YAxis />
                          <Tooltip />
                          <Bar dataKey="activity" fill="#3B82F6" />
                        </BarChart>
                      </ResponsiveContainer>
                    </div>
                  </div>

                  {/* Interaction Trends */}
                  <div className="mb-8">
                    <h3 className="text-lg font-semibold text-gray-900 mb-4">Interaction Trends</h3>
                    <div className="h-64">
                      <ResponsiveContainer width="100%" height="100%">
                        <LineChart
                          data={aiData.analytics_data.interaction_trends.dates.map((date, index) => ({
                            date,
                            interactions: aiData.analytics_data.interaction_trends.counts[index]
                          }))}
                        >
                          <CartesianGrid strokeDasharray="3 3" />
                          <XAxis dataKey="date" />
                          <YAxis />
                          <Tooltip />
                          <Line type="monotone" dataKey="interactions" stroke="#10B981" strokeWidth={2} />
                        </LineChart>
                      </ResponsiveContainer>
                    </div>
                  </div>

                  {/* Similarity Breakdown */}
                  <div className="mb-8">
                    <h3 className="text-lg font-semibold text-gray-900 mb-4">Similarity Analysis</h3>
                    <div className="h-64">
                      <ResponsiveContainer width="100%" height="100%">
                        <BarChart
                          data={aiData.analytics_data.similarity_breakdown.factors.map((factor, index) => ({
                            factor,
                            score: aiData.analytics_data.similarity_breakdown.scores[index]
                          }))}
                        >
                          <CartesianGrid strokeDasharray="3 3" />
                          <XAxis dataKey="factor" />
                          <YAxis domain={[0, 1]} />
                          <Tooltip formatter={(value) => [`${(value * 100).toFixed(1)}%`, 'Score']} />
                          <Bar dataKey="score" fill="#F59E0B" />
                        </BarChart>
                      </ResponsiveContainer>
                    </div>
                    <div className="mt-4 text-center">
                      <span className="text-sm text-gray-600">Overall Similarity: </span>
                      <span className="font-semibold text-blue-600">
                        {(aiData.analytics_data.similarity_breakdown.overall_similarity * 100).toFixed(1)}%
                      </span>
                    </div>
                  </div>

                  {/* Purchase Funnel */}
                  <div className="mb-8">
                    <h3 className="text-lg font-semibold text-gray-900 mb-4">Purchase Funnel</h3>
                    <div className="h-64">
                      <ResponsiveContainer width="100%" height="100%">
                        <AreaChart
                          data={aiData.analytics_data.purchase_funnel.stages.map((stage, index) => ({
                            stage,
                            conversions: aiData.analytics_data.purchase_funnel.conversions[index],
                            rate: (aiData.analytics_data.purchase_funnel.conversion_rates[index] * 100).toFixed(1)
                          }))}
                        >
                          <CartesianGrid strokeDasharray="3 3" />
                          <XAxis dataKey="stage" />
                          <YAxis />
                          <Tooltip formatter={(value, name) => [
                            name === 'rate' ? `${value}%` : value,
                            name === 'rate' ? 'Conversion Rate' : 'Conversions'
                          ]} />
                          <Area type="monotone" dataKey="conversions" stackId="1" stroke="#8B5CF6" fill="#8B5CF6" fillOpacity={0.6} />
                        </AreaChart>
                      </ResponsiveContainer>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
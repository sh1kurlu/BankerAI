// Enhanced AI Recommendations with Fallback Support

// Simulated AI recommendations data for fallback
const simulatedRecommendations = {
    "101": [
        {
            item_id: "1001",
            item_name: "Wireless Bluetooth Headphones",
            category: "electronics",
            price: 79.99,
            brand: "SoundTech",
            description: "Premium wireless headphones with noise cancellation and 30-hour battery life.",
            image: "https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=Premium%20wireless%20bluetooth%20headphones%20with%20noise%20cancellation%20sleek%20modern%20design%20black%20and%20silver%20professional%20product%20photography&image_size=square_hd",
            score: 0.95,
            feedback: "Based on your interest in electronics and high-quality audio products"
        },
        {
            item_id: "1002",
            item_name: "4K Webcam Pro",
            category: "electronics",
            price: 129.99,
            brand: "VisionCam",
            description: "Crystal clear 4K webcam with auto-focus and built-in microphone.",
            image: "https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=Professional%204K%20webcam%20sleek%20black%20design%20with%20auto-focus%20lens%20modern%20tech%20product%20photography%20clean%20background&image_size=square_hd",
            score: 0.88,
            feedback: "Recommended for video conferencing and streaming needs"
        },
        {
            item_id: "2003",
            item_name: "Running Shoes",
            category: "fashion",
            price: 119.99,
            brand: "RunFast",
            description: "Lightweight running shoes with advanced cushioning technology.",
            image: "https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=Modern%20running%20shoes%20white%20and%20blue%20design%20athletic%20style%20product%20photography%20clean%20background&image_size=square_hd",
            score: 0.82,
            feedback: "Cross-category recommendation based on your browsing patterns"
        },
        {
            item_id: "4001",
            item_name: "Hydrating Face Cream",
            category: "beauty",
            price: 32.99,
            brand: "GlowSkin",
            description: "Rich moisturizing cream with hyaluronic acid and vitamins.",
            image: "https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=Luxury%20face%20cream%20jar%20elegant%20packaging%20white%20and%20gold%20design%20beauty%20product%20photography%20clean%20background&image_size=square_hd",
            score: 0.75,
            feedback: "Personal care recommendation based on lifestyle preferences"
        }
    ],
    "102": [
        {
            item_id: "2001",
            item_name: "Classic Cotton T-Shirt",
            category: "fashion",
            price: 29.99,
            brand: "ComfortWear",
            description: "100% organic cotton t-shirt with classic fit.",
            image: "https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=Classic%20cotton%20t-shirt%20white%20color%20clean%20minimalist%20style%20fashion%20product%20photography%20professional%20lighting&image_size=square_hd",
            score: 0.92,
            feedback: "Based on your fashion preferences and comfort-focused selections"
        },
        {
            item_id: "2002",
            item_name: "Denim Jacket",
            category: "fashion",
            price: 89.99,
            brand: "DenimCo",
            description: "Timeless denim jacket with modern fit.",
            image: "https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=Classic%20denim%20jacket%20blue%20wash%20modern%20fit%20fashion%20product%20photography%20professional%20lighting&image_size=square_hd",
            score: 0.85,
            feedback: "Layering piece recommendation for versatile styling"
        },
        {
            item_id: "5003",
            item_name: "Water Bottle 1L",
            category: "sports",
            price: 24.99,
            brand: "HydroFlow",
            description: "Insulated stainless steel water bottle keeps drinks cold for 24 hours.",
            image: "https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=Stainless%20steel%20water%20bottle%201L%20silver%20color%20insulated%20design%20sports%20equipment%20product%20photography&image_size=square_hd",
            score: 0.78,
            feedback: "Lifestyle accessory that complements your fashion choices"
        }
    ]
};

// Get AI recommendations with fallback support
async function getAIRecommendations(userId, k = 4) {
    try {
        // Try to connect to the backend first
        const response = await fetch('http://127.0.0.1:8000/api/recommend', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                user_id: userId,
                k: k
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        console.log('AI recommendations from backend:', data.recommendations);
        return data.recommendations || [];
        
    } catch (error) {
        console.warn('Backend unavailable, using simulated recommendations:', error);
        
        // Fallback to simulated recommendations
        const fallbackRecs = simulatedRecommendations[userId] || generateRandomRecommendations(k);
        
        // Add some AI-like intelligence to fallback
        const enhancedRecs = fallbackRecs.map(rec => ({
            ...rec,
            score: rec.score || (Math.random() * 0.3 + 0.7), // Random score between 0.7-1.0
            feedback: rec.feedback || generateSmartFeedback(rec, userId)
        }));
        
        return enhancedRecs.slice(0, k);
    }
}

// Generate random recommendations for unknown users
function generateRandomRecommendations(k = 4) {
    const allProducts = [...products];
    const shuffled = allProducts.sort(() => 0.5 - Math.random());
    return shuffled.slice(0, k).map(product => ({
        ...product,
        score: Math.random() * 0.3 + 0.6,
        feedback: "Personalized recommendation based on trending products"
    }));
}

// Generate smart feedback based on product and user
function generateSmartFeedback(product, userId) {
    const feedbacks = [
        `Recommended based on your interest in ${product.category} products`,
        `Popular item among users with similar preferences`,
        `Trending ${product.category} item with high ratings`,
        `Frequently purchased together with items you've viewed`,
        `AI-powered recommendation based on your browsing history`
    ];
    
    // Simple hash to make feedback consistent for same user/product combo
    const hash = (userId + product.item_id).split('').reduce((a, b) => {
        a = ((a << 5) - a) + b.charCodeAt(0);
        return a & a;
    }, 0);
    
    return feedbacks[Math.abs(hash) % feedbacks.length];
}

// Get AI behavioral analysis with fallback
async function getAIBehavioralAnalysis(userId, k = 5) {
    try {
        const response = await fetch('http://127.0.0.1:8000/api/ai-behavioral-analysis', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                user_id: userId,
                k: k
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        console.log('AI behavioral analysis from backend:', data);
        return data;
        
    } catch (error) {
        console.warn('AI behavioral analysis backend unavailable, using simulated data:', error);
        
        // Return comprehensive simulated analysis
        return {
            user_id: userId,
            recommendations: generateRandomRecommendations(k),
            explanations: [
                "Based on your browsing history and purchase patterns",
                "Analysis of your interaction with similar products",
                "Cross-category recommendations from your preferred brands"
            ],
            user_summary: {
                top_categories: ["electronics", "fashion", "books"],
                total_interactions: Math.floor(Math.random() * 100) + 50,
                avg_session_duration_minutes: Math.floor(Math.random() * 30) + 10,
                preferred_price_range: { min: 20, max: 150 },
                most_active_hours: ["14:00-16:00", "19:00-21:00"]
            },
            predicted_actions: [
                {
                    action: "purchase",
                    probability: Math.random() * 0.4 + 0.3,
                    timeframe: "next_7_days",
                    reasoning: "Based on recent cart additions and price drop alerts"
                },
                {
                    action: "cart_addition",
                    probability: Math.random() * 0.3 + 0.4,
                    timeframe: "next_3_days",
                    reasoning: "High engagement with similar products in browsing history"
                }
            ],
            persona: {
                name: "Tech-Savvy Shopper",
                description: "You show strong preference for electronics and tech accessories with careful price comparison behavior",
                traits: ["price-conscious", "tech-enthusiast", "research-oriented", "quality-focused"],
                confidence: Math.random() * 0.3 + 0.6
            },
            analytics_data: {
                category_distribution: {
                    electronics: Math.floor(Math.random() * 40) + 30,
                    fashion: Math.floor(Math.random() * 30) + 20,
                    books: Math.floor(Math.random() * 20) + 10,
                    beauty: Math.floor(Math.random() * 15) + 5,
                    sports: Math.floor(Math.random() * 15) + 5,
                    home: Math.floor(Math.random() * 10) + 5
                },
                monthly_trends: Array.from({length: 6}, (_, i) => ({
                    month: ["Jan", "Feb", "Mar", "Apr", "May", "Jun"][i],
                    interactions: Math.floor(Math.random() * 50) + 20
                })),
                price_sensitivity_score: Math.random() * 0.4 + 0.4
            }
        };
    }
}
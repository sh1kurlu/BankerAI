// Real-time User Behavior Tracking System
// Automatically tracks all user interactions and streams to backend

class RealtimeUserTracker {
    constructor() {
        this.apiBase = 'http://127.0.0.1:8001';
        this.userId = this.getOrCreateUserId();
        this.sessionId = this.generateSessionId();
        this.eventQueue = [];
        this.isTracking = false;
        this.batchSize = 5;
        this.flushInterval = 3000; // Send events every 3 seconds
        this.initializeRealtimeTracking();
    }

    // Get existing user ID or create new one automatically
    getOrCreateUserId() {
        let userId = localStorage.getItem('marketplace_user_id');
        if (!userId) {
            userId = this.generateUserId();
            localStorage.setItem('marketplace_user_id', userId);
            console.log('🆕 New user created:', userId);
        }
        return userId;
    }

    // Generate unique user ID
    generateUserId() {
        return 'user_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }

    // Generate session ID
    generateSessionId() {
        return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }

    // Initialize real-time tracking
    initializeRealtimeTracking() {
        this.startEventFlushing();
        this.trackPageViewAuto({item_id: 'main_page', item_name: 'Main Page', category: 'page', price: 0, brand: 'system'});
        this.setupClickTracking();
        this.setupScrollTracking();
        this.setupTimeTracking();
        this.isTracking = true;
        console.log('📊 Real-time tracking initialized for user:', this.userId);
    }

    // Queue event for batch sending
    queueEvent(eventData) {
        const event = {
            ...eventData,
            user_id: this.userId,
            session_id: this.sessionId,
            timestamp: new Date().toISOString().slice(0, 19).replace('T', ' '),
            page_url: window.location.href,
            referrer: document.referrer,
            user_agent: navigator.userAgent,
            screen_resolution: `${window.screen.width}x${window.screen.height}`,
            viewport: `${window.innerWidth}x${window.innerHeight}`
        };

        this.eventQueue.push(event);
        console.log('📝 Event queued:', event.event_type, event.item_id || '');

        // Send immediately if queue reaches batch size
        if (this.eventQueue.length >= this.batchSize) {
            this.flushEvents();
        }
    }

    // Send queued events to backend
    async flushEvents() {
        if (this.eventQueue.length === 0) return;

        const events = [...this.eventQueue];
        this.eventQueue = []; // Clear queue immediately

        try {
            const response = await fetch(`${this.apiBase}/api/track_events_batch`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ events })
            });

            if (response.ok) {
                console.log('✅ Events sent successfully:', events.length);
            } else {
                console.error('❌ Failed to send events:', response.status);
                // Re-add events to queue for retry
                this.eventQueue.unshift(...events);
            }
        } catch (error) {
            console.error('❌ Error sending events:', error);
            // Re-add events to queue for retry
            this.eventQueue.unshift(...events);
        }
    }

    // Start automatic event flushing
    startEventFlushing() {
        setInterval(() => {
            if (this.eventQueue.length > 0) {
                this.flushEvents();
            }
        }, this.flushInterval);
    }

    // Track page view automatically
    trackPageViewAuto(pagePath, additionalData = {}) {
        this.queueEvent({
            event_type: "view_page",
            item_id: pagePath,
            item_name: `Page: ${pagePath}`,
            category: "page_view",
            price: 0,
            brand: "system",
            ...additionalData
        });
    }

    // Track product view automatically
    trackProductViewAuto(product, additionalData = {}) {
        this.queueEvent({
            event_type: "view_product",
            item_id: product.item_id,
            item_name: product.item_name,
            category: product.category,
            price: product.price,
            brand: product.brand,
            ...additionalData
        });
    }

    // Track product click automatically
    trackProductClickAuto(product, element = "unknown", position = "unknown") {
        this.queueEvent({
            event_type: "click_product",
            item_id: product.item_id,
            item_name: product.item_name,
            category: product.category,
            price: product.price,
            brand: product.brand,
            element: element,
            position: position
        });
    }

    // Track add to cart automatically
    trackAddToCartAuto(product, quantity = 1, additionalData = {}) {
        this.queueEvent({
            event_type: "add_to_cart",
            item_id: product.item_id,
            item_name: product.item_name,
            category: product.category,
            price: product.price,
            brand: product.brand,
            quantity: quantity,
            cart_total: this.getCartTotal(),
            ...additionalData
        });
    }

    // Track purchase automatically
    trackPurchaseAuto(cartItems, totalAmount, additionalData = {}) {
        this.queueEvent({
            event_type: "purchase",
            items: cartItems.map(item => ({
                item_id: item.item_id,
                item_name: item.item_name,
                category: item.category,
                price: item.price,
                brand: item.brand,
                quantity: item.quantity
            })),
            total_amount: totalAmount,
            payment_method: additionalData.payment_method || "simulated",
            ...additionalData
        });
    }

    // Track search automatically
    trackSearchAuto(query, resultsCount = 0, additionalData = {}) {
        this.queueEvent({
            event_type: "search",
            search_query: query,
            results_count: resultsCount,
            ...additionalData
        });
    }

    // Track category view automatically
    trackCategoryViewAuto(category, productCount = 0, additionalData = {}) {
        this.queueEvent({
            event_type: "view_category",
            category: category,
            product_count: productCount,
            ...additionalData
        });
    }

    // Track recommendation interaction automatically
    trackRecommendationInteractionAuto(recommendation, action = "view", additionalData = {}) {
        this.queueEvent({
            event_type: "recommendation_interaction",
            recommendation_action: action,
            item_id: recommendation.item_id,
            item_name: recommendation.item_name,
            category: recommendation.category,
            price: recommendation.price,
            score: recommendation.score || 0,
            ...additionalData
        });
    }

    // Track time spent on page
    trackTimeSpentAuto(pageName, timeSpent, additionalData = {}) {
        this.queueEvent({
            event_type: "time_spent",
            page_name: pageName,
            time_spent_seconds: timeSpent,
            ...additionalData
        });
    }

    // Track scroll depth
    trackScrollDepthAuto(pageName, scrollDepth, additionalData = {}) {
        this.queueEvent({
            event_type: "scroll_depth",
            page_name: pageName,
            scroll_depth_percent: scrollDepth,
            ...additionalData
        });
    }

    // Setup automatic click tracking
    setupClickTracking() {
        document.addEventListener('click', (e) => {
            const productElement = e.target.closest('[data-product-id]');
            if (productElement) {
                const productId = productElement.dataset.productId;
                const product = this.findProductById(productId);
                if (product) {
                    this.trackProductClickAuto(product, e.target.tagName, 'auto_detected');
                }
            }

            // Track recommendation clicks
            const recommendationElement = e.target.closest('[data-recommendation-id]');
            if (recommendationElement) {
                const recommendationId = recommendationElement.dataset.recommendationId;
                const recommendation = this.findRecommendationById(recommendationId);
                if (recommendation) {
                    this.trackRecommendationInteractionAuto(recommendation, 'click');
                }
            }
        });
    }

    // Setup scroll tracking
    setupScrollTracking() {
        let maxScrollDepth = 0;
        let scrollTimer = null;

        window.addEventListener('scroll', () => {
            const scrollDepth = Math.round((window.scrollY / (document.body.scrollHeight - window.innerHeight)) * 100);
            if (scrollDepth > maxScrollDepth) {
                maxScrollDepth = scrollDepth;
            }

            // Track scroll depth at 25%, 50%, 75%, 100%
            const thresholds = [25, 50, 75, 100];
            thresholds.forEach(threshold => {
                if (scrollDepth >= threshold && !this[`scroll_${threshold}_tracked`]) {
                    this[`scroll_${threshold}_tracked`] = true;
                    this.trackScrollDepthAuto(window.location.pathname, threshold);
                }
            });
        });

        // Track time spent on page
        let pageEnterTime = Date.now();
        window.addEventListener('beforeunload', () => {
            const timeSpent = Math.round((Date.now() - pageEnterTime) / 1000);
            this.trackTimeSpentAuto(window.location.pathname, timeSpent);
            this.flushEvents(); // Send any remaining events
        });
    }

    // Setup time-based tracking
    setupTimeTracking() {
        // Track page view events
        this.trackPageViewAuto(window.location.pathname);

        // Track session duration periodically
        setInterval(() => {
            this.trackTimeSpentAuto(window.location.pathname, 30); // Track every 30 seconds
        }, 30000);
    }

    // Helper functions
    findProductById(productId) {
        if (typeof products !== 'undefined' && products) {
            return products.find(p => p.item_id === productId);
        }
        return null;
    }

    findRecommendationById(recommendationId) {
        // This would need to be implemented based on how recommendations are stored
        return null;
    }

    getCartTotal() {
        if (typeof cart !== 'undefined' && cart.getTotal) {
            return cart.getTotal();
        }
        return 0;
    }

    // Get current user info
    getCurrentUserInfo() {
        return {
            userId: this.userId,
            sessionId: this.sessionId,
            eventsInQueue: this.eventQueue.length,
            isTracking: this.isTracking
        };
    }

    // Get real-time user insights
    async getRealtimeInsights() {
        try {
            const response = await fetch(`${this.apiBase}/api/realtime-insights/${this.userId}`);
            if (response.ok) {
                return await response.json();
            }
        } catch (error) {
            console.error('Error getting realtime insights:', error);
        }
        return null;
    }

    // Get current user info
    getCurrentUserInfo() {
        return {
            userId: this.userId,
            sessionId: this.sessionId,
            isTracking: this.isTracking,
            eventsInQueue: this.eventQueue.length
        };
    }
}

// Global functions for easy integration
let realtimeTracker;

window.trackProductViewAuto = (product, additionalData) => realtimeTracker.trackProductViewAuto(product, additionalData);
window.trackProductClickAuto = (product, element, position) => realtimeTracker.trackProductClickAuto(product, element, position);
window.trackAddToCartAuto = (product, quantity, additionalData) => realtimeTracker.trackAddToCartAuto(product, quantity, additionalData);
window.trackPurchaseAuto = (cartItems, totalAmount, additionalData) => realtimeTracker.trackPurchaseAuto(cartItems, totalAmount, additionalData);
window.trackSearchAuto = (query, resultsCount, additionalData) => realtimeTracker.trackSearchAuto(query, resultsCount, additionalData);
window.trackCategoryViewAuto = (category, productCount, additionalData) => realtimeTracker.trackCategoryViewAuto(category, productCount, additionalData);
window.trackRecommendationInteractionAuto = (recommendation, action, additionalData) => realtimeTracker.trackRecommendationInteractionAuto(recommendation, action, additionalData);

// Get current user info
window.getCurrentUserInfo = () => realtimeTracker.getCurrentUserInfo();

// Initialize real-time tracker
realtimeTracker = new RealtimeUserTracker();
window.getRealtimeInsights = () => realtimeTracker.getRealtimeInsights();

// Enhanced tracking functions that work with DOM elements
window.trackProductElementClick = (element) => {
    const productElement = element.closest('[data-product-id]');
    if (productElement) {
        const productId = productElement.dataset.productId;
        const product = window.findProductById(productId);
        if (product) {
            realtimeTracker.trackProductClickAuto(product, element.tagName, 'auto_detected');
        }
    }
};

window.trackRecommendationElementClick = (element) => {
    const recommendationElement = element.closest('[data-recommendation-id]');
    if (recommendationElement) {
        const recommendationId = recommendationElement.dataset.recommendationId;
        const recommendation = window.findRecommendationById(recommendationId);
        if (recommendation) {
            realtimeTracker.trackRecommendationInteractionAuto(recommendation, 'click');
        }
    }
};

console.log('🚀 Real-time behavior tracking system initialized!');
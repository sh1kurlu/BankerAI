// User Behavior Tracking System

class UserTracker {
    constructor() {
        this.apiBase = 'http://127.0.0.1:8000';
        this.userId = this.getUserId();
        this.sessionId = this.generateSessionId();
        this.pageViewStartTime = null;
        this.productViewStartTimes = new Map();
        this.initializeTracking();
    }

    // Get or generate user ID
    getUserId() {
        let userId = localStorage.getItem('marketplace_user_id');
        if (!userId) {
            userId = this.generateUserId();
            localStorage.setItem('marketplace_user_id', userId);
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

    // Initialize tracking
    initializeTracking() {
        // Update user ID from input field if available
        const userIdInput = document.getElementById('user-id');
        if (userIdInput) {
            userIdInput.addEventListener('change', (e) => {
                if (e.target.value.trim()) {
                    this.userId = e.target.value.trim();
                    localStorage.setItem('marketplace_user_id', this.userId);
                    console.log('User ID updated:', this.userId);
                }
            });

            // Set current user ID in input
            userIdInput.value = this.userId;
        }

        // Track page view on load
        this.trackPageView(document.title);
    }

    // Track product view (with time tracking)
    trackProductView(product) {
        const viewStartTime = Date.now();
        this.productViewStartTimes.set(product.item_id, viewStartTime);

        const event = {
            user_id: this.userId,
            item_id: product.item_id,
            event_type: "view",
            timestamp: new Date().toISOString(),
            item_name: product.item_name,
            category: product.category,
            price: product.price,
            brand: product.brand,
            session_id: this.sessionId,
            page_url: window.location.href,
            referrer: document.referrer || null,
            user_agent: navigator.userAgent || null,
            screen_resolution: `${window.screen.width}x${window.screen.height}` || null,
            viewport: `${window.innerWidth}x${window.innerHeight}` || null
        };
        
        this.sendEvent(event);
        console.log('Product view tracked:', event);
    }

    // Track time spent on product page
    trackProductViewTime(product, timeSpentSeconds) {
        const event = {
            user_id: this.userId,
            item_id: product.item_id,
            event_type: "view",
            timestamp: new Date().toISOString(),
            time_spent_seconds: timeSpentSeconds,
            item_name: product.item_name,
            category: product.category,
            price: product.price,
            session_id: this.sessionId,
            page_url: window.location.href
        };
        
        this.sendEvent(event);
        console.log('Product view time tracked:', event);
    }

    // Track product click
    trackProductClick(product) {
        const event = {
            user_id: this.userId,
            item_id: product.item_id,
            event_type: "click",
            timestamp: new Date().toISOString(),
            item_name: product.item_name,
            category: product.category,
            price: product.price,
            brand: product.brand,
            session_id: this.sessionId,
            page_url: window.location.href,
            referrer: document.referrer || null
        };
        
        this.sendEvent(event);
        console.log('Product click tracked:', event);
    }

    // Track add to cart
    trackAddToCart(product, quantity = 1) {
        const event = {
            user_id: this.userId,
            item_id: product.item_id,
            event_type: "add_to_cart",
            timestamp: new Date().toISOString(),
            item_name: product.item_name,
            category: product.category,
            price: product.price,
            brand: product.brand,
            quantity: quantity,
            session_id: this.sessionId,
            page_url: window.location.href
        };
        
        this.sendEvent(event);
        console.log('Add to cart tracked:', event);
    }

    // Track purchase
    trackPurchase(cartItems, totalAmount) {
        // Track each item in the purchase
        cartItems.forEach(item => {
            const event = {
                user_id: this.userId,
                item_id: item.item_id,
                event_type: "purchase",
                timestamp: new Date().toISOString(),
                item_name: item.item_name,
                category: item.category,
                price: item.price,
                brand: item.brand,
                quantity: item.quantity,
                session_id: this.sessionId,
                page_url: window.location.href
            };
            
            this.sendEvent(event);
        });
        
        console.log('Purchase tracked:', { items: cartItems.length, total: totalAmount });
    }

    // Track search
    trackSearch(query, resultsCount = 0) {
        const event = {
            user_id: this.userId,
            event_type: "search",
            timestamp: new Date().toISOString(),
            search_query: query,
            results_count: resultsCount,
            session_id: this.sessionId,
            page_url: window.location.href
        };
        
        this.sendEvent(event);
        console.log('Search tracked:', event);
    }

    // Track category view
    trackCategoryView(category, productCount = 0) {
        const event = {
            user_id: this.userId,
            event_type: "view",
            timestamp: new Date().toISOString(),
            category: category,
            session_id: this.sessionId,
            page_url: window.location.href
        };
        
        this.sendEvent(event);
        console.log('Category view tracked:', event);
    }

    // Track page view
    trackPageView(pageName, additionalData = {}) {
        this.pageViewStartTime = Date.now();
        
        const event = {
            user_id: this.userId,
            event_type: "view",
            timestamp: new Date().toISOString(),
            page_url: window.location.href,
            referrer: document.referrer || null,
            session_id: this.sessionId,
            user_agent: navigator.userAgent || null,
            screen_resolution: `${window.screen.width}x${window.screen.height}` || null,
            viewport: `${window.innerWidth}x${window.innerHeight}` || null,
            ...additionalData
        };
        
        this.sendEvent(event);
        console.log('Page view tracked:', event);
    }

    // Track recommendation interaction
    trackRecommendationInteraction(recommendation, action = "view") {
        const event = {
            user_id: this.userId,
            event_type: "click",
            timestamp: new Date().toISOString(),
            item_id: recommendation.item_id,
            item_name: recommendation.item_name,
            category: recommendation.category,
            price: recommendation.price,
            recommendation_action: action,
            session_id: this.sessionId,
            page_url: window.location.href
        };
        
        this.sendEvent(event);
        console.log('Recommendation interaction tracked:', event);
    }

    // Send event to backend
    async sendEvent(eventData) {
        try {
            const response = await fetch(`${this.apiBase}/api/track_event`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(eventData)
            });

            if (!response.ok) {
                console.error('Failed to track event:', response.status, response.statusText);
                return false;
            }

            const result = await response.json();
            console.log('Event tracked successfully:', result);
            return true;
        } catch (error) {
            console.error('Error tracking event:', error);
            return false;
        }
    }

    // Get cart total (helper function)
    getCartTotal() {
        if (typeof cart !== 'undefined' && cart.getTotal) {
            return cart.getTotal();
        }
        return 0;
    }

    // Batch track multiple events
    async trackEvents(events) {
        const promises = events.map(event => this.sendEvent(event));
        return Promise.all(promises);
    }

    // Get tracking summary
    getTrackingSummary() {
        return {
            userId: this.userId,
            sessionId: this.sessionId,
            eventsSent: this.eventsSent || 0,
            apiBase: this.apiBase
        };
    }
}

// Initialize tracker
const userTracker = new UserTracker();

// Make tracking functions available globally
window.trackingFunctions = {
    // Track product interactions
    viewProduct: (product) => userTracker.trackProductView(product),
    clickProduct: (product) => userTracker.trackProductClick(product),
    addToCart: (product, quantity = 1) => userTracker.trackAddToCart(product, quantity),
    purchase: (cartItems, totalAmount) => userTracker.trackPurchase(cartItems, totalAmount),
    
    // Track navigation
    search: (query, resultsCount) => userTracker.trackSearch(query, resultsCount),
    viewCategory: (category, productCount) => userTracker.trackCategoryView(category, productCount),
    viewPage: (pageName, additionalData) => userTracker.trackPageView(pageName, additionalData),
    
    // Track recommendations
    interactWithRecommendation: (recommendation, action) => userTracker.trackRecommendationInteraction(recommendation, action),
    
    // Get current user info
    getUserId: () => userTracker.userId,
    getTrackingSummary: () => userTracker.getTrackingSummary()
};

// Global tracking functions for easy access
window.trackProductView = (product) => userTracker.trackProductView(product);
window.trackProductClick = (product) => userTracker.trackProductClick(product);
window.trackAddToCart = (product, quantity) => userTracker.trackAddToCart(product, quantity);
window.trackPurchase = (cartItems, totalAmount) => userTracker.trackPurchase(cartItems, totalAmount);
window.trackSearch = (query, resultsCount) => userTracker.trackSearch(query, resultsCount);
window.trackCategoryView = (category, productCount) => userTracker.trackCategoryView(category, productCount);
window.trackPageView = (pageName, additionalData) => userTracker.trackPageView(pageName, additionalData);
window.trackRecommendationInteraction = (recommendation, action) => userTracker.trackRecommendationInteraction(recommendation, action);
window.trackProductViewTime = (product, timeSpent) => userTracker.trackProductViewTime(product, timeSpent);
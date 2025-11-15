// Step-by-step User Behavior Tracking System

class UserTracker {
    constructor() {
        this.apiBase = 'http://127.0.0.1:8000';
        this.userId = this.getUserId();
        this.sessionId = this.generateSessionId();
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
    }

    // Track product view
    trackProductView(product) {
        const event = {
            user_id: this.userId,
            event_type: "view_product",
            timestamp: new Date().toISOString(),
            item_id: product.item_id,
            item_name: product.item_name,
            category: product.category,
            price: product.price,
            brand: product.brand,
            session_id: this.sessionId,
            page_url: window.location.href,
            referrer: document.referrer
        };

        this.sendEvent(event);
        console.log('Product view tracked:', event);
    }

    // Track product click
    trackProductClick(product) {
        const event = {
            user_id: this.userId,
            event_type: "click_product",
            timestamp: new Date().toISOString(),
            item_id: product.item_id,
            item_name: product.item_name,
            category: product.category,
            price: product.price,
            brand: product.brand,
            session_id: this.sessionId,
            page_url: window.location.href,
            referrer: document.referrer
        };

        this.sendEvent(event);
        console.log('Product click tracked:', event);
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
}

// Initialize tracker
const userTracker = new UserTracker();

// Global tracking functions for easy access
window.trackProductView = (product) => userTracker.trackProductView(product);
window.trackProductClick = (product) => userTracker.trackProductClick(product);
window.trackPageView = (pageName, additionalData) => {
    const event = {
        user_id: userTracker.userId,
        event_type: "page_view",
        timestamp: new Date().toISOString(),
        page_name: pageName,
        page_url: window.location.href,
        session_id: userTracker.sessionId,
        ...additionalData
    };
    userTracker.sendEvent(event);
};
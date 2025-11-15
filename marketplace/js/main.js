// Main Marketplace JavaScript

// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeMarketplace();
});

// Initialize marketplace
function initializeMarketplace() {
    console.log('Initializing MarketPlace...');
    
    // Track page view
    if (typeof trackPageView === 'function') {
        trackPageView('home_page', {
            page_title: document.title,
            user_agent: navigator.userAgent,
            screen_resolution: `${window.screen.width}x${window.screen.height}`
        });
    }

    // Render featured products
    renderFeaturedProducts();
    
    // Setup AI recommendations
    setupAIRecommendations();
    
    // Setup product interactions
    setupProductInteractions();
    
    // Setup category interactions
    setupCategoryInteractions();
    
    console.log('MarketPlace initialized successfully');
}

// Render featured products
function renderFeaturedProducts() {
    const featuredContainer = document.getElementById('featured-products');
    if (!featuredContainer) return;

    const featuredProducts = getRandomProducts(8); // Get 8 random products for featured section
    
    featuredContainer.innerHTML = featuredProducts.map(product => `
        <div class="product-card bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-all duration-300 fade-in" 
             data-item-id="${product.item_id}">
            <div class="relative overflow-hidden">
                <img src="${product.image}" alt="${product.item_name}" class="product-image w-full h-48 object-cover">
                <div class="absolute inset-0 bg-black bg-opacity-0 hover:bg-opacity-10 transition-all duration-300"></div>
            </div>
            <div class="product-info p-4">
                <h3 class="product-title text-lg font-semibold text-gray-800 mb-2 line-clamp-2">${product.item_name}</h3>
                <p class="product-brand text-sm text-gray-600 mb-2">${product.brand}</p>
                <p class="product-description text-sm text-gray-600 mb-3 line-clamp-2">${product.description}</p>
                <div class="flex items-center justify-between mb-4">
                    <span class="product-price text-xl font-bold text-blue-600">$${product.price.toFixed(2)}</span>
                    <span class="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded">${product.category}</span>
                </div>
                <div class="flex space-x-2">
                    <button class="add-to-cart-btn flex-1 bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition-colors text-sm font-medium" 
                            data-item-id="${product.item_id}">
                        <svg class="w-4 h-4 inline mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4m0 0L7 13m0 0l-1.5 6M7 13l-1.5 6m0 0h9m-9 0V19a2 2 0 002 2h7a2 2 0 002-2v-1.5M16 6a2 2 0 11-4 0 2 2 0 014 0z"></path>
                        </svg>
                        Add to Cart
                    </button>
                    <button class="view-details-btn bg-gray-100 text-gray-700 py-2 px-3 rounded-lg hover:bg-gray-200 transition-colors text-sm" 
                            data-item-id="${product.item_id}">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>
                        </svg>
                    </button>
                </div>
            </div>
        </div>
    `).join('');
}

// Setup AI recommendations
function setupAIRecommendations() {
    const recommendationsBtn = document.getElementById('get-recommendations-btn');
    const recommendationsSection = document.getElementById('recommendations-section');
    const recommendationsGrid = document.getElementById('recommendations-grid');

    if (!recommendationsBtn || !recommendationsSection || !recommendationsGrid) return;

    recommendationsBtn.addEventListener('click', async function() {
        const userId = document.getElementById('user-id').value.trim();
        
        if (!userId) {
            alert('Please enter a user ID to get recommendations');
            return;
        }

        // Show loading state
        recommendationsBtn.innerHTML = '<div class="loading-spinner mr-2"></div> Getting Recommendations...';
        recommendationsBtn.disabled = true;

        try {
            // Get AI recommendations
            const recommendations = await getAIRecommendations(userId, 4);
            
            if (recommendations && recommendations.length > 0) {
                renderRecommendations(recommendations);
                recommendationsSection.classList.remove('hidden');
                
                // Track recommendation interaction
                recommendations.forEach(rec => {
                    if (typeof trackRecommendationInteraction === 'function') {
                        trackRecommendationInteraction(rec, 'view');
                    }
                });
            } else {
                recommendationsGrid.innerHTML = '<p class="text-gray-500 text-center col-span-full">No recommendations available. Try browsing some products first!</p>';
                recommendationsSection.classList.remove('hidden');
            }
        } catch (error) {
            console.error('Error getting recommendations:', error);
            recommendationsGrid.innerHTML = '<p class="text-red-500 text-center col-span-full">Error loading recommendations. Please try again.</p>';
            recommendationsSection.classList.remove('hidden');
        } finally {
            // Reset button state
            recommendationsBtn.innerHTML = 'Get AI Recommendations';
            recommendationsBtn.disabled = false;
        }
    });
}

// Get AI recommendations from backend
async function getAIRecommendations(userId, k = 4) {
    try {
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
        return data.recommendations || [];
    } catch (error) {
        console.error('Error fetching recommendations:', error);
        throw error;
    }
}

// Render recommendations
function renderRecommendations(recommendations) {
    const recommendationsGrid = document.getElementById('recommendations-grid');
    if (!recommendationsGrid) return;

    recommendationsGrid.innerHTML = recommendations.map(rec => `
        <div class="product-card recommendation-card bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-all duration-300 fade-in" 
             data-item-id="${rec.item_id}">
            <div class="recommendation-badge">AI Recommended</div>
            <div class="relative overflow-hidden">
                <img src="${rec.image || 'https://via.placeholder.com/300x200?text=Product+Image'}" 
                     alt="${rec.item_name}" class="product-image w-full h-48 object-cover">
                <div class="absolute inset-0 bg-black bg-opacity-0 hover:bg-opacity-10 transition-all duration-300"></div>
            </div>
            <div class="product-info p-4">
                <h3 class="product-title text-lg font-semibold text-gray-800 mb-2 line-clamp-2">${rec.item_name}</h3>
                <p class="product-brand text-sm text-gray-600 mb-2">${rec.brand || 'Unknown Brand'}</p>
                <p class="product-description text-sm text-gray-600 mb-3 line-clamp-2">${rec.description || rec.feedback || 'Recommended based on your preferences'}</p>
                <div class="flex items-center justify-between mb-4">
                    <span class="product-price text-xl font-bold text-blue-600">$${(rec.price || 0).toFixed(2)}</span>
                    <span class="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded">${rec.category || 'General'}</span>
                </div>
                ${rec.score ? `<div class="mb-2">
                    <div class="flex items-center">
                        <span class="text-sm text-gray-600 mr-2">Score:</span>
                        <div class="flex-1 bg-gray-200 rounded-full h-2">
                            <div class="bg-blue-600 h-2 rounded-full" style="width: ${(rec.score * 100)}%"></div>
                        </div>
                        <span class="text-sm text-gray-600 ml-2">${(rec.score * 100).toFixed(0)}%</span>
                    </div>
                </div>` : ''}
                ${rec.feedback ? `<div class="mb-3 text-xs text-gray-600 bg-blue-50 p-2 rounded">
                    <strong>Why recommended:</strong> ${rec.feedback}
                </div>` : ''}
                <div class="flex space-x-2">
                    <button class="add-to-cart-btn flex-1 bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition-colors text-sm font-medium" 
                            data-item-id="${rec.item_id}">
                        <svg class="w-4 h-4 inline mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4m0 0L7 13m0 0l-1.5 6M7 13l-1.5 6m0 0h9m-9 0V19a2 2 0 002 2h7a2 2 0 002-2v-1.5M16 6a2 2 0 11-4 0 2 2 0 014 0z"></path>
                        </svg>
                        Add to Cart
                    </button>
                    <button class="view-details-btn bg-gray-100 text-gray-700 py-2 px-3 rounded-lg hover:bg-gray-200 transition-colors text-sm" 
                            data-item-id="${rec.item_id}">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>
                        </svg>
                    </button>
                </div>
            </div>
        </div>
    `).join('');
}

// Setup product interactions
function setupProductInteractions() {
    // Product card clicks
    document.addEventListener('click', function(e) {
        const productCard = e.target.closest('.product-card');
        const viewDetailsBtn = e.target.closest('.view-details-btn');
        
        if (productCard && !e.target.closest('.add-to-cart-btn')) {
            const itemId = productCard.dataset.itemId;
            if (itemId) {
                const product = getProductById(itemId);
                if (product) {
                    // Track product click
                    if (typeof trackProductClick === 'function') {
                        trackProductClick(product);
                    }
                    
                    // Navigate to product detail page
                    window.location.href = `product.html?item_id=${itemId}`;
                }
            }
        }
        
        if (viewDetailsBtn) {
            const itemId = viewDetailsBtn.dataset.itemId;
            if (itemId) {
                const product = getProductById(itemId);
                if (product) {
                    // Track product click
                    if (typeof trackProductClick === 'function') {
                        trackProductClick(product);
                    }
                    
                    // Navigate to product detail page
                    window.location.href = `product.html?item_id=${itemId}`;
                }
            }
        }
    });

    // Track product views (when cards come into view)
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const itemId = entry.target.dataset.itemId;
                if (itemId) {
                    const product = getProductById(itemId);
                    if (product) {
                        // Track product view
                        if (typeof trackProductView === 'function') {
                            trackProductView(product);
                        }
                        
                        // Stop observing this element
                        observer.unobserve(entry.target);
                    }
                }
            }
        });
    }, { threshold: 0.5 });

    // Observe all product cards
    setTimeout(() => {
        document.querySelectorAll('.product-card[data-item-id]').forEach(card => {
            observer.observe(card);
        });
    }, 1000);
}

// Setup category interactions
function setupCategoryInteractions() {
    // Category card clicks
    document.addEventListener('click', function(e) {
        const categoryCard = e.target.closest('.category-card');
        if (categoryCard) {
            const category = categoryCard.querySelector('h4')?.textContent.toLowerCase();
            if (category) {
                // Track category view
                if (typeof trackCategoryView === 'function') {
                    const products = getProductsByCategory(category);
                    trackCategoryView(category, products.length);
                }
            }
        }
    });
}

// Utility functions
function formatPrice(price) {
    return `$${price.toFixed(2)}`;
}

function truncateText(text, maxLength = 100) {
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength) + '...';
}

// Global functions for use in other pages
window.renderProductCard = function(product) {
    return `
        <div class="product-card bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-all duration-300" 
             data-item-id="${product.item_id}">
            <div class="relative overflow-hidden">
                <img src="${product.image}" alt="${product.item_name}" class="product-image w-full h-48 object-cover">
                <div class="absolute inset-0 bg-black bg-opacity-0 hover:bg-opacity-10 transition-all duration-300"></div>
            </div>
            <div class="product-info p-4">
                <h3 class="product-title text-lg font-semibold text-gray-800 mb-2 line-clamp-2">${product.item_name}</h3>
                <p class="product-brand text-sm text-gray-600 mb-2">${product.brand}</p>
                <p class="product-description text-sm text-gray-600 mb-3 line-clamp-2">${product.description}</p>
                <div class="flex items-center justify-between mb-4">
                    <span class="product-price text-xl font-bold text-blue-600">$${product.price.toFixed(2)}</span>
                    <span class="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded">${product.category}</span>
                </div>
                <div class="flex space-x-2">
                    <button class="add-to-cart-btn flex-1 bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition-colors text-sm font-medium" 
                            data-item-id="${product.item_id}">
                        Add to Cart
                    </button>
                    <button class="view-details-btn bg-gray-100 text-gray-700 py-2 px-3 rounded-lg hover:bg-gray-200 transition-colors text-sm" 
                            data-item-id="${product.item_id}">
                        View
                    </button>
                </div>
            </div>
        </div>
    `;
};

window.showLoadingSpinner = function(container) {
    if (container) {
        container.innerHTML = '<div class="flex justify-center items-center py-8"><div class="loading-spinner"></div></div>';
    }
};

window.showErrorMessage = function(container, message) {
    if (container) {
        container.innerHTML = `<div class="alert alert-error">${message}</div>`;
    }
};

window.showSuccessMessage = function(container, message) {
    if (container) {
        container.innerHTML = `<div class="alert alert-success">${message}</div>`;
    }
};
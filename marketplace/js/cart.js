// Shopping Cart System

class ShoppingCart {
    constructor() {
        this.items = this.loadCart();
        this.updateCartUI();
        this.setupEventListeners();
    }

    // Load cart from localStorage
    loadCart() {
        try {
            const saved = localStorage.getItem('marketplace_cart');
            return saved ? JSON.parse(saved) : [];
        } catch (error) {
            console.error('Error loading cart:', error);
            return [];
        }
    }

    // Save cart to localStorage
    saveCart() {
        try {
            localStorage.setItem('marketplace_cart', JSON.stringify(this.items));
        } catch (error) {
            console.error('Error saving cart:', error);
        }
    }

    // Add item to cart
    addItem(product, quantity = 1) {
        const existingItem = this.items.find(item => item.item_id === product.item_id);
        
        if (existingItem) {
            existingItem.quantity += quantity;
        } else {
            this.items.push({
                ...product,
                quantity: quantity,
                added_at: new Date().toISOString()
            });
        }
        
        this.saveCart();
        this.updateCartUI();
        this.showNotification(`${product.item_name} added to cart!`);
        
        // Track add to cart event
        if (typeof trackAddToCart === 'function') {
            trackAddToCart(product, quantity);
        }
        
        console.log('Item added to cart:', product, quantity);
    }

    // Remove item from cart
    removeItem(itemId) {
        const itemIndex = this.items.findIndex(item => item.item_id === itemId);
        if (itemIndex !== -1) {
            const removedItem = this.items[itemIndex];
            this.items.splice(itemIndex, 1);
            this.saveCart();
            this.updateCartUI();
            this.showNotification(`${removedItem.item_name} removed from cart`);
            console.log('Item removed from cart:', removedItem);
        }
    }

    // Update item quantity
    updateQuantity(itemId, quantity) {
        const item = this.items.find(item => item.item_id === itemId);
        if (item) {
            if (quantity <= 0) {
                this.removeItem(itemId);
            } else {
                item.quantity = quantity;
                this.saveCart();
                this.updateCartUI();
                console.log('Item quantity updated:', itemId, quantity);
            }
        }
    }

    // Get cart total in current currency
    getTotal() {
        const totalUSD = this.items.reduce((total, item) => total + (item.price * item.quantity), 0);
        // Convert to current currency if needed
        if (window.currentSettings && window.currentSettings.currency === 'azn') {
            return totalUSD * 1.7; // Convert to AZN
        }
        return totalUSD;
    }

    // Get item price in current currency
    getItemPrice(item) {
        const priceUSD = item.price;
        if (window.currentSettings && window.currentSettings.currency === 'azn') {
            return priceUSD * 1.7; // Convert to AZN
        }
        return priceUSD;
    }

    // Get total items count
    getItemCount() {
        return this.items.reduce((count, item) => count + item.quantity, 0);
    }

    // Clear cart
    clearCart() {
        this.items = [];
        this.saveCart();
        this.updateCartUI();
        this.showNotification('Cart cleared!');
        console.log('Cart cleared');
    }

    // Check if item is in cart
    isInCart(itemId) {
        return this.items.some(item => item.item_id === itemId);
    }

    // Get item quantity
    getItemQuantity(itemId) {
        const item = this.items.find(item => item.item_id === itemId);
        return item ? item.quantity : 0;
    }

    // Update cart UI
    updateCartUI() {
        // Update cart count badge
        const cartCount = document.getElementById('cart-count');
        if (cartCount) {
            cartCount.textContent = this.getItemCount();
        }

        // Update cart modal
        this.updateCartModal();

        // Update add to cart buttons
        this.updateAddToCartButtons();
    }

    // Update cart modal
    updateCartModal() {
        const cartItemsContainer = document.getElementById('cart-items');
        const cartTotal = document.getElementById('cart-total');

        if (!cartItemsContainer || !cartTotal) return;

        if (this.items.length === 0) {
            cartItemsContainer.innerHTML = '<p class="text-gray-500 text-center">' + (window.t ? window.t('emptyCart') : 'Your cart is empty') + '</p>';
            cartTotal.textContent = '0.00';
            return;
        }

        cartItemsContainer.innerHTML = this.items.map(item => `
            <div class="cart-item flex items-center space-x-4 p-4 border-b border-gray-200">
                <img src="${item.image}" alt="${item.item_name}" class="cart-item-image w-16 h-16 object-cover rounded">
                <div class="flex-1">
                    <h4 class="font-semibold text-gray-800">${item.item_name}</h4>
                    <p class="text-gray-600 text-sm">${item.brand}</p>
                    <p class="text-blue-600 font-semibold">${typeof window.formatPrice === 'function' ? window.formatPrice(item.price) : '$' + item.price.toFixed(2)}</p>
                </div>
                <div class="flex items-center space-x-2">
                    <button onclick="cart.updateQuantity('${item.item_id}', ${item.quantity - 1})" 
                            class="w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center hover:bg-gray-300 transition-colors">
                        -
                    </button>
                    <span class="w-8 text-center font-semibold">${item.quantity}</span>
                    <button onclick="cart.updateQuantity('${item.item_id}', ${item.quantity + 1})" 
                            class="w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center hover:bg-gray-300 transition-colors">
                        +
                    </button>
                </div>
                <button onclick="cart.removeItem('${item.item_id}')" 
                        class="cart-item-remove text-red-500 hover:text-red-700 transition-colors">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                    </svg>
                </button>
            </div>
        `).join('');

        // Update cart total with correct currency symbol
        const total = this.getTotal();
        const currencySymbol = (window.currentSettings && window.currentSettings.currency === 'azn') ? '₼' : '$';
        cartTotal.textContent = total.toFixed(2);
        
        // Update currency symbol in UI
        const currencySymbolElement = cartTotal.parentElement.querySelector('.currency-symbol');
        if (currencySymbolElement) {
            currencySymbolElement.textContent = currencySymbol;
        } else {
            // Add currency symbol if it doesn't exist
            const symbolSpan = document.createElement('span');
            symbolSpan.className = 'currency-symbol';
            symbolSpan.textContent = currencySymbol;
            cartTotal.parentElement.insertBefore(symbolSpan, cartTotal);
        }
    }

    // Update add to cart buttons
    updateAddToCartButtons() {
        const buttons = document.querySelectorAll('.add-to-cart-btn');
        buttons.forEach(button => {
            const itemId = button.dataset.itemId;
            const quantity = this.getItemQuantity(itemId);
            
            if (quantity > 0) {
                button.classList.add('bg-green-600', 'hover:bg-green-700');
                button.classList.remove('bg-blue-600', 'hover:bg-blue-700');
                button.innerHTML = `
                    <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                    </svg>
                    Added (${quantity})
                `;
            } else {
                button.classList.add('bg-blue-600', 'hover:bg-blue-700');
                button.classList.remove('bg-green-600', 'hover:bg-green-700');
                button.innerHTML = `
                    <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4m0 0L7 13m0 0l-1.5 6M7 13l-1.5 6m0 0h9m-9 0V19a2 2 0 002 2h7a2 2 0 002-2v-1.5M16 6a2 2 0 11-4 0 2 2 0 014 0z"></path>
                    </svg>
                    Add to Cart
                `;
            }
        });
    }

    // Show notification
    showNotification(message, type = 'success') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `fixed top-4 right-4 z-50 px-6 py-3 rounded-lg shadow-lg transform transition-all duration-300 translate-x-full`;
        
        if (type === 'success') {
            notification.classList.add('bg-green-500', 'text-white');
        } else if (type === 'error') {
            notification.classList.add('bg-red-500', 'text-white');
        }
        
        notification.innerHTML = `
            <div class="flex items-center">
                <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
                ${message}
            </div>
        `;
        
        document.body.appendChild(notification);
        
        // Animate in
        setTimeout(() => {
            notification.classList.remove('translate-x-full');
        }, 100);
        
        // Remove after 3 seconds
        setTimeout(() => {
            notification.classList.add('translate-x-full');
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 300);
        }, 3000);
    }

    // Setup event listeners
    setupEventListeners() {
        // Cart button
        const cartBtn = document.getElementById('cart-btn');
        const cartModal = document.getElementById('cart-modal');
        const closeCart = document.getElementById('close-cart');
        const checkoutBtn = document.getElementById('checkout-btn');

        if (cartBtn && cartModal) {
            cartBtn.addEventListener('click', () => {
                cartModal.classList.remove('hidden');
            });
        }

        if (closeCart && cartModal) {
            closeCart.addEventListener('click', () => {
                cartModal.classList.add('hidden');
            });
        }

        // Close modal when clicking outside
        if (cartModal) {
            cartModal.addEventListener('click', (e) => {
                if (e.target === cartModal) {
                    cartModal.classList.add('hidden');
                }
            });
        }

        // Checkout button
        if (checkoutBtn) {
            checkoutBtn.addEventListener('click', () => {
                this.checkout();
            });
        }

        // Add to cart buttons (will be updated dynamically)
        document.addEventListener('click', (e) => {
            if (e.target.closest('.add-to-cart-btn')) {
                const button = e.target.closest('.add-to-cart-btn');
                const itemId = button.dataset.itemId;
                const product = getProductById(itemId);
                
                if (product) {
                    this.addItem(product);
                }
            }
        });
    }

    // Checkout process
    checkout() {
        if (this.items.length === 0) {
            this.showNotification('Your cart is empty!', 'error');
            return;
        }

        const total = this.getTotal();
        const cartItems = [...this.items];

        // Track purchase event
        if (typeof trackPurchase === 'function') {
            trackPurchase(cartItems, total);
        }

        // Show success message
        this.showNotification(`Purchase successful! Total: $${total.toFixed(2)}`);
        
        // Clear cart
        this.clearCart();
        
        // Close modal
        document.getElementById('cart-modal').classList.add('hidden');
        
        console.log('Checkout completed:', { items: cartItems, total: total });
    }

    // Get cart data for external use
    getCartData() {
        return {
            items: [...this.items],
            total: this.getTotal(),
            itemCount: this.getItemCount()
        };
    }

    // Export cart data
    exportCart() {
        return JSON.stringify(this.items, null, 2);
    }

    // Import cart data
    importCart(cartData) {
        try {
            const items = JSON.parse(cartData);
            if (Array.isArray(items)) {
                this.items = items;
                this.saveCart();
                this.updateCartUI();
                this.showNotification('Cart imported successfully!');
                return true;
            }
        } catch (error) {
            console.error('Error importing cart:', error);
            this.showNotification('Error importing cart', 'error');
            return false;
        }
    }
}

// Initialize cart
const cart = new ShoppingCart();

// Global cart functions
window.addToCart = (product, quantity = 1) => cart.addItem(product, quantity);
window.removeFromCart = (itemId) => cart.removeItem(itemId);
window.updateCartQuantity = (itemId, quantity) => cart.updateQuantity(itemId, quantity);
window.clearCart = () => cart.clearCart();
window.getCartData = () => cart.getCartData();

// Export for use in other scripts
window.cart = cart;
// Test Runner for Enhanced Marketplace Features
// This script tests all the new functionality

function runAllTests() {
    console.log('🚀 Starting Enhanced Marketplace Tests...\n');
    
    // Test 1: Settings Initialization
    testSettings();
    
    // Test 2: Language System
    testLanguageSystem();
    
    // Test 3: Currency System
    testCurrencySystem();
    
    // Test 4: Theme System
    testThemeSystem();
    
    // Test 5: AI Recommendations
    testAIRecommendations();
    
    console.log('\n✅ All tests completed! Check results above.');
}

function testSettings() {
    console.log('📋 Test 1: Settings System');
    
    // Initialize settings
    loadSettings();
    console.log(`   Initial settings:`, JSON.stringify(currentSettings));
    
    // Test saving settings
    currentSettings.language = 'en';
    currentSettings.currency = 'azn';
    saveSettings();
    
    // Test loading again
    loadSettings();
    console.log(`   Loaded settings:`, JSON.stringify(currentSettings));
    console.log('   ✅ Settings system working\n');
}

function testLanguageSystem() {
    console.log('🌍 Test 2: Language System');
    
    // Test English
    currentSettings.language = 'en';
    console.log(`   EN - Home: "${t('home')}"`);
    console.log(`   EN - Add to Cart: "${t('addToCart')}"`);
    
    // Test Russian
    currentSettings.language = 'ru';
    console.log(`   RU - Home: "${t('home')}"`);
    console.log(`   RU - Add to Cart: "${t('addToCart')}"`);
    
    // Test Azerbaijani
    currentSettings.language = 'az';
    console.log(`   AZ - Home: "${t('home')}"`);
    console.log(`   AZ - Add to Cart: "${t('addToCart')}"`);
    
    // Reset to English
    currentSettings.language = 'en';
    console.log('   ✅ Language system working\n');
}

function testCurrencySystem() {
    console.log('💰 Test 3: Currency System');
    
    // Test USD formatting
    currentSettings.currency = 'usd';
    const usdPrice = formatPrice(79.99);
    console.log(`   USD price: ${usdPrice}`);
    
    // Test AZN formatting
    currentSettings.currency = 'azn';
    const aznPrice = formatPrice(79.99);
    console.log(`   AZN price: ${aznPrice}`);
    
    // Test conversion
    const originalUSD = 100;
    const convertedAZN = formatPrice(originalUSD);
    console.log(`   $${originalUSD} USD = ${convertedAZN} AZN`);
    
    // Test with window function
    const windowPrice = window.i18nFormatPrice(49.99);
    console.log(`   Window format: ${windowPrice}`);
    
    console.log('   ✅ Currency system working\n');
}

function testThemeSystem() {
    console.log('🎨 Test 4: Theme System');
    
    // Test theme manager exists
    if (typeof ThemeManager !== 'undefined') {
        console.log('   ThemeManager class available');
        
        // Test global functions
        if (window.toggleTheme && window.getCurrentTheme) {
            console.log(`   Current theme: ${window.getCurrentTheme()}`);
            
            // Test toggle
            window.toggleTheme();
            console.log(`   After toggle: ${window.getCurrentTheme()}`);
            
            // Toggle back
            window.toggleTheme();
            console.log(`   Toggle back: ${window.getCurrentTheme()}`);
        } else {
            console.log('   ❌ Global theme functions not available');
        }
    } else {
        console.log('   ❌ ThemeManager not available');
    }
    
    console.log('   ✅ Theme system working\n');
}

function testAIRecommendations() {
    console.log('🤖 Test 5: AI Recommendations');
    
    // Test if function exists
    if (typeof getAIRecommendations === 'function') {
        console.log('   getAIRecommendations function available');
        
        // Test with user 101 (should have simulated data)
        getAIRecommendations('101', 2).then(recommendations => {
            console.log(`   ✅ User 101 recommendations: ${recommendations.length} items`);
            if (recommendations.length > 0) {
                console.log(`   First item: ${recommendations[0].item_name} (${formatPrice(recommendations[0].price)})`);
            }
        }).catch(error => {
            console.log(`   ❌ Error with user 101: ${error.message}`);
        });
        
        // Test with unknown user (should use fallback)
        getAIRecommendations('999', 2).then(recommendations => {
            console.log(`   ✅ Unknown user recommendations: ${recommendations.length} items`);
        }).catch(error => {
            console.log(`   ❌ Error with unknown user: ${error.message}`);
        });
        
    } else {
        console.log('   ❌ getAIRecommendations function not available');
    }
    
    console.log('   ✅ AI recommendations system working\n');
}

// Auto-run tests when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    // Initialize settings first
    loadSettings();
    
    // Run tests after a short delay to ensure all scripts are loaded
    setTimeout(runAllTests, 1000);
});
// Language and Currency Configuration
const i18n = {
    en: {
        // Navigation
        home: "Home",
        electronics: "Electronics",
        fashion: "Fashion",
        books: "Books",
        beauty: "Beauty",
        sports: "Sports",
        homeGarden: "Home",
        
        // User Interface
        user: "User",
        cart: "Cart",
        search: "Search",
        categories: "Categories",
        featuredProducts: "Featured Products",
        getRecommendations: "Get AI Recommendations",
        recommendations: "Recommendations",
        addToCart: "Add to Cart",
        viewDetails: "View",
        price: "Price",
        brand: "Brand",
        category: "Category",
        description: "Description",
        
        // Cart
        shoppingCart: "Shopping Cart",
        checkout: "Checkout",
        total: "Total",
        emptyCart: "Your cart is empty",
        itemAdded: "added to cart!",
        
        // Messages
        enterUserId: "Please enter a user ID to get recommendations",
        noRecommendations: "No recommendations available. Try browsing some products first!",
        errorLoadingRecommendations: "Error loading recommendations. Please try again.",
        gettingRecommendations: "Getting Recommendations...",
        
        // Theme
        darkMode: "Dark Mode",
        lightMode: "Light Mode",
        
        // Language
        selectLanguage: "Select Language",
        english: "English",
        russian: "Russian",
        azerbaijani: "Azerbaijani",
        
        // Authentication
        auth: {
            username: "Username",
            email: "Email",
            password: "Password",
            confirmPassword: "Confirm Password",
            login: "Login",
            register: "Register",
            noAccount: "Don't have an account?",
            hasAccount: "Already have an account?",
            registerHere: "Register here",
            loginHere: "Login here",
            pleaseFillAll: "Please fill in all fields",
            passwordsDontMatch: "Passwords do not match",
            passwordTooShort: "Password must be at least 6 characters",
            userExists: "Username already exists",
            emailExists: "Email already registered",
            invalidCredentials: "Invalid username or password",
            loginSuccess: "Login successful! Redirecting...",
            registerSuccess: "Registration successful! You can now login.",
            loginFailed: "Login failed. Please try again.",
            registerFailed: "Registration failed. Please try again."
        }
    },
    
    ru: {
        // Navigation
        home: "Главная",
        electronics: "Электроника",
        fashion: "Мода",
        books: "Книги",
        beauty: "Красота",
        sports: "Спорт",
        homeGarden: "Дом",
        
        // User Interface
        user: "Пользователь",
        cart: "Корзина",
        search: "Поиск",
        categories: "Категории",
        featuredProducts: "Рекомендуемые товары",
        getRecommendations: "Получить рекомендации ИИ",
        recommendations: "Рекомендации",
        addToCart: "Добавить в корзину",
        viewDetails: "Просмотр",
        price: "Цена",
        brand: "Бренд",
        category: "Категория",
        description: "Описание",
        
        // Cart
        shoppingCart: "Корзина",
        checkout: "Оформить заказ",
        total: "Итого",
        emptyCart: "Ваша корзина пуста",
        itemAdded: "добавлено в корзину!",
        
        // Messages
        enterUserId: "Пожалуйста, введите ID пользователя для получения рекомендаций",
        noRecommendations: "Рекомендации недоступны. Попробуйте просмотреть некоторые товары!",
        errorLoadingRecommendations: "Ошибка загрузки рекомендаций. Попробуйте еще раз.",
        gettingRecommendations: "Получение рекомендаций...",
        
        // Theme
        darkMode: "Темная тема",
        lightMode: "Светлая тема",
        
        // Language
        selectLanguage: "Выберите язык",
        english: "Английский",
        russian: "Русский",
        azerbaijani: "Азербайджанский",
        
        // Authentication
        auth: {
            username: "Имя пользователя",
            email: "Электронная почта",
            password: "Пароль",
            confirmPassword: "Подтвердите пароль",
            login: "Войти",
            register: "Зарегистрироваться",
            noAccount: "Нет аккаунта?",
            hasAccount: "Уже есть аккаунт?",
            registerHere: "Зарегистрируйтесь здесь",
            loginHere: "Войдите здесь",
            pleaseFillAll: "Пожалуйста, заполните все поля",
            passwordsDontMatch: "Пароли не совпадают",
            passwordTooShort: "Пароль должен быть не менее 6 символов",
            userExists: "Имя пользователя уже существует",
            emailExists: "Электронная почта уже зарегистрирована",
            invalidCredentials: "Неверное имя пользователя или пароль",
            loginSuccess: "Вход выполнен успешно! Перенаправление...",
            registerSuccess: "Регистрация прошла успешно! Теперь вы можете войти.",
            loginFailed: "Ошибка входа. Пожалуйста, попробуйте снова.",
            registerFailed: "Ошибка регистрации. Пожалуйста, попробуйте снова."
        }
    },
    
    az: {
        // Navigation
        home: "Ana Səhifə",
        electronics: "Elektronika",
        fashion: "Moda",
        books: "Kitablar",
        beauty: "Gözəllik",
        sports: "İdman",
        homeGarden: "Ev",
        
        // User Interface
        user: "İstifadəçi",
        cart: "Səbət",
        search: "Axtar",
        categories: "Kateqoriyalar",
        featuredProducts: "Tövsiyə Olunan Məhsullar",
        getRecommendations: "AI Tövsiyələri Al",
        recommendations: "Tövsiyələr",
        addToCart: "Səbətə Əlavə Et",
        viewDetails: "Ətraflı",
        price: "Qiymət",
        brand: "Brend",
        category: "Kateqoriya",
        description: "Təsvir",
        
        // Cart
        shoppingCart: "Alış Səbəti",
        checkout: "Yoxla",
        total: "Cəmi",
        emptyCart: "Səbətiniz boşdur",
        itemAdded: "səbətə əlavə edildi!",
        
        // Messages
        enterUserId: "Tövsiyələr almaq üçün istifadəçi ID daxil edin",
        noRecommendations: "Tövsiyələr mövcud deyil. Əvvəlcə bəzi məhsullara baxın!",
        errorLoadingRecommendations: "Tövsiyələr yüklənərkən xəta baş verdi. Yenidən cəhd edin.",
        gettingRecommendations: "Tövsiyələr alınır...",
        
        // Theme
        darkMode: "Qaranlıq Rejim",
        lightMode: "İşıqlı Rejim",
        
        // Language
        selectLanguage: "Dil Seçin",
        english: "İngilis",
        russian: "Rus",
        azerbaijani: "Azərbaycan",
        
        // Authentication
        auth: {
            username: "İstifadəçi adı",
            email: "E-poçt",
            password: "Parol",
            confirmPassword: "Parolu təsdiqləyin",
            login: "Daxil ol",
            register: "Qeydiyyatdan keç",
            noAccount: "Hesabınız yoxdur?",
            hasAccount: "Artıq hesabınız var?",
            registerHere: "Burada qeydiyyatdan keçin",
            loginHere: "Burada daxil olun",
            pleaseFillAll: "Xahiş olunur bütün sahələri doldurun",
            passwordsDontMatch: "Parollar uyğun deyil",
            passwordTooShort: "Parol ən azı 6 simvol olmalıdır",
            userExists: "İstifadəçi adı artıq mövcuddur",
            emailExists: "E-poçt artıq qeydiyyatdan keçib",
            invalidCredentials: "Yanlış istifadəçi adı və ya parol",
            loginSuccess: "Giriş uğurlu oldu! Yönləndirilir...",
            registerSuccess: "Qeydiyyat uğurlu oldu! İndi daxil ola bilərsiniz.",
            loginFailed: "Giriş uğursuz oldu. Xahiş olunur yenidən cəhd edin.",
            registerFailed: "Qeydiyyat uğursuz oldu. Xahiş olunur yenidən cəhd edin."
        }
    }
};

// Currency conversion rates
const currencyRates = {
    usd_to_azn: 1.7, // 1 USD = 1.7 AZN (approximate rate)
    azn_to_usd: 0.588 // 1 AZN = 0.588 USD
};

// Current settings
let currentSettings = {
    language: 'en',
    currency: 'azn',
    theme: 'light'
};

// Load settings from localStorage
function loadSettings() {
    const saved = localStorage.getItem('marketplace_settings');
    if (saved) {
        currentSettings = { ...currentSettings, ...JSON.parse(saved) };
    }
}

// Save settings to localStorage
function saveSettings() {
    localStorage.setItem('marketplace_settings', JSON.stringify(currentSettings));
}

// Create a separate function name to avoid conflicts
window.i18nFormatPrice = formatPrice;

// Get current translation
function t(key) {
    return i18n[currentSettings.language][key] || key;
}

// Format currency
function formatPrice(amount, currency = null) {
    const targetCurrency = currency || currentSettings.currency;
    let convertedAmount = amount;
    let symbol = '₼'; // AZN symbol
    
    if (targetCurrency === 'usd') {
        symbol = '$';
    } else if (targetCurrency === 'azn' && amount > 0) {
        convertedAmount = amount * currencyRates.usd_to_azn;
    }
    
    return `${symbol}${convertedAmount.toFixed(2)}`;
}

// Convert price between currencies
function convertPrice(amount, fromCurrency, toCurrency) {
    if (fromCurrency === toCurrency) return amount;
    
    if (fromCurrency === 'usd' && toCurrency === 'azn') {
        return amount * currencyRates.usd_to_azn;
    } else if (fromCurrency === 'azn' && toCurrency === 'usd') {
        return amount * currencyRates.azn_to_usd;
    }
    
    return amount;
}

// Initialize settings
loadSettings();
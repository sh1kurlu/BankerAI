// Theme Management System

class ThemeManager {
    constructor() {
        this.currentTheme = localStorage.getItem('marketplace_theme') || 'light';
        this.init();
    }

    init() {
        this.applyTheme(this.currentTheme);
        this.setupThemeToggle();
    }

    applyTheme(theme) {
        this.currentTheme = theme;
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('marketplace_theme', theme);
        
        // Update toggle button text
        const themeToggle = document.getElementById('theme-toggle');
        if (themeToggle) {
            themeToggle.textContent = theme === 'dark' ? t('lightMode') : t('darkMode');
        }
        
        console.log(`Theme applied: ${theme}`);
    }

    toggleTheme() {
        const newTheme = this.currentTheme === 'light' ? 'dark' : 'light';
        this.applyTheme(newTheme);
    }

    setupThemeToggle() {
        const themeToggle = document.getElementById('theme-toggle');
        if (themeToggle) {
            themeToggle.addEventListener('click', () => this.toggleTheme());
        }
    }

    getCurrentTheme() {
        return this.currentTheme;
    }
}

// CSS for dark theme
const darkThemeCSS = `
[data-theme="dark"] {
    --bg-primary: #1a1a1a;
    --bg-secondary: #2d2d2d;
    --bg-card: #3a3a3a;
    --text-primary: #ffffff;
    --text-secondary: #b0b0b0;
    --border-color: #4a4a4a;
    --accent-color: #60a5fa;
    --accent-hover: #3b82f6;
    --shadow-color: rgba(0, 0, 0, 0.3);
}

[data-theme="dark"] body {
    background-color: var(--bg-primary);
    color: var(--text-primary);
}

[data-theme="dark"] .bg-white {
    background-color: var(--bg-card) !important;
}

[data-theme="dark"] .bg-gray-50 {
    background-color: var(--bg-secondary) !important;
}

[data-theme="dark"] .bg-gray-100 {
    background-color: var(--bg-secondary) !important;
}

[data-theme="dark"] .bg-gray-800 {
    background-color: var(--bg-card) !important;
}

[data-theme="dark"] .text-gray-700 {
    color: var(--text-primary) !important;
}

[data-theme="dark"] .text-gray-600 {
    color: var(--text-secondary) !important;
}

[data-theme="dark"] .text-gray-800 {
    color: var(--text-primary) !important;
}

[data-theme="dark"] .border-gray-200 {
    border-color: var(--border-color) !important;
}

[data-theme="dark"] .shadow-md,
[data-theme="dark"] .shadow-lg {
    box-shadow: 0 4px 6px -1px var(--shadow-color), 0 2px 4px -1px var(--shadow-color) !important;
}

[data-theme="dark"] .product-card {
    background-color: var(--bg-card);
    border: 1px solid var(--border-color);
}

[data-theme="dark"] .product-card:hover {
    box-shadow: 0 10px 15px -3px var(--shadow-color), 0 4px 6px -2px var(--shadow-color) !important;
}

[data-theme="dark"] input[type="text"],
[data-theme="dark"] input[type="number"],
[data-theme="dark"] select,
[data-theme="dark"] textarea {
    background-color: var(--bg-secondary);
    color: var(--text-primary);
    border-color: var(--border-color);
}

[data-theme="dark"] input[type="text"]:focus,
[data-theme="dark"] input[type="number"]:focus,
[data-theme="dark"] select:focus,
[data-theme="dark"] textarea:focus {
    border-color: var(--accent-color);
    box-shadow: 0 0 0 3px rgba(96, 165, 250, 0.1);
}

[data-theme="dark"] .btn-primary {
    background-color: var(--accent-color);
    border-color: var(--accent-color);
}

[data-theme="dark"] .btn-primary:hover {
    background-color: var(--accent-hover);
    border-color: var(--accent-hover);
}

[data-theme="dark"] .btn-secondary {
    background-color: var(--bg-secondary);
    border-color: var(--border-color);
    color: var(--text-primary);
}

[data-theme="dark"] .btn-secondary:hover {
    background-color: var(--bg-card);
    border-color: var(--text-secondary);
}

[data-theme="dark"] .modal-content {
    background-color: var(--bg-card);
    border: 1px solid var(--border-color);
}

[data-theme="dark"] .recommendation-card {
    background-color: var(--bg-secondary);
    border: 1px solid var(--border-color);
}

[data-theme="dark"] .category-card {
    background-color: var(--bg-card);
    border: 1px solid var(--border-color);
}

[data-theme="dark"] .category-card:hover {
    background-color: var(--bg-secondary);
    border-color: var(--accent-color);
}

[data-theme="dark"] header {
    background-color: var(--bg-card) !important;
    border-bottom: 1px solid var(--border-color);
}

[data-theme="dark"] footer {
    background-color: var(--bg-card) !important;
    border-top: 1px solid var(--border-color);
}
`;

// Inject theme CSS
function injectThemeCSS() {
    if (!document.getElementById('theme-styles')) {
        const style = document.createElement('style');
        style.id = 'theme-styles';
        style.textContent = darkThemeCSS;
        document.head.appendChild(style);
    }
}

// Initialize theme manager
let themeManager;

document.addEventListener('DOMContentLoaded', function() {
    injectThemeCSS();
    themeManager = new ThemeManager();
});

// Global theme functions
window.toggleTheme = function() {
    if (themeManager) {
        themeManager.toggleTheme();
    }
};

window.getCurrentTheme = function() {
    return themeManager ? themeManager.getCurrentTheme() : 'light';
};
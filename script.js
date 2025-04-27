// Global variables and constants
const pageTitle = 'SFYNX 7';

// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Only call initApp here - don't call it in other places to avoid duplication
    initApp();
});

// Initialize the application
function initApp() {
    console.log("initApp called");
    
    // Clear any existing title first to prevent duplicates
    const existingTitle = document.querySelector('.sidebar-title');
    if (existingTitle) {
        existingTitle.remove();
    }
    
    setupNavigation();
    loadHomePage();
    addStaticTitle();
}

// Set up navigation between pages
function setupNavigation() {
    const homeLink = document.querySelector('a[href="#home"]');
    const aboutLink = document.querySelector('a[href="#about"]');
    
    if (homeLink) {
        homeLink.addEventListener('click', function(e) {
            e.preventDefault();
            loadPage('home');
        });
    }
    
    if (aboutLink) {
        aboutLink.addEventListener('click', function(e) {
            e.preventDefault();
            loadPage('about');
        });
    }
    
    // Check for hash in URL on page load
    const hash = window.location.hash;
    if (hash === '#about') {
        loadPage('about');
    } else {
        loadPage('home');
    }
}

// Add static title below "About" in navigation
function addStaticTitle() {
    // Get the sidebar
    const sidebar = document.querySelector('.sidebar');
    if (!sidebar) return;
    
    // Check if title already exists and remove if it does
    const existingTitle = document.querySelector('.sidebar-title');
    if (existingTitle) {
        existingTitle.remove();
    }
    
    // Create title element
    const titleElement = document.createElement('div');
    titleElement.className = 'sidebar-title';
    titleElement.textContent = pageTitle;
    
    // Add title after About link
    sidebar.appendChild(titleElement);
    
    // Add CSS for the title
    const style = document.createElement('style');
    style.textContent = `
        .sidebar-title {
            font-family: 'Fira Code', monospace;
            font-size: 16px;
            font-weight: bold;
            text-align: left;
            color: #d8d8d8;
            margin-top: 10px;
            padding: 10px 10px;
            letter-spacing: 0.5px;
        }
    `;
    document.head.appendChild(style);
}

// Load the specified page content
function loadPage(page) {
    const contentDiv = document.getElementById('content');
    if (!contentDiv) return;
    
    // Update URL hash
    window.location.hash = page;
    console.log(`Loading page: ${page}`);
    
    if (page === 'home') {
        contentDiv.innerHTML = window.loadHomePage();
        
        // Re-setup event listeners for the home page
        const fileButton = document.getElementById('fileButton');
        const fileInput = document.getElementById('fileInput');
        const fileName = document.getElementById('fileName');
        const searchForm = document.getElementById('searchForm');
        
        if (fileButton && fileInput && fileName) {
            fileButton.addEventListener('click', () => {
                fileInput.click();
            });
            
            fileInput.addEventListener('change', function(e) {
                if (this.files.length > 0) {
                    fileName.textContent = this.files[0].name;
                } else {
                    fileName.textContent = 'No file chosen';
                }
            });
        }
        
        if (searchForm) {
            searchForm.addEventListener('submit', function(e) {
                e.preventDefault();
                window.searchQuotes();
            });
        }
    } else if (page === 'about') {
        console.log("About to load about page...");
        console.log("loadAboutPage available:", typeof window.loadAboutPage === 'function');
        contentDiv.innerHTML = window.loadAboutPage();
        console.log("About page loaded.");
    }
}

// Make key functions globally available
window.initApp = initApp;
window.setupNavigation = setupNavigation;
window.loadPage = loadPage;

// Function to initialize the page
function initializePage() {
    console.log("Initializing page - script.js");
    setupEventListeners();
}

// Setup event listeners
function setupEventListeners() {
    console.log("Setting up event listeners");
    document.querySelectorAll('.sidebar a').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const page = this.getAttribute('data-page');
            loadContent(page);
        });
    });

    window.addEventListener('resize', debounce(() => {
        console.log("Window resized");
    }, 250));
}

// Debounce function to limit the rate at which a function can fire
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Async function to load content dynamically
async function loadContent(page) {
    console.log(`Loading content for page: ${page}`);
    const contentDiv = document.getElementById('content');
    if (!contentDiv) {
        console.error("Content div not found");
        return;
    }

    try {
        let content;
        switch (page) {
            case 'home':
                console.log("Loading home page using global function");
                if (typeof window.loadHomePage === 'function') {
                    content = window.loadHomePage();
                } else {
                    throw new Error('loadHomePage function not found on window object');
                }
                break;
            case 'about':
                console.log("Loading about page (assuming global loadAboutPage)");
                if (typeof window.loadAboutPage === 'function') {
                     content = window.loadAboutPage();
                 } else {
                     content = `<h2>About</h2><p>About page content not loaded.</p>`;
                     console.warn('loadAboutPage function not found');
                 }
                break;
            default:
                console.log(`Loading default content for ${page}`);
                content = `<h2>${page}</h2><p>Content for ${page} goes here.</p>`;
        }
        
        contentDiv.innerHTML = content;
        console.log("Content loaded into div");
        
        if (page === 'home') {
            console.log("Setting up home page components after content load");
        }
    } catch (error) {
        console.error(`Error loading ${page} content:`, error);
        contentDiv.innerHTML = `<p>Error loading content. Please try again.</p>`;
    }
}
// Global variables and constants
const pageTitle = '- SFINX RESEARCH AIN -';
const ASCII_SIGIL_INTERVAL = 3330;

// Mouse object for particle interaction
const mouse = {
    x: null,
    y: null,
    radius: 50
};

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
                console.log("Loading home page");
                const { loadHomePage } = await import('./home.js');
                content = loadHomePage();
                break;
            case 'about':
                console.log("Loading about page");
                const { loadAboutPage } = await import('./about.js');
                content = loadAboutPage();
                break;
            default:
                console.log(`Loading default content for ${page}`);
                content = `<h2>${page}</h2><p>Content for ${page} goes here.</p>`;
        }
        
        contentDiv.innerHTML = content;
        console.log("Content loaded into div");
        
        if (page === 'home') {
            console.log("Setting up home page components");
            setupCanvasTitle(pageTitle);
            generateAsciiSigil();
            setupFileInputListener();
        }
    } catch (error) {
        console.error(`Error loading ${page} content:`, error);
        contentDiv.innerHTML = `<p>Error loading content. Please try again.</p>`;
    }
}

// Function to initialize the page
function initializePage() {
    console.log("Initializing page");
    generateSigil();
    loadContent('home');
    setupEventListeners();
    setInterval(generateAsciiSigil, ASCII_SIGIL_INTERVAL);
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
        const canvas = document.getElementById('titleCanvas');
        if (canvas) {
            setupCanvasTitle(pageTitle);
        }
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

function setupFileInputListener() {
    const fileInput = document.getElementById('fileInput');
    if (fileInput) {
        fileInput.addEventListener('change', function(event) {
            const fileName = event.target.files[0]?.name;
            const label = document.querySelector('.file-label');
            if (label) {
                label.textContent = fileName ? `File selected: ${fileName}` : 'Upload a file (PDF or TXT)';
            }
        });
    }
}

// Function to set up the canvas title
function setupCanvasTitle(title = pageTitle) {
    const canvas = document.getElementById('titleCanvas');
    if (!canvas) return;  // Exit if canvas doesn't exist

    const ctx = canvas.getContext('2d');
    canvas.width = canvas.offsetWidth;
    canvas.height = 200;

    // Get canvas position
    const canvasRect = canvas.getBoundingClientRect();

    // Update mouse position relative to canvas
    function updateMousePos(e) {
        mouse.x = e.clientX - canvasRect.left;
        mouse.y = e.clientY - canvasRect.top;
    }

    // Add mousemove event listener to canvas
    canvas.addEventListener('mousemove', updateMousePos);

    const particles = [];
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
    const text = title;

    // Class for each particle
    class Particle {
        constructor(x, y, char, isTitle = false) {
            this.x = x;
            this.y = y;
            this.char = char;
            this.size = isTitle ? 18 : 12;
            this.color = isTitle ? '#ffffff' : 'rgba(255, 255, 255, 0.5)';
            this.baseX = x;
            this.baseY = y;
            this.density = isTitle ? (Math.random() * 50) + 5 : (Math.random() * 30) + 1;
        }

        draw() {
            ctx.fillStyle = this.color;
            ctx.font = `${this.size}px Courier`;
            ctx.fillText(this.char, this.x, this.y);
        }

        update() {
            if (mouse.x === null || mouse.y === null) return;

            let dx = mouse.x - this.x;
            let dy = mouse.y - this.y;
            let distance = Math.sqrt(dx * dx + dy * dy);
            let forceDirectionX = dx / distance;
            let forceDirectionY = dy / distance;
            let maxDistance = mouse.radius;
            let force = (maxDistance - distance) / maxDistance;
            let directionX = forceDirectionX * force * this.density;
            let directionY = forceDirectionY * force * this.density;

            if (distance < mouse.radius) {
                this.x -= directionX;
                this.y -= directionY;
            } else {
                if (this.x !== this.baseX) {
                    let dx = this.x - this.baseX;
                    this.x -= dx / 10;
                }
                if (this.y !== this.baseY) {
                    let dy = this.y - this.baseY;
                    this.y -= dy / 10;
                }
            }
        }
    }

    // Initialize particles based on the title text and random characters
    function initParticles() {
        particles.length = 0;

        let size = 20;
        let x = 20;  // Start from the left edge with a small padding
        let y = 100;

        ctx.font = `${size}px Courier`;
        ctx.fillStyle = 'white';
        ctx.textAlign = 'left';
        ctx.fillText(text, x, y);

        const pixelData = ctx.getImageData(0, 0, canvas.width, canvas.height).data;

        for (let y = 0; y < canvas.height; y += 4) {
            for (let x = 0; x < canvas.width; x += 4) {
                if (pixelData[(y * canvas.width + x) * 4 + 3] > 128) {
                    let posX = x + Math.random() * 4;
                    let posY = y + Math.random() * 4;
                    particles.push(new Particle(posX, posY, chars[Math.floor(Math.random() * chars.length)]));
                }
            }
        }

        for (let i = 0; i < text.length; i++) {
            let posX = x + i * 20;
            let posY = 100;
            particles.push(new Particle(posX, posY, text[i], true));
        }
    }

    // Animate the particles
    function animateParticles() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        particles.forEach(particle => {
            particle.draw();
            particle.update();// Initialize the page when the DOM is fully loaded
            document.addEventListener('DOMContentLoaded', initializePage);
            
        });
        requestAnimationFrame(animateParticles);
    }

    initParticles();
    animateParticles();

    // Cleanup function
    return function cleanup() {
        canvas.removeEventListener('mousemove', updateMousePos);
    };
}

// Function to generate complex sigil pattern
function generateSigil() {
    const svg = document.getElementById('background-sigil');
    const numPaths = 50;
    let paths = '';

    for (let i = 0; i < numPaths; i++) {
        const points = [];
        for (let j = 0; j < 5; j++) {
            points.push(`${Math.random() * 1000},${Math.random() * 1000}`);
        }
        paths += `<path d="M${points.join(' L')}" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="2" />`;
    }

    svg.innerHTML = paths;
}

// Generate ASCII sigil art
function generateAsciiSigil() {
    const ascii = document.getElementById('ascii-sigil');
    if (ascii) {
        const chars = '╔╗╚╝║═╠╣╦╩╬';
        let art = '';
        for (let i = 0; i < 10; i++) {
            for (let j = 0; j < 40; j++) {
                art += chars[Math.floor(Math.random() * chars.length)];
            }
            art += '\n';
        }
        ascii.textContent = art;
    }
}

// Search quotes function
async function searchQuotes() {
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = 'Invoking...';

    const url = document.getElementById('urlInput').value;
    const file = document.getElementById('fileInput').files[0];
    const targetSum = document.getElementById('targetSum').value;

    if (!targetSum) {
        resultsDiv.innerHTML = 'Please enter a target sum.';
        return;
    }

    let formData = new FormData();
    formData.append('targetSum', targetSum);

    if (file) {
        formData.append('file', file);
    } else if (url) {
        formData.append('url', url);
    } else {
        resultsDiv.innerHTML = 'Please provide either a URL or upload a file.';
        return;
    }

    try {
        const response = await fetch('/api/gematria', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            if (data.quotes.length === 0) {
                resultsDiv.innerHTML = 'No matching quotes found.';
            } else {
                resultsDiv.innerHTML = `
                    <p>Total quotes found: ${data.quotes.length}</p>
                    <div class="quotes-container">
                        ${data.quotes.map(quote => `
                            <div class="quote">
                                <p>${quote.text}</p>
                                <p class="quote-info">Sum: ${quote.sum}, Source: ${quote.url}</p>
                            </div>
                        `).join('')}
                    </div>
                `;
            }
        } else {
            resultsDiv.innerHTML = `Error: ${data.error}`;
            if (data.traceback) {
                console.error('Server traceback:', data.traceback);
            }
        }
    } catch (error) {
        console.error('Fetch error:', error);
        resultsDiv.innerHTML = `An error occurred: ${error.message}`;
    }
}


// Initialize the page when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', () => {
    console.log("DOM fully loaded");
    initializePage();
});


// Expose necessary functions to global scope
window.searchQuotes = searchQuotes;
window.generateAsciiSigil = generateAsciiSigil;
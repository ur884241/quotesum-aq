// Global variables to hold dynamic page title
const pageTitle = 'SFINX RESEARCH AIN';  // Default title for the page

// Function to set up the canvas title with generative art overlay and interactive behavior
function setupCanvasTitle(title = pageTitle) {
    const canvas = document.getElementById('titleCanvas');
    const ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth;
    canvas.height = 200;

    const particles = [];
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
    const text = title;

    // Class for each particle
    class Particle {
        constructor(x, y, char, isTitle = false) {
            this.x = x;
            this.y = y;
            this.char = char;
            this.size = isTitle ? 18 : 12;  // Different size for title characters
            this.color = isTitle ? '#ffffff' : 'rgba(255, 255, 255, 0.5)';  // Different color for title
            this.baseX = x;
            this.baseY = y;
            this.density = isTitle ? (Math.random() * 50) + 5 : (Math.random() * 30) + 1;  // Title particles have higher density
        }

        draw() {
            ctx.fillStyle = this.color;
            ctx.font = `${this.size}px Courier`;
            ctx.fillText(this.char, this.x, this.y);  // Draw the character
        }

        update() {
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

        // Set font size for measuring title text
        let size = 24;
        let x = (canvas.width - ctx.measureText(text).width) / 2.3;
        let y = 100;

        ctx.font = `${size}px Courier`;
        ctx.fillStyle = 'white';
        ctx.fillText(text, x, y);

        // Get pixel data to create particles for the title text
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

        // Create particles specifically for the title text
        for (let i = 0; i < text.length; i++) {
            let posX = (canvas.width - ctx.measureText(text).width) / 2.3 + i * 20;  // Position title characters in center
            let posY = 100;
            particles.push(new Particle(posX, posY, text[i], true));  // `true` marks it as a title particle
        }
    }

    // Animate the particles to interact and move like the title
    function animateParticles() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        particles.forEach(particle => {
            particle.draw();
            particle.update();
        });
        requestAnimationFrame(animateParticles);
    }

    initParticles();  // Initialize particles
    animateParticles();  // Start animation
}

// Mouse object to track user's mouse movement for particle interaction
const mouse = {
    x: null,
    y: null,
    radius: 100
}

window.addEventListener('mousemove', function(event) {
    mouse.x = event.x;
    mouse.y = event.y;
});

// Function to generate complex sigil pattern without adding the title overlay
function generateSigil() {
    const svg = document.getElementById('background-sigil');
    const numPaths = 50;
    let paths = '';

    // Create complex sigil pattern without title
    for (let i = 0; i < numPaths; i++) {
        const points = [];
        for (let j = 0; j < 5; j++) {
            points.push(`${Math.random() * 1000},${Math.random() * 1000}`);
        }
        paths += `<path d="M${points.join(' L')}" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="2" />`;
    }

    svg.innerHTML = paths;  // Apply generated paths to SVG
}

// Generate ASCII sigil art
function generateAsciiSigil() {
    const ascii = document.getElementById('ascii-sigil');
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

// Initialize the page with the new title
generateSigil();  // Generate sigil pattern without overlay title
setupCanvasTitle(pageTitle);  // Overlay title on Canvas generative art
generateAsciiSigil();  // Generate ASCII sigil art

// Regenerate ASCII sigil every few seconds
setInterval(generateAsciiSigil, 3330);


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
                resultsDiv.innerHTML = `<p>Total quotes found: ${data.quotes.length}</p>`;
                resultsDiv.innerHTML += data.quotes.map(quote => `
                    <div class="quote">
                        <p>${quote.text}</p>
                        <p class="quote-info">Sum: ${quote.sum}, Source: ${quote.url}</p>
                    </div>
                `).join('');
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


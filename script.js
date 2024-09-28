// Generate complex sigil pattern
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

// Generate ASCII sigil
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

async function searchQuotes() {
    const urlInput = document.getElementById('urlInput');
    const targetSumInput = document.getElementById('targetSum');
    const resultsDiv = document.getElementById('results');

    if (!urlInput.value || !targetSumInput.value) {
        resultsDiv.innerHTML = '<p class="error">Please fill in both fields.</p>';
        return;
    }

    const url = urlInput.value;
    const targetSum = parseInt(targetSumInput.value);

    if (isNaN(targetSum)) {
        resultsDiv.innerHTML = '<p class="error">Please enter a valid number for the target sum.</p>';
        return;
    }

    resultsDiv.innerHTML = 'Searching for quotes...';

    try {
        const response = await fetch('/api/gematria', {
            method: 'POST',
            body: JSON.stringify({ url, targetSum }),
            headers: { 'Content-Type': 'application/json' }
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();

        if (data.success) {
            resultsDiv.innerHTML = `<h2>Found ${data.quotes.length} matching quotes:</h2>`;
            data.quotes.forEach((quote, index) => {
                resultsDiv.innerHTML += `<div class="quote"><p>${index + 1}. '${quote.text}' (Sum: ${quote.sum})</p></div>`;
            });
        } else {
            resultsDiv.innerHTML = `<p class="error">Error: ${data.error}</p>`;
        }
    } catch (error) {
        resultsDiv.innerHTML = `<p class="error">Error: ${error.message}</p>`;
    }
}

// Initialize
generateSigil();
generateAsciiSigil();

// Regenerate ASCII sigil every 10 seconds
setInterval(generateAsciiSigil, 3330);


const canvas = document.getElementById('titleCanvas');
const ctx = canvas.getContext('2d');

canvas.width = window.innerWidth;
canvas.height = 200;

const particles = [];
const text = 'GEMATRIA-SUM QUOTE FINDER';
const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';

class Particle {
    constructor(x, y, char) {
        this.x = x;
        this.y = y;
        this.char = char;
        this.size = 12;
        this.baseX = x;
        this.baseY = y;
        this.density = (Math.random() * 30) + 1;
    }

    draw() {
        ctx.fillStyle = 'white';
        ctx.font = '12px Courier';
        ctx.fillText(this.char, this.x, this.y);
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
                this.x -= dx/10;
            }
            if (this.y !== this.baseY) {
                let dy = this.y - this.baseY;
                this.y -= dy/10;
            }
        }
    }
}

function init() {
    particles.length = 0;
    let size = 24;
    let x = (canvas.width - ctx.measureText(text).width) / 2;
    let y = 100;

    ctx.font = size + 'px Courier';
    ctx.fillStyle = 'white';
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
}

const mouse = {
    x: null,
    y: null,
    radius: 100
}

window.addEventListener('mousemove', function(event) {
    mouse.x = event.x;
    mouse.y = event.y;
});

function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    for (let i = 0; i < particles.length; i++) {
        particles[i].draw();
        particles[i].update();
    }
    requestAnimationFrame(animate);
}

init();
animate();

// Periodically reinitialize to create fading effect
setInterval(() => {
    init();
}, 5000);
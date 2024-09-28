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
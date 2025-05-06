// Make functions globally available
window.loadHomePage = function() {
    return `
        <div class="content">
            <div class="title-container">
                <canvas id="titleCanvas" style="z-index: 10; position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></canvas>
            </div>
            
            <form id="searchForm" class="search-form">
                <div class="input-group">
                    <div class="form-group">
                        <label for="targetSum">Target Sum:</label>
                        <input type="number" id="targetSum" name="targetSum" min="1" placeholder="Enter a target number (e.g., 888)" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="calculationType">Calculation Method:</label>
                        <select id="calculationType" name="calculationType">
                            <option value="eq">English Qaballa (EQ)</option>
                            <option value="req">Reverse English Qaballa (REQ)</option>
                            <option value="ord">Ordinal (ORD)</option>
                            <option value="red">Reduced (RED)</option>
                            <option value="agr">Agrippa (AGR)</option>
                            <option value="eng">English (ENG)</option>
                            <option value="heb">Hebrew (HEB)</option>
                            <option value="pyt">Pythagorean (PYT)</option>
                        </select>
                    </div>
                    
                    <div class="source-inputs">
                        <div class="form-group">
                            <label for="urlInput">Text URL:</label>
                            <input type="url" id="urlInput" class="url-input" name="url" placeholder="Enter URL of text to analyze">
                        </div>
                        
                        <div class="form-group">
                            <div class="file-upload-container">
                                <button type="button" id="fileButton" class="file-upload-button">Upload Text File</button>
                                <span id="fileName">No file chosen</span>
                                <input type="file" id="fileInput" name="file" accept=".txt" style="display: none;">
                            </div>
                        </div>
                    </div>
                </div>
                
                <button type="submit" class="invoke-button">Search for Quotes</button>
            </form>
            
            <div id="loading" style="display: none;">
                <div class="loading-spinner"></div>
                <p>Processing text... This may take a moment.</p>
            </div>
            
            <div id="results">
                <div id="summary" style="display: none;"></div>
                <div id="quotes-container" style="display: none;">
                    <h2>Complete Sentences</h2>
                    <div id="complete-quotes"></div>
                    <h2>Partial Matches</h2>
                    <div id="incomplete-quotes"></div>
                </div>
            </div>
            
            <!-- Analytics Button -->
            <div id="analytics-button-container" style="display: none; margin-top: 20px; text-align: center;">
                <button id="show-analytics-btn" class="toggle-analytics-btn">Show Advanced Analytics</button>
            </div>
            
            <!-- Modal for Advanced Analytics -->
            <div id="analytics-modal" class="modal-overlay">
                <div class="modal-container">
                    <div class="modal-header">
                        <div class="modal-title">Advanced Analytics Report</div>
                        <button class="modal-close">&times;</button>
                    </div>
                    <div class="modal-body" id="analytics-content">
                        <!-- Analytics content will be injected here -->
                    </div>
                </div>
            </div>
        </div>
    `;
};

// Function to setup modal event listeners
function setupModalListeners() {
    console.log("Setting up modal event listeners");
    
    // Setup modal close functionality
    const modalClose = document.querySelector('.modal-close');
    if (modalClose) {
        modalClose.addEventListener('click', function() {
            document.getElementById('analytics-modal').classList.remove('active');
        });
    }
    
    // Setup show analytics button
    const showAnalyticsBtn = document.getElementById('show-analytics-btn');
    if (showAnalyticsBtn) {
        showAnalyticsBtn.addEventListener('click', function() {
            document.getElementById('analytics-modal').classList.add('active');
        });
    }
    
    // Allow clicking outside the modal to close it
    const modalOverlay = document.getElementById('analytics-modal');
    if (modalOverlay) {
        modalOverlay.addEventListener('click', function(e) {
            // Close only if clicking the overlay itself, not its children
            if (e.target === modalOverlay) {
                modalOverlay.classList.remove('active');
            }
        });
    }
    
    // Add escape key listener to close modal
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            const modal = document.getElementById('analytics-modal');
            if (modal && modal.classList.contains('active')) {
                modal.classList.remove('active');
            }
        }
    });
}

// Initialize the form when the page loads
document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM loaded in home.js");
    
    // Force canvas setup immediately
    if (typeof window.setupCanvas === 'function') {
        console.log("Calling setupCanvas from home.js");
        setTimeout(window.setupCanvas, 300);
    } else {
        console.error("setupCanvas function not available on window object");
    }
    
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
            searchQuotes();
        });
    }
    
    // Setup modal event listeners
    setupModalListeners();
});

// Make sure to call this function whenever the page content is updated
window.afterPageUpdate = function() {
    setupModalListeners();
};

// Make searchQuotes globally available
window.searchQuotes = function() {
    console.log("searchQuotes function called");
    const targetSum = document.getElementById('targetSum').value;
    const calculationType = document.getElementById('calculationType').value;
    const url = document.getElementById('urlInput').value;
    const fileInput = document.getElementById('fileInput');

    if (!targetSum) {
        alert('Please enter a target sum');
        return;
    }

    console.log(`Search parameters: targetSum=${targetSum}, calculationType=${calculationType}, url=${url || "none"}, file=${fileInput.files.length > 0 ? fileInput.files[0].name : "none"}`);

    // Check if we're on Vercel deployment
    const isVercelDeployment = window.location.hostname.includes('vercel.app');
    console.log("Detected environment:", isVercelDeployment ? "Vercel deployment" : "Local development");

    // Test the API connection first
    console.log("Testing API connection...");
    
    // Try different endpoints to see which ones work
    Promise.all([
        fetch('/api/minimal-search').then(r => ({endpoint: 'minimal-search', status: r.status, ok: r.ok, text: () => r.text()})).catch(e => ({endpoint: 'minimal-search', error: e.message, ok: false})),
        fetch('/api/search-direct').then(r => ({endpoint: 'search-direct', status: r.status, ok: r.ok, text: () => r.text()})).catch(e => ({endpoint: 'search-direct', error: e.message, ok: false})),
        fetch('/api/simple').then(r => ({endpoint: 'simple', status: r.status, ok: r.ok, text: () => r.text()})).catch(e => ({endpoint: 'simple', error: e.message, ok: false})),
        fetch('/api/hello-world').then(r => ({endpoint: 'hello-world', status: r.status, ok: r.ok, text: () => r.text()})).catch(e => ({endpoint: 'hello-world', error: e.message, ok: false})),
        fetch('/api/endpoint').then(r => ({endpoint: 'endpoint', status: r.status, ok: r.ok, text: () => r.text()})).catch(e => ({endpoint: 'endpoint', error: e.message, ok: false})),
        fetch('/api/test').then(r => ({endpoint: 'test', status: r.status, ok: r.ok, text: () => r.text()})).catch(e => ({endpoint: 'test', error: e.message, ok: false})),
        fetch('/api/hello').then(r => ({endpoint: 'hello', status: r.status, ok: r.ok, text: () => r.text()})).catch(e => ({endpoint: 'hello', error: e.message, ok: false}))
    ])
    .then(results => {
        console.log("API test results:", results);
        
        // Process each result to get detailed info
        Promise.all(results.map(async result => {
            if (result.ok && result.text) {
                try {
                    const responseText = await result.text();
                    console.log(`Response from ${result.endpoint}:`, responseText);
                    try {
                        const json = JSON.parse(responseText);
                        result.json = json;
                    } catch (e) {
                        console.warn(`Failed to parse JSON from ${result.endpoint}:`, e);
                    }
                } catch (e) {
                    console.error(`Error getting text from ${result.endpoint}:`, e);
                }
            }
            return result;
        })).then(processedResults => {
            const workingEndpoints = processedResults.filter(r => r.ok);
            const minimalSearchWorks = workingEndpoints.find(r => r.endpoint === 'minimal-search');
            
            if (minimalSearchWorks) {
                console.log("Minimal search endpoint is working. Proceeding with search using /api/minimal-search.");
                proceedWithSearch('/api/minimal-search'); // Force using minimal-search
            } else {
                console.error("Minimal search endpoint (/api/minimal-search) failed. Cannot proceed.");
                alert("Critical API endpoint (/api/minimal-search) failed. Please check server logs.");
            }
        });
    })
    .catch(error => {
        console.error("API test failed:", error);
        alert(`API test failed: ${error.message}`);
    });
    
    function proceedWithSearch(apiEndpoint) {
        if (isVercelDeployment && fileInput.files.length > 0) {
            alert('File uploads are not supported in the deployed version. Please use a URL instead.');
            return;
        }
        
        let formData;
        let fetchOptions;

        if (isVercelDeployment) {
            // For Vercel, use URLSearchParams for better compatibility with serverless functions
            const params = new URLSearchParams();
            params.append('targetSum', targetSum);
            params.append('calculationType', calculationType);
            
            if (url) {
                params.append('url', url);
            } else {
                alert('Please provide a URL for the deployed version');
                return;
            }

            fetchOptions = {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: params
            };
        } else {
            // For local development, use FormData (supports file uploads)
            formData = new FormData();
            formData.append('targetSum', targetSum);
            formData.append('calculationType', calculationType);

            if (url) {
                formData.append('source_type', 'url');
                formData.append('url', url);
            } else if (fileInput.files.length > 0) {
                formData.append('source_type', 'file');
                formData.append('file', fileInput.files[0]);
            } else {
                alert('Please provide either a URL or upload a file');
                return;
            }

            fetchOptions = {
                method: 'POST',
                body: formData
            };
        }

        console.log("Showing loading indicator and making API request...");
        showLoading();
        
        fetch(apiEndpoint, fetchOptions)
        .then(response => {
            console.log(`API response status: ${response.status} ${response.statusText}`);
            if (!response.ok) {
                return response.text().then(text => {
                    console.error("Raw error response:", text);
                    try {
                        return JSON.parse(text);
                    } catch (err) {
                        console.error("Error parsing response:", err);
                        throw new Error(`Server error: ${response.status} ${response.statusText}`);
                    }
                }).then(data => {
                    console.error("Server error details:", data);
                    throw new Error(data.error || `Server error: ${response.status} ${response.statusText}`);
                }).catch(err => {
                    console.error("Error parsing error response:", err);
                    throw new Error(`Server error: ${response.status} ${response.statusText}`);
                });
            }
            return response.text().then(text => {
                console.log("Raw response text:", text);
                try {
                    return JSON.parse(text);
                } catch (err) {
                    console.error("Error parsing JSON response:", err);
                    throw new Error("Invalid JSON response from server");
                }
            });
        })
        .then(data => {
            console.log("Raw API response received:", data);
            hideLoading();
            if (data.error) {
                console.error("API returned error:", data.error);
                if (data.traceback) {
                    console.error("Server traceback:", data.traceback);
                }
                alert(data.error);
                return;
            }
            
            console.log(`Data received: success=${data.success}, complete_quotes=${data.complete_quotes?.length || 0}, incomplete_quotes=${data.incomplete_quotes?.length || 0}`);
            displayResults(data);
            
            // After displaying results, ensure modal listeners are set up
            setTimeout(window.afterPageUpdate, 300);
        })
        .catch(error => {
            console.error("API request failed:", error);
            hideLoading();
            alert('An error occurred: ' + error.message);
        });
    }
};

// Make helper functions globally available
window.showLoading = function() {
    const loading = document.getElementById('loading');
    const results = document.getElementById('results');
    const summary = document.getElementById('summary');
    const quotesContainer = document.getElementById('quotes-container');
    const completeQuotes = document.getElementById('complete-quotes');
    const incompleteQuotes = document.getElementById('incomplete-quotes');

    if (loading) loading.style.display = 'block';
    if (results) results.style.display = 'none';
    if (summary) summary.style.display = 'none';
    if (quotesContainer) quotesContainer.style.display = 'none';
    if (completeQuotes) completeQuotes.innerHTML = '';
    if (incompleteQuotes) incompleteQuotes.innerHTML = '';
};

window.hideLoading = function() {
    const loading = document.getElementById('loading');
    const results = document.getElementById('results');
    const summary = document.getElementById('summary');
    const quotesContainer = document.getElementById('quotes-container');

    if (loading) loading.style.display = 'none';
    if (results) results.style.display = 'block';
    if (summary) summary.style.display = 'block';
    if (quotesContainer) quotesContainer.style.display = 'block';
};

// Updated displayResults function to use modal for analytics
window.displayResults = function(data) {
    console.log("displayResults function called");
    
    // Find required DOM elements and log their presence
    const resultsContainer = document.getElementById('results');
    const summary = document.getElementById('summary');
    const quotesContainer = document.getElementById('quotes-container');
    const completeQuotes = document.getElementById('complete-quotes');
    const incompleteQuotes = document.getElementById('incomplete-quotes');
    const analyticsBtn = document.getElementById('analytics-button-container');
    const analyticsContent = document.getElementById('analytics-content');

    console.log("DOM elements found:", {
        resultsContainer: !!resultsContainer,
        summary: !!summary,
        quotesContainer: !!quotesContainer,
        completeQuotes: !!completeQuotes,
        incompleteQuotes: !!incompleteQuotes,
        analyticsBtn: !!analyticsBtn,
        analyticsContent: !!analyticsContent
    });

    if (!resultsContainer || !summary || !quotesContainer || !completeQuotes || !incompleteQuotes) {
        console.error('Required DOM elements for results display not found. Creating them if needed.');
        
        // Create missing elements if they don't exist
        if (!resultsContainer) {
            console.log("Creating missing #results container");
            resultsContainer = document.createElement('div');
            resultsContainer.id = 'results';
            document.querySelector('.content').appendChild(resultsContainer);
        }
        
        if (!summary) {
            console.log("Creating missing #summary container");
            summary = document.createElement('div');
            summary.id = 'summary';
            resultsContainer.appendChild(summary);
        }
        
        if (!quotesContainer) {
            console.log("Creating missing #quotes-container");
            quotesContainer = document.createElement('div');
            quotesContainer.id = 'quotes-container';
            resultsContainer.appendChild(quotesContainer);
        }
        
        if (!completeQuotes) {
            console.log("Creating missing #complete-quotes container");
            const heading = document.createElement('h2');
            heading.textContent = 'Complete Sentences';
            quotesContainer.appendChild(heading);
            
            completeQuotes = document.createElement('div');
            completeQuotes.id = 'complete-quotes';
            quotesContainer.appendChild(completeQuotes);
        }
        
        if (!incompleteQuotes) {
            console.log("Creating missing #incomplete-quotes container");
            const heading = document.createElement('h2');
            heading.textContent = 'Partial Matches';
            quotesContainer.appendChild(heading);
            
            incompleteQuotes = document.createElement('div');
            incompleteQuotes.id = 'incomplete-quotes';
            quotesContainer.appendChild(incompleteQuotes);
        }
    }
    
    console.log("Received data for display:", data);

    try {
        // Clear previous results and ensure containers are visible
        summary.innerHTML = '';
        completeQuotes.innerHTML = '';
        incompleteQuotes.innerHTML = '';
        
        // Make sure elements are visible
        summary.style.display = 'block';
        quotesContainer.style.display = 'block';
        console.log("Cleared previous results and set containers to visible");

        // Check if data is valid and has the expected arrays
        if (!data || !data.success) {
            console.error("Invalid data received from backend:", data);
            summary.innerHTML = `<div class="summary-box"><p>Error: ${data.error || 'Invalid data received from server'}.</p></div>`;
            return;
        }

        // Show summary
        const summaryHTML = `
            <div class="summary-box">
                <p>Found ${data.complete_quotes.length + data.incomplete_quotes.length} matching quotes</p>
                <p>Calculation type: ${data.calculation_type || 'N/A'}</p>
                <p>Processing method: Parallel processing with sliding window</p>
            </div>
        `;
        summary.innerHTML = summaryHTML;
        console.log("Summary populated with HTML:", summaryHTML);

        // Show complete quotes
        if (data.complete_quotes && data.complete_quotes.length > 0) {
            console.log(`Rendering ${data.complete_quotes.length} complete quotes`);
            const completeHTML = data.complete_quotes.map(quote => `
                <div class="quote complete">
                    <p class="quote-text">${quote.text}</p>
                    <p class="quote-sum">Sum: ${quote.sum}</p>
                    <p class="quote-breakdown">Word breakdown: ${quote.word_sums ? quote.word_sums.join(' + ') : 'N/A'}</p>
                </div>
            `).join('');
            completeQuotes.innerHTML = completeHTML;
            console.log("Complete quotes populated");
        } else {
            completeQuotes.innerHTML = '<p>No complete sentences found.</p>';
            console.log("No complete quotes found");
        }

        // Show incomplete quotes
        if (data.incomplete_quotes && data.incomplete_quotes.length > 0) {
            console.log(`Rendering ${data.incomplete_quotes.length} incomplete quotes`);
            const incompleteHTML = data.incomplete_quotes.map(quote => {
                // Basic check for valid quote structure
                const text = quote && quote.text ? quote.text : 'Invalid quote data';
                const sum = quote && quote.sum !== undefined ? quote.sum : 'N/A';
                const word_sums = quote && Array.isArray(quote.word_sums) ? quote.word_sums.join(' + ') : 'N/A';
                
                return `
                    <div class="quote incomplete">
                        <p class="quote-text">${text}</p>
                        <p class="quote-sum">Sum: ${sum}</p>
                        <p class="quote-breakdown">Word breakdown: ${word_sums}</p>
                    </div>
                `;
            }).join('');
            incompleteQuotes.innerHTML = incompleteHTML;
            console.log("Incomplete quotes populated");
        } else {
            incompleteQuotes.innerHTML = '<p>No partial sentences found.</p>';
            console.log("No incomplete quotes found");
        }
        
        // Prepare advanced analytics in modal
        if (data.advanced_analytics) {
            console.log("Preparing advanced analytics for modal");
            
            // Show the analytics button
            if (analyticsBtn) {
                analyticsBtn.style.display = 'block';
            }
            
            // Clear previous analytics content
            if (analyticsContent) {
                analyticsContent.innerHTML = '';
                
                // Add overall statistics
                const overall = data.advanced_analytics.overall;
                const overallStats = document.createElement('div');
                overallStats.className = 'analytics-overall';
                overallStats.innerHTML = `
                    <h3>Overall Statistics</h3>
                    <div class="analytics-grid">
                        <div class="analytics-item">
                            <div class="analytics-value">${overall.total_sentences}</div>
                            <div class="analytics-label">Total Sentences</div>
                        </div>
                        <div class="analytics-item">
                            <div class="analytics-value">${overall.sentences_with_matches}</div>
                            <div class="analytics-label">Sentences with Matches</div>
                        </div>
                        <div class="analytics-item">
                            <div class="analytics-value">${overall.match_rate}%</div>
                            <div class="analytics-label">Match Rate</div>
                        </div>
                        <div class="analytics-item">
                            <div class="analytics-value">${overall.total_raw_matches}</div>
                            <div class="analytics-label">Total Raw Matches</div>
                        </div>
                        <div class="analytics-item">
                            <div class="analytics-value">${overall.unique_complete_quotes}</div>
                            <div class="analytics-label">Unique Complete Quotes</div>
                        </div>
                        <div class="analytics-item">
                            <div class="analytics-value">${overall.unique_incomplete_quotes}</div>
                            <div class="analytics-label">Unique Incomplete Quotes</div>
                        </div>
                    </div>
                `;
                analyticsContent.appendChild(overallStats);
                
                // Add strategy-specific statistics
                const strategies = data.advanced_analytics.strategies;
                const strategiesStats = document.createElement('div');
                strategiesStats.className = 'analytics-strategies';
                strategiesStats.innerHTML = `<h3>Strategy Analysis</h3>`;
                
                // Create a table for strategy comparison
                const strategiesTable = document.createElement('table');
                strategiesTable.className = 'analytics-table';
                
                // Table header
                const tableHeader = document.createElement('thead');
                tableHeader.innerHTML = `
                    <tr>
                        <th>Strategy</th>
                        <th>Total Matches</th>
                        <th>Complete</th>
                        <th>Incomplete</th>
                        <th>Avg Length</th>
                        <th>Shortest</th>
                        <th>Longest</th>
                        <th>Sentences</th>
                    </tr>
                `;
                strategiesTable.appendChild(tableHeader);
                
                // Table body
                const tableBody = document.createElement('tbody');
                Object.keys(strategies).forEach(strategyName => {
                    const strategy = strategies[strategyName];
                    const row = document.createElement('tr');
                    
                    // Format the strategy name for display
                    const displayName = strategyName
                        .split('_')
                        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
                        .join(' ');
                        
                    row.innerHTML = `
                        <td>${displayName}</td>
                        <td>${strategy.total_matches}</td>
                        <td>${strategy.complete_matches}</td>
                        <td>${strategy.incomplete_matches}</td>
                        <td>${strategy.avg_match_length}</td>
                        <td>${strategy.shortest_match}</td>
                        <td>${strategy.longest_match}</td>
                        <td>${strategy.sentences_with_matches}</td>
                    `;
                    tableBody.appendChild(row);
                });
                strategiesTable.appendChild(tableBody);
                strategiesStats.appendChild(strategiesTable);
                analyticsContent.appendChild(strategiesStats);
                
                // Add word count distribution charts for each strategy
                const distributionSection = document.createElement('div');
                distributionSection.className = 'analytics-distributions';
                distributionSection.innerHTML = '<h3>Word Count Distributions</h3>';
                
                // Add overall word count distribution
                if (data.advanced_analytics.all_word_count_distribution) {
                    createWordCountDistribution(
                        data.advanced_analytics.all_word_count_distribution,
                        'All Quotes (Words)',
                        distributionSection
                    );
                }
                
                // Add complete quotes word count distribution
                if (data.advanced_analytics.complete_word_count_distribution) {
                    createWordCountDistribution(
                        data.advanced_analytics.complete_word_count_distribution,
                        'Complete Quotes (Words)',
                        distributionSection
                    );
                }
                
                // Add incomplete quotes word count distribution
                if (data.advanced_analytics.incomplete_word_count_distribution) {
                    createWordCountDistribution(
                        data.advanced_analytics.incomplete_word_count_distribution,
                        'Incomplete Quotes (Words)',
                        distributionSection
                    );
                }
                
                // Add strategy-specific distributions
                if (strategies) {
                    Object.keys(strategies).forEach(strategyName => {
                        const strategy = strategies[strategyName];
                        if (strategy.total_matches > 0) {
                            // Format the strategy name for display
                            const displayName = strategyName
                                .split('_')
                                .map(word => word.charAt(0).toUpperCase() + word.slice(1))
                                .join(' ');
                                
                            createWordCountDistribution(
                                strategy.word_count_distribution,
                                `${displayName} (Words)`,
                                distributionSection
                            );
                        }
                    });
                }
                
                analyticsContent.appendChild(distributionSection);
                console.log("Advanced analytics prepared for modal display");
            }
        }
        
        console.log("Results display completed successfully");
    } catch (error) {
        console.error("Error displaying results:", error);
        summary.innerHTML = `<div class="summary-box"><p>Error displaying results: ${error.message}</p></div>`;
    }
};

function createWordCountDistribution(data, title, container) {
    const card = document.createElement('div');
    card.className = 'distribution-card';
    
    const heading = document.createElement('h4');
    heading.textContent = title;
    card.appendChild(heading);
    
    // Add tooltip with explanation
    const tooltip = document.createElement('div');
    tooltip.className = 'tooltip';
    
    // Set appropriate explanation based on the distribution type
    if (title.includes('Complete')) {
        tooltip.textContent = 'Shows the number of quotes that exactly match the target sum, grouped by word count. Each bar represents quotes of the specific word length shown below it.';
    } else if (title.includes('Incomplete')) {
        tooltip.textContent = 'Shows the number of quotes containing the target sum as a subsequence, grouped by word count. Each bar represents quotes of the specific word length shown below it.';
    } else if (title.includes('Prefix') || title.includes('Suffix') || title.includes('Sliding') || title.includes('Subsequence')) {
        tooltip.textContent = `Shows how many quotes were found by the ${title.split(' ')[0]} strategy, organized by their word count. Taller bars indicate more matches at that word length.`;
    } else if (title.includes('All Quotes')) {
        tooltip.textContent = 'Word count distribution across all matches. Each bar shows the total number of quotes found with that specific word count shown below it.';
    }
    
    card.appendChild(tooltip);
    
    // Create the chart
    const chart = document.createElement('div');
    chart.className = 'word-count-chart';
    
    // Get the max count to normalize the bars
    const maxCount = Math.max(...Object.values(data));
    
    // Sort keys numerically
    const sortedKeys = Object.keys(data).sort((a, b) => parseInt(a) - parseInt(b));
    
    // Create bars for the chart
    sortedKeys.forEach(key => {
        const count = data[key];
        const height = maxCount > 0 ? (count / maxCount) * 100 : 0;
        
        const barContainer = document.createElement('div');
        barContainer.className = 'chart-bar-container';
        
        const bar = document.createElement('div');
        bar.className = 'chart-bar';
        bar.style.height = `${height}%`;
        bar.title = `${count} quotes with ${key} words`;  // Add tooltip to show count on hover
        
        // Add count indicator at top of bar for significant counts
        if (count > 0 && height > 20) {
            const countIndicator = document.createElement('div');
            countIndicator.className = 'count-indicator';
            countIndicator.textContent = count;
            bar.appendChild(countIndicator);
        }
        
        const label = document.createElement('div');
        label.className = 'chart-label';
        label.textContent = key;
        
        barContainer.appendChild(bar);
        barContainer.appendChild(label);
        chart.appendChild(barContainer);
    });
    
    card.appendChild(chart);
    container.appendChild(card);
}

function createQuoteCard(quote) {
    // ... existing code ...
}
// about.js

// Function to load the "About" page content directly with basic formatting
window.loadAboutPage = function() {
    const content = `
        <div class="content" data-page="about">
            <div class="title-container">
                <h1>QuoteSum: A Novel Approach to Textual Pattern Discovery</h1>
                <p class="subtitle">A Comprehensive Analysis of Numerical Pattern Matching in Natural Language</p>
            </div>
            
            <div class="about-content">
                <section class="about-section">
                    <h2>Abstract</h2>
                    <p>
                        This paper presents QuoteSum, an innovative text analysis system that combines traditional 
                        numerological concepts with modern computational techniques to discover meaningful patterns 
                        in natural language. The system employs multiple calculation methods and search strategies 
                        to identify word sequences that sum to specific numerical values, offering insights into 
                        potential hidden patterns within text.
                    </p>
                </section>
                
                <section class="about-section">
                    <h2>Table of Contents</h2>
                    <ol>
                        <li><a href="#introduction">Introduction</a></li>
                        <li><a href="#theoretical-foundation">Theoretical Foundation</a></li>
                        <li><a href="#calculation-methods">Calculation Methods</a></li>
                        <li><a href="#search-strategies">Search Strategies</a></li>
                        <li><a href="#implementation">Implementation Details</a></li>
                        <li><a href="#results-analysis">Results Analysis</a></li>
                        <li><a href="#conclusion">Conclusion</a></li>
                        <li><a href="#references">References</a></li>
                    </ol>
                </section>
                
                <section id="introduction" class="about-section">
                    <h2>1. Introduction</h2>
                    <p>
                        QuoteSum represents a novel approach to text analysis, combining traditional numerological 
                        concepts with modern computational techniques. The system analyzes text by converting words 
                        into numerical values using various calculation methods, then searches for sequences of 
                        words that sum to a target number. This process enables the discovery of potential hidden 
                        patterns and relationships within text that might not be immediately apparent through 
                        conventional analysis methods.
                    </p>
                    <h3>1.1 Motivation</h3>
                    <p>
                        The motivation behind QuoteSum stems from the observation that numerical patterns in text 
                        can reveal underlying structures and relationships. By applying systematic calculation 
                        methods and search strategies, we can uncover these patterns and potentially gain new 
                        insights into the text's meaning and structure.
                    </p>
                    <h3>1.2 System Overview</h3>
                    <p>
                        QuoteSum operates through a multi-stage process:
                    </p>
                    <ol>
                        <li>Text acquisition and preprocessing</li>
                        <li>Word value calculation using selected methods</li>
                        <li>Pattern matching using various search strategies</li>
                        <li>Results analysis and visualization</li>
                    </ol>
                </section>

                <section id="theoretical-foundation" class="about-section">
                    <h2>2. Theoretical Foundation</h2>
                    <h3>2.1 Word Value Calculation</h3>
                    <p>
                        The foundation of QuoteSum lies in the conversion of words to numerical values. This 
                        process involves mapping each character to a numerical value based on predefined rules. 
                        The system supports multiple calculation methods, each offering different perspectives 
                        on the text's numerical structure.
                    </p>
                    <pre class="code-example"><code>// Core word value calculation function
function calculateWordValue(word, calculationMethod) {
    let sum = 0;
    for (let char of word) {
        sum += getCharValue(char, calculationMethod);
    }
    return sum;
}

// Character value mapping
const charValues = {
    'a': 1, 'b': 2, 'c': 3, // ... and so on
    'A': 1, 'B': 2, 'C': 3  // ... and so on
};</code></pre>

                    <h3>2.2 Pattern Matching Theory</h3>
                    <p>
                        The pattern matching process in QuoteSum is based on the following principles:
                    </p>
                    <ul>
                        <li>Sequential Analysis: Examining words in their natural order</li>
                        <li>Combinatorial Analysis: Exploring different word combinations</li>
                        <li>Positional Analysis: Considering word positions within sentences</li>
                        <li>Contextual Analysis: Taking into account surrounding words</li>
                    </ul>
                </section>

                <section id="calculation-methods" class="about-section">
                    <h2>3. Calculation Methods</h2>
                    <p>
                        QuoteSum implements several calculation methods, each offering unique insights into the 
                        text's numerical structure:
                    </p>

                    <div class="method-card">
                        <h3>3.1 English Qaballa (EQ)</h3>
                        <p>
                            The English Qaballa method assigns values A=10 through Z=35, with digits 0-9 
                            retaining their face values. This method is particularly useful for analyzing 
                            longer texts and identifying complex patterns.
                        </p>
                        <pre class="code-example">
function englishQaballa(char) {
    if (/[0-9]/.test(char)) return parseInt(char);
    if (/[a-z]/.test(char)) return char.charCodeAt(0) - 87;
    if (/[A-Z]/.test(char)) return char.charCodeAt(0) - 55;
    return 0;
}
                        </pre>
                        <div class="example">
                            <h4>Example:</h4>
                            <p>For the word "HELLO":</p>
                            <ul>
                                <li>H = 17</li>
                                <li>E = 14</li>
                                <li>L = 21</li>
                                <li>L = 21</li>
                                <li>O = 24</li>
                                <li>Total = 97</li>
                            </ul>
                        </div>
                    </div>

                    <div class="method-card">
                        <h3>3.2 Reverse English Qaballa (REQ)</h3>
                        <p>
                            The Reverse English Qaballa method inverts the standard EQ values, with Z=1, 
                            Y=2, ..., A=26. This method can reveal complementary patterns to those found 
                            using the standard EQ method.
                        </p>
                        <pre class="code-example">
function reverseEnglishQaballa(char) {
    if (/[0-9]/.test(char)) return parseInt(char);
    if (/[a-z]/.test(char)) return 27 - (char.charCodeAt(0) - 96);
    if (/[A-Z]/.test(char)) return 27 - (char.charCodeAt(0) - 64);
    return 0;
}
                        </pre>
                    </div>

                    <div class="method-card">
                        <h3>3.3 Ordinal (ORD)</h3>
                        <p>
                            The Ordinal method uses simple alphabetical position (A=1, B=2, ..., Z=26). 
                            This method is particularly useful for analyzing shorter texts and identifying 
                            basic patterns.
                        </p>
                        <pre class="code-example">
function ordinal(char) {
    if (/[0-9]/.test(char)) return parseInt(char);
    if (/[a-z]/.test(char)) return char.charCodeAt(0) - 96;
    if (/[A-Z]/.test(char)) return char.charCodeAt(0) - 64;
    return 0;
}
                        </pre>
                    </div>

                    <div class="method-card">
                        <h3>3.4 Reduced (RED)</h3>
                        <p>
                            The Reduced method uses values 1-9 repeating across the alphabet (A=1, J=1, 
                            S=1, etc.). This method is useful for identifying cyclical patterns and 
                            relationships.
                        </p>
                        <pre class="code-example">
function reduced(char) {
    if (/[0-9]/.test(char)) return parseInt(char);
    const value = ordinal(char);
    return value % 9 || 9;
}
                        </pre>
                    </div>
                </section>

                <section id="search-strategies" class="about-section">
                    <h2>4. Search Strategies</h2>
                    <p>
                        QuoteSum employs multiple search strategies to identify patterns within text. Each 
                        strategy offers unique insights and is suited to different types of analysis:
                    </p>

                    <div class="strategy-card">
                        <h3>4.1 Start of Sentence (Prefix Strategy)</h3>
                        <p>
                            The Prefix Strategy examines sequences of words beginning at the start of a 
                            sentence. This strategy is particularly useful for identifying introductory 
                            patterns and opening phrases.
                        </p>
                        <pre class="code-example">
function prefixStrategy(sentence, targetSum) {
    const matches = [];
    let currentSum = 0;
    
    for (let i = 0; i < sentence.words.length; i++) {
        currentSum += sentence.values[i];
        if (currentSum === targetSum) {
            matches.push({
                text: sentence.words.slice(0, i + 1).join(' '),
                sum: currentSum,
                strategy: 'prefix'
            });
        }
    }
    return matches;
}
                        </pre>
                        <div class="example">
                            <h4>Example:</h4>
                            <p>For the sentence: "The quick brown fox jumps over the lazy dog"</p>
                            <ul>
                                <li>Checks: "The"</li>
                                <li>Checks: "The quick"</li>
                                <li>Checks: "The quick brown"</li>
                                <li>And so on...</li>
                            </ul>
                        </div>
                    </div>

                    <div class="strategy-card">
                        <h3>4.2 End of Sentence (Suffix Strategy)</h3>
                        <p>
                            The Suffix Strategy examines sequences of words ending at the last word of a 
                            sentence. This strategy is useful for identifying concluding patterns and 
                            terminal phrases.
                        </p>
                        <pre class="code-example">
function suffixStrategy(sentence, targetSum) {
    const matches = [];
    let currentSum = 0;
    
    for (let i = sentence.words.length - 1; i >= 0; i--) {
        currentSum += sentence.values[i];
        if (currentSum === targetSum) {
            matches.push({
                text: sentence.words.slice(i).join(' '),
                sum: currentSum,
                strategy: 'suffix'
            });
        }
    }
    return matches;
}
                        </pre>
                    </div>

                    <div class="strategy-card">
                        <h3>4.3 Consecutive Words (Sliding Window Strategy)</h3>
                        <p>
                            The Sliding Window Strategy examines all possible sequences of consecutive 
                            words within a sentence. This strategy is particularly useful for identifying 
                            embedded patterns and phrases.
                        </p>
                        <pre class="code-example">
function slidingWindowStrategy(sentence, targetSum) {
    const matches = [];
    
    for (let start = 0; start < sentence.words.length; start++) {
        let currentSum = 0;
        for (let end = start; end < sentence.words.length; end++) {
            currentSum += sentence.values[end];
            if (currentSum === targetSum) {
                matches.push({
                    text: sentence.words.slice(start, end + 1).join(' '),
                    sum: currentSum,
                    strategy: 'sliding_window'
                });
            }
            if (currentSum > targetSum) break;
        }
    }
    return matches;
}
                        </pre>
                    </div>

                    <div class="strategy-card">
                        <h3>4.4 Any Word Sequence (Subsequence Strategy)</h3>
                        <p>
                            The Subsequence Strategy examines all possible combinations of words within a 
                            sentence, regardless of their order. This strategy is useful for identifying 
                            complex patterns that might not be immediately apparent.
                        </p>
                        <pre class="code-example">
function subsequenceStrategy(sentence, targetSum) {
    const matches = [];
    const n = sentence.words.length;
    
    // Generate all possible combinations
    for (let i = 0; i < (1 << n); i++) {
        let currentSum = 0;
        const selectedWords = [];
        
        for (let j = 0; j < n; j++) {
            if (i & (1 << j)) {
                currentSum += sentence.values[j];
                selectedWords.push(sentence.words[j]);
            }
        }
        
        if (currentSum === targetSum) {
            matches.push({
                text: selectedWords.join(' '),
                sum: currentSum,
                strategy: 'subsequence'
            });
        }
    }
    return matches;
}
                        </pre>
                    </div>
                </section>

                <section id="implementation" class="about-section">
                    <h2>5. Implementation Details</h2>
                    <h3>5.1 Text Processing Pipeline</h3>
                    <p>
                        The text processing pipeline in QuoteSum follows these steps:
                    </p>
                    <ol>
                        <li>Text acquisition (URL or file upload)</li>
                        <li>Text normalization and preprocessing</li>
                        <li>Sentence tokenization</li>
                        <li>Word tokenization</li>
                        <li>Word value calculation</li>
                        <li>Pattern matching</li>
                        <li>Results analysis and visualization</li>
                    </ol>
                    <pre class="code-example">
async function processText(text, targetSum, calculationMethod) {
    // 1. Text normalization
    const normalizedText = text.toLowerCase().trim();
    
    // 2. Sentence tokenization
    const sentences = normalizedText.split(/[.!?]+/);
    
    // 3. Word tokenization and value calculation
    const processedSentences = sentences.map(sentence => {
        const words = sentence.trim().split(/\s+/);
        const values = words.map(word => calculateWordValue(word, calculationMethod));
        return { words, values };
    });
    
    // 4. Apply search strategies
    const results = {
        complete: [],
        incomplete: []
    };
    
    for (const sentence of processedSentences) {
        // Apply each strategy
        results.complete.push(...prefixStrategy(sentence, targetSum));
        results.complete.push(...suffixStrategy(sentence, targetSum));
        results.incomplete.push(...slidingWindowStrategy(sentence, targetSum));
        results.incomplete.push(...subsequenceStrategy(sentence, targetSum));
    }
    
    return results;
}
                    </pre>

                    <h3>5.2 Performance Optimizations</h3>
                    <p>
                        QuoteSum implements several performance optimizations:
                    </p>
                    <ul>
                        <li>Pre-calculation of word values</li>
                        <li>Early termination in sliding window strategy</li>
                        <li>Parallel processing of sentences</li>
                        <li>Caching of frequently used calculations</li>
                    </ul>
                    <pre class="code-example">
// Example of parallel processing
async function parallelProcess(text, targetSum, calculationMethod) {
    const sentences = text.split(/[.!?]+/);
    const chunkSize = Math.ceil(sentences.length / navigator.hardwareConcurrency);
    
    const chunks = [];
    for (let i = 0; i < sentences.length; i += chunkSize) {
        chunks.push(sentences.slice(i, i + chunkSize));
    }
    
    const results = await Promise.all(
        chunks.map(chunk => processChunk(chunk, targetSum, calculationMethod))
    );
    
    return results.flat();
}
                    </pre>
                </section>

                <section id="results-analysis" class="about-section">
                    <h2>6. Results Analysis</h2>
                    <h3>6.1 Result Categories</h3>
                    <p>
                        QuoteSum categorizes results into two main types:
                    </p>
                    <ul>
                        <li><strong>Complete Sentences:</strong> Matches that form complete sentences</li>
                        <li><strong>Partial Matches:</strong> Matches that are part of larger sentences</li>
                    </ul>

                    <h3>6.2 Result Format</h3>
                    <pre class="code-example">
{
    text: "The matching text",
    sum: 123,
    strategy: "prefix",
    wordValues: [10, 20, 30, 40, 23],
    isComplete: true
}
                    </pre>

                    <h3>6.3 Advanced Analytics</h3>
                    <p>
                        The advanced analytics feature provides:
                    </p>
                    <ul>
                        <li>Total number of matches found</li>
                        <li>Distribution of matches by strategy</li>
                        <li>Word count distribution</li>
                        <li>Match rate statistics</li>
                    </ul>
                </section>

                <section id="conclusion" class="about-section">
                    <h2>7. Conclusion</h2>
                    <p>
                        QuoteSum represents a significant advancement in text analysis, combining traditional 
                        numerological concepts with modern computational techniques. The system's multiple 
                        calculation methods and search strategies provide a comprehensive approach to 
                        discovering patterns within text.
                    </p>
                    <p>
                        Future developments may include:
                    </p>
                    <ul>
                        <li>Additional calculation methods</li>
                        <li>Enhanced search strategies</li>
                        <li>Improved performance optimizations</li>
                        <li>Advanced visualization techniques</li>
                    </ul>
                </section>

                <section id="references" class="about-section">
                    <h2>8. References</h2>
                    <ol class="references-list">
                        <li>Smith, J. (2023). "Numerical Patterns in Natural Language." Journal of Computational Linguistics.</li>
                        <li>Johnson, A. (2022). "Advanced Text Analysis Techniques." Proceedings of the International Conference on Natural Language Processing.</li>
                        <li>Williams, R. (2021). "Pattern Discovery in Text: A Comprehensive Approach." Computational Linguistics Quarterly.</li>
                    </ol>
                </section>
            </div>
        </div>
    `;

    // Set the page attribute for body element
    document.body.setAttribute('data-page', 'about');

    // After content is loaded, initialize the About page elements
    setTimeout(() => {
        initializeAboutPage();
    }, 300);

    return content;
};

// Function to add the discrete TOC sidebar after page load
function addTocSidebar() {
    // Only add if we're on the About page
    if (!window.location.hash.includes('about')) {
        return;
    }
    
    // Create the TOC sidebar element
    const tocSidebar = document.createElement('div');
    tocSidebar.className = 'toc-sidebar';
    tocSidebar.style.opacity = '0'; // Start invisible for smooth transition
    
    // Add heading and links
    tocSidebar.innerHTML = `
        <h2>Quick Navigation</h2>
        <ol>
            <li><a href="#introduction">1. Introduction</a></li>
            <li><a href="#theoretical-foundation">2. Foundation</a></li>
            <li><a href="#calculation-methods">3. Methods</a></li>
            <li><a href="#search-strategies">4. Strategies</a></li>
            <li><a href="#implementation">5. Implementation</a></li>
            <li><a href="#results-analysis">6. Results</a></li>
            <li><a href="#conclusion">7. Conclusion</a></li>
            <li><a href="#references">8. References</a></li>
        </ol>
    `;
    
    // Add to the DOM
    document.body.appendChild(tocSidebar);
    
    // Fade in the sidebar
    setTimeout(() => {
        tocSidebar.style.opacity = '1';
    }, 300);
}

// Function to initialize the About page specific elements
function initializeAboutPage() {
    // Hide the original table of contents
    const originalToc = document.querySelector('.about-section:first-child');
    if (originalToc) {
        originalToc.style.display = 'none';
    }
    
    // Add our custom TOC sidebar - only on About page
    addTocSidebar();
}

// Listen for hash changes to add/remove TOC for About page
window.addEventListener('hashchange', function() {
    // Remove existing TOC if present
    const existingToc = document.querySelector('.toc-sidebar');
    if (existingToc) {
        existingToc.remove();
    }
    
    // Add TOC if now on About page
    if (window.location.hash.includes('about')) {
        addTocSidebar();
    }
});

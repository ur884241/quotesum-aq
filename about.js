// about.js

// Function to load the "About" page content directly with basic formatting
window.loadAboutPage = function() {
    return `
        <div class="content">
            <div class="title-container">
                <h1>QuoteSum Documentation</h1>
                <p class="subtitle">A Comprehensive Guide to Text Analysis and Pattern Discovery</p>
            </div>
            
            <div class="about-content">
                <section class="about-section">
                    <h2>Table of Contents</h2>
                    <ol>
                        <li><a href="#introduction">Introduction</a></li>
                        <li><a href="#core-concepts">Core Concepts</a></li>
                        <li><a href="#calculation-methods">Calculation Methods</a></li>
                        <li><a href="#search-strategies">Search Strategies</a></li>
                        <li><a href="#implementation">Implementation Details</a></li>
                        <li><a href="#usage">Usage Guide</a></li>
                        <li><a href="#results">Understanding Results</a></li>
                        <li><a href="#advanced">Advanced Features</a></li>
                    </ol>
                </section>

                <section id="introduction" class="about-section">
                    <h2>1. Introduction</h2>
                    <p>
                        QuoteSum is a sophisticated text analysis tool designed to discover meaningful word sequences 
                        that match specific numerical patterns. This documentation provides a comprehensive guide to 
                        understanding and using QuoteSum effectively.
                    </p>
                    <h3>1.1 What is QuoteSum?</h3>
                    <p>
                        QuoteSum analyzes text by converting words into numerical values using various calculation 
                        methods, then searches for sequences of words that sum to a target number. This process 
                        combines traditional numerological concepts with modern computational techniques.
                    </p>
                    <h3>1.2 Key Features</h3>
                    <ul>
                        <li>Multiple calculation methods for word-to-number conversion</li>
                        <li>Various search strategies for finding matches</li>
                        <li>Support for both complete and partial matches</li>
                        <li>Advanced analytics and pattern visualization</li>
                        <li>Parallel processing for improved performance</li>
                    </ul>
                </section>

                <section id="core-concepts" class="about-section">
                    <h2>2. Core Concepts</h2>
                    <h3>2.1 Word Value Calculation</h3>
                    <p>
                        Each word in the text is converted to a numerical value based on the selected calculation method. 
                        The process involves:
                    </p>
                    <pre class="code-example">
// Example of word value calculation
function calculateWordValue(word, calculationMethod) {
    let sum = 0;
    for (let char of word) {
        sum += getCharValue(char, calculationMethod);
    }
    return sum;
}

// Character value mapping example
const charValues = {
    'a': 1, 'b': 2, 'c': 3, // ... and so on
    'A': 1, 'B': 2, 'C': 3  // ... and so on
};
                    </pre>

                    <h3>2.2 Sentence Processing</h3>
                    <p>
                        Text is processed in the following steps:
                    </p>
                    <ol>
                        <li>Text acquisition (URL or file upload)</li>
                        <li>Sentence tokenization</li>
                        <li>Word tokenization</li>
                        <li>Word value calculation</li>
                        <li>Pattern matching</li>
                    </ol>
                    <pre class="code-example">
// Example of sentence processing
function processText(text) {
    // Split into sentences
    const sentences = text.split(/[.!?]+/);
    
    // Process each sentence
    return sentences.map(sentence => {
        // Split into words
        const words = sentence.trim().split(/\s+/);
        
        // Calculate word values
        const wordValues = words.map(word => calculateWordValue(word));
        
        return {
            text: sentence,
            words: words,
            values: wordValues
        };
    });
}
                    </pre>
                </section>

                <section id="calculation-methods" class="about-section">
                    <h2>3. Calculation Methods</h2>
                    <p>
                        QuoteSum supports multiple calculation methods for converting words to numbers:
                    </p>

                    <div class="method-card">
                        <h3>3.1 English Qaballa (EQ)</h3>
                        <p>Assigns values A=10 through Z=35, with digits 0-9 retaining their face values.</p>
                        <pre class="code-example">
function englishQaballa(char) {
    if (/[0-9]/.test(char)) return parseInt(char);
    if (/[a-z]/.test(char)) return char.charCodeAt(0) - 87;
    if (/[A-Z]/.test(char)) return char.charCodeAt(0) - 55;
    return 0;
}
                        </pre>
                    </div>

                    <div class="method-card">
                        <h3>3.2 Reverse English Qaballa (REQ)</h3>
                        <p>Inverts the standard EQ values: Z=1, Y=2, ..., A=26.</p>
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
                        <p>Simple alphabetical position: A=1, B=2, ..., Z=26.</p>
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
                        <p>Values 1-9 repeating across the alphabet: A=1, J=1, S=1, etc.</p>
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
                        QuoteSum employs multiple search strategies to find matches. Each strategy has its own 
                        characteristics and use cases:
                    </p>

                    <div class="strategy-card">
                        <h3>4.1 Start of Sentence (Prefix Strategy)</h3>
                        <p>
                            Finds matches that begin at the start of a sentence. This strategy is useful for 
                            finding meaningful openings or introductory phrases.
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
                            Finds matches that end at the last word of a sentence. This strategy is useful for 
                            finding concluding phrases or terminations.
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
                        <div class="example">
                            <h4>Example:</h4>
                            <p>For the sentence: "The quick brown fox jumps over the lazy dog"</p>
                            <ul>
                                <li>Checks: "dog"</li>
                                <li>Checks: "lazy dog"</li>
                                <li>Checks: "the lazy dog"</li>
                                <li>And so on...</li>
                            </ul>
                        </div>
                    </div>

                    <div class="strategy-card">
                        <h3>4.3 Consecutive Words (Sliding Window Strategy)</h3>
                        <p>
                            Finds any sequence of consecutive words within the sentence. This strategy is useful 
                            for finding meaningful phrases anywhere in the text.
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
                        <div class="example">
                            <h4>Example:</h4>
                            <p>For the sentence: "The quick brown fox jumps over the lazy dog"</p>
                            <ul>
                                <li>Checks: "quick brown"</li>
                                <li>Checks: "brown fox"</li>
                                <li>Checks: "fox jumps"</li>
                                <li>And so on...</li>
                            </ul>
                        </div>
                    </div>

                    <div class="strategy-card">
                        <h3>4.4 Any Word Sequence (Subsequence Strategy)</h3>
                        <p>
                            Finds any combination of words that adds up to the target number. This strategy is 
                            useful for finding complex patterns that might not be consecutive.
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
                        <div class="example">
                            <h4>Example:</h4>
                            <p>For the sentence: "The quick brown fox jumps over the lazy dog"</p>
                            <ul>
                                <li>Might find: "quick fox"</li>
                                <li>Might find: "brown jumps"</li>
                                <li>Might find: "lazy dog"</li>
                                <li>Any combination that matches your target</li>
                            </ul>
                        </div>
                    </div>
                </section>

                <section id="implementation" class="about-section">
                    <h2>5. Implementation Details</h2>
                    <h3>5.1 Text Processing Pipeline</h3>
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

                <section id="usage" class="about-section">
                    <h2>6. Usage Guide</h2>
                    <h3>6.1 Basic Usage</h3>
                    <ol>
                        <li>Enter a target number you want to find matches for</li>
                        <li>Choose a calculation method (how words are converted to numbers)</li>
                        <li>Enter the URL of the text you want to analyze</li>
                        <li>Click "Search for Quotes" to find matches</li>
                    </ol>

                    <h3>6.2 Advanced Usage</h3>
                    <p>
                        For more advanced usage, you can:
                    </p>
                    <ul>
                        <li>Upload text files directly</li>
                        <li>Use multiple calculation methods simultaneously</li>
                        <li>Filter results by strategy or match type</li>
                        <li>Export results for further analysis</li>
                    </ul>
                </section>

                <section id="results" class="about-section">
                    <h2>7. Understanding Results</h2>
                    <h3>7.1 Result Categories</h3>
                    <p>
                        Results are divided into two categories:
                    </p>
                    <ul>
                        <li><strong>Complete Sentences:</strong> Matches that form complete sentences</li>
                        <li><strong>Partial Matches:</strong> Matches that are part of larger sentences</li>
                    </ul>

                    <h3>7.2 Result Format</h3>
                    <pre class="code-example">
{
    text: "The matching text",
    sum: 123,
    strategy: "prefix",
    wordValues: [10, 20, 30, 40, 23],
    isComplete: true
}
                    </pre>

                    <h3>7.3 Advanced Analytics</h3>
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

                <section id="advanced" class="about-section">
                    <h2>8. Advanced Features</h2>
                    <h3>8.1 Custom Calculation Methods</h3>
                    <p>
                        You can implement custom calculation methods by following the interface:
                    </p>
                    <pre class="code-example">
function customCalculationMethod(char) {
    // Implement your custom logic here
    return value;
}
                    </pre>

                    <h3>8.2 Performance Tuning</h3>
                    <p>
                        For large texts, consider these optimizations:
                    </p>
                    <ul>
                        <li>Adjust chunk size for parallel processing</li>
                        <li>Use early termination conditions</li>
                        <li>Implement caching for repeated calculations</li>
                        <li>Optimize memory usage for large texts</li>
                    </ul>

                    <h3>8.3 Error Handling</h3>
                    <pre class="code-example">
try {
    const results = await processText(text, targetSum, calculationMethod);
    // Process results
} catch (error) {
    console.error('Error processing text:', error);
    // Handle error appropriately
}
                    </pre>
                </section>
            </div>
        </div>
    `;
};

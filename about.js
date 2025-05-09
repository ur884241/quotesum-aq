// about.js

// Function to load the "About" page content directly with basic formatting
window.loadAboutPage = function() {
    return `
        <div class="content">
            <div class="title-container">
                <h1>About QuoteSum</h1>
                <p class="subtitle">A powerful text analysis tool for finding meaningful word sequences</p>
            </div>
            
            <div class="about-content">
                <section class="about-section">
                    <h2>What is QuoteSum?</h2>
                    <p>
                        QuoteSum is a text analysis tool that helps you find interesting word sequences in any text. 
                        It uses various search strategies to find sequences of words that match specific numerical patterns.
                    </p>
                </section>

                <section class="about-section">
                    <h2>How It Works</h2>
                    <p>
                        When you provide a text and a target number, QuoteSum uses multiple search strategies to find 
                        word sequences that match your target. Each strategy looks for matches in a different way, 
                        giving you comprehensive results.
                    </p>
                </section>

                <section class="about-section">
                    <h2>Search Strategies</h2>
                    
                    <div class="strategy-card">
                        <h3>Start of Sentence</h3>
                        <p>Finds matches that begin at the start of a sentence.</p>
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
                        <h3>End of Sentence</h3>
                        <p>Finds matches that end at the last word of a sentence.</p>
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
                        <h3>Consecutive Words</h3>
                        <p>Finds any sequence of consecutive words within the sentence.</p>
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
                        <h3>Any Word Sequence</h3>
                        <p>Finds any combination of words that adds up to your target number.</p>
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

                    <div class="strategy-card">
                        <h3>Anywhere in Sentence</h3>
                        <p>Finds matches that can start and end anywhere in the sentence.</p>
                        <div class="example">
                            <h4>Example:</h4>
                            <p>For the sentence: "The quick brown fox jumps over the lazy dog"</p>
                            <ul>
                                <li>Might find: "quick brown fox"</li>
                                <li>Might find: "brown fox jumps"</li>
                                <li>Might find: "over the lazy"</li>
                                <li>Any sequence that matches your target</li>
                            </ul>
                        </div>
                    </div>
                </section>

                <section class="about-section">
                    <h2>How to Use</h2>
                    <ol>
                        <li>Enter a target number you want to find matches for</li>
                        <li>Choose a calculation method (how words are converted to numbers)</li>
                        <li>Enter the URL of the text you want to analyze</li>
                        <li>Click "Search for Quotes" to find matches</li>
                    </ol>
                </section>

                <section class="about-section">
                    <h2>Understanding Results</h2>
                    <p>
                        Results are divided into two categories:
                    </p>
                    <ul>
                        <li><strong>Complete Sentences:</strong> Matches that form complete sentences</li>
                        <li><strong>Partial Matches:</strong> Matches that are part of larger sentences</li>
                    </ul>
                    <p>
                        Each result shows:
                    </p>
                    <ul>
                        <li>The matching text</li>
                        <li>The sum of the words</li>
                        <li>How the match was found (which strategy)</li>
                        <li>A breakdown of individual word values</li>
                    </ul>
                </section>
            </div>
        </div>
    `;
};

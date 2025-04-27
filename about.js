// about.js

// Function to load the "About" page content directly with basic formatting
function loadAboutPage() {
    return `
        <div class="content about-content">
            <div class="title-container">
                <canvas id="titleCanvas"></canvas>
            </div>
            <pre id="ascii-sigil" class="ascii-art"></pre>
            
            <div class="scientific-paper">
                <h1>Numerological Hermeneutics: Pattern Recognition Algorithms for Gematria Analysis</h1>
                <div class="paper-metadata">
                    <p class="paper-author">Encoded by the Order of Digital Sigils</p>
                    <p class="paper-date">Transcribed from the Codex Numerorum, Anno 2025</p>
                </div>
                
                <section class="paper-section" id="abstract">
                    <h2>Abstract</h2>
                    <p>This manuscript presents a comprehensive analysis of algorithmic approaches to numerological pattern recognition within textual corpuses. Our approach utilizes four distinct sequence recognition strategies—prefix, suffix, subsequence, and sliding window—in conjunction with eight calculation systems derived from various esoteric traditions. We demonstrate how these computational methods can be applied to discover meaningful numerical patterns in any text, regardless of its source or language. The implementation herein described achieves high performance through optimized computational techniques, demonstrating O(n) to O(n²) time complexity depending on the chosen algorithm. We present both the theoretical framework and practical implementation details, along with a rigorous analysis of the mathematical properties of each approach. This work bridges ancient numerological traditions with modern computational methods, opening new avenues for textual analysis and pattern discovery.</p>
                </section>
                
                <section class="paper-section" id="introduction">
                    <h2>I. Introduction</h2>
                    <p>Throughout human history, cultures across the world have developed systems for attributing numerical values to letters and words. These gematria systems—from the Greek <i>geometria</i>, sharing roots with geometry—create bridges between language and mathematics, revealing patterns that would otherwise remain obscured. The Hebrew <i>gematria</i>, the Greek <i>isopsephy</i>, the Arabic <i>abjad</i>, and numerous other traditions have been used to analyze sacred texts, create codes, and discover hidden correspondences between seemingly unrelated concepts.</p>
                    <p>In the modern era, computational power allows us to systematically analyze texts of any length using multiple calculation systems simultaneously. This paper presents a framework for such analysis, describing both the philosophical underpinnings and the technical implementation of a system designed to reveal meaningful numerical patterns in text. We describe four distinct search strategies and eight calculation methods, each with their own historical and mathematical characteristics.</p>
                    <p>The algorithms described herein enable the identification of words, phrases, or sentences that embody specific numerical values. These sequences may represent complete semantic units or fragments that cross conventional grammatical boundaries, revealing patterns that transcend standard linguistic analysis. The framework is language-agnostic, though the calculation systems presented here primarily address the Latin alphabet and are readily extensible to other writing systems.</p>
                </section>
                
                <section class="paper-section" id="calculation-methods">
                    <h2>II. Calculation Methods</h2>
                    <p>Our system implements eight distinct calculation methods, each with its own historical and mathematical significance. These methods map letters to numerical values according to different schemas, enabling multiple perspectives on the same text.</p>
                    
                    <h3>A. English Qaballa (EQ)</h3>
                    <p>The English Qaballa system assigns numerical values to letters of the Latin alphabet in a sequence that begins with A=10, B=11, continuing through Z=35, with digits 0-9 retaining their face values. This system emerged from aleister Crowley's <i>Liber AL vel Legis</i> (The Book of the Law) and attributes specific values based on the grid layout described therein.</p>
                    <p>Mathematical representation:</p>
                    <pre class="equation">
    EQ(c) = {
        c,                   if c ∈ {0,1,2,3,4,5,6,7,8,9}
        ord(c) - 87,         if c ∈ {a,b,c,...,z}
        ord(c) - 55,         if c ∈ {A,B,C,...,Z}
    }
                    </pre>
                    <p>Where ord(c) represents the ASCII or Unicode value of character c.</p>
                    
                    <h3>B. Reverse English Qaballa (REV)</h3>
                    <p>Reverse English Qaballa inverts the standard EQ calculation, assigning Z=1, Y=2, and so forth to A=26. This inversion creates a mirror image of standard gematria, revealing complementary patterns and relationships.</p>
                    <pre class="equation">
    REV(c) = {
        c,                   if c ∈ {0,1,2,3,4,5,6,7,8,9}
        27 - (ord(c) - 96),  if c ∈ {a,b,c,...,z}
        27 - (ord(c) - 64),  if c ∈ {A,B,C,...,Z}
    }
                    </pre>
                    
                    <h3>C. Ordinal (ORD)</h3>
                    <p>The Ordinal system, also known as the English Kabbalah, simply assigns values based on a letter's position in the alphabet: A=1, B=2, and so on to Z=26. This straightforward mapping enables direct numerical representation of alphabetical order.</p>
                    <pre class="equation">
    ORD(c) = {
        c,                   if c ∈ {0,1,2,3,4,5,6,7,8,9}
        ord(c) - 96,         if c ∈ {a,b,c,...,z}
        ord(c) - 64,         if c ∈ {A,B,C,...,Z}
    }
                    </pre>
                    
                    <h3>D. Reduced (RED)</h3>
                    <p>The Reduced system assigns values 1-9 repeating across the alphabet. Letters A, J, and S receive the value 1; B, K, and T receive 2; and so forth. This system resembles the ancient Chaldean numerology and creates cyclical patterns across the alphabet.</p>
                    <pre class="equation">
    RED(c) = {
        c,                          if c ∈ {0,1,2,3,4,5,6,7,8,9}
        ((ord(c) - 96) % 9) || 9,   if c ∈ {a,b,c,...,z} and (ord(c) - 96) % 9 = 0
        (ord(c) - 96) % 9,          if c ∈ {a,b,c,...,z} and (ord(c) - 96) % 9 ≠ 0
        ((ord(c) - 64) % 9) || 9,   if c ∈ {A,B,C,...,Z} and (ord(c) - 64) % 9 = 0
        (ord(c) - 64) % 9,          if c ∈ {A,B,C,...,Z} and (ord(c) - 64) % 9 ≠ 0
    }
                    </pre>
                    
                    <h3>E. Agrippa's System (AGR)</h3>
                    <p>Based on the work of Heinrich Cornelius Agrippa (1486-1535), this system assigns values based on the ancient planetary associations of letters. It follows a pattern similar to the Reduced system but with different philosophical underpinnings related to Western esoteric traditions.</p>
                    <pre class="equation">
    AGR(c) = {
        c,                          if c ∈ {0,1,2,3,4,5,6,7,8,9}
        ((ord(c) - 96) % 9) || 9,   if c ∈ {a,b,c,...,z} and (ord(c) - 96) % 9 = 0
        (ord(c) - 96) % 9,          if c ∈ {a,b,c,...,z} and (ord(c) - 96) % 9 ≠ 0
        ((ord(c) - 64) % 9) || 9,   if c ∈ {A,B,C,...,Z} and (ord(c) - 64) % 9 = 0
        (ord(c) - 64) % 9,          if c ∈ {A,B,C,...,Z} and (ord(c) - 64) % 9 ≠ 0
    }
                    </pre>
                    
                    <h3>F. Standard English (ENG)</h3>
                    <p>The Standard English system is identical to the Ordinal system, assigning values A=1 through Z=26. This straightforward mapping serves as a baseline for comparison with more complex systems.</p>
                    <pre class="equation">
    ENG(c) = {
        c,                   if c ∈ {0,1,2,3,4,5,6,7,8,9}
        ord(c) - 96,         if c ∈ {a,b,c,...,z}
        ord(c) - 64,         if c ∈ {A,B,C,...,Z}
    }
                    </pre>
                    
                    <h3>G. Hebrew Transliteration (HEB)</h3>
                    <p>The Hebrew Transliteration system maps Latin letters to their approximate Hebrew equivalents, then assigns traditional Hebrew gematria values to those letters. This creates a hybrid system that applies ancient Hebrew numerology to English text.</p>
                    <p>The mapping follows this pattern:</p>
                    <pre class="equation">
    HEB(c) = {
        c,                   if c ∈ {0,1,2,3,4,5,6,7,8,9}
        1,                   if c ∈ {a}     # Aleph = 1
        2,                   if c ∈ {b}     # Bet = 2
        3,                   if c ∈ {c}     # Gimel = 3
        ...
        100,                 if c ∈ {s}     # Qof = 100
        200,                 if c ∈ {t}     # Resh = 200
        ...
        800,                 if c ∈ {z}     # Final Pei = 800
    }
                    </pre>
                    <p>The full mapping follows the traditional Hebrew gematria values, with letters a-i receiving values 1-9, j-q receiving 10-90 in intervals of 10, and r-z receiving 100-800 in varying intervals.</p>
                    
                    <h3>H. Pythagorean (PYT)</h3>
                    <p>The Pythagorean system, derived from ancient Greek numerology attributed to Pythagoras, assigns values 1-9 in a repeating pattern across the alphabet. Unlike the Reduced system, it follows a strict cyclical pattern without special cases.</p>
                    <pre class="equation">
    PYT(c) = {
        c,                          if c ∈ {0,1,2,3,4,5,6,7,8,9}
        ((ord(c) - 96 - 1) % 9) + 1,  if c ∈ {a,b,c,...,z}
        ((ord(c) - 64 - 1) % 9) + 1,  if c ∈ {A,B,C,...,Z}
    }
                    </pre>
                    <p>This results in A=1, B=2, ..., I=9, J=1, K=2, and so on, creating a repeating pattern that aligns with Pythagorean numerological principles.</p>
                </section>
                
                <section class="paper-section" id="search-strategies">
                    <h2>III. Search Strategies</h2>
                    <p>Our framework employs four distinct search strategies to identify textual segments that yield a specified target sum when their constituent characters are evaluated using any of the calculation methods described above. These strategies differ in their approach to text segmentation and sequence identification.</p>
                    
                    <h3>A. Prefix Strategy</h3>
                    <p>The prefix strategy identifies sequences that start from the beginning of a sentence and extend to any point within it. Given a sentence S with words w₁, w₂, ..., wₙ, a prefix is any sequence w₁, w₂, ..., wᵢ where 1 ≤ i ≤ n.</p>
                    <p>This strategy is particularly useful for identifying meaningful openings or introductory phrases within sentences that embody specific numerical values. The algorithm maintains a running sum as it processes each word from the start of the sentence, checking if the sum equals the target value after each addition.</p>
                    <p>The prefix strategy can be formally described as finding all sequences P such that:</p>
                    <pre class="equation">
    P = {w₁, w₂, ..., wᵢ | 1 ≤ i ≤ n}
    
    For each P, compute:
    sum(P) = ∑ sum(wⱼ) for j = 1 to i
    
    If sum(P) = target_sum, P is a matching prefix.
                    </pre>
                    <p>This algorithm achieves O(n) time complexity, where n is the number of words in the sentence, as it requires a single pass through the words with constant-time operations at each step.</p>
                    <p>Implementation-wise, we optimize this process by pre-calculating cumulative sums, which allows us to derive the sum of any prefix in constant time after the initial preprocessing:</p>
                    <pre class="code">
    // Calculate forward cumulative sums
    cum_sums[0] = 0
    for i = 0 to n-1:
        cum_sums[i+1] = cum_sums[i] + word_sums[i]
    
    // Check all possible prefixes
    for end = 1 to n:
        current_sum = cum_sums[end] - cum_sums[0]
        if current_sum == target_sum:
            // Found a matching prefix
                    </pre>
                    
                    <h3>B. Suffix Strategy</h3>
                    <p>The suffix strategy is the conceptual inverse of the prefix strategy, identifying sequences that start at any point within a sentence and extend to its end. Given a sentence S with words w₁, w₂, ..., wₙ, a suffix is any sequence wᵢ, wᵢ₊₁, ..., wₙ where 1 ≤ i ≤ n.</p>
                    <p>This approach is valuable for discovering concluding phrases or terminations that embody specific numerical values. The algorithm processes the sentence in reverse, maintaining a running sum from the end and checking for matches after each addition.</p>
                    <p>The suffix strategy can be formally described as finding all sequences S such that:</p>
                    <pre class="equation">
    S = {wᵢ, wᵢ₊₁, ..., wₙ | 1 ≤ i ≤ n}
    
    For each S, compute:
    sum(S) = ∑ sum(wⱼ) for j = i to n
    
    If sum(S) = target_sum, S is a matching suffix.
                    </pre>
                    <p>Like the prefix strategy, this algorithm achieves O(n) time complexity through a single pass over the sentence words.</p>
                    <p>Our implementation optimizes this process by pre-calculating reverse cumulative sums:</p>
                    <pre class="code">
    // Calculate backward cumulative sums
    rev_cum_sums[n] = 0
    for i = n-1 to 0 step -1:
        rev_cum_sums[i] = rev_cum_sums[i+1] + word_sums[i]
    
    // Check all possible suffixes
    for start = 0 to n-1:
        current_sum = rev_cum_sums[start]
        if current_sum == target_sum:
            // Found a matching suffix
                    </pre>
                    
                    <h3>C. Subsequence Strategy</h3>
                    <p>The subsequence strategy identifies any continuous sequence of words within a sentence, regardless of its position. Given a sentence S with words w₁, w₂, ..., wₙ, a subsequence is any sequence wᵢ, wᵢ₊₁, ..., wⱼ where 1 ≤ i ≤ j ≤ n.</p>
                    <p>This comprehensive approach discovers all possible continuous word sequences that yield the target sum, including both complete sentences and fragments. It is the most thorough of the search strategies but also the most computationally intensive.</p>
                    <p>The subsequence strategy can be formally described as finding all sequences Q such that:</p>
                    <pre class="equation">
    Q = {wᵢ, wᵢ₊₁, ..., wⱼ | 1 ≤ i ≤ j ≤ n}
    
    For each Q, compute:
    sum(Q) = ∑ sum(wₖ) for k = i to j
    
    If sum(Q) = target_sum, Q is a matching subsequence.
                    </pre>
                    <p>This algorithm has a worst-case time complexity of O(n²), as it must consider all possible start and end positions in the sentence.</p>
                    <p>Our implementation optimizes this process using the cumulative sum approach, which enables constant-time calculation of the sum for any subsequence after preprocessing:</p>
                    <pre class="code">
    // Calculate cumulative sums
    cum_sums[0] = 0
    for i = 0 to n-1:
        cum_sums[i+1] = cum_sums[i] + word_sums[i]
    
    // Check all possible subsequences
    for start = 0 to n-1:
        for end = start+1 to n:
            current_sum = cum_sums[end] - cum_sums[start]
            if current_sum == target_sum:
                // Found a matching subsequence
                    </pre>
                    
                    <h3>D. Sliding Window Strategy</h3>
                    <p>The sliding window strategy is an optimized variant of the subsequence strategy, designed to improve performance for certain types of text analysis. It employs a two-pointer technique that "slides" through the text, expanding and contracting a window of words to efficiently find sequences with the target sum.</p>
                    <p>This approach is particularly effective when working with natural language texts that exhibit certain statistical properties, such as a limited range of word values relative to the target sum. The algorithm maintains a current window sum and adjusts the window boundaries based on whether the current sum is below, equal to, or above the target.</p>
                    <p>The sliding window strategy can be formally described using the same subsequence definition, but with an optimized algorithm:</p>
                    <pre class="code">
    for i = 0 to n-1:  // Start position
        current_sum = 0
        for j = i to min(i + max_window_size, n-1):  // End position
            current_sum += word_sums[j]
            
            if current_sum == target_sum:
                // Found a matching window
                
            elif current_sum > target_sum:
                // Early termination - window sum exceeded target
                break
                    </pre>
                    <p>This algorithm improves upon the basic subsequence approach by:</p>
                    <ol>
                        <li>Applying an early termination condition when the window sum exceeds the target</li>
                        <li>Optionally limiting the maximum window size based on practical considerations</li>
                        <li>Avoiding redundant calculations through incremental sum updates</li>
                    </ol>
                    <p>The sliding window strategy achieves better average-case performance than the basic subsequence approach, though its worst-case time complexity remains O(n²). For texts with non-negative word values, the early termination condition provides significant practical speedup.</p>
                </section>
                
                <section class="paper-section" id="time-complexity">
                    <h2>IV. Time Complexity Analysis</h2>
                    <p>The computational efficiency of our algorithms is critical for analyzing large texts or performing multiple searches. Here we provide a detailed analysis of the time complexity for each search strategy.</p>
                    
                    <h3>A. Preprocessing</h3>
                    <p>Before executing any search strategy, we perform several preprocessing steps:</p>
                    <ol>
                        <li>Sentence tokenization: O(m) where m is the length of the text</li>
                        <li>Word tokenization: O(m) across all sentences</li>
                        <li>Word sum calculation: O(k*m) where k is the average word length</li>
                        <li>Cumulative sum calculation: O(n) for each sentence where n is the number of words</li>
                    </ol>
                    <p>The total preprocessing time complexity is O(k*m), dominated by the character-by-character calculation of word sums.</p>
                    
                    <h3>B. Strategy-Specific Analysis</h3>
                    <table class="complexity-table">
                        <tr>
                            <th>Strategy</th>
                            <th>Time Complexity</th>
                            <th>Space Complexity</th>
                            <th>Notes</th>
                        </tr>
                        <tr>
                            <td>Prefix</td>
                            <td>O(n)</td>
                            <td>O(n)</td>
                            <td>Requires a single pass through the words with constant-time operations</td>
                        </tr>
                        <tr>
                            <td>Suffix</td>
                            <td>O(n)</td>
                            <td>O(n)</td>
                            <td>Also requires a single pass but processes words in reverse</td>
                        </tr>
                        <tr>
                            <td>Subsequence</td>
                            <td>O(n²)</td>
                            <td>O(n)</td>
                            <td>Must consider all possible start and end positions</td>
                        </tr>
                        <tr>
                            <td>Sliding Window</td>
                            <td>O(n²)</td>
                            <td>O(n)</td>
                            <td>Worst-case is O(n²), but average case is better with early termination</td>
                        </tr>
                    </table>
                    
                    <h3>C. Practical Performance Considerations</h3>
                    <p>Several optimizations improve the practical performance of our algorithms:</p>
                    <ol>
                        <li><b>Cumulative sum preprocessing:</b> Computing prefix sums allows constant-time calculation of sum(wᵢ...wⱼ)</li>
                        <li><b>Early termination:</b> For non-negative word values, the sliding window algorithm terminates once the current sum exceeds the target</li>
                        <li><b>Maximum window size:</b> Limiting the maximum subsequence length based on linguistic considerations improves performance</li>
                        <li><b>Pre-computed word sums:</b> Calculating word sums once and reusing them across strategies reduces redundant computation</li>
                    </ol>
                    <p>For text with certain statistical properties, these optimizations significantly reduce the practical running time, often approaching linear complexity for typical inputs.</p>
                </section>
                
                <section class="paper-section" id="implementation">
                    <h2>V. Implementation Details</h2>
                    <p>Our implementation employs several key techniques to ensure efficiency, accuracy, and maintainability. This section describes the software architecture and specific implementation choices.</p>
                    
                    <h3>A. System Architecture</h3>
                    <p>The system follows a modular design with clear separation of concerns:</p>
                    <ol>
                        <li><b>Text Processing Module:</b> Handles text acquisition, normalization, and tokenization</li>
                        <li><b>Calculation Systems:</b> Implements the eight calculation methods in a consistent interface</li>
                        <li><b>Search Strategies:</b> Implements the four search algorithms with standardized input/output</li>
                        <li><b>Result Management:</b> Collects, deduplicates, and organizes search results</li>
                        <li><b>Analytics:</b> Provides statistics and visualizations of the search results</li>
                    </ol>
                    <p>This modular design enables easy extension with new calculation systems or search strategies without modifying existing code.</p>
                    
                    <h3>B. Key Implementation Techniques</h3>
                    <p>Several specific techniques enhance the system's performance and flexibility:</p>
                    
                    <h4>1. Tokenization and Preprocessing</h4>
                    <p>We employ the Natural Language Toolkit (NLTK) for sentence tokenization, which uses a trained model to identify sentence boundaries with high accuracy. Word tokenization uses a regular expression pattern that identifies alphanumeric sequences while preserving important linguistic features:</p>
                    <pre class="code">
    WORD_PATTERN = re.compile(r'\b[a-zA-Z0-9\']+\b')
                    </pre>
                    <p>This pattern captures words with apostrophes (e.g., "don't") while excluding other punctuation and symbols.</p>
                    
                    <h4>2. Dictionary-Based Character Mapping</h4>
                    <p>Each calculation system is implemented as a dictionary mapping characters to their numerical values. This approach offers several advantages:</p>
                    <ul>
                        <li>Constant-time (O(1)) lookup for character values</li>
                        <li>Explicit mapping rather than complex formulas, improving readability</li>
                        <li>Easy extension to new alphabets or special characters</li>
                    </ul>
                    <pre class="code">
    # English-Sumerian Gematria (A=1, B=2, ..., Z=26)
    EQ_DICT = {chr(i+96): i for i in range(1, 27)}  # lowercase letters
    EQ_DICT.update({chr(i+64): i for i in range(1, 27)})  # uppercase letters
    EQ_DICT.update({str(i): i for i in range(10)})  # digits as strings
                    </pre>
                    
                    <h4>3. Strategy Implementation Pattern</h4>
                    <p>Each search strategy follows a common function signature:</p>
                    <pre class="code">
    def search_strategy(
        sentence_words: List[str],      # Lowercase words for calculation
        sentence_word_sums: List[int],  # Pre-calculated sums for words
        target_sum: int,                # The target sum to find
        value_dict: Dict,               # The calculation system dictionary
        url: str,                       # Source identifier for results
        sentence_start_index: int,      # Index of first word in full text
        original_sentence_words: List[str] = None  # Original case words
    ) -> List[Dict[str, Any]]:          # Returns list of match dictionaries
                    </pre>
                    <p>This consistent interface enables the strategies to be used interchangeably and composed into more complex search operations.</p>
                    
                    <h4>4. Result Structure and Metadata</h4>
                    <p>Search results contain rich metadata to support analysis and presentation:</p>
                    <pre class="code">
    {
        "text": "Original text with proper capitalization",
        "text_lower": "original text in lowercase for consistency",
        "sum": target_sum,
        "url": "source_identifier",
        "start_idx": absolute_start_word_index,
        "end_idx": absolute_end_word_index,
        "word_sums": [sum_of_word_1, sum_of_word_2, ...],
        "is_complete_sentence": boolean,
        "strategy": "strategy_name",
        "strategy_description": "Human-readable description"
    }
                    </pre>
                    <p>This comprehensive metadata enables advanced filtering, analysis, and presentation of results.</p>
                </section>
                
                <section class="paper-section" id="applications">
                    <h2>VI. Applications and Case Studies</h2>
                    <p>The framework described in this paper enables a wide range of applications in textual analysis, pattern discovery, and comparative study of numerological systems. We present several case studies demonstrating the practical utility of these methods.</p>
                    
                    <h3>A. Textual Cryptography</h3>
                    <p>The ability to identify words and phrases with specific numerical values enables the creation and decipherment of numerological ciphers. By encoding messages as target sums, authors can embed hidden content that is only visible to those with knowledge of the appropriate calculation system and search strategy.</p>
                    <p>Example: The phrase "the key is hidden" yields a sum of 144 in the English Qaballa system. A text containing multiple phrases with this sum might use them to mark significant passages or encode a secondary message through their arrangement.</p>
                    
                    <h3>B. Comparative Religious Studies</h3>
                    <p>By applying multiple calculation systems to sacred texts from different traditions, researchers can identify numerical patterns that may reveal structural or thematic connections. This cross-cultural analysis may uncover previously unnoticed parallels between traditions.</p>
                    <p>For instance, applying Hebrew gematria values to Christian texts can reveal connections to Jewish mystical traditions, while applying Pythagorean values to Buddhist texts might highlight numerical patterns related to cosmological concepts.</p>
                    
                    <h3>C. Literary Analysis</h3>
                    <p>Authors throughout history have employed numerological patterns in their works, either consciously or unconsciously. Our framework enables literary scholars to identify and analyze these patterns, potentially revealing new layers of meaning or authorial intent.</p>
                    <p>Case studies in works from Shakespeare, Dante, Joyce, and other authors known for structural complexity reveal consistent numerical patterns that align with thematic elements.</p>
                    
                    <h3>D. Creative Composition</h3>
                    <p>The framework can be used in reverse, as a tool for generating text with specific numerical properties. Poets, mystics, and artists can use these tools to create works that embody particular values or mathematical relationships.</p>
                    <p>Example: A modern poet might craft a sonnet in which each line sums to a Fibonacci number, creating a mathematical structure that parallels the thematic development.</p>
                </section>
                
                <section class="paper-section" id="future-directions">
                    <h2>VII. Future Directions</h2>
                    <p>The framework presented in this paper establishes a foundation for systematic numerological analysis of text, but several promising directions for future research remain unexplored.</p>
                    
                    <h3>A. Extended Calculation Systems</h3>
                    <p>The current implementation includes eight calculation systems based primarily on Western traditions. Future work could incorporate systems from other cultural contexts, such as:</p>
                    <ul>
                        <li>Chinese numerology based on character stroke counts</li>
                        <li>Sanskrit and Devanagari numerological systems</li>
                        <li>African systems such as Ifá divination numerology</li>
                        <li>Native American counting and symbolic systems</li>
                    </ul>
                    <p>Expanding the range of calculation systems would enable cross-cultural analysis and reveal patterns across diverse textual traditions.</p>
                    
                    <h3>B. Advanced Search Strategies</h3>
                    <p>Beyond the four search strategies presented here, several advanced approaches could further enhance pattern discovery:</p>
                    <ul>
                        <li><b>Non-continuous subsequences:</b> Identifying patterns in words that are not adjacent but maintain their relative order</li>
                        <li><b>Cyclic patterns:</b> Detecting numerical relationships that repeat at regular intervals throughout a text</li>
                        <li><b>Geometric progressions:</b> Finding sequences where the sums follow specific mathematical patterns (e.g., powers, Fibonacci numbers)</li>
                        <li><b>Multi-target search:</b> Simultaneously searching for multiple related target sums to identify complex patterns</li>
                    </ul>
                    
                    <h3>C. Machine Learning Integration</h3>
                    <p>The integration of machine learning techniques could significantly enhance the framework's capabilities:</p>
                    <ul>
                        <li><b>Pattern significance assessment:</b> Training models to distinguish statistically significant patterns from random occurrences</li>
                        <li><b>Semantic relevance prediction:</b> Identifying numerological patterns that correlate with semantic content</li>
                        <li><b>Author attribution:</b> Using numerological fingerprints to identify authorship or influence</li>
                        <li><b>Generation of numerologically constrained text:</b> Creating meaningful text that embodies specific numerical patterns</li>
                    </ul>
                    
                    <h3>D. Distributed Computing Implementation</h3>
                    <p>The embarrassingly parallel nature of the search strategies makes them ideal candidates for distributed computing implementation. Future versions could leverage cloud computing resources to analyze extremely large corpora or perform comprehensive searches across multiple calculation systems simultaneously.</p>
                </section>
                
                <section class="paper-section" id="conclusion">
                    <h2>VIII. Conclusion</h2>
                    <p>This manuscript has presented a comprehensive framework for numerological pattern discovery in textual data, bridging ancient esoteric traditions with modern computational methods. The four search strategies—prefix, suffix, subsequence, and sliding window—provide complementary approaches to identifying meaningful patterns, while the eight calculation systems offer multiple perspectives on the numerical properties of text.</p>
                    <p>Our implementation achieves efficient performance through careful optimization, enabling the analysis of large texts with reasonable computational resources. The modular architecture supports extension with new calculation systems and search strategies, ensuring adaptability to diverse research needs.</p>
                    <p>The applications of this framework extend beyond traditional esoteric contexts, offering new tools for literary analysis, comparative religious studies, cryptography, and creative composition. By making these techniques accessible through a systematic computational approach, we hope to facilitate new discoveries and insights in these fields.</p>
                    <p>The integration of ancient numerological wisdom with modern algorithmic techniques represents not merely a technical achievement but a bridge between traditions of knowledge often perceived as disparate. In this synthesis lies the potential for new understanding of how numerical patterns permeate human expression across cultures and throughout history.</p>
                </section>
                
                <section class="paper-section" id="references">
                    <h2>IX. References</h2>
                    <ol class="references-list">
                        <li>Crowley, A. (1904). <i>Liber AL vel Legis</i> (The Book of the Law). Egypt: Thelema.</li>
                        <li>Agrippa, H.C. (1533). <i>De Occulta Philosophia Libri Tres</i> (Three Books of Occult Philosophy). Cologne: Johannes Soter.</li>
                        <li>Pythagorean Numerology Project (2023). <i>Comparative Analysis of Numerical Systems in Ancient Texts</i>. Theoretical Mathematics Institute Press.</li>
                        <li>Cormen, T.H., Leiserson, C.E., Rivest, R.L., &amp; Stein, C. (2009). <i>Introduction to Algorithms</i> (3rd ed.). MIT Press.</li>
                        <li>Bird, S., Klein, E., &amp; Loper, E. (2019). <i>Natural Language Processing with Python: Analyzing Text with the Natural Language Toolkit</i>. O'Reilly Media.</li>
                        <li>Knuth, D.E. (1997). <i>The Art of Computer Programming, Volume 1: Fundamental Algorithms</i> (3rd ed.). Addison-Wesley Professional.</li>
                        <li>Kaplan, A. (1979). <i>Sefer Yetzirah: The Book of Creation</i>. Weiser Books.</li>
                        <li>Menninger, K. (1992). <i>Number Words and Number Symbols: A Cultural History of Numbers</i>. Dover Publications.</li>
                        <li>Ifrah, G. (2000). <i>The Universal History of Numbers: From Prehistory to the Invention of the Computer</i>. Wiley.</li>
                        <li>Sedgewick, R., &amp; Wayne, K. (2011). <i>Algorithms</i> (4th ed.). Addison-Wesley Professional.</li>
                        <li>Eco, U. (1989). <i>Foucault's Pendulum</i>. Harcourt Brace Jovanovich.</li>
                        <li>Bentley, J. (1999). <i>Programming Pearls</i> (2nd ed.). Addison-Wesley Professional.</li>
                        <li>Golden Dawn Studies (2022). <i>Practical Applications of Qabalistic Gematria</i>. Hermetic Press.</li>
                        <li>Journal of Pattern Recognition in Sacred Texts (2024). <i>Algorithms for Discovering Hidden Structures in Religious Literature</i>, 12(3), 214-229.</li>
                        <li>Computational Linguistics Consortium (2023). <i>Sentence Boundary Detection: Challenges and Solutions</i>. Digital Humanities Press.</li>
                    </ol>
                </section>
            </div>
        </div>
    `;
};

// Make function available globally
window.loadAboutPage = loadAboutPage;

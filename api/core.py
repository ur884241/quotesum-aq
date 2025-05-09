import re
import requests
import logging
import os
import nltk
from typing import Dict, List, Any
from api.search_strategies import STRATEGY_FUNCTIONS, ALL_STRATEGIES

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- NLTK Data Setup --- 
# Define a local directory for NLTK data within the project
LOCAL_NLTK_DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'nltk_data')

# Ensure the local directory exists
if not os.path.exists(LOCAL_NLTK_DATA_DIR):
    try:
        os.makedirs(LOCAL_NLTK_DATA_DIR)
        logger.info(f"Created local NLTK data directory: {LOCAL_NLTK_DATA_DIR}")
    except OSError as e:
        logger.error(f"Failed to create local NLTK data directory {LOCAL_NLTK_DATA_DIR}: {e}")

# Add the local directory to NLTK's data path if it's not already there
if LOCAL_NLTK_DATA_DIR not in nltk.data.path:
    nltk.data.path.append(LOCAL_NLTK_DATA_DIR)
    logger.info(f"Added {LOCAL_NLTK_DATA_DIR} to nltk.data.path")

def fetch_text_from_url(url):
    """Fetch text content from a URL."""
    try:
        logger.info(f"Making HTTP request to URL: {url}")
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an exception for HTTP errors
        logger.info(f"Successfully retrieved content from URL: {url}")
        return response.text
    except requests.RequestException as e:
        logger.error(f"Error fetching URL {url}: {e}")
        if hasattr(e.response, 'status_code'):
            error_msg = f"HTTP {e.response.status_code}: {str(e)}"
        else:
            error_msg = str(e)
        raise Exception(f"Error fetching URL: {error_msg}")

def fetch_text(url):
    """
    Fetch text content from a URL, handling basic error cases.
    This function is used by app.py to retrieve text from a URL.
    """
    try:
        # Add basic http:// if not present
        if not url.startswith(('http://', 'https://')):
            logger.info(f"Adding http:// prefix to URL: {url}")
            url = 'http://' + url
            
        logger.info(f"Fetching text from URL: {url}")
        text = fetch_text_from_url(url)
        
        if not text or not text.strip():
            raise Exception("Retrieved empty text content")
            
        # Handle Project Gutenberg texts
        if 'gutenberg.org' in url:
            logger.info("Processing Project Gutenberg text")
            # Split text into lines
            lines = text.split('\n')
            
            # Find start and end markers
            start_marker = "*** START OF THIS PROJECT GUTENBERG EBOOK"
            end_marker = "*** END OF THIS PROJECT GUTENBERG EBOOK"
            
            start_idx = -1
            end_idx = -1
            
            for i, line in enumerate(lines):
                if start_marker in line:
                    start_idx = i + 1
                elif end_marker in line:
                    end_idx = i
                    break
            
            if start_idx != -1 and end_idx != -1:
                # Extract the actual content
                content_lines = lines[start_idx:end_idx]
                text = '\n'.join(content_lines)
                logger.info(f"Extracted Gutenberg content: {len(content_lines)} lines")
            else:
                logger.warning("Could not find Gutenberg markers, using full text")
            
        return text
    except Exception as e:
        logger.error(f"Error in fetch_text: {str(e)}")
        raise Exception(f"Failed to fetch text from URL: {str(e)}")

def create_eq_dict():
    """Create a dictionary mapping letters and numbers to their English Qaballa values."""
    # English Qaballa alphanumerical values
    eq_values = {
        # Numbers
        '0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
        # Letters
        'a': 10, 'b': 11, 'c': 12, 'd': 13, 'e': 14, 'f': 15, 'g': 16, 'h': 17, 'i': 18, 'j': 19,
        'k': 20, 'l': 21, 'm': 22, 'n': 23, 'o': 24, 'p': 25, 'q': 26, 'r': 27, 's': 28, 't': 29,
        'u': 30, 'v': 31, 'w': 32, 'x': 33, 'y': 34, 'z': 35
    }
    return eq_values

def create_reverse_eq_dict():
    """Create a dictionary mapping letters to their reverse English Qaballa values."""
    return {chr(97 + i): 36 - i for i in range(26)}

def create_ordinal_dict():
    """Create a dictionary mapping letters to their ordinal values."""
    return {chr(97 + i): i + 1 for i in range(26)}

def create_reduced_dict():
    """Create a dictionary mapping letters to their reduced values (sum of digits)."""
    return {chr(97 + i): ((i + 1) % 9) or 9 for i in range(26)}

def create_agrippa_dict():
    """Create a dictionary mapping letters to their Agrippa values."""
    return {chr(97 + i): ((i + 1) % 9) or 9 for i in range(26)}

def create_english_dict():
    """Create a dictionary mapping letters to their English values."""
    return {chr(97 + i): i + 1 for i in range(26)}

def create_hebrew_dict():
    """Create a dictionary mapping letters to their Hebrew values."""
    hebrew_values = {
        'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8, 'i': 9,
        'j': 10, 'k': 20, 'l': 30, 'm': 40, 'n': 50, 'o': 60, 'p': 70, 'q': 80,
        'r': 90, 's': 100, 't': 200, 'u': 300, 'v': 400, 'w': 500, 'x': 600,
        'y': 700, 'z': 800
    }
    return hebrew_values

def create_pythagorean_dict():
    """Create a dictionary mapping letters to their Pythagorean values."""
    pythagorean_values = {
        'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8, 'i': 9,
        'j': 1, 'k': 2, 'l': 3, 'm': 4, 'n': 5, 'o': 6, 'p': 7, 'q': 8, 'r': 9,
        's': 1, 't': 2, 'u': 3, 'v': 4, 'w': 5, 'x': 6, 'y': 7, 'z': 8
    }
    return pythagorean_values

# Initialize all dictionaries
VALUE_DICTS = {
    'eq': create_eq_dict(),
    'reverse_eq': create_reverse_eq_dict(),
    'ordinal': create_ordinal_dict(),
    'reduced': create_reduced_dict(),
    'agrippa': create_agrippa_dict(),
    'english': create_english_dict(),
    'hebrew': create_hebrew_dict(),
    'pythagorean': create_pythagorean_dict()
}

def calculate_all_sums(text):
    """Calculate all possible gematria sums for a given text."""
    text_lower = text.lower()
    sums = {}
    for name, value_dict in VALUE_DICTS.items():
        sums[name] = sum(value_dict.get(c, 0) for c in text_lower if c.isalnum() or c.isdigit())
    return sums

# Word tokenization pattern (consistent)
WORD_PATTERN = re.compile(r'\b\w+\b')

def simple_sentence_tokenize(text):
    """A simple sentence tokenizer that doesn't rely on NLTK."""
    # Split on common sentence endings
    sentences = []
    current = []
    
    # Common sentence endings
    endings = ['.', '!', '?', '...']
    
    # Split text into lines first
    lines = text.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Split on sentence endings
        parts = []
        current_part = []
        
        for char in line:
            current_part.append(char)
            if char in endings:
                parts.append(''.join(current_part))
                current_part = []
                
        if current_part:
            parts.append(''.join(current_part))
            
        # Clean up and add non-empty sentences
        for part in parts:
            part = part.strip()
            if part:
                sentences.append(part)
                
    return sentences

def find_matching_quotes(text, target_sum, url, calculation_type='eq', source_type='other'):
    """Find quotes in the text that match the target sum using multiple strategies."""
    try:
        logger.info(f"Starting search with target_sum={target_sum}, calculation_type={calculation_type}, source_type={source_type}")

        # Select the primary value dictionary for this search
        primary_value_dict = VALUE_DICTS.get(calculation_type, VALUE_DICTS['eq'])
        logger.info(f"Using primary calculation type: {calculation_type}")

        # Use simple sentence tokenization
        sentences = simple_sentence_tokenize(text)
        logger.info(f"Tokenized into {len(sentences)} sentences using simple tokenizer.")
        
        # Run search strategies
        all_matches = []
        sentence_start_index = 0  # Track the starting index of each sentence

        # For advanced analytics
        strategy_stats = {
            strategy_name: {
                "total_matches": 0,
                "complete_matches": 0,
                "incomplete_matches": 0,
                "word_count_distribution": {},
                "sentences_with_matches": 0,
                "longest_match": 0,
                "shortest_match": float('inf'),
                "avg_match_length": 0
            } for strategy_name in ALL_STRATEGIES
        }
        
        sentences_analyzed = 0
        sentences_with_matches = 0

        for sentence in sentences:
            sentences_analyzed += 1
            sentence_has_matches = False
            
            # Tokenize sentence into words for original case display
            original_sentence_words = WORD_PATTERN.findall(sentence)
            if not original_sentence_words:
                continue
                
            # Lowercase version for calculations
            sentence_lower = sentence.lower()
            sentence_words_lower = WORD_PATTERN.findall(sentence_lower)
            
            # Pre-calculate sums for words in this sentence using the primary method
            sentence_word_sums = [
                sum(primary_value_dict.get(c, 0) for c in word if c.isalnum() or c.isdigit()) 
                for word in sentence_words_lower
            ]

            # Log the calculation and strategies being applied
            logger.info(f"Applying strategies to sentence of {len(sentence_words_lower)} words using '{calculation_type}' calculation")
            
            # Apply all search strategies
            for strategy_name in ALL_STRATEGIES:
                logger.info(f"Running '{strategy_name}' strategy on sentence starting with: '{original_sentence_words[0] if original_sentence_words else ''}'")
                
                if strategy_name in STRATEGY_FUNCTIONS:
                    strategy_func = STRATEGY_FUNCTIONS[strategy_name]
                    strategy_matches = strategy_func(
                        sentence_words_lower,
                        sentence_word_sums,
                        target_sum,
                        primary_value_dict,
                        url,
                        sentence_start_index,
                        original_sentence_words
                    )
                    
                    if strategy_matches:
                        sentence_has_matches = True
                        all_matches.extend(strategy_matches)
                        
                        # Update strategy stats
                        stats = strategy_stats[strategy_name]
                        stats["total_matches"] += len(strategy_matches)
                        stats["complete_matches"] += sum(1 for m in strategy_matches if m.get("is_complete_sentence", False))
                        stats["incomplete_matches"] += sum(1 for m in strategy_matches if not m.get("is_complete_sentence", False))
                        
                        # Update word count distribution
                        for match in strategy_matches:
                            word_count = len(match["text"].split())
                            stats["word_count_distribution"][word_count] = stats["word_count_distribution"].get(word_count, 0) + 1
                            
                            # Update longest/shortest match
                            stats["longest_match"] = max(stats["longest_match"], word_count)
                            stats["shortest_match"] = min(stats["shortest_match"], word_count)
            
            # Update sentence start index for next sentence
            sentence_start_index += len(original_sentence_words)
            
            if sentence_has_matches:
                sentences_with_matches += 1
                for stats in strategy_stats.values():
                    stats["sentences_with_matches"] += 1

        # Calculate average match lengths
        for stats in strategy_stats.values():
            if stats["total_matches"] > 0:
                total_words = sum(count * freq for count, freq in stats["word_count_distribution"].items())
                stats["avg_match_length"] = total_words / stats["total_matches"]

        # Prepare the response
        response = {
            "matches": all_matches,
            "stats": {
                "total_sentences_analyzed": sentences_analyzed,
                "sentences_with_matches": sentences_with_matches,
                "total_matches": len(all_matches),
                "strategy_stats": strategy_stats
            }
        }

        return response

    except Exception as e:
        logger.error(f"Error in find_matching_quotes: {str(e)}")
        raise Exception(f"Error finding matching quotes: {str(e)}") 
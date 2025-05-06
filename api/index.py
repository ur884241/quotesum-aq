import re
import requests
import logging
import math
import os # Import os module
from typing import List, Dict, Any
import nltk
from nltk.tokenize.punkt import PunktSentenceTokenizer # Import specific tokenizer

# Import search strategy functions
from .search_strategies import STRATEGY_FUNCTIONS, ALL_STRATEGIES

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- NLTK Data Setup --- 
# Define a local directory for NLTK data within the project
LOCAL_NLTK_DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'nltk_data') # Go up one level from api

# Ensure the local directory exists
if not os.path.exists(LOCAL_NLTK_DATA_DIR):
    try:
        os.makedirs(LOCAL_NLTK_DATA_DIR)
        logger.info(f"Created local NLTK data directory: {LOCAL_NLTK_DATA_DIR}")
    except OSError as e:
        logger.error(f"Failed to create local NLTK data directory {LOCAL_NLTK_DATA_DIR}: {e}")
        # Might fail later if directory creation failed

# Add the local directory to NLTK's data path if it's not already there
if LOCAL_NLTK_DATA_DIR not in nltk.data.path:
    nltk.data.path.append(LOCAL_NLTK_DATA_DIR)
    logger.info(f"Added {LOCAL_NLTK_DATA_DIR} to nltk.data.path")

# Initial check/download at startup (optional but can be good)
try:
    nltk.data.find('tokenizers/punkt', paths=[LOCAL_NLTK_DATA_DIR]) # Check specific path
except LookupError:
    logger.info("NLTK 'punkt' not found in local dir at startup. Will attempt download on first use.")
# --- End NLTK Data Setup ---

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

# Define calculate_all_sums here, accessible by strategies if needed
# (Or pass VALUE_DICTS to the strategy functions)
def calculate_all_sums(text):
    """Calculate all possible gematria sums for a given text."""
    text_lower = text.lower()
    sums = {}
    for name, value_dict in VALUE_DICTS.items():
        sums[name] = sum(value_dict.get(c, 0) for c in text_lower if c.isalnum() or c.isdigit())
    return sums

# Word tokenization pattern (consistent)
WORD_PATTERN = re.compile(r'\b\w+\b')

# Global variable to hold the loaded tokenizer to avoid reloading every time
PUNKT_TOKENIZER = None

def load_punkt_tokenizer():
    """Loads the NLTK Punkt tokenizer, downloading if necessary to local dir."""
    global PUNKT_TOKENIZER
    if PUNKT_TOKENIZER is None:
        try:
            logger.info(f"Loading NLTK Punkt tokenizer (expecting data in {LOCAL_NLTK_DATA_DIR})...")
            # Load using the resource identifier; NLTK will check nltk.data.path
            PUNKT_TOKENIZER = nltk.data.load('tokenizers/punkt/english.pickle') 
            logger.info("NLTK Punkt tokenizer loaded successfully.")
        except LookupError:
            logger.warning(f"NLTK 'punkt' resource not found in {nltk.data.path}. Downloading to {LOCAL_NLTK_DATA_DIR}...")
            try:
                # Download specifically to the local directory
                nltk.download('punkt', download_dir=LOCAL_NLTK_DATA_DIR, quiet=True, raise_on_error=True)
                logger.info(f"NLTK 'punkt' downloaded to {LOCAL_NLTK_DATA_DIR}. Reloading tokenizer...")
                # Try loading again after download, using the identifier
                PUNKT_TOKENIZER = nltk.data.load('tokenizers/punkt/english.pickle')
                logger.info("NLTK Punkt tokenizer reloaded successfully from local dir.")
            except Exception as download_exc:
                logger.error(f"Failed to download NLTK 'punkt' resource to {LOCAL_NLTK_DATA_DIR}: {download_exc}")
                PUNKT_TOKENIZER = None 
                raise LookupError(f"Failed to load NLTK Punkt tokenizer after download attempt to {LOCAL_NLTK_DATA_DIR}.")
    return PUNKT_TOKENIZER

def find_matching_quotes(text, target_sum, url, calculation_type='eq', source_type='other'):
    """Find quotes in the text that match the target sum using multiple strategies."""
    try:
        logger.info(f"Starting search with target_sum={target_sum}, calculation_type={calculation_type}, source_type={source_type}")

        # Select the primary value dictionary for this search
        primary_value_dict = VALUE_DICTS.get(calculation_type, VALUE_DICTS['eq'])
        logger.info(f"Using primary calculation type: {calculation_type}")

        # --- Simple NLTK setup and tokenization ---
        sentences = []
        try:
            # Only download if not already done
            try:
                nltk.data.find('tokenizers/punkt')
                logger.info("NLTK 'punkt' found in data path.")
            except LookupError:
                logger.info("NLTK 'punkt' not found. Downloading to default location...")
                nltk.download('punkt', quiet=True)

            # Simple usage of sent_tokenize with no fancy loading
            sentences = nltk.tokenize.sent_tokenize(text)
            logger.info(f"Tokenized into {len(sentences)} sentences using nltk.tokenize.sent_tokenize.")
        except Exception as e:
            logger.error(f"Error during sentence tokenization: {e}")
            # Fall back to simple split by periods if NLTK fails
            logger.warning("Falling back to simple sentence splitting by periods.")
            # Simple backup tokenization - split by periods and basic cleanup
            sentences = [s.strip() for s in text.split('.') if s.strip()]
            logger.info(f"Tokenized into {len(sentences)} sentences using fallback method.")
        
        # Run search strategies
        all_matches = []
        original_word_index = 0

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
                        original_word_index,
                        original_sentence_words
                    )
                    
                    strategy_count = len(strategy_matches)
                    logger.info(f"'{strategy_name}' strategy found {strategy_count} matches with target sum {target_sum}")
                    
                    # Update analytics
                    if strategy_count > 0:
                        sentence_has_matches = True
                        strategy_stats[strategy_name]["total_matches"] += strategy_count
                        
                        for match in strategy_matches:
                            word_count = len(match.get("word_sums", []))
                            if word_count in strategy_stats[strategy_name]["word_count_distribution"]:
                                strategy_stats[strategy_name]["word_count_distribution"][word_count] += 1
                            else:
                                strategy_stats[strategy_name]["word_count_distribution"][word_count] = 1
                                
                            if match.get("is_complete_sentence", False):
                                strategy_stats[strategy_name]["complete_matches"] += 1
                            else:
                                strategy_stats[strategy_name]["incomplete_matches"] += 1
                                
                            strategy_stats[strategy_name]["longest_match"] = max(strategy_stats[strategy_name]["longest_match"], word_count)
                            strategy_stats[strategy_name]["shortest_match"] = min(strategy_stats[strategy_name]["shortest_match"], word_count)
                    
                    all_matches.extend(strategy_matches)
                else:
                    logger.warning(f"Strategy '{strategy_name}' not found in STRATEGY_FUNCTIONS")
            
            if sentence_has_matches:
                sentences_with_matches += 1
                for strategy_name in ALL_STRATEGIES:
                    if strategy_name in STRATEGY_FUNCTIONS and any(match.get("strategy", "") == strategy_name for match in all_matches):
                        strategy_stats[strategy_name]["sentences_with_matches"] += 1

            # Update the starting index for the next sentence
            original_word_index += len(sentence_words_lower)

        logger.info(f"Found {len(all_matches)} raw matches across all strategies for target sum {target_sum}.")

        # Process and deduplicate results
        complete_quotes = []
        incomplete_quotes = []
        seen_quotes_text = set()

        for match in all_matches:
            quote_text = match["text"]  # Use the original case version
            if quote_text not in seen_quotes_text:
                seen_quotes_text.add(quote_text)
                
                # Calculate all sums for this match (using the lowercase text)
                if "text_lower" in match:
                    match['all_sums'] = calculate_all_sums(match["text_lower"])
                else:
                    match['all_sums'] = calculate_all_sums(quote_text.lower())
                
                # Add the search strategy to the output
                strategy_name = match.get('strategy', 'unknown')
                    
                # Classify based on completeness
                if match.get('is_complete_sentence', False):
                    # Log complete sentence finds (these are more interesting)
                    logger.info(f"Found complete sentence match using '{strategy_name}' strategy: '{quote_text}'")
                    complete_quotes.append(match)
                else:
                    incomplete_quotes.append(match)
        
        # Calculate average match length for each strategy
        for strategy_name in ALL_STRATEGIES:
            total_matches = strategy_stats[strategy_name]["total_matches"]
            if total_matches > 0:
                total_words = sum(count * word_count for word_count, count in strategy_stats[strategy_name]["word_count_distribution"].items())
                strategy_stats[strategy_name]["avg_match_length"] = round(total_words / total_matches, 2)
            # Handle case where no matches were found
            if strategy_stats[strategy_name]["shortest_match"] == float('inf'):
                strategy_stats[strategy_name]["shortest_match"] = 0
                
        # Calculate overall statistics
        overall_stats = {
            "total_sentences": sentences_analyzed,
            "sentences_with_matches": sentences_with_matches,
            "match_rate": round(sentences_with_matches / sentences_analyzed * 100, 2) if sentences_analyzed > 0 else 0,
            "total_raw_matches": len(all_matches),
            "unique_complete_quotes": len(complete_quotes),
            "unique_incomplete_quotes": len(incomplete_quotes),
            "total_unique_quotes": len(complete_quotes) + len(incomplete_quotes)
        }
        
        logger.info(f"Found {len(complete_quotes)} unique complete quotes and {len(incomplete_quotes)} unique incomplete quotes after deduplication.")
        
        return {
            "success": True,
            "complete_quotes": complete_quotes,
            "incomplete_quotes": incomplete_quotes,
            "text_length": original_word_index,
            "calculation_type": calculation_type,
            "source_type": source_type,
            "advanced_analytics": {
                "overall": overall_stats,
                "strategies": strategy_stats
            }
        }
        
    except Exception as e:
        logger.exception(f"Error in find_matching_quotes: {str(e)}") # Log full traceback
        return {
            "success": False,
            "error": f"An internal error occurred during search: {str(e)}"
        }

# Note: The placeholder calculate_all_sums in search_strategies.py is not used.
# The main calculate_all_sums in this file is used after aggregation.
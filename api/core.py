import re
import requests
import logging
import os
import nltk
from typing import Dict, List, Any

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
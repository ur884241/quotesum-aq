import logging
from api import fetch_text

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    try:
        # Test with a known working URL
        test_url = "https://www.gutenberg.org/cache/epub/1998/pg1998.txt"
        logger.info(f"Testing api.fetch_text with: {test_url}")
        
        text = fetch_text(test_url)
        logger.info(f"Successfully fetched text (first 100 chars): {text[:100]}")
        
        logger.info("API fetch_text functionality works correctly!")
    except Exception as e:
        logger.error(f"Test failed: {str(e)}") 
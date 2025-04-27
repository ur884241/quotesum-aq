import requests
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
        raise Exception(f"Error fetching URL: {e}")

def fetch_text(url):
    """
    Fetch text content from a URL, handling basic error cases.
    """
    try:
        # Add basic http:// if not present
        if not url.startswith(('http://', 'https://')):
            logger.info(f"Adding http:// prefix to URL: {url}")
            url = 'http://' + url
            
        logger.info(f"Fetching text from URL: {url}")
        return fetch_text_from_url(url)
    except Exception as e:
        logger.error(f"Error in fetch_text: {str(e)}")
        raise Exception(f"Failed to fetch text from URL: {str(e)}")

if __name__ == "__main__":
    try:
        # Test with a known working URL
        test_url = "https://www.gutenberg.org/cache/epub/1998/pg1998.txt"
        logger.info(f"Testing URL fetching with: {test_url}")
        
        text = fetch_text(test_url)
        logger.info(f"Successfully fetched text (first 100 chars): {text[:100]}")
        
        logger.info("URL fetching functionality works correctly!")
    except Exception as e:
        logger.error(f"Test failed: {str(e)}") 
from http.server import BaseHTTPRequestHandler
import json
import re
import requests
import logging
from pymongo import MongoClient
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Starting API script")

MONGO_URI = os.environ.get('MONGO_URI')
logger.info(f"MONGO_URI is {'set' if MONGO_URI else 'not set'}")

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    # Force a connection to verify it works
    client.server_info()
    logger.info("Successfully connected to MongoDB")
    db = client.gematria_db
    quotes_collection = db.quotes
except Exception as e:
    logger.error(f"Failed to connect to MongoDB: {str(e)}")

def insert_quote(text, sum_value):
    logger.info(f"Attempting to insert quote: {text[:30]}...")
    try:
        quote = {"text": text, "sum": sum_value}
        result = quotes_collection.insert_one(quote)
        logger.info(f"Successfully inserted quote with id: {result.inserted_id}")
    except Exception as e:
        logger.error(f"Failed to insert quote: {str(e)}")

def get_quotes_by_sum(target_sum):
    logger.info(f"Attempting to retrieve quotes for sum: {target_sum}")
    try:
        quotes = list(quotes_collection.find({"sum": target_sum}, {"_id": 0}))
        logger.info(f"Retrieved {len(quotes)} quotes")
        return quotes
    except Exception as e:
        logger.error(f"Failed to retrieve quotes: {str(e)}")
        return []

def fetch_text(url):
    """Fetch text content from a given URL."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        logger.error(f"Error fetching text from URL: {e}")
        raise

def create_eq_dict():
    """Create a dictionary mapping letters to their corrected English Qaballa values."""
    return {chr(97 + i): 10 + i for i in range(26)}

EQ_DICT = create_eq_dict()

def eq_value(char):
    """Return the corrected English Qaballa value for a given character."""
    return EQ_DICT.get(char.lower(), 0)

def eq_sum(text):
    """Calculate the corrected English Qaballa sum for a given text."""
    return sum(eq_value(c) for c in text)

def find_sentence_start_quotes(text, target_sum, max_length=50):
    sentences = re.split(r"(?<=[.!?])\s+", text)
    quotes = []

    for sentence in sentences:
        words = sentence.split()
        current_sum = 0
        for i in range(min(len(words), max_length)):
            current_sum += eq_sum(words[i])
            if current_sum == target_sum:
                quote = " ".join(words[: i + 1])
                quote_obj = {"text": quote, "sum": target_sum}
                quotes.append(quote_obj)
                logger.info(f"Found matching quote: {quote[:30]}...")
                insert_quote(quote, target_sum)
            elif current_sum > target_sum:
                break

    logger.info(f"Found {len(quotes)} matching quotes in text")
    return quotes

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        logger.info("Received POST request")
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        body = json.loads(post_data.decode('utf-8'))
        
        try:
            url = body.get('url')
            target_sum = int(body.get('targetSum'))

            logger.info(f"Processing request for URL: {url} and target sum: {target_sum}")

            matching_quotes = get_quotes_by_sum(target_sum)
            logger.info(f"Retrieved {len(matching_quotes)} quotes from database")

            if len(matching_quotes) < 5:
                logger.info("Not enough quotes found in database, fetching text from URL")
                text = fetch_text(url)
                new_quotes = find_sentence_start_quotes(text, target_sum)
                matching_quotes.extend(new_quotes)

            response = {
                'success': True,
                'quotes': matching_quotes
            }

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            logger.info("Response sent successfully")

        except Exception as e:
            logger.error(f"Error processing request: {str(e)}")
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            error_response = {'success': False, 'error': str(e)}
            self.wfile.write(json.dumps(error_response).encode())

    def do_GET(self):
        logger.info(f"Received GET request: {self.path}")
        if self.path == '/debug-mongo':
            try:
                client.server_info()  # This will raise an exception if the connection fails
                message = {"status": "Connected to MongoDB successfully"}
                logger.info("MongoDB connection test successful")
            except Exception as e:
                message = {"status": "Failed to connect to MongoDB", "error": str(e)}
                logger.error(f"MongoDB connection test failed: {str(e)}")
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(message).encode())
        else:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            message = {"message": "Gematria function is running. Use POST to submit a request."}
            self.wfile.write(json.dumps(message).encode())
            logger.info("Sent GET response")

logger.info("API script loaded successfully")
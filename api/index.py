from http.server import BaseHTTPRequestHandler
import json
import re
import requests
import logging
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import os
import traceback

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Starting API script")

# MongoDB connection setup
MONGO_URI = os.environ.get('MONGO_URI')
DB_NAME = "gematria_db"
COLLECTION_NAME = "quotes"

if not MONGO_URI:
    logger.error("MONGO_URI environment variable is not set")
    raise ValueError("MONGO_URI environment variable is not set")

# Append database name to the URI if not already present
if "?" in MONGO_URI and not MONGO_URI.split("?")[0].endswith(DB_NAME):
    MONGO_URI = MONGO_URI.replace("?", f"/{DB_NAME}?")
elif "?" not in MONGO_URI:
    MONGO_URI += f"/{DB_NAME}"

logger.info(f"Connecting to MongoDB database: {DB_NAME}")

# Global MongoDB client variable
mongo_client = None
quotes_collection = None

def get_db():
    global mongo_client
    global quotes_collection
    
    if mongo_client is None:
        logger.info("Connecting to MongoDB...")
        mongo_client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
        mongo_client.admin.command('ping')  # Test connection
        logger.info("Pinged your deployment. You successfully connected to MongoDB!")
        db = mongo_client[DB_NAME]
        quotes_collection = db[COLLECTION_NAME]
        logger.info(f"Using collection: {COLLECTION_NAME}")
    return quotes_collection

def insert_quote(text, sum_value):
    logger.info(f"Attempting to insert quote: {text[:30]}...")
    try:
        quote = {"text": text, "sum": sum_value}
        result = get_db().insert_one(quote)
        logger.info(f"Successfully inserted quote with id: {result.inserted_id}")
    except Exception as e:
        logger.error(f"Failed to insert quote: {str(e)}")

def get_quotes_by_sum(target_sum):
    logger.info(f"Attempting to retrieve quotes for sum: {target_sum}")
    try:
        quotes = list(get_db().find({"sum": target_sum}, {"_id": 0}))
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
    def send_json_response(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

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

            self.send_json_response(response)
            logger.info("Response sent successfully")

        except Exception as e:
            logger.error(f"Error processing request: {str(e)}")
            error_response = {'success': False, 'error': str(e)}
            self.send_json_response(error_response, 500)

    def do_GET(self):
        logger.info(f"Received GET request: {self.path}")
        try:
            if self.path == '/api/gematria/debug-mongo':
                if mongo_client is not None:
                    try:
                        mongo_client.admin.command('ping')
                        message = {"status": "Connected to MongoDB successfully"}
                        logger.info("MongoDB connection test successful")
                    except Exception as e:
                        message = {"status": "Failed to connect to MongoDB", "error": str(e)}
                        logger.error(f"MongoDB connection test failed: {str(e)}")
                else:
                    message = {"status": "MongoDB client is not initialized"}
                    logger.error("MongoDB client is not initialized")
            else:
                message = {"message": "Gematria function is running. Use POST to submit a request."}
            
            self.send_json_response(message)
        except Exception as e:
            logger.error(f"Error in GET request: {str(e)}")
            logger.error(traceback.format_exc())
            self.send_json_response({"error": "Internal server error"}, 500)

logger.info("API script loaded successfully")

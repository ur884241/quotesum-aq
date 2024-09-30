from http.server import BaseHTTPRequestHandler
import json
import re
import requests
import logging
import traceback
import sys
import os
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from urllib.parse import urlparse

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# MongoDB setup
MONGODB_URI = os.environ.get('MONGODB_URI')
if not MONGODB_URI:
    raise ValueError("MONGODB_URI environment variable is not set")

uri_parts = urlparse(MONGODB_URI)
DB_NAME = uri_parts.path.strip('/') or "gematria_db"

client = MongoClient(MONGODB_URI, server_api=ServerApi('1'), connectTimeoutMS=30000, socketTimeoutMS=None, connect=False, maxPoolsize=1)
db = client[DB_NAME]
quotes_collection = db['quotes']

# Helper functions
def create_eq_dict():
    return {chr(97 + i): 10 + i for i in range(26)}

EQ_DICT = create_eq_dict()

def eq_value(char):
    return EQ_DICT.get(char.lower(), 0)

def eq_sum(text):
    return sum(eq_value(c) for c in text)

def fetch_text(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        logger.error(f"Error fetching text from URL: {e}")
        raise

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

def log_error(e):
    error_type, error_value, error_traceback = sys.exc_info()
    print(f"Error Type: {error_type}", file=sys.stderr)
    print(f"Error Value: {error_value}", file=sys.stderr)
    print("Traceback:", file=sys.stderr)
    traceback.print_tb(error_traceback, file=sys.stderr)
    print(f"Full traceback: {traceback.format_exc()}", file=sys.stderr)

class handler(BaseHTTPRequestHandler):
    def send_json_response(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_GET(self):
        logger.info(f"Received GET request: {self.path}")
        try:
            if self.path == '/api/test-mongodb':
                try:
                    client.admin.command('ping')
                    self.send_json_response({"status": "MongoDB connection successful"})
                except Exception as e:
                    log_error(e)
                    self.send_json_response({"error": "MongoDB connection failed", "details": str(e)}, 500)
            elif self.path == '/api/test-env':
                env_vars = {key: value for key, value in os.environ.items() if not key.lower().contains('secret')}
                self.send_json_response({"environment_variables": env_vars})
            elif self.path == '/api/gematria/debug-mongo':
                if client is not None:
                    try:
                        client.admin.command('ping')
                        message = {"status": "Connected to MongoDB successfully"}
                        logger.info("MongoDB connection test successful")
                    except Exception as e:
                        message = {"status": "Failed to connect to MongoDB", "error": str(e)}
                        logger.error(f"MongoDB connection test failed: {str(e)}")
                else:
                    message = {"status": "MongoDB client is not initialized"}
                    logger.error("MongoDB client is not initialized")
                self.send_json_response(message)
            else:
                message = {"message": "Gematria function is running. Use POST to submit a request."}
                self.send_json_response(message)
        except Exception as e:
            log_error(e)
            self.send_json_response({"error": "Internal server error", "details": str(e)}, 500)

    def do_POST(self):
        logger.info("Received POST request")
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            body = json.loads(post_data.decode('utf-8'))
            
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
            log_error(e)
            error_response = {'success': False, 'error': str(e), 'traceback': traceback.format_exc()}
            self.send_json_response(error_response, 500)

def main(req):
    try:
        return handler(req, ("", 0), None).wfile.getvalue()
    except Exception as e:
        log_error(e)
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal Server Error", "details": str(e)})
        }

logger.info("API script loaded successfully")
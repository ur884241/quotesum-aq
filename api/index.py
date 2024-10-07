from http.server import BaseHTTPRequestHandler
import json
import re
import requests
import logging
import traceback
import sys
import os
import cgi
import io
import PyPDF2
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

def insert_quote(text, sum_value, url):
    logger.info(f"Attempting to insert quote: {text[:30]}...")
    try:
        quote = {"text": text, "sum": sum_value, "url": url}
        result = quotes_collection.insert_one(quote)
        logger.info(f"Successfully inserted quote with id: {result.inserted_id}")
    except Exception as e:
        logger.error(f"Failed to insert quote: {str(e)}")

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

def find_sentence_start_quotes(text, target_sum, url, max_length=50):
    sentences = re.split(r"(?<=[.!?])\s+", text)
    quotes = []

    for sentence in sentences:
        words = sentence.split()
        current_sum = 0
        for i in range(min(len(words), max_length)):
            current_sum += eq_sum(words[i])
            if current_sum == target_sum:
                quote = " ".join(words[: i + 1])
                quote_obj = {"text": quote, "sum": target_sum, "url": url}
                quotes.append(quote_obj)
                logger.info(f"Found matching quote: {quote[:30]}...")
                insert_quote(quote, target_sum, url)
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
        try:
            content_type, pdict = cgi.parse_header(self.headers.get('content-type'))
            
            if content_type == 'multipart/form-data':
                form = cgi.FieldStorage(
                    fp=self.rfile,
                    headers=self.headers,
                    environ={'REQUEST_METHOD': 'POST',
                             'CONTENT_TYPE': self.headers['Content-Type'],
                             })
                
                target_sum = int(form.getvalue('targetSum'))
                
                if 'file' in form:
                    file_item = form['file']
                    if file_item.filename:
                        logger.info(f"Processing uploaded file: {file_item.filename}")
                        text = self.process_uploaded_file(file_item)
                        url = file_item.filename  # Use filename as URL for uploaded files
                    else:
                        self.send_json_response({'success': False, 'error': 'No file uploaded'}, 400)
                        return
                elif 'url' in form:
                    url = form.getvalue('url')
                    if url:
                        logger.info(f"Processing URL: {url}")
                        text = fetch_text(url)
                    else:
                        self.send_json_response({'success': False, 'error': 'No URL provided'}, 400)
                        return
                else:
                    self.send_json_response({'success': False, 'error': 'No file or URL provided'}, 400)
                    return
            else:
                self.send_json_response({'success': False, 'error': 'Unsupported content type'}, 400)
                return

            # Find quotes only from the current text
            matching_quotes = find_sentence_start_quotes(text, target_sum, url)
            
            response = {
                'success': True,
                'quotes': matching_quotes
            }

            self.send_json_response(response)
            logger.info(f"Response sent successfully with {len(matching_quotes)} quotes from the current text")

        except Exception as e:
            logger.error(f"Error processing request: {str(e)}")
            logger.error(traceback.format_exc())
            error_response = {'success': False, 'error': str(e), 'traceback': traceback.format_exc()}
            self.send_json_response(error_response, 500)

    def process_uploaded_file(self, file_item):
        filename = file_item.filename
        file_content = file_item.file.read()
        
        if filename.lower().endswith('.pdf'):
            return self.extract_text_from_pdf(file_content)
        elif filename.lower().endswith('.txt'):
            return file_content.decode('utf-8')
        else:
            raise ValueError("Unsupported file type. Please upload a PDF or TXT file.")

    def extract_text_from_pdf(self, pdf_content):
        pdf_file = io.BytesIO(pdf_content)
        reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text

    def do_GET(self):
        logger.info(f"Received GET request: {self.path}")
        try:
            if self.path == '/api/gematria/debug-mongo':
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
            else:
                message = {"message": "Gematria function is running. Use POST to submit a request."}
            
            self.send_json_response(message)
        except Exception as e:
            logger.error(f"Error in GET request: {str(e)}")
            logger.error(traceback.format_exc())
            self.send_json_response({"error": "Internal server error"}, 500)

def main(request):
    return handler(request, ("", 0), None).wfile.getvalue()

logger.info("API script loaded successfully")
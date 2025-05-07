import re
import requests
import logging
import math
import os
from typing import List, Dict, Any
import nltk
from nltk.tokenize.punkt import PunktSentenceTokenizer
from http.server import BaseHTTPRequestHandler
import json
import traceback
import urllib.parse

# Import search strategy functions using absolute imports
from api.search_strategies import STRATEGY_FUNCTIONS, ALL_STRATEGIES
from api.core import (
    fetch_text, calculate_all_sums, VALUE_DICTS,
    WORD_PATTERN, load_punkt_tokenizer, find_matching_quotes
)

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

def handler(event, context):
    """AWS Lambda handler function."""
    try:
        # Parse the request body
        body = json.loads(event.get('body', '{}'))
        url = body.get('url', '')
        target_sum = body.get('target_sum', 0)
        calculation_type = body.get('calculation_type', 'eq')
        source_type = body.get('source_type', 'other')

        # Validate inputs
        if not url:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'URL is required'})
            }

        # Fetch and process the text
        text = fetch_text(url)
        results = find_matching_quotes(text, target_sum, url, calculation_type, source_type)

        return {
            'statusCode': 200,
            'body': json.dumps(results)
        }
    except Exception as e:
        logger.error(f"Error in handler: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

class VercelHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests."""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'status': 'ok'}).encode())

    def do_POST(self):
        """Handle POST requests."""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            body = json.loads(post_data.decode('utf-8'))

            url = body.get('url', '')
            target_sum = body.get('target_sum', 0)
            calculation_type = body.get('calculation_type', 'eq')
            source_type = body.get('source_type', 'other')

            # Validate inputs
            if not url:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'URL is required'}).encode())
                return

            # Fetch and process the text
            text = fetch_text(url)
            results = find_matching_quotes(text, target_sum, url, calculation_type, source_type)

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(results).encode())
        except Exception as e:
            logger.error(f"Error in POST handler: {str(e)}")
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode()) 
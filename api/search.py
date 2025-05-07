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
# In Vercel's environment, we can't write to the filesystem
# So we'll use NLTK's default data path
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    logger.info("Downloading NLTK 'punkt' data...")
    nltk.download('punkt', quiet=True)
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

def vercel_handler(request):
    """Vercel serverless function handler."""
    if request.method == 'GET':
        return {
            'statusCode': 200,
            'body': json.dumps({'status': 'ok'})
        }
    
    try:
        body = json.loads(request.body)
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
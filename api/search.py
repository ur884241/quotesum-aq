import json
import sys
import os
import logging
import traceback
import urllib.parse

# Add parent directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# Import core functionality
from api.index import fetch_text, find_matching_quotes

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def handler(request):
    """Serverless handler function for Vercel"""
    try:
        logger.info("API/search endpoint called")
        
        # Check if this is a POST request
        method = request.get('method', '')
        logger.info(f"Request method: {method}")
        
        if method != 'POST':
            return {
                'statusCode': 405,
                'body': json.dumps({"error": "Method not allowed. Use POST."}),
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                }
            }
            
        # Get form data
        body = request.get('body', '')
        headers = request.get('headers', {})
        content_type = headers.get('content-type', '')
        logger.info(f"Content-Type: {content_type}")
        
        # Parse form data
        params = {}
        
        if 'application/x-www-form-urlencoded' in content_type:
            try:
                params = urllib.parse.parse_qs(body)
                params = {k: v[0] if isinstance(v, list) and len(v) == 1 else v for k, v in params.items()}
            except Exception as e:
                logger.error(f"Error parsing form data: {str(e)}")
        elif 'application/json' in content_type:
            try:
                params = json.loads(body)
            except json.JSONDecodeError as e:
                logger.error(f"Error parsing JSON: {str(e)}")
        
        logger.info(f"Parsed parameters: {params}")
        
        # Extract query parameters
        target_sum = params.get('targetSum')
        url = params.get('url')
        calculation_type = params.get('calculationType', 'eq')
        
        logger.info(f"Search parameters: target_sum={target_sum}, url={url}, calculation_type={calculation_type}")
        
        # Validate parameters
        if not target_sum:
            return {
                'statusCode': 400,
                'body': json.dumps({"error": "Target sum is required"}),
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                }
            }
            
        if not url:
            return {
                'statusCode': 400,
                'body': json.dumps({"error": "URL is required"}),
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                }
            }
        
        try:
            # Fetch text from URL
            logger.info(f"Fetching text from URL: {url}")
            text = fetch_text(url)
            logger.info(f"Successfully fetched text, length: {len(text) if text else 0}")
            
            if not text:
                return {
                    'statusCode': 400,
                    'body': json.dumps({"error": "Failed to read text content"}),
                    'headers': {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*'
                    }
                }
                
            # Find matching quotes
            logger.info(f"Starting search with text length: {len(text)}")
            results = find_matching_quotes(text, int(target_sum), url, calculation_type=calculation_type)
            logger.info(f"Search completed successfully")
            
            # Return success response
            return {
                'statusCode': 200,
                'body': json.dumps(results),
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                }
            }
            
        except Exception as e:
            logger.error(f"Error processing request: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            
            return {
                'statusCode': 500,
                'body': json.dumps({
                    "error": f"Error processing request: {str(e)}",
                    "traceback": traceback.format_exc()
                }),
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                }
            }
            
    except Exception as e:
        logger.error(f"Unhandled error: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        
        return {
            'statusCode': 500,
            'body': json.dumps({
                "error": f"Server error: {str(e)}",
                "traceback": traceback.format_exc()
            }),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            }
        } 
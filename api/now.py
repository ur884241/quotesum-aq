from http.server import BaseHTTPRequestHandler
import json
import traceback
import logging
import os
import sys

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the core functionality
from api.index import fetch_text, find_matching_quotes

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"status": "API is running"}).encode())
        
    def do_POST(self):
        try:
            # Parse request
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode('utf-8')
            content_type = self.headers.get('Content-Type', '')
            
            logger.info(f"Received POST request to {self.path}")
            logger.info(f"Content-Type: {content_type}")
            
            if '/api/search' in self.path:
                # Parse form data
                form_data = {}
                
                if 'application/x-www-form-urlencoded' in content_type:
                    import urllib.parse
                    form_data = urllib.parse.parse_qs(post_data)
                    # Extract single values from lists
                    form_data = {k: v[0] if isinstance(v, list) and len(v) == 1 else v 
                              for k, v in form_data.items()}
                elif 'application/json' in content_type:
                    form_data = json.loads(post_data)
                else:
                    self.send_error_json(400, "Unsupported content type. Use application/x-www-form-urlencoded or application/json")
                    return
                
                logger.info(f"Parsed form data: {form_data}")
                
                # Extract parameters
                target_sum = form_data.get('targetSum')
                url = form_data.get('url')
                calculation_type = form_data.get('calculationType', 'eq')
                
                logger.info(f"Processing search request: target_sum={target_sum}, url={url}, calculation_type={calculation_type}")
                
                if not target_sum:
                    self.send_error_json(400, "Target sum is required")
                    return
                
                if not url:
                    self.send_error_json(400, "URL is required")
                    return
                
                try:
                    # Fetch text from URL
                    logger.info(f"Fetching text from URL: {url}")
                    text = fetch_text(url)
                    logger.info(f"Successfully fetched text, length: {len(text) if text else 0}")
                    
                    if not text:
                        self.send_error_json(400, "Failed to read text content")
                        return
                    
                    # Find matching quotes
                    logger.info(f"Starting search with text length: {len(text)}")
                    results = find_matching_quotes(text, int(target_sum), url, calculation_type=calculation_type)
                    logger.info(f"Search completed successfully")
                    
                    # Send response
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps(results).encode())
                    
                except Exception as e:
                    logger.error(f"Error processing request: {str(e)}")
                    logger.error(f"Traceback: {traceback.format_exc()}")
                    self.send_error_json(500, f"Error processing request: {str(e)}")
            else:
                self.send_error_json(404, "Not Found")
                
        except Exception as e:
            logger.error(f"Unhandled error: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            self.send_error_json(500, f"Server error: {str(e)}")
    
    def send_error_json(self, status, message):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps({"error": message}).encode())

def handler(request, response):
    # Create a Handler instance
    handler = Handler()
    
    # Set request and client address
    handler.path = request.get('path', '/')
    handler.headers = request.get('headers', {})
    handler.client_address = ('vercel-serverless', 0)
    
    # Handle request based on method
    method = request.get('method', 'GET')
    
    if method == 'POST':
        handler.do_POST()
    else:
        handler.do_GET()
        
    # Return response
    return response 
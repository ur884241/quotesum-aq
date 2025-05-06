from http.server import BaseHTTPRequestHandler
import json
import sys
import os
import logging
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

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps({"status": "Search API is ready"}).encode())
        
    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode('utf-8')
            content_type = self.headers.get('Content-Type', '')
            
            logger.info(f"Received POST request with content type: {content_type}")
            
            # Parse form data
            form_data = {}
            if 'application/x-www-form-urlencoded' in content_type:
                form_data = urllib.parse.parse_qs(post_data)
                # Extract single values from lists
                form_data = {k: v[0] if isinstance(v, list) and len(v) == 1 else v for k, v in form_data.items()}
            elif 'application/json' in content_type:
                form_data = json.loads(post_data)
                
            # Extract parameters
            target_sum = form_data.get('targetSum')
            url = form_data.get('url')
            calculation_type = form_data.get('calculationType', 'eq')
            
            logger.info(f"Processing request: target_sum={target_sum}, url={url}, calculation_type={calculation_type}")
            
            if not target_sum or not url:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Target sum and URL are required"}).encode())
                return
                
            # Process the request
            text = fetch_text(url)
            if not text:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Failed to fetch text from URL"}).encode())
                return
                
            # Find matching quotes
            results = find_matching_quotes(text, int(target_sum), url, calculation_type=calculation_type)
            
            # Send response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(results).encode())
            
        except Exception as e:
            logger.error(f"Error processing request: {str(e)}")
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode()) 
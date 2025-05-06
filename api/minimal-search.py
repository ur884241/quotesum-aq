from http.server import BaseHTTPRequestHandler
import json
import logging
import urllib.parse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Handler(BaseHTTPRequestHandler):
    def send_json_response(self, status_code, data):
        """Helper method to send JSON response"""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_GET(self):
        try:
            response_data = {
                "success": True,
                "mock": True,
                "message": "GET request to minimal-search successful",
                "complete_quotes": [{"text": "Mock GET quote", "sum": 123}],
                "incomplete_quotes": []
            }
            self.send_json_response(200, response_data)
        except Exception as e:
            logger.error(f"Error in GET handler: {str(e)}")
            self.send_json_response(500, {
                "success": False,
                "error": str(e)
            })

    def do_POST(self):
        try:
            # Read request body
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode('utf-8')
            content_type = self.headers.get('Content-Type', '')
            
            logger.info(f"Received POST request with content type: {content_type}")
            logger.info(f"Raw post data: {post_data}")
            
            # Parse request data based on content type
            if 'application/x-www-form-urlencoded' in content_type:
                form_data = urllib.parse.parse_qs(post_data)
                # Extract single values from lists
                form_data = {k: v[0] if isinstance(v, list) and len(v) == 1 else v for k, v in form_data.items()}
                logger.info(f"Parsed form data: {form_data}")
            else:
                self.send_json_response(400, {
                    "success": False,
                    "error": "Unsupported content type. Use application/x-www-form-urlencoded"
                })
                return

            # Mock response for POST
            response_data = {
                "success": True,
                "mock": True,
                "message": "POST request to minimal-search successful",
                "complete_quotes": [{"text": "Mock POST quote", "sum": 123}],
                "incomplete_quotes": []
            }
            self.send_json_response(200, response_data)
            
        except Exception as e:
            logger.error(f"Error in POST handler: {str(e)}")
            self.send_json_response(500, {
                "success": False,
                "error": str(e)
            })

# The class Handler is automatically detected by Vercel
# No need for an explicit handler(request,response) function at the bottom 
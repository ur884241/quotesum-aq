from http.server import BaseHTTPRequestHandler
import json

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        response_data = {
            "success": True,
            "mock": True,
            "message": "GET request to minimal-search successful",
            "complete_quotes": [{"text": "Mock GET quote", "sum": 123}],
            "incomplete_quotes": []
        }
        self.wfile.write(json.dumps(response_data).encode())

    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        response_data = {
            "success": True,
            "mock": True,
            "message": "POST request to minimal-search successful",
            "complete_quotes": [{"text": "Mock POST quote", "sum": 123}],
            "incomplete_quotes": []
        }
        self.wfile.write(json.dumps(response_data).encode())

# The class Handler is automatically detected by Vercel
# No need for an explicit handler(request,response) function at the bottom 
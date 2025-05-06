from http.server import BaseHTTPRequestHandler
import json

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        response_data = {
            "message": "Hello from Vercel serverless function",
            "status": "OK"
        }
        self.wfile.write(json.dumps(response_data).encode())
        
    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        response_data = {
            "message": "Hello from Vercel serverless function (POST)",
            "status": "OK"
        }
        self.wfile.write(json.dumps(response_data).encode()) 
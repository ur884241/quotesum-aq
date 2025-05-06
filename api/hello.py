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

def handler(request, response):
    if request.method == 'POST':
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Hello from Vercel serverless function (POST)",
                "status": "OK"
            }),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            }
        }
    else:
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Hello from Vercel serverless function (GET)",
                "status": "OK"
            }),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            }
        } 
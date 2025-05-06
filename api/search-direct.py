import json
import sys
import os

# Add parent directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# Import core functionality
try:
    from api.index import fetch_text, find_matching_quotes
except ImportError:
    def fetch_text(url):
        return f"Mock text from {url}"
    
    def find_matching_quotes(text, target_sum, url, calculation_type='eq', source_type='other'):
        return {
            "success": True,
            "mock": True,
            "complete_quotes": [
                {"text": "This is a mock quote", "sum": target_sum}
            ],
            "incomplete_quotes": []
        }

def handler(request, response):
    """Simple serverless handler for Vercel"""
    try:
        # Handle GET requests - just return a status
        if request.get('method') == 'GET':
            return {
                "statusCode": 200,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps({"status": "Search API is ready"})
            }
        
        # Get form data
        body = request.get('body', '')
        headers = request.get('headers', {})
        content_type = headers.get('content-type', '')
        
        # Parse form data
        params = {}
        if 'application/x-www-form-urlencoded' in content_type:
            import urllib.parse
            params = urllib.parse.parse_qs(body)
            # Extract single values from lists
            params = {k: v[0] if isinstance(v, list) and len(v) == 1 else v for k, v in params.items()}
        elif 'application/json' in content_type:
            params = json.loads(body)
        
        # Extract parameters
        target_sum = params.get('targetSum')
        url = params.get('url')
        calculation_type = params.get('calculationType', 'eq')
        
        # Validate parameters
        if not target_sum or not url:
            return {
                "statusCode": 400,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps({"error": "Target sum and URL are required"})
            }
        
        # Process the request
        text = fetch_text(url)
        if not text:
            return {
                "statusCode": 400,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps({"error": "Failed to fetch text from URL"})
            }
        
        # Find matching quotes
        results = find_matching_quotes(text, int(target_sum), url, calculation_type=calculation_type)
        
        # Return success response
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps(results)
        }
        
    except Exception as e:
        # Return error response
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"error": str(e)})
        } 
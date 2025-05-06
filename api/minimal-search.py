import json
import logging
import urllib.parse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def handler(request):
    """Serverless function handler for Vercel"""
    try:
        logger.info("Received serverless request")
        method = request.get('method', 'GET')
        
        # Handle GET requests
        if method == 'GET':
            response_data = {
                "success": True,
                "mock": True,
                "message": "GET request to minimal-search successful",
                "complete_quotes": [{"text": "Mock GET quote", "sum": 123}],
                "incomplete_quotes": []
            }
            return {
                "statusCode": 200,
                "body": json.dumps(response_data),
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                }
            }
        
        # Handle POST requests
        elif method == 'POST':
            # Get request body and content type
            body = request.get('body', '')
            headers = request.get('headers', {})
            content_type = headers.get('content-type', '')
            
            logger.info(f"Received POST request with content type: {content_type}")
            logger.info(f"Raw post data: {body}")
            
            # Parse request data based on content type
            if 'application/x-www-form-urlencoded' in content_type:
                form_data = urllib.parse.parse_qs(body)
                # Extract single values from lists
                form_data = {k: v[0] if isinstance(v, list) and len(v) == 1 else v for k, v in form_data.items()}
                logger.info(f"Parsed form data: {form_data}")
            else:
                return {
                    "statusCode": 400,
                    "body": json.dumps({
                        "success": False,
                        "error": "Unsupported content type. Use application/x-www-form-urlencoded"
                    }),
                    "headers": {
                        "Content-Type": "application/json",
                        "Access-Control-Allow-Origin": "*"
                    }
                }

            # Mock response for POST
            response_data = {
                "success": True,
                "mock": True,
                "message": "POST request to minimal-search successful",
                "complete_quotes": [{"text": "Mock POST quote", "sum": 123}],
                "incomplete_quotes": []
            }
            return {
                "statusCode": 200,
                "body": json.dumps(response_data),
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                }
            }
            
        else:
            return {
                "statusCode": 405,
                "body": json.dumps({
                    "success": False,
                    "error": "Method not allowed"
                }),
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                }
            }
            
    except Exception as e:
        logger.error(f"Error in handler: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({
                "success": False,
                "error": str(e)
            }),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            }
        } 
from flask import Flask, request, jsonify
import logging
import traceback
import os
import json
import tempfile
from api.core import fetch_text
from api.search import find_matching_quotes

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)

# Helper function to parse multipart form data
def parse_multipart_form(request_body, content_type):
    """Parse multipart form data manually for serverless environment"""
    import cgi
    from io import BytesIO
    
    environ = {
        'REQUEST_METHOD': 'POST',
        'CONTENT_TYPE': content_type,
        'CONTENT_LENGTH': len(request_body)
    }
    
    form = cgi.FieldStorage(
        fp=BytesIO(request_body),
        environ=environ,
        keep_blank_values=True
    )
    
    result = {}
    for field in form.keys():
        if form[field].filename:
            # This is a file upload
            result[field] = {
                'filename': form[field].filename,
                'content': form[field].file.read()
            }
        else:
            # This is a regular field
            result[field] = form[field].value
            
    return result

def handler(request):
    """Handle serverless requests for Vercel"""
    try:
        logger.info("Received serverless request")
        
        # Check if this is a POST request to /api/search
        if request.path == "/api/search" and request.method == "POST":
            logger.info("Processing /api/search request")
            
            # Get form data
            content_type = request.headers.get('content-type', '')
            
            if 'multipart/form-data' in content_type:
                # Parse multipart form data for file uploads
                form_data = parse_multipart_form(request.body, content_type)
                target_sum = form_data.get('targetSum')
                url = form_data.get('url')
                calculation_type = form_data.get('calculationType', 'eq')
                source_type = form_data.get('sourceType', 'other')
                
                # Check if file was uploaded
                file_data = form_data.get('file')
                file = None
                if file_data:
                    # Create a temp file
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.txt') as temp_file:
                        temp_file.write(file_data['content'])
                        file_path = temp_file.name
                    
                    with open(file_path, 'r', encoding='utf-8') as f:
                        text = f.read()
                    
                    # Clean up
                    os.unlink(file_path)
            else:
                # Regular form data
                form_data = request.form
                target_sum = form_data.get('targetSum')
                url = form_data.get('url')
                calculation_type = form_data.get('calculationType', 'eq')
                source_type = form_data.get('sourceType', 'other')
                file = None
                
            logger.info(f"Request params: target_sum={target_sum}, url={url}, calculation_type={calculation_type}")
            
            if not target_sum:
                return {
                    "statusCode": 400,
                    "body": json.dumps({"error": "Target sum is required"}),
                    "headers": {"Content-Type": "application/json"}
                }
            
            text = None
            
            try:
                if url:
                    logger.info(f"Fetching text from URL: {url}")
                    text = fetch_text(url)
                    logger.info(f"Text fetched successfully, length: {len(text) if text else 0}")
                elif file:
                    logger.info(f"Processing uploaded file")
                    # Use the text that was already read from the file
                    logger.info(f"File processed successfully, length: {len(text) if text else 0}")
                else:
                    return {
                        "statusCode": 400,
                        "body": json.dumps({"error": "Either URL or a valid .txt file is required"}),
                        "headers": {"Content-Type": "application/json"}
                    }
                
                if not text:
                    return {
                        "statusCode": 400,
                        "body": json.dumps({"error": "Failed to read text content"}),
                        "headers": {"Content-Type": "application/json"}
                    }
                
                logger.info("Starting search for quotes")
                results = find_matching_quotes(text, int(target_sum), url, calculation_type=calculation_type, source_type=source_type)
                
                return {
                    "statusCode": 200,
                    "body": json.dumps(results),
                    "headers": {"Content-Type": "application/json"}
                }
                
            except Exception as e:
                logger.error(f"Error processing request: {str(e)}")
                logger.error(f"Traceback: {traceback.format_exc()}")
                
                return {
                    "statusCode": 500,
                    "body": json.dumps({
                        "error": f"Error processing request: {str(e)}",
                        "traceback": traceback.format_exc()
                    }),
                    "headers": {"Content-Type": "application/json"}
                }
                
        # Return 404 for unsupported routes
        return {
            "statusCode": 404,
            "body": json.dumps({"error": "Not Found"}),
            "headers": {"Content-Type": "application/json"}
        }
        
    except Exception as e:
        logger.error(f"Unhandled error in handler: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": f"Server error: {str(e)}",
                "traceback": traceback.format_exc()
            }),
            "headers": {"Content-Type": "application/json"}
        } 
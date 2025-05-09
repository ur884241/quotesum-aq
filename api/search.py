from flask import Flask, request, jsonify
import logging
import json
from api.core import find_matching_quotes, fetch_text

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/api/search', methods=['POST'])
def search():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        # Extract parameters
        url = data.get('url')
        target_sum = data.get('target_sum')
        calculation_type = data.get('calculation_type', 'eq')
        source_type = data.get('source_type', 'other')

        # Validate required parameters
        if not url:
            return jsonify({"error": "URL is required"}), 400
        if not target_sum:
            return jsonify({"error": "Target sum is required"}), 400

        # Fetch text from URL
        text = fetch_text(url)

        # Find matching quotes
        result = find_matching_quotes(
            text=text,
            target_sum=target_sum,
            url=url,
            calculation_type=calculation_type,
            source_type=source_type
        )

        return jsonify(result)

    except Exception as e:
        logger.error(f"Error in search endpoint: {str(e)}")
        return jsonify({"error": str(e)}), 500

def vercel_handler(request):
    """Vercel serverless function handler."""
    try:
        # Handle CORS preflight
        if request.method == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type'
                }
            }

        # Handle GET request
        if request.method == 'GET':
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'status': 'ok'})
            }

        # Handle POST request
        if request.method == 'POST':
            try:
                # Get request body
                if isinstance(request.body, str):
                    body = json.loads(request.body)
                else:
                    body = request.body

                logger.info(f"Received request body: {body}")

                # Extract parameters
                url = body.get('url')
                target_sum = body.get('targetSum')  # Note: frontend uses targetSum
                calculation_type = body.get('calculationType', 'eq')  # Note: frontend uses calculationType
                source_type = body.get('source_type', 'other')

                # Validate inputs
                if not url:
                    return {
                        'statusCode': 400,
                        'headers': {
                            'Content-Type': 'application/json',
                            'Access-Control-Allow-Origin': '*'
                        },
                        'body': json.dumps({'error': 'URL is required'})
                    }

                if not target_sum:
                    return {
                        'statusCode': 400,
                        'headers': {
                            'Content-Type': 'application/json',
                            'Access-Control-Allow-Origin': '*'
                        },
                        'body': json.dumps({'error': 'Target sum is required'})
                    }

                logger.info(f"Processing request with url={url}, target_sum={target_sum}, calculation_type={calculation_type}")

                # Fetch and process the text
                text = fetch_text(url)
                results = find_matching_quotes(
                    text=text,
                    target_sum=target_sum,
                    url=url,
                    calculation_type=calculation_type,
                    source_type=source_type
                )

                return {
                    'statusCode': 200,
                    'headers': {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*'
                    },
                    'body': json.dumps(results)
                }

            except json.JSONDecodeError as e:
                logger.error(f"JSON decode error: {str(e)}")
                return {
                    'statusCode': 400,
                    'headers': {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*'
                    },
                    'body': json.dumps({'error': 'Invalid JSON in request body'})
                }
            except Exception as e:
                logger.error(f"Error processing request: {str(e)}")
                return {
                    'statusCode': 500,
                    'headers': {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*'
                    },
                    'body': json.dumps({
                        'error': str(e),
                        'message': 'An error occurred while processing your request'
                    })
                }

        # Handle unsupported methods
        return {
            'statusCode': 405,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': 'Method not allowed'})
        }

    except Exception as e:
        logger.error(f"Error in vercel_handler: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': str(e),
                'message': 'An unexpected error occurred'
            })
        }

if __name__ == '__main__':
    app.run(debug=True) 
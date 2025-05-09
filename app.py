from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS
import tempfile
import os
import traceback
from api.core import fetch_text
from api.search import find_matching_quotes
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

# Error handler for all exceptions
@app.errorhandler(Exception)
def handle_error(error):
    logger.error(f"Unhandled error: {str(error)}")
    logger.error(f"Traceback: {traceback.format_exc()}")
    return jsonify({
        'error': f'Server error: {str(error)}',
        'traceback': traceback.format_exc()
    }), 500

@app.route('/api/search', methods=['POST'])
def search():
    try:
        logger.info("Received search request")
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        # Extract parameters with support for both camelCase and snake_case
        target_sum = data.get('targetSum') or data.get('target_sum')
        url = data.get('url')
        calculation_type = data.get('calculationType') or data.get('calculation_type', 'eq')
        source_type = data.get('sourceType') or data.get('source_type', 'other')

        logger.info(f"Request parameters: target_sum={target_sum}, url={url}, calculation_type={calculation_type}")

        if not target_sum:
            return jsonify({'error': 'Target sum is required'}), 400
        if not url:
            return jsonify({'error': 'URL is required'}), 400

        try:
            logger.info(f"Fetching text from URL: {url}")
            text = fetch_text(url)
            logger.info(f"Successfully fetched text from URL, length: {len(text) if text else 0}")

            if not text:
                return jsonify({'error': 'Failed to read text content'}), 400

            logger.info("Starting quote search")
            results = find_matching_quotes(text, int(target_sum), url, calculation_type=calculation_type, source_type=source_type)
            logger.info(f"Search completed successfully")
            return jsonify(results)

        except Exception as e:
            logger.error(f"Error processing request: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            return jsonify({
                'error': f'Error processing request: {str(e)}',
                'traceback': traceback.format_exc()
            }), 500

    except Exception as e:
        logger.error(f"Server error: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return jsonify({
            'error': f'Server error: {str(e)}',
            'traceback': traceback.format_exc()
        }), 500

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 
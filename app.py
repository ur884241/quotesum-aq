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
        target_sum = request.form.get('targetSum')
        url = request.form.get('url')
        file = request.files.get('file')
        calculation_type = request.form.get('calculationType', 'eq')
        source_type = request.form.get('sourceType', 'other')

        logger.info(f"Request parameters: target_sum={target_sum}, url={url}, calculation_type={calculation_type}")

        if not target_sum:
            return jsonify({'error': 'Target sum is required'}), 400

        text = None
        try:
            if url:
                logger.info(f"Fetching text from URL: {url}")
                text = fetch_text(url)
                logger.info(f"Successfully fetched text from URL, length: {len(text) if text else 0}")
            elif file and file.filename.endswith('.txt'):
                logger.info(f"Processing uploaded file: {file.filename}")
                # Save the file temporarily
                with tempfile.NamedTemporaryFile(delete=False, suffix='.txt') as temp_file:
                    file.save(temp_file.name)
                    with open(temp_file.name, 'r', encoding='utf-8') as f:
                        text = f.read()
                # Clean up the temporary file
                os.unlink(temp_file.name)
                logger.info(f"Successfully processed file, length: {len(text) if text else 0}")
            else:
                return jsonify({'error': 'Either URL or a valid .txt file is required'}), 400

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
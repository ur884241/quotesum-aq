from flask import Flask, request, send_from_directory, jsonify, Response
from api.search import find_matching_quotes
from api.core import fetch_text
import os
import traceback
import json

app = Flask(__name__, 
            static_folder='.',
            static_url_path='')

def process_request(request):
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
        print(f"Error in process_request: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500

@app.route('/api/search', methods=['POST'])
def search_handler():
    try:
        response = process_request(request)
        return response
    except Exception as e:
        print(f"Error in search_handler: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        })

@app.route('/<path:path>')
def serve_static(path):
    try:
        return send_from_directory('.', path)
    except Exception as e:
        print(f"Error serving static file {path}: {str(e)}")
        return str(e), 404

@app.route('/')
def serve_index():
    try:
        return send_from_directory('.', 'index.html')
    except Exception as e:
        print(f"Error serving index: {str(e)}")
        return str(e), 500

if __name__ == '__main__':
    print("Starting server...")
    print("Current working directory:", os.getcwd())
    print("Files in directory:", os.listdir('.'))
    app.run(debug=True, port=5000) 
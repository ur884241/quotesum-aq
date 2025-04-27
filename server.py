from flask import Flask, request, send_from_directory, jsonify, Response
from api.index import process_request
import os
import traceback
import json

app = Flask(__name__, 
            static_folder='.',
            static_url_path='')

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
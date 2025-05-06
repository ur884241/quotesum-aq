from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS
import tempfile
import os
from api.index import find_matching_quotes, fetch_text

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

@app.route('/api/search', methods=['POST'])
def search():
    try:
        target_sum = request.form.get('targetSum')
        url = request.form.get('url')
        file = request.files.get('file')
        calculation_type = request.form.get('calculationType', 'eq')
        source_type = request.form.get('sourceType', 'other')

        if not target_sum:
            return jsonify({'error': 'Target sum is required'}), 400

        text = None
        try:
            if url:
                text = fetch_text(url)
            elif file and file.filename.endswith('.txt'):
                # Save the file temporarily
                with tempfile.NamedTemporaryFile(delete=False, suffix='.txt') as temp_file:
                    file.save(temp_file.name)
                    with open(temp_file.name, 'r', encoding='utf-8') as f:
                        text = f.read()
                # Clean up the temporary file
                os.unlink(temp_file.name)
            else:
                return jsonify({'error': 'Either URL or a valid .txt file is required'}), 400

            if not text:
                return jsonify({'error': 'Failed to read text content'}), 400

            results = find_matching_quotes(text, int(target_sum), url, calculation_type=calculation_type, source_type=source_type)
            return jsonify(results)

        except Exception as e:
            # Log the specific error for debugging
            app.logger.error(f"Error processing request: {str(e)}")
            return jsonify({'error': f'Error processing request: {str(e)}'}), 500

    except Exception as e:
        # Log the specific error for debugging
        app.logger.error(f"Server error: {str(e)}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 
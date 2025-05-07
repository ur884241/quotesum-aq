from flask import Flask, request, jsonify
import logging
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

if __name__ == '__main__':
    app.run(debug=True) 
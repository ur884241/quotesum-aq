from http.server import BaseHTTPRequestHandler
import json
import re
import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

def fetch_text(url):
    """Fetch text content from a given URL."""
    response = requests.get(url, timeout=10)
    if response.status_code != 200:
        raise ValueError(f"Failed to fetch text: {response.status_code} {response.reason}")
    return response.text

def create_eq_dict():
    """Create a dictionary mapping letters to their corrected English Qaballa values."""
    return {chr(97 + i): 10 + i for i in range(26)}

# Create the English Qaballa dictionary
EQ_DICT = create_eq_dict()

def eq_value(char):
    """Return the corrected English Qaballa value for a given character."""
    return EQ_DICT.get(char.lower(), 0)

def eq_sum(text):
    """Calculate the corrected English Qaballa sum for a given text."""
    return sum(eq_value(c) for c in text)

def find_sentence_start_quotes(text, target_sum, max_length=50):
    """
    Find quotes that start sentences and have a specific English Qaballa sum.
    Args:
        text (str): The text to search in.
        target_sum (int): The target English Qaballa sum.
        max_length (int): Maximum number of words in a quote.
    Returns:
        list: A list of matching quotes.
    """
    sentences = re.split(r"(?<=[.!?])\s+", text)
    quotes = []

    for sentence in sentences:
        words = sentence.split()
        current_sum = 0
        for i in range(min(len(words), max_length)):
            current_sum += eq_sum(words[i])
            if current_sum == target_sum:
                quote = " ".join(words[: i + 1])
                quotes.append(quote)
            elif current_sum > target_sum:
                break

    return quotes

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        body = json.loads(post_data)

        # Extract URL and target sum from the request body
        url = body.get('url')
        target_sum = body.get('target_sum')

        if not url or not target_sum:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'Missing url or target_sum in request body')
            return

        try:
            text = fetch_text(url)
            quotes = find_sentence_start_quotes(text, target_sum)
            response = {'quotes': quotes}
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
        except Exception as e:
            logging.error(f"Error processing request: {e}")
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b'Internal server error')

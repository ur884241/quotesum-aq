from flask import Flask, render_template, request, jsonify
import requests
import re

app = Flask(__name__)

def create_eq_dict():
    return {chr(97 + i): 10 + i for i in range(26)}

EQ_DICT = create_eq_dict()

def eq_value(char):
    return EQ_DICT.get(char.lower(), 0)

def eq_sum(text):
    return sum(eq_value(c) for c in text)

def find_sentence_start_quotes(text, target_sum, max_length=50):
    sentences = re.split(r'(?<=[.!?])\s+', text)
    quotes = []
    
    for sentence in sentences:
        words = sentence.split()
        current_sum = 0
        for i in range(min(len(words), max_length)):
            current_sum += eq_sum(words[i])
            if current_sum == target_sum:
                quote = ' '.join(words[:i+1])
                quotes.append(quote)
            elif current_sum > target_sum:
                break
    
    return quotes

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    url = request.form['url']
    target_sum = int(request.form['target_sum'])
    
    try:
        response = requests.get(url)
        text = response.text
        matching_quotes = find_sentence_start_quotes(text, target_sum)
        return jsonify({
            'success': True,
            'quotes': [{'text': quote, 'sum': eq_sum(quote)} for quote in matching_quotes]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
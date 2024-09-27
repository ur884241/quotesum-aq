import json
import requests
import re

# Create a dictionary with the alphabetical gematria values
def create_eq_dict():
    return {chr(97 + i): 10 + i for i in range(26)}

EQ_DICT = create_eq_dict()

# Calculate gematria value of a single character
def eq_value(char):
    return EQ_DICT.get(char.lower(), 0)

# Calculate gematria sum of a text
def eq_sum(text):
    return sum(eq_value(c) for c in text)

# Find sentences starting with matching quotes
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

# The Netlify handler function
def handler(event, context):
    try:
        # Parse the body from the event (sent as JSON)
        body = json.loads(event['body'])
        url = body.get('url')
        target_sum = int(body.get('targetSum'))

        # Fetch the text file from the URL
        response = requests.get(url)
        if response.status_code != 200:
            return {
                'statusCode': 400,
                'body': json.dumps({'success': False, 'error': 'Failed to fetch the file from the provided URL'})
            }

        text = response.text
        matching_quotes = find_sentence_start_quotes(text, target_sum)

        # Return the matching quotes and their sums
        return {
            'statusCode': 200,
            'body': json.dumps({
                'success': True,
                'quotes': [{'text': quote, 'sum': eq_sum(quote)} for quote in matching_quotes]
            })
        }
    
    # Error handling
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'success': False, 'error': str(e)})
        }

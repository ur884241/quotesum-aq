import json
import requests
import re

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

def handler(event, context):
    try:
        body = json.loads(event['body'])
        url = body.get('url')
        target_sum = int(body.get('targetSum'))

        response = requests.get(url)
        text = response.text
        matching_quotes = find_sentence_start_quotes(text, target_sum)

        return {
            'statusCode': 200,
            'body': json.dumps({
                'success': True,
                'quotes': [{'text': quote, 'sum': eq_sum(quote)} for quote in matching_quotes]
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'success': False, 'error': str(e)})
        }

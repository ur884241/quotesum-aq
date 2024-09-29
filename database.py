from pymongo import MongoClient
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# MongoDB setup
MONGO_URI = os.environ.get('MONGO_URI')
client = MongoClient(MONGO_URI)
db = client.gematria_db
quotes_collection = db.quotes

def insert_quote(text, sum_value):
    """Insert a quote into the MongoDB database."""
    quote = {"text": text, "sum": sum_value}
    try:
        result = quotes_collection.insert_one(quote)
        logging.info(f"Inserted quote with ID: {result.inserted_id}")
    except Exception as e:
        logging.error(f"Error inserting quote: {str(e)}")

def get_quotes_by_sum(target_sum):
    """Retrieve quotes from the MongoDB database by sum value."""
    try:
        quotes = list(quotes_collection.find({"sum": target_sum}, {"_id": 0}))
        logging.info(f"Retrieved {len(quotes)} quotes for sum {target_sum}")
        return quotes
    except Exception as e:
        logging.error(f"Error retrieving quotes: {str(e)}")
        return []
from pymongo import MongoClient
import os

# MongoDB setup
MONGO_URI = os.environ.get('MONGO_URI')
client = MongoClient(MONGO_URI)
db = client.gematria_db
quotes_collection = db.quotes

def insert_quote(text, sum_value):
    """Insert a quote into the MongoDB database."""
    quote = {"text": text, "sum": sum_value}
    quotes_collection.insert_one(quote)

def get_quotes_by_sum(target_sum):
    """Retrieve quotes from the MongoDB database by sum value."""
    return list(quotes_collection.find({"sum": target_sum}, {"_id": 0}))
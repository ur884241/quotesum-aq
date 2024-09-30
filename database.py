import logging
from pymongo import MongoClient
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("database.py is being imported")

MONGO_URI = os.environ.get('MONGO_URI')
logger.info(f"MONGO_URI: {MONGO_URI[:10]}...") # Log the first 10 characters of the URI for security

try:
    client = MongoClient(MONGO_URI)
    db = client.gematria_db
    quotes_collection = db.quotes
    logger.info("Successfully connected to MongoDB")
except Exception as e:
    logger.error(f"Failed to connect to MongoDB: {str(e)}")

def insert_quote(text, sum_value):
    logger.info(f"Attempting to insert quote: {text[:30]}...")
    try:
        quote = {"text": text, "sum": sum_value}
        result = quotes_collection.insert_one(quote)
        logger.info(f"Successfully inserted quote with id: {result.inserted_id}")
    except Exception as e:
        logger.error(f"Failed to insert quote: {str(e)}")

def get_quotes_by_sum(target_sum):
    logger.info(f"Attempting to retrieve quotes for sum: {target_sum}")
    try:
        quotes = list(quotes_collection.find({"sum": target_sum}, {"_id": 0}))
        logger.info(f"Retrieved {len(quotes)} quotes")
        return quotes
    except Exception as e:
        logger.error(f"Failed to retrieve quotes: {str(e)}")
        return []

logger.info("database.py has been fully loaded")
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# MongoDB setup
MONGO_URI = os.environ.get('MONGO_URI')
if not MONGO_URI:
    logger.error("MONGO_URI environment variable is not set")
    raise ValueError("MONGO_URI environment variable is not set")

try:
    client = MongoClient(MONGO_URI)
    # The ismaster command is cheap and does not require auth.
    client.admin.command('ismaster')
    logger.info("Successfully connected to MongoDB")
except ConnectionFailure:
    logger.error("Server not available")
    raise

db = client.gematria_db
quotes_collection = db.quotes

def insert_quote(text, sum_value):
    """Insert a quote into the MongoDB database."""
    quote = {"text": text, "sum": sum_value}
    try:
        result = quotes_collection.insert_one(quote)
        logger.info(f"Inserted quote with ID: {result.inserted_id}")
        return True
    except Exception as e:
        logger.error(f"Error inserting quote: {str(e)}")
        return False

def get_quotes_by_sum(target_sum):
    """Retrieve quotes from the MongoDB database by sum value."""
    try:
        quotes = list(quotes_collection.find({"sum": target_sum}, {"_id": 0}))
        logger.info(f"Retrieved {len(quotes)} quotes for sum {target_sum}")
        return quotes
    except Exception as e:
        logger.error(f"Error retrieving quotes: {str(e)}")
        return []

logger.info("database.py module loaded successfully")
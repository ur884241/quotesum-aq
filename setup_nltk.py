import nltk
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define a local directory for NLTK data within the project
LOCAL_NLTK_DATA_DIR = os.path.join(os.path.dirname(__file__), 'nltk_data')

# Ensure the local directory exists
if not os.path.exists(LOCAL_NLTK_DATA_DIR):
    try:
        os.makedirs(LOCAL_NLTK_DATA_DIR)
        logger.info(f"Created local NLTK data directory: {LOCAL_NLTK_DATA_DIR}")
    except OSError as e:
        logger.error(f"Failed to create local NLTK data directory {LOCAL_NLTK_DATA_DIR}: {e}")

# Add the local directory to NLTK's data path if it's not already there
if LOCAL_NLTK_DATA_DIR not in nltk.data.path:
    nltk.data.path.append(LOCAL_NLTK_DATA_DIR)
    logger.info(f"Added {LOCAL_NLTK_DATA_DIR} to nltk.data.path")

# Download required NLTK data
required_packages = [
    'punkt',  # For sentence tokenization
    'averaged_perceptron_tagger',  # For POS tagging
    'wordnet'  # For word meanings
]

for package in required_packages:
    try:
        logger.info(f"Downloading NLTK package: {package}")
        nltk.download(package, download_dir=LOCAL_NLTK_DATA_DIR)
        logger.info(f"Successfully downloaded {package}")
    except Exception as e:
        logger.error(f"Failed to download {package}: {e}")

logger.info("NLTK setup complete!") 
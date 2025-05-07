from http.server import BaseHTTPRequestHandler
import json
import sys
import os
import logging
import urllib.parse
import nltk
from typing import List, Dict, Any
from api.core import (
    fetch_text, calculate_all_sums, VALUE_DICTS,
    WORD_PATTERN, load_punkt_tokenizer
)
from api.search_strategies import STRATEGY_FUNCTIONS, ALL_STRATEGIES

# Add parent directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps({"status": "Search API is ready"}).encode())
        
    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode('utf-8')
            content_type = self.headers.get('Content-Type', '')
            
            logger.info(f"Received POST request with content type: {content_type}")
            
            # Parse form data
            form_data = {}
            if 'application/x-www-form-urlencoded' in content_type:
                form_data = urllib.parse.parse_qs(post_data)
                # Extract single values from lists
                form_data = {k: v[0] if isinstance(v, list) and len(v) == 1 else v for k, v in form_data.items()}
            elif 'application/json' in content_type:
                form_data = json.loads(post_data)
                
            # Extract parameters
            target_sum = form_data.get('targetSum')
            url = form_data.get('url')
            calculation_type = form_data.get('calculationType', 'eq')
            
            logger.info(f"Processing request: target_sum={target_sum}, url={url}, calculation_type={calculation_type}")
            
            if not target_sum or not url:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Target sum and URL are required"}).encode())
                return
                
            # Process the request
            text = fetch_text(url)
            if not text:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Failed to fetch text from URL"}).encode())
                return
                
            # Find matching quotes
            results = find_matching_quotes(text, int(target_sum), url, calculation_type=calculation_type)
            
            # Send response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(results).encode())
            
        except Exception as e:
            logger.error(f"Error processing request: {str(e)}")
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode()) 

def find_matching_quotes(text, target_sum, url, calculation_type='eq', source_type='other'):
    """Find quotes in the text that match the target sum using multiple strategies."""
    try:
        logger.info(f"Starting search with target_sum={target_sum}, calculation_type={calculation_type}, source_type={source_type}")

        # Select the primary value dictionary for this search
        primary_value_dict = VALUE_DICTS.get(calculation_type, VALUE_DICTS['eq'])
        logger.info(f"Using primary calculation type: {calculation_type}")

        # --- Simple NLTK setup and tokenization ---
        sentences = []
        try:
            # Only download if not already done
            try:
                nltk.data.find('tokenizers/punkt')
                logger.info("NLTK 'punkt' found in data path.")
            except LookupError:
                logger.info("NLTK 'punkt' not found. Downloading to default location...")
                nltk.download('punkt', quiet=True)

            # Simple usage of sent_tokenize with no fancy loading
            sentences = nltk.tokenize.sent_tokenize(text)
            logger.info(f"Tokenized into {len(sentences)} sentences using nltk.tokenize.sent_tokenize.")
        except Exception as e:
            logger.error(f"Error during sentence tokenization: {e}")
            # Fall back to simple split by periods if NLTK fails
            logger.warning("Falling back to simple sentence splitting by periods.")
            # Simple backup tokenization - split by periods and basic cleanup
            sentences = [s.strip() for s in text.split('.') if s.strip()]
            logger.info(f"Tokenized into {len(sentences)} sentences using fallback method.")
        
        # Run search strategies
        all_matches = []
        original_word_index = 0

        # For advanced analytics
        strategy_stats = {
            strategy_name: {
                "total_matches": 0,
                "complete_matches": 0,
                "incomplete_matches": 0,
                "word_count_distribution": {},
                "sentences_with_matches": 0,
                "longest_match": 0,
                "shortest_match": float('inf'),
                "avg_match_length": 0
            } for strategy_name in ALL_STRATEGIES
        }
        
        sentences_analyzed = 0
        sentences_with_matches = 0

        for sentence in sentences:
            sentences_analyzed += 1
            sentence_has_matches = False
            
            # Tokenize sentence into words for original case display
            original_sentence_words = WORD_PATTERN.findall(sentence)
            if not original_sentence_words:
                continue
                
            # Lowercase version for calculations
            sentence_lower = sentence.lower()
            sentence_words_lower = WORD_PATTERN.findall(sentence_lower)
            
            # Pre-calculate sums for words in this sentence using the primary method
            sentence_word_sums = [
                sum(primary_value_dict.get(c, 0) for c in word if c.isalnum() or c.isdigit()) 
                for word in sentence_words_lower
            ]

            # Log the calculation and strategies being applied
            logger.info(f"Applying strategies to sentence of {len(sentence_words_lower)} words using '{calculation_type}' calculation")
            
            # Apply all search strategies
            for strategy_name in ALL_STRATEGIES:
                logger.info(f"Running '{strategy_name}' strategy on sentence starting with: '{original_sentence_words[0] if original_sentence_words else ''}'")
                
                if strategy_name in STRATEGY_FUNCTIONS:
                    strategy_func = STRATEGY_FUNCTIONS[strategy_name]
                    strategy_matches = strategy_func(
                        sentence_words_lower,
                        sentence_word_sums,
                        target_sum,
                        primary_value_dict, 
                        url,
                        original_word_index,
                        original_sentence_words
                    )
                    
                    strategy_count = len(strategy_matches)
                    logger.info(f"'{strategy_name}' strategy found {strategy_count} matches with target sum {target_sum}")
                    
                    # Update analytics
                    if strategy_count > 0:
                        sentence_has_matches = True
                        strategy_stats[strategy_name]["total_matches"] += strategy_count
                        
                        for match in strategy_matches:
                            word_count = len(match.get("word_sums", []))
                            if word_count in strategy_stats[strategy_name]["word_count_distribution"]:
                                strategy_stats[strategy_name]["word_count_distribution"][word_count] += 1
                            else:
                                strategy_stats[strategy_name]["word_count_distribution"][word_count] = 1
                                
                            if match.get("is_complete_sentence", False):
                                strategy_stats[strategy_name]["complete_matches"] += 1
                            else:
                                strategy_stats[strategy_name]["incomplete_matches"] += 1
                                
                            strategy_stats[strategy_name]["longest_match"] = max(strategy_stats[strategy_name]["longest_match"], word_count)
                            strategy_stats[strategy_name]["shortest_match"] = min(strategy_stats[strategy_name]["shortest_match"], word_count)
                    
                    all_matches.extend(strategy_matches)
                else:
                    logger.warning(f"Strategy '{strategy_name}' not found in STRATEGY_FUNCTIONS")
            
            if sentence_has_matches:
                sentences_with_matches += 1
                for strategy_name in ALL_STRATEGIES:
                    if strategy_name in STRATEGY_FUNCTIONS and any(match.get("strategy", "") == strategy_name for match in all_matches):
                        strategy_stats[strategy_name]["sentences_with_matches"] += 1

            # Update the starting index for the next sentence
            original_word_index += len(sentence_words_lower)

        logger.info(f"Found {len(all_matches)} raw matches across all strategies for target sum {target_sum}.")

        # Process and deduplicate results
        complete_quotes = []
        incomplete_quotes = []
        seen_quotes_text = set()

        for match in all_matches:
            quote_text = match["text"]  # Use the original case version
            if quote_text not in seen_quotes_text:
                seen_quotes_text.add(quote_text)
                
                # Calculate all sums for this match (using the lowercase text)
                if "text_lower" in match:
                    match['all_sums'] = calculate_all_sums(match["text_lower"])
                else:
                    match['all_sums'] = calculate_all_sums(quote_text.lower())
                
                # Add the search strategy to the output
                strategy_name = match.get('strategy', 'unknown')
                    
                # Classify based on completeness
                if match.get('is_complete_sentence', False):
                    # Log complete sentence finds (these are more interesting)
                    logger.info(f"Found complete sentence match using '{strategy_name}' strategy: '{quote_text}'")
                    complete_quotes.append(match)
                else:
                    incomplete_quotes.append(match)
        
        # Calculate average match length for each strategy
        for strategy_name in ALL_STRATEGIES:
            total_matches = strategy_stats[strategy_name]["total_matches"]
            if total_matches > 0:
                total_words = sum(count * word_count for word_count, count in strategy_stats[strategy_name]["word_count_distribution"].items())
                strategy_stats[strategy_name]["avg_match_length"] = round(total_words / total_matches, 2)
            # Handle case where no matches were found
            if strategy_stats[strategy_name]["shortest_match"] == float('inf'):
                strategy_stats[strategy_name]["shortest_match"] = 0
                
        # Calculate overall statistics
        overall_stats = {
            "total_sentences": sentences_analyzed,
            "sentences_with_matches": sentences_with_matches,
            "match_rate": round(sentences_with_matches / sentences_analyzed * 100, 2) if sentences_analyzed > 0 else 0,
            "total_raw_matches": len(all_matches),
            "unique_complete_quotes": len(complete_quotes),
            "unique_incomplete_quotes": len(incomplete_quotes),
            "total_unique_quotes": len(complete_quotes) + len(incomplete_quotes)
        }
        
        logger.info(f"Found {len(complete_quotes)} unique complete quotes and {len(incomplete_quotes)} unique incomplete quotes after deduplication.")
        
        return {
            "success": True,
            "complete_quotes": complete_quotes,
            "incomplete_quotes": incomplete_quotes,
            "text_length": original_word_index,
            "calculation_type": calculation_type,
            "source_type": source_type,
            "advanced_analytics": {
                "overall": overall_stats,
                "strategies": strategy_stats
            }
        }
        
    except Exception as e:
        logger.exception(f"Error in find_matching_quotes: {str(e)}") # Log full traceback
        return {
            "success": False,
            "error": f"An internal error occurred during search: {str(e)}"
        } 
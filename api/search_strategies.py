import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

# Define calculation dictionaries (or import them if they remain in index.py)
# For now, let's assume they might be passed or redefined here if needed.
# We'll need access to the main value_dict and calculate_all_sums

# Placeholder for calculate_all_sums - this should ideally be shared or imported
def calculate_all_sums(text, value_dicts):
    # This needs to be implemented based on the main index.py logic
    # or passed as an argument/imported.
    # For now, return an empty dict.
    # logger.warning("calculate_all_sums needs proper implementation/import in search_strategies.py")
    return {}


def search_sliding_window(
    sentence_words: List[str],      # Lowercase words for calculation
    sentence_word_sums: List[int],  # Pre-calculated sums for words
    target_sum: int,
    value_dict: Dict,
    url: str,
    sentence_start_index: int,
    original_sentence_words: List[str] = None  # Original case words for display
) -> List[Dict[str, Any]]:
    """
    Finds matching quotes using a sliding window approach within a single sentence.
    Checks all possible sub-sequences within the sentence.

    Args:
        sentence_words: List of words in lowercase for calculation.
        sentence_word_sums: List of pre-calculated sums for words.
        target_sum: The target gematria sum.
        value_dict: The dictionary used for sum calculation (e.g., EQ_DICT).
        url: Source URL (for result metadata).
        sentence_start_index: The index of the first word of this sentence in the original full text word list.
        original_sentence_words: List of words with original case for display (if None, sentence_words is used).

    Returns:
        A list of dictionaries, each representing a found quote match.
    """
    matches = []
    max_window_size = 20  # Keep the window limit reasonable
    num_words = len(sentence_words)

    # If original case words not provided, use the calculation words
    if original_sentence_words is None:
        original_sentence_words = sentence_words

    if num_words == 0:
        return []

    for i in range(num_words):
        current_sum = 0
        for j in range(i, min(i + max_window_size, num_words)):
            current_sum += sentence_word_sums[j]
            
            if current_sum == target_sum:
                # Use original casing for display
                current_words_slice = original_sentence_words[i:j+1]
                quote_text = " ".join(current_words_slice)
                
                # Lowercase version for any additional processing
                current_words_slice_lower = sentence_words[i:j+1]
                quote_text_lower = " ".join(current_words_slice_lower)
                
                all_sums_data = calculate_all_sums(quote_text_lower, {})

                # Determine if complete based on sentence boundaries
                is_complete_sentence = (j == num_words - 1)

                quote_data = {
                    "text": quote_text,  # Original case
                    "text_lower": quote_text_lower,  # Lowercase (if needed)
                    "sum": target_sum,
                    "url": url,
                    "start_idx": sentence_start_index + i,
                    "end_idx": sentence_start_index + j,
                    "all_sums": all_sums_data,
                    "word_sums": sentence_word_sums[i:j+1],
                    "is_complete_sentence": is_complete_sentence,
                    "strategy": "sliding_window"
                }
                matches.append(quote_data)
                
            elif current_sum > target_sum:
                break
                
    return matches

def search_sentence_prefix(
    sentence_words: List[str],      # Lowercase words for calculation  
    sentence_word_sums: List[int],  # Pre-calculated sums for words
    target_sum: int,
    value_dict: Dict,
    url: str,
    sentence_start_index: int,
    original_sentence_words: List[str] = None  # Original case words for display
) -> List[Dict[str, Any]]:
    """
    Finds matching quotes by checking only prefixes of the sentence (starting from the first word).

    Args:
        sentence_words: List of words in lowercase for calculation.
        sentence_word_sums: List of pre-calculated sums for words.
        target_sum: The target gematria sum.
        value_dict: The dictionary used for sum calculation (e.g., EQ_DICT).
        url: Source URL (for result metadata).
        sentence_start_index: The index of the first word of this sentence in the original full text word list.
        original_sentence_words: List of words with original case for display (if None, sentence_words is used).

    Returns:
        A list of dictionaries, each representing a found quote match.
    """
    matches = []
    num_words = len(sentence_words)
    current_sum = 0

    # If original case words not provided, use the calculation words
    if original_sentence_words is None:
        original_sentence_words = sentence_words

    if num_words == 0:
        return []

    for j in range(num_words):
        current_sum += sentence_word_sums[j]
        
        if current_sum == target_sum:
            # Use original casing for display
            current_words_slice = original_sentence_words[0:j+1]
            quote_text = " ".join(current_words_slice)
            
            # Lowercase version for any additional processing
            current_words_slice_lower = sentence_words[0:j+1]
            quote_text_lower = " ".join(current_words_slice_lower)
            
            all_sums_data = calculate_all_sums(quote_text_lower, {})

            # A prefix match is complete ONLY if it uses the entire sentence
            is_complete_sentence = (j == num_words - 1)

            quote_data = {
                "text": quote_text,  # Original case
                "text_lower": quote_text_lower,  # Lowercase (if needed)
                "sum": target_sum,
                "url": url,
                "start_idx": sentence_start_index,
                "end_idx": sentence_start_index + j,
                "all_sums": all_sums_data,
                "word_sums": sentence_word_sums[0:j+1],
                "is_complete_sentence": is_complete_sentence,
                "strategy": "sentence_prefix"
            }
            matches.append(quote_data)
            
        elif current_sum > target_sum:
            break
            
    return matches 
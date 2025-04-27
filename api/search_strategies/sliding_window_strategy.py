import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

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
    Checks all possible sub-sequences within the sentence with optimized performance.

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

    # Strategy name for result identification
    STRATEGY_NAME = "sliding_window"
    
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

                # Determine if complete based on sentence boundaries
                is_complete_sentence = (i == 0 and j == num_words - 1)

                quote_data = {
                    "text": quote_text,  # Original case
                    "text_lower": quote_text_lower,  # Lowercase (if needed)
                    "sum": target_sum,
                    "url": url,
                    "start_idx": sentence_start_index + i,
                    "end_idx": sentence_start_index + j,
                    "word_sums": sentence_word_sums[i:j+1],
                    "is_complete_sentence": is_complete_sentence,
                    "strategy": STRATEGY_NAME,
                    "strategy_description": "Optimized sliding window search"
                }
                matches.append(quote_data)
                
            elif current_sum > target_sum:
                # Early termination optimization - if we've already exceeded the target sum, 
                # adding more words won't help
                break
                
    return matches 
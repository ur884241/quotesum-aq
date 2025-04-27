import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

def search_sentence_infix(
    sentence_words: List[str],
    sentence_word_sums: List[int],
    target_sum: int,
    value_dict: Dict,
    url: str,
    sentence_start_index: int,
    original_sentence_words: List[str] = None
) -> List[Dict[str, Any]]:
    """
    Finds matching quotes by checking all possible substrings (infixes) of a sentence.
    
    Args:
        sentence_words: List of words in lowercase for calculation.
        sentence_word_sums: List of pre-calculated sums for words.
        target_sum: The target gematria sum.
        value_dict: The dictionary used for sum calculation.
        url: Source URL (for result metadata).
        sentence_start_index: The index of the first word of this sentence in the original full text.
        original_sentence_words: List of words with original case for display (if None, sentence_words is used).

    Returns:
        A list of dictionaries, each representing a found quote match.
    """
    matches = []
    num_words = len(sentence_words)
    
    # Strategy name for result identification
    STRATEGY_NAME = "sentence_infix"
    
    # If original case words not provided, use the calculation words
    if original_sentence_words is None:
        original_sentence_words = sentence_words
    
    if num_words == 0:
        return []
    
    # Check all possible substrings of the sentence
    for start in range(num_words):
        current_sum = 0
        for end in range(start, num_words):
            current_sum += sentence_word_sums[end]
            
            # Check if we've found a match
            if current_sum == target_sum:
                # Use original casing for display
                current_words_slice = original_sentence_words[start:end+1]
                quote_text = " ".join(current_words_slice)
                
                # Lowercase version for additional processing
                current_words_slice_lower = sentence_words[start:end+1]
                quote_text_lower = " ".join(current_words_slice_lower)
                
                # An infix is a complete sentence only if it's the entire sentence
                is_complete_sentence = (start == 0 and end == num_words - 1)
                
                quote_data = {
                    "text": quote_text,
                    "text_lower": quote_text_lower,
                    "sum": target_sum,
                    "url": url,
                    "start_idx": sentence_start_index + start,
                    "end_idx": sentence_start_index + end,
                    "word_sums": sentence_word_sums[start:end+1],
                    "is_complete_sentence": is_complete_sentence,
                    "strategy": STRATEGY_NAME,
                    "strategy_description": "Substring within sentence"
                }
                matches.append(quote_data)
    
    return matches 
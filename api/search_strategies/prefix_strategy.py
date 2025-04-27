import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

def search_sentence_prefix(
    sentence_words: List[str],       # Lowercase words for calculation  
    sentence_word_sums: List[int],   # Pre-calculated sums for words
    target_sum: int,
    value_dict: Dict,
    url: str,
    sentence_start_index: int,
    original_sentence_words: List[str] = None  # Original case words for display
) -> List[Dict[str, Any]]:
    """
    Finds matching quotes by checking all possible prefixes of a sentence.
    A prefix is a continuous sequence of words that starts the sentence.
    
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
    STRATEGY_NAME = "prefix"
    
    # If original case words not provided, use the calculation words
    if original_sentence_words is None:
        original_sentence_words = sentence_words
    
    if num_words == 0:
        return []
    
    # Calculate forward cumulative sums
    # cum_sums[i] represents the sum of words from position 0 to i-1
    cum_sums = [0] * (num_words + 1)
    for i in range(num_words):
        cum_sums[i + 1] = cum_sums[i] + sentence_word_sums[i]
    
    # Check all possible prefixes (first words of the sentence)
    for end in range(1, num_words + 1):  # end is exclusive, so we go up to num_words+1
        # Current prefix sum is directly available in our cumulative sums
        current_sum = cum_sums[end] - cum_sums[0]  # Sum from 0 to end-1
        
        # Check if we've found a match
        if current_sum == target_sum:
            # Use original casing for display
            current_words_slice = original_sentence_words[:end]
            quote_text = " ".join(current_words_slice)
            
            # Lowercase version for additional processing
            current_words_slice_lower = sentence_words[:end]
            quote_text_lower = " ".join(current_words_slice_lower)
            
            # A prefix is a complete sentence only if it ends at the end of the sentence
            is_complete_sentence = (end == num_words)
            
            quote_data = {
                "text": quote_text,
                "text_lower": quote_text_lower,
                "sum": target_sum,
                "url": url,
                "start_idx": sentence_start_index,
                "end_idx": sentence_start_index + end - 1,
                "word_sums": sentence_word_sums[:end],
                "is_complete_sentence": is_complete_sentence,
                "strategy": STRATEGY_NAME,
                "strategy_description": "Prefix of sentence (beginning words)"
            }
            matches.append(quote_data)
    
    return matches 
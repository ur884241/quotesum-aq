from api.search_strategies.prefix_strategy import search_sentence_prefix
from api.search_strategies.suffix_strategy import search_sentence_suffix
from api.search_strategies.subsequence_strategy import search_sentence_subsequence
from api.search_strategies.sliding_window_strategy import search_sliding_window

# Dictionary mapping strategy names to their functions
STRATEGY_FUNCTIONS = {
    "prefix": search_sentence_prefix,
    "suffix": search_sentence_suffix,
    "subsequence": search_sentence_subsequence,
    "sliding_window": search_sliding_window,
}

# List of all available strategies
ALL_STRATEGIES = list(STRATEGY_FUNCTIONS.keys())

__all__ = [
    'search_sentence_prefix', 
    'search_sentence_suffix', 
    'search_sentence_subsequence',
    'search_sliding_window',
    'STRATEGY_FUNCTIONS',
    'ALL_STRATEGIES'
] 
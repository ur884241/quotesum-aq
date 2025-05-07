# This file marks the api directory as a Python package
from api.core import fetch_text, find_matching_quotes
from api.search_strategies import STRATEGY_FUNCTIONS, ALL_STRATEGIES

__all__ = ['fetch_text', 'find_matching_quotes', 'STRATEGY_FUNCTIONS', 'ALL_STRATEGIES']

 
# This file marks the api directory as a Python package
from .core import fetch_text
from .index import find_matching_quotes

__all__ = ['find_matching_quotes', 'fetch_text'] 
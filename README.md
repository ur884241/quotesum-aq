# Sigil Gematria Quote Finder

A web application that finds quotes in text content matching a specific gematria sum value. The application supports multiple search strategies and calculation methods.

## Features

- Search for quotes in text content from URLs or uploaded text files
- Multiple search strategies:
  - Prefix search (beginning of sentences)
  - Suffix search (end of sentences)
  - Subsequence search (any continuous part of sentences)
- Multiple calculation methods:
  - English Qabbalah (A=1, B=2, etc.)
  - Reverse (Z=1, Y=2, etc.)
  - Jewish Gematria
  - Simple Gematria (A=1, B=2, ..., I=9, J=1, K=2, etc.)
- Visual representation with ASCII art and animated title

## Setup

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd quotesum-aq
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

### Running the Application

1. Start the Flask server:
   ```
   python app.py
   ```

2. Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

## Usage

1. Enter a target sum value in the "Target Sum" field
2. Select a calculation method from the dropdown
3. Choose your text source:
   - Enter a URL in the URL field
   - Upload a .txt file
4. Click "Invoke" to search for matching quotes
5. View results, which will be categorized as:
   - Complete quotes (full sentences)
   - Incomplete quotes (parts of sentences)

## Search Strategies

The application employs three main search strategies:

1. **Prefix Strategy**: Finds quotes that start at the beginning of a sentence
2. **Suffix Strategy**: Finds quotes that end at the end of a sentence
3. **Subsequence Strategy**: Finds any continuous sequence of words within a sentence

## Development

### Project Structure

```
quotesum-aq/
├── api/
│   ├── search_strategies/
│   │   ├── __init__.py
│   │   ├── prefix_strategy.py
│   │   ├── suffix_strategy.py
│   │   └── subsequence_strategy.py
│   ├── __init__.py
│   └── index.py
├── static/
│   ├── home.js
│   ├── script.js
│   └── styles.css
├── app.py
├── index.html
└── requirements.txt
```

### Adding New Search Strategies

To add a new search strategy:

1. Create a new file in the `api/search_strategies/` directory
2. Implement a function that follows the signature pattern of existing strategies
3. Add the function to the `STRATEGY_FUNCTIONS` dictionary in `api/search_strategies/__init__.py`

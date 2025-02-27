# Tesla Earnings Analyzer

A LangGraph-based system for analyzing Tesla earnings reports. This project extracts information from PDF earnings reports, embeds the content into Redis, analyzes the data, and generates a structured Markdown report.

## Features

- PDF text extraction and chunking
- Vector embedding using HuggingFace models
- Semantic search capabilities
- LLM-powered analysis using Claude 3.7 Sonnet
- Markdown report generation

## Installation

1. Clone this repository
2. Install dependencies using UV:

```bash
uv pip install -r requirements.txt
```

3. Create a `.env` file based on `.env.example` and add your API keys

## Usage

```bash
python main.py --pdf_path path/to/tesla/earnings.pdf
```

## Project Structure

- `agents/`: Contains agent implementations for each step of the workflow
- `main.py`: Entry point for the application
- `config.py`: Configuration settings

## Requirements

- Python 3.9+
- Redis server
- Anthropic API key
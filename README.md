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

WARNING - using Huggingface embeddings (large install)

```bash
uv sync
```

3. Create a `.env` file based on `.env.example` and add your Claude API keys

4. Add file `tsla-20240331-gen.py` to the /data directory or rename in the config.py to your file name.

5. Run

## Usage

```bash
uv run reporter
```

## Project Structure

- `agents/`: Contains agent implementations for each step of the workflow
- `utils/` : Contains PDF chunking and embedding operations, configure in the config.py
- `main.py`: Entry point for the application
- `config.py`: Configuration settings

## Requirements

- Python 3.12+
- Redis server
- Anthropic API key
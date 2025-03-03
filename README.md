# Tesla Earnings Analyzer

A LangGraph-based system for analyzing Tesla earnings reports. This project extracts information from PDF earnings reports, embeds the content into Redis vector store, analyzes the data, and generates a structured Markdown report.

## Features

- PDF text extraction and chunking
- Multi-agent
- Vector embedding using Ollama Models
- Semantic search capabilities
- LLM-powered analysis using Claude 3.7 Sonnet
- Markdown report generation

## Installation

1. Clone this repository
2. Install dependencies using UV:
3. Run Ollama locally for embeddings, select embedding model
4. Run Redis-stack locally or update config to cloud

```bash
uv sync
```

3. Create a `.env` file based on `.env.example` and add your Claude API keys

4. Add financial pdf files to `/data` directory.

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
- Ollama
- Anthropic API key
"""Configuration settings for the Tesla Earnings Analyzer."""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
if not ANTHROPIC_API_KEY:
    raise ValueError("ANTHROPIC_API_KEY environment variable not set")

# Vector Store Settings
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:10001")
REDIS_INDEX_NAME = os.getenv("REDIS_INDEX_NAME", "tsla_earnings")

# File Paths
PDF_PATH = os.getenv("PDF_PATH", "data/tsla-20240331-gen.pdf")
OUTPUT_PATH = os.getenv("OUTPUT_PATH", "tesla_earnings_analysis.md")
GRAPH_PATH = os.getenv("GRAPH_PATH", "output/workflow/workflow_graph.png")

# Model Settings
CLAUDE_MODEL = "claude-3-7-sonnet-latest"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Document Processing
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 100
RETRIEVAL_K = 3

# Analysis Queries
QUESTION_COUNT = 5

# Report Section Template
REPORT_TEMPLATE = """
# Tesla Earnings Report Summary

## Financial Highlights

## Performance Analysis

## Growth Metrics

## Challenges and Risks

## Future Outlook

## Conclusion
"""
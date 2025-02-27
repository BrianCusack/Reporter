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
OUTPUT_PATH = os.getenv("OUTPUT_PATH", "output/tesla_earnings_analysis.md")

# Model Settings
CLAUDE_MODEL = "claude-3-7-sonnet-latest"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Document Processing
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 100
RETRIEVAL_K = 3

# Analysis Queries
ANALYSIS_QUERIES = [
    "What were Tesla's total revenue and profit for the reported period?",
    "What are the main highlights from the earnings report?",
    "How did Tesla perform compared to previous quarters?",
    "What are the key growth metrics mentioned in the report?",
    "What challenges or risks were mentioned in the report?",
    "What is Tesla's outlook or guidance for future quarters?"
]

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
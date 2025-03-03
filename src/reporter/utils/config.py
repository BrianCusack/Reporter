"""Configuration settings for the Tesla Earnings Analyzer using Pydantic."""

from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator

class Settings(BaseSettings):
    # API Keys
    ANTHROPIC_API_KEY: str

    # LangChain Settings
    LANGCHAIN_TRACING_V2: str = "false"
    LANGCHAIN_ENDPOINT: str = "https://api.smith.langchain.com"
    LANGCHAIN_API_KEY: Optional[str] = None
    LANGCHAIN_PROJECT: str = "pdf-reporter"
    LANGCHAIN_CALLBACKS_BACKGROUND: str = "true"

    # Vector Store Settings
    REDIS_URL: str = "redis://localhost:10001"
    REDIS_INDEX_NAME: str = "tsla_earnings"

    # File Paths
    PDF_PATH: Path = Path("data/")
    OUTPUT_PATH: Path = Path("tesla_earnings_analysis.md")
    GRAPH_PATH: Path = Path("output/workflow/workflow_graph.png")

    # Model Settings
    CLAUDE_MODEL: str = "claude-3-7-sonnet-latest"
    EMBEDDING_MODEL: str = "nomic-embed-text"
    OLLAMA_BASE_URL: Optional[str] = None

    # Document Processing
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 100
    RETRIEVAL_K: int = 3

    # Analysis Settings
    QUESTION_COUNT: int = 10

    # Template Settings
    TEMPLATE_PATH: Path = Path(__file__).parent.parent / "agents" / "template.yml"

    @field_validator("PDF_PATH", "OUTPUT_PATH", "GRAPH_PATH")
    @classmethod
    def create_directories(cls, v: Path) -> Path:
        v.parent.mkdir(parents=True, exist_ok=True)
        return v

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )

# Create a single instance to be used throughout the application
settings = Settings()

# Export the instance
__all__ = ['settings']
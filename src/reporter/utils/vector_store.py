"""Vector Store Agent for the Tesla Earnings Analyzer."""

from typing import Dict, Any
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_redis import RedisConfig, RedisVectorStore
import redis
import reporter.utils.config as config
from reporter.utils.logging import setup_logger

logger = setup_logger(__name__)

def vector_store_agent(chunks: Dict[str, Any]) -> None:
    """
    Embedding and storing chunks in a Redis vector store.
    """

    try:

        logger.info(f"Embedding {len(chunks)} chunks into Redis")
        
        # Initialize Redis connection for index management
        redis_client = redis.from_url(config.REDIS_URL)
        
        # Delete existing index if it exists
        try:
            redis_client.ft("tsla_earnings").dropindex(delete_documents=True)
            logger.info("Dropped existing index and documents")
        except:
            logger.info("No existing index found")
        
        embeddings = HuggingFaceEmbeddings(
            model_name=config.EMBEDDING_MODEL
        )
        
        redis_config = RedisConfig(
            index_name="tsla_earnings",
            redis_url=config.REDIS_URL,
            overwrite=True  # This will handle index dropping and recreation
        )
        
        redis_store = RedisVectorStore(embeddings, redis_config)
        
        # Add chunks to Redis store
        texts = [chunk.page_content for chunk in chunks]
        metadatas = [getattr(chunk, 'metadata', {}) for chunk in chunks]
        redis_store.add_texts(texts=texts, metadatas=metadatas)
        
        logger.info(f"Successfully embedded {len(texts)} chunks into fresh Redis index")

    except Exception as e:
        error_msg = f"Error loading embeddings: {str(e)}"
        logger.error(error_msg)
        
def check_redis_vectorstore_exists() -> bool:
    """
    Check if the Redis vector store exists.
    """
    try:
        redis_client = redis.from_url(config.REDIS_URL)
        info = redis_client.ft("tsla_earnings").info()
        if info.get('num_records') > 0:
            return True
        else:
            logger.error("No records found")
            return False
    except Exception as e:
        error_msg = f"Error checking Redis index: {str(e)}"
        logger.error(error_msg)
        return False
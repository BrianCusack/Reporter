"""Analysis Agent for the Tesla Earnings Analyzer."""

from typing import Dict, Any
from langchain_redis import RedisVectorStore

from langchain_anthropic import ChatAnthropic
from langchain_huggingface import HuggingFaceEmbeddings
import reporter.utils.config as config
from reporter.utils.logging import setup_logger

logger = setup_logger(__name__)

def analysis_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Agent that analyzes the embedded document by querying the vector store.
    
    Args:
        state: Current state with embedded status
        
    Returns:
        Updated state with analysis results or error
    """
    # Initialize return state with existing values
    return_state = {**state}
    
    try:
        logger.info("Initializing analysis agent...")
        
        # Initialize LLM
        llm = ChatAnthropic(
            model=config.CLAUDE_MODEL,
            temperature=0,
            api_key=config.ANTHROPIC_API_KEY
        )
        logger.info("LLM initialized successfully")
        
        # Connect to existing Redis index with HuggingFace embeddings
        logger.info("Connecting to Redis vector store...")
        embeddings = HuggingFaceEmbeddings(
            model_name=config.EMBEDDING_MODEL
        )

        redis_store = RedisVectorStore(
            redis_url=config.REDIS_URL,
            index_name=config.REDIS_INDEX_NAME,
            embeddings=embeddings
        )
        logger.info("Redis connection established")
        
        # Perform semantic search and analysis for each query
        logger.info("Beginning analysis of queries...")
        analysis_results = {}
        questions = state.get("questions", [])
        for query in questions:
            logger.info(f"Processing query: {query}...")
            # Get relevant chunks
            docs = redis_store.similarity_search(query, k=config.RETRIEVAL_K)
            logger.info(f"Retrieved {len(docs)} relevant results")
            context = "\n\n".join([doc.page_content for doc in docs])
            
            # Use Claude to analyze the relevant chunks
            response = llm.invoke(
                f"""Based on the following excerpts from Tesla's earnings report, answer this question: 
                
                Question: {query}
                
                Excerpts:
                {context}
                
                Provide a concise, factual answer based only on the information in these excerpts.
                """
            )
            logger.info("Analysis complete for query")
            
            # Store result
            analysis_results[query] = response.content
        
        logger.info("Analysis completed successfully")
        return_state.update({
            "analysis": analysis_results
            })
        
    except Exception as e:
        logger.error(f"Error during analysis: {str(e)}")
        return_state.update({
            "error": f"Error during analysis: {str(e)}"
        })
    
    return return_state
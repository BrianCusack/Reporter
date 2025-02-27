"""PDF Loader Agent for the Tesla Earnings Analyzer."""

from typing import Dict, Any

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

import reporter.utils.config as config
from reporter.utils.logging import setup_logger

logger = setup_logger(__name__)

def pdf_loader_tool(path: str) -> Dict[str, Any]:
    """
    Loader for splitting PDF documents.
    
    Args:
        pdf file path
        
    Returns:
        Updated state with document chunks or error
    """
    try:
        logger.info(f"Loading PDF: {path}")
        
        # Load PDF
        loader = PyPDFLoader(path)
        documents = loader.load()
        
        # Split documents into chunks
        logger.info(f"Splitting {len(documents)} pages into chunks")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.CHUNK_SIZE,
            chunk_overlap=config.CHUNK_OVERLAP
        )
        chunks = text_splitter.split_documents(documents)
        logger.info(f"Split {len(chunks)} chunks")
        
        # Update state with chunks
        return  chunks
    except Exception as e:
        logger.error(f"Error loading PDF: {str(e)}")
        return None

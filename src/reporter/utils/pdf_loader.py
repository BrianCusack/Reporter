"""PDF Loader Agent for the Tesla Earnings Analyzer."""

from typing import List
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema import Document

from reporter.utils.config import settings as config
from utils.log_setup import setup_logger

logger = setup_logger(__name__)


def load_pdfs_from_directory(directory: str) -> List[Document]:
    """
    Load all PDFs from a directory and split them into chunks.

    Args:
        directory: Path to directory containing PDFs

    Returns:
        List of document chunks from all PDFs
    """
    try:
        all_chunks = []
        pdf_files = Path(directory).glob("*.pdf")

        for pdf_path in pdf_files:
            logger.info(f"Processing PDF: {pdf_path}")
            chunks = pdf_loader_tool(str(pdf_path))
            if chunks:
                all_chunks.extend(chunks)
                logger.info(f"Added {len(chunks)} chunks from {pdf_path.name}")
            else:
                logger.warning(f"Failed to process {pdf_path.name}")

        logger.info(f"Total chunks processed: {len(all_chunks)}")
        return all_chunks

    except Exception as e:
        logger.error(f"Error processing PDFs in directory: {str(e)}")
        return []


def pdf_loader_tool(path: str) -> List[Document]:
    """
    Load and chunk a single PDF document.

    Args:
        path: Path to PDF file

    Returns:
        List of document chunks
    """
    try:
        logger.info(f"Loading PDF: {path}")

        # Load PDF
        loader = PyPDFLoader(path)
        documents = loader.load()

        # Split documents into chunks
        logger.info(f"Splitting {len(documents)} pages into chunks")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.CHUNK_SIZE, chunk_overlap=config.CHUNK_OVERLAP
        )
        chunks = text_splitter.split_documents(documents)
        logger.info(f"Split {len(chunks)} chunks")

        return chunks
    except Exception as e:
        logger.error(f"Error loading PDF: {str(e)}")
        return []

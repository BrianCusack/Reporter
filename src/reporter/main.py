"""Main entry point for the Tesla Earnings Analyzer."""

import os
import sys
from datetime import datetime
import reporter.utils.config as config
from reporter.utils.logging import setup_logger
from reporter.utils.pdf_loader import pdf_loader_tool
from reporter.utils.vector_store import vector_store_agent, check_redis_vectorstore_exists
from reporter.graph import create_workflow

from langchain_core.runnables.graph import MermaidDrawMethod


logger = setup_logger(__name__)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
base_path = os.path.dirname(os.path.abspath(__file__))
pdf_path=os.path.join(base_path, config.PDF_PATH)
output_path=os.path.join(base_path, f'output/reports/{timestamp}_{config.OUTPUT_PATH}')


def process_earnings_report() -> None:
    """
    Process a Tesla earnings report PDF.
    
    Args:
        pdf_path: Path to the PDF file
        output_path: Path to save the generated report
    """
    if not os.path.exists(pdf_path):
        logger.error(f"PDF file not found at: {config.PDF_PATH}")
        sys.exit(1)
        
    logger.info(f"Processing earnings report from: {config.PDF_PATH}")
    
    # get chunks from pdf
    if check_redis_vectorstore_exists():
        logger.info("Redis vector store already exists")
    else:
        logger.info("Creating new Redis vector store")
        pdf_chunks = pdf_loader_tool(pdf_path)
        if not pdf_chunks:
            logger.error("Error loading PDF")
            sys.exit(1)
        vector_store_agent(pdf_chunks)
    
    # Create and compile the workflow
    app = create_workflow()
    
    # Save graph with timestamp
    
    graph_path = os.path.join(base_path, config.GRAPH_PATH)
    
    # Generate and save graph
    graph_png = app.get_graph().draw_mermaid_png(draw_method=MermaidDrawMethod.API)
    with open(graph_path, "wb") as f:
        f.write(graph_png)
    logger.info(f"Workflow graph saved to: {graph_path}")
    
    # Initialize state
    initial_state = {"pdf_path": pdf_path, "output_path": output_path}
    
    # Execute the graph
    for event in app.stream(initial_state):
        if "error" in event and event["error"]:
            logger.error(f"Error: {event['error']}")

if __name__ == "__main__":
    
    # Process the report
    process_earnings_report()
"""Main entry point for the Tesla Earnings Analyzer."""

import os
import sys
from typing import TypedDict, List, Dict, Any

from langgraph.graph import StateGraph, END
import reporter.config as config
from reporter.utils.logging import setup_logger
from reporter.utils.pdf_loader import pdf_loader_tool
from reporter.utils.vector_store import vector_store_agent

logger = setup_logger(__name__)

from reporter.agents import (
    analysis_agent as analyzer, 
    report_generator_tool as report_generator
    )

# Type definitions for our state
class AgentState(TypedDict):
    pdf_path: str
    output_path: str
    analysis: Dict[str, Any]
    report: str
    error: str

def create_workflow() -> StateGraph:
    """
    Create the workflow graph for processing Tesla earnings reports.
    
    Returns:
        Compiled StateGraph workflow
    """
    # Define the workflow graph
    workflow = StateGraph(AgentState)

    # Add nodes
    workflow.add_node("analyzer", analyzer)
    workflow.add_node("report_generator", report_generator)

    # Define edges
    workflow.set_entry_point("analyzer")
    workflow.add_edge("analyzer", "report_generator")
    workflow.add_edge("report_generator", END)

    workflow.add_conditional_edges(
        "analyzer",
        lambda state: "error" if "error" in state and state["error"] else "report_generator"
    )
    
    # Compile the graph
    return workflow.compile()

def process_earnings_report() -> None:
    """
    Process a Tesla earnings report PDF.
    
    Args:
        pdf_path: Path to the PDF file
        output_path: Path to save the generated report
    """
    
    base_path = os.path.dirname(os.path.abspath(__file__))
    pdf_path=os.path.join(base_path, config.PDF_PATH)
    output_path=os.path.join(base_path, config.OUTPUT_PATH)
    
    if not os.path.exists(pdf_path):
        logger.error(f"PDF file not found at: {config.PDF_PATH}")
        sys.exit(1)
        
    logger.info(f"Processing earnings report from: {config.PDF_PATH}")
    
    # get chunks from pdf
    pdf_chunks = pdf_loader_tool(pdf_path)
    if not pdf_chunks:
        logger.error("Error loading PDF")
        sys.exit(1)
    vector_store_agent(pdf_chunks)
    
    # Create and compile the workflow
    app = create_workflow()
    
    # Initialize state
    initial_state = {"pdf_path": pdf_path, "output_path": output_path}
    
    # Execute the graph
    for event in app.stream(initial_state):
        if "error" in event and event["error"]:
            logger.error(f"Error: {event['error']}")

if __name__ == "__main__":
    
    # Process the report
    process_earnings_report()
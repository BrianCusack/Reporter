"""Report Generator Agent for the Tesla Earnings Analyzer."""

from datetime import datetime
from typing import Dict, Any
import json
import os

from langchain_anthropic import ChatAnthropic

import reporter.utils.config as config
from reporter.utils.logging import setup_logger

logger = setup_logger(__name__)

def report_generator_tool(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Agent that generates the final markdown report.
    
    Args:
        state: Current state with analysis results
        
    Returns:
        Updated state with generated report or error
    """
    return_state = {**state}
    try:
        analysis = state["analysis"]
        output_path = state.get("output_path")
        
        # Initialize LLM
        llm = ChatAnthropic(
            model=config.CLAUDE_MODEL,
            temperature=0,
            anthropic_api_key=config.ANTHROPIC_API_KEY
        )
        logger.info("LLM initialized successfully")
        # Prompt for generating the report
        report_prompt = f"""
        You are a financial analyst creating a summary report of Tesla's earnings.
        Using the analysis below, create a well-structured markdown report following this format:
        {config.REPORT_TEMPLATE}
        
        Here's the analysis to use:
        {json.dumps(analysis, indent=2)}
        
        Create a professional, concise report with appropriate headers and bullet points where relevant.
        Only include information that is explicitly mentioned in the analysis.
        """
        
        # Generate report using Claude
        logger.info("Invoking LLM for report generation...")
        response = llm.invoke(report_prompt)
        report = response.content
        
        # Make sure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Save report to file
        with open(output_path, "w") as f:
            f.write(report)
        
        logger.info(f"Report saved to {config.OUTPUT_PATH}")
        
        return_state.update({
            "report": report
        })
    except Exception as e:
        logger.error(f"Error generating report: {str(e)}")
        return_state.update({
            "error": f"Error generating report: {str(e)}"
        })
    return return_state
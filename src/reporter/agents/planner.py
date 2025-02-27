"""Plan the questions needed to fill the report"""

from datetime import datetime
from typing import Dict, Any
import ast
import re
import os

from langchain_anthropic import ChatAnthropic
import reporter.utils.config as config
from reporter.utils.logging import setup_logger

logger = setup_logger(__name__)

def parse_questions(response: str) -> list[str]:
    """Parse questions from LLM response and validate"""
    # Try to find a Python list in the response using regex
    list_match = re.search(r'\[(.*?)\]', response.replace('\n', ' '), re.DOTALL)
    if not list_match:
        raise ValueError("No list found in response")
    
    try:
        # Safely evaluate the list string
        questions = ast.literal_eval(list_match.group(0))
        if not isinstance(questions, list) or not all(isinstance(q, str) for q in questions):
            raise ValueError("Invalid questions format")
        return questions
    except (SyntaxError, ValueError) as e:
        raise ValueError(f"Failed to parse questions: {str(e)}")
    
def to_file(questions: list[str], filename: str) -> None:
    """Write questions to a file"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{filename}"
    base_path = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(base_path.replace('/agents','/output/questions'), filename)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w") as f:
        f.write("\n".join(questions))
    logger.info(f"Questions written to: {filepath}")

def planner_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Agent that plans the questions needed to fill the report.
    
    Args:
        state: Current state with embedded status
        
    Returns:
        Updated state with planned list of questions or error
    """
    # Initialize return state with existing values
    return_state = {**state}
    
    try:
        logger.info("Initializing planner agent...")
        
        # Initialize LLM
        llm = ChatAnthropic(
            model=config.CLAUDE_MODEL,
            temperature=0,
            api_key=config.ANTHROPIC_API_KEY
        )
        logger.info("LLM initialized successfully")
        
        # Plan questions for the report
        logger.info("Planning questions for the report...")
        template = config.REPORT_TEMPLATE
        prompt = f"""Generate a list of {config.QUESTION_COUNT}x relevant questions based on this report structure.
            Format your response as a Python list of strings. Example: ["Question 1?", "Question 2?"]

            Report structure:
            {template}

            Questions:"""
            
        response = llm.invoke(prompt)
        questions = parse_questions(response.content)
        
        # Write questions to a file
        to_file(questions, "questions.txt")
        
        if not questions:
            raise ValueError("No questions were generated")
            
        return_state["questions"] = questions
        logger.info(f"Successfully planned {len(questions)} questions")
        
    except Exception as e:
        error_msg = f"Error planning questions: {str(e)}"
        logger.error(error_msg)
        return_state["error"] = error_msg
    
    return return_state
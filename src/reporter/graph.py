from typing import TypedDict, Dict, Any
from langgraph.graph import StateGraph, END

from reporter.agents import (
    analysis_agent as analyzer,
    report_generator_tool as report_generator,
    planner_agent as planner,
)


# Type definitions for our state
class AgentState(TypedDict):
    pdf_path: str
    output_path: str
    questions: list
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
    workflow.add_node("planner", planner)
    workflow.add_node("analyzer", analyzer)
    workflow.add_node("report_generator", report_generator)

    # Define edges
    workflow.set_entry_point("planner")
    workflow.add_edge("planner", "analyzer")
    workflow.add_edge("analyzer", "report_generator")
    workflow.add_edge("report_generator", END)

    workflow.add_conditional_edges(
        "planner",
        lambda state: "error" if "error" in state and state["error"] else "analyzer",
    )

    workflow.add_conditional_edges(
        "analyzer",
        lambda state: "error"
        if "error" in state and state["error"]
        else "report_generator",
    )

    # Compile the graph
    return workflow

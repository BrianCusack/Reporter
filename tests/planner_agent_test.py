# test planner agent structured output as list of strings
from reporter.agents.planner import planner_agent


def test_planner_agent():
    state = {
        "pdf_path": "test.pdf",
        "output_path": "test_output.pdf",
        "questions": [],
        "analysis": {},
        "report": "",
        "error": "",
    }

    updated_state = planner_agent(state)

    assert isinstance(updated_state["questions"], list)
    assert all(isinstance(question, str) for question in updated_state["questions"])
    assert len(updated_state["questions"]) > 0

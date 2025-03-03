import pytest
from unittest.mock import Mock, patch
import time
import numpy as np
import redis
from reporter.agents.planner import planner_agent

# filepath: src/reporter/agents/test_planner.py


@pytest.fixture
def mock_llm_response():
    return """Here are some questions: ["What is the main goal?", "What are the key findings?"]"""

@pytest.fixture
def base_state():
    return {
        "pdf_path": "test.pdf",
        "output_path": "test_output.pdf",
        "questions": [],
        "analysis": {},
        "report": "",
        "error": "",
    }

@pytest.fixture
def mock_llm():
    mock = Mock()
    mock.invoke.return_value = Mock(content="""["What is the main goal?", "What are the key findings?"]""")
    return mock

def test_planner_agent_success(base_state, mock_llm):
    with patch('reporter.agents.planner.ChatAnthropic', return_value=mock_llm):
        with patch('reporter.agents.planner.to_file') as mock_to_file:
            result = planner_agent(base_state)
            
            assert isinstance(result["questions"], list)
            assert len(result["questions"]) == 2
            assert result["questions"][0] == "What is the main goal?"
            assert "error" not in result
            mock_to_file.assert_called_once()

def test_planner_agent_error_handling(base_state, mock_llm):
    mock_llm.invoke.side_effect = Exception("API Error")
    
    with patch('reporter.agents.planner.ChatAnthropic', return_value=mock_llm):
        result = planner_agent(base_state)
        
        assert "error" in result
        assert "API Error" in result["error"]
        assert result["questions"] == []

def test_embedding_performance():
    # Setup connections
    redis_client = redis.Redis(host='localhost', port=6379)
    dragonfly_client = redis.Redis(host='localhost', port=6380)
    
    # Create test data
    dim = 1536  # Common embedding dimension
    num_vectors = 1000
    test_embeddings = np.random.rand(num_vectors, dim).astype(np.float32)
    
    # Test Redis insertion
    redis_start = time.time()
    for i, embedding in enumerate(test_embeddings):
        redis_client.hset(
            f"doc:{i}",
            mapping={
                "embedding": embedding.tobytes(),
                "text": f"Document {i}"
            }
        )
    redis_time = time.time() - redis_start
    
    # Test Dragonfly insertion
    dragonfly_start = time.time()
    for i, embedding in enumerate(test_embeddings):
        dragonfly_client.hset(
            f"doc:{i}",
            mapping={
                "embedding": embedding.tobytes(),
                "text": f"Document {i}"
            }
        )
    dragonfly_time = time.time() - dragonfly_start
    
    print(f"\nPerformance Results:\nRedis insertion time: {redis_time:.2f} seconds\nDragonfly insertion time: {dragonfly_time:.2f} seconds")
    
    # Cleanup
    redis_client.flushall()
    dragonfly_client.flushall()
    
    assert True  # Test passes if it completes
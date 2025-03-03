from reporter.utils.vector_store import (
    vector_store_agent,
    check_redis_vectorstore_exists,
)
# test vector_store.py functions


def test_vector_store_agent():
    chunks = {
        "page_content": "This is a test page content",
        "metadata": {"test": "metadata"},
    }
    vector_store_agent(chunks)
    assert True


def test_check_redis_vectorstore_exists():
    check_redis_vectorstore_exists()
    assert True

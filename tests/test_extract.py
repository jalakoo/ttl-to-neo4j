import pytest
from rdflib import Namespace
from extract import extract_prefixes_from_ttl


@pytest.fixture
def test_ttl_content():
    return """
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix owl: <http://www.w3.org/2002/07/owl#> .
    @prefix test: <http://test.org/> .
    """


def test_extract_prefixes_from_ttl(test_ttl_content, requests_mock):
    # Setup mock response
    test_url = "http://example.com/test.ttl"
    requests_mock.get(test_url, text=test_ttl_content, status_code=200)

    # Execute function
    result = extract_prefixes_from_ttl(test_url)

    # Verify results
    assert isinstance(result, dict)
    assert len(result) == 3
    assert "rdf" in result
    assert "owl" in result
    assert "test" in result

    # Verify namespace values
    assert str(result["rdf"]) == "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    assert str(result["owl"]) == "http://www.w3.org/2002/07/owl#"
    assert str(result["test"]) == "http://test.org/"

    # Verify all values are Namespace instances
    for prefix in result.values():
        assert isinstance(prefix, Namespace)


def test_extract_prefixes_failed_request(requests_mock):
    # Setup mock response for failed request
    test_url = "http://example.com/nonexistent.ttl"
    requests_mock.get(test_url, status_code=404)

    # Verify exception is raised for failed request
    with pytest.raises(Exception) as exc_info:
        extract_prefixes_from_ttl(test_url)

    assert "Failed to fetch the file" in str(exc_info.value)

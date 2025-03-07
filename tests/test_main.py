import pytest
from unittest.mock import Mock, patch
from main import upload


@pytest.fixture
def mock_request():
    request = Mock()
    request.get_json.return_value = {
        "uri": "neo4j://localhost:7687",
        "username": "neo4j",
        "password": "test123",
        "ttl_url": "https://example.com/ontology.ttl",
    }
    return request


@pytest.fixture
def mock_neo4j_store():
    with patch("main.Neo4jStore") as mock:
        yield mock


@pytest.fixture
def mock_graph():
    with patch("main.Graph") as mock:
        yield mock


@pytest.fixture
def mock_extract_prefixes():
    with patch("main.extract_prefixes_from_ttl") as mock:
        mock.return_value = {"ex": "http://example.org/"}
        yield mock


def test_upload_success(
    mock_request, mock_neo4j_store, mock_graph, mock_extract_prefixes
):
    response, status_code = upload(mock_request)
    assert status_code == 200
    assert response == "Success"
    mock_extract_prefixes.assert_called_once_with("https://example.com/ontology.ttl")


def test_upload_missing_uri(mock_request):
    mock_request.get_json.return_value = {
        "username": "neo4j",
        "password": "test123",
        "ttl_url": "https://example.com/ontology.ttl",
    }
    response, status_code = upload(mock_request)
    assert status_code == 400
    assert response == "No uri provided"


def test_upload_missing_username(mock_request):
    mock_request.get_json.return_value = {
        "uri": "neo4j://localhost:7687",
        "password": "test123",
        "ttl_url": "https://example.com/ontology.ttl",
    }
    response, status_code = upload(mock_request)
    assert status_code == 400
    assert response == "No username provided"


def test_upload_missing_password(mock_request):
    mock_request.get_json.return_value = {
        "uri": "neo4j://localhost:7687",
        "username": "neo4j",
        "ttl_url": "https://example.com/ontology.ttl",
    }
    response, status_code = upload(mock_request)
    assert status_code == 400
    assert response == "No password provided"


def test_upload_missing_ttl_url(mock_request):
    mock_request.get_json.return_value = {
        "uri": "neo4j://localhost:7687",
        "username": "neo4j",
        "password": "test123",
    }
    response, status_code = upload(mock_request)
    assert status_code == 400
    assert response == "No ttl_url provided"


def test_upload_neo4j_error(
    mock_request, mock_neo4j_store, mock_graph, mock_extract_prefixes
):
    mock_graph.return_value.parse.side_effect = Exception("Neo4j Error")
    response, status_code = upload(mock_request)
    assert status_code == 500
    assert response == "Failed to upload to Neo4j"

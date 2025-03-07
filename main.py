from rdflib_neo4j import Neo4jStoreConfig, Neo4jStore, HANDLE_VOCAB_URI_STRATEGY
from rdflib import Namespace, Graph, URIRef, RDF, SKOS, Literal
from extract import extract_prefixes_from_ttl
import functions_framework
import os


@functions_framework.http
def upload(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    # Get basic auth credentials from environment variables
    auth_username = os.environ.get("AUTH_USERNAME")
    auth_password = os.environ.get("AUTH_PASSWORD")

    # Check if auth credentials are provided in environment
    if not auth_username or not auth_password:
        return "Authentication credentials not configured", 500

    # Check for basic auth in request
    auth = request.authorization
    if not auth or auth.username != auth_username or auth.password != auth_password:
        return "Unauthorized", 401

    request_json = request.get_json(silent=True)
    if request_json is None:
        raise ValueError("No JSON payload provided")

    # Get neo4j uri from the request
    uri = request_json.get("uri", None)
    if uri is None:
        ## Return failure code
        return "No uri provided", 400

    # Get neo4j username from the request
    username = request_json.get("username", None)
    if username is None:
        ## Return failure code
        return "No username provided", 400

    # Get neo4j password from the request
    password = request_json.get("password", None)
    if password is None:
        ## Return failure code
        return ("No password provided", 400)

    # Get the TTL file URL from the request
    ttl_file = request_json.get("ttl_url", None)
    if ttl_file is None:
        ## Return failure code
        return "No ttl_url provided", 400

    # Extract prefixes from the TTL file
    prefixes = extract_prefixes_from_ttl(ttl_file)

    # Create a Neo4jStoreConfig object
    auth_data = {
        "uri": uri,
        "database": "neo4j",
        "user": username,
        "pwd": password,
    }

    config = Neo4jStoreConfig(
        auth_data=auth_data,
        custom_prefixes=prefixes,
        handle_vocab_uri_strategy=HANDLE_VOCAB_URI_STRATEGY.IGNORE,
        batching=False,
    )

    # neo4j_store = Neo4jStore(config=config)
    # graph_store = Graph(store=neo4j_store)

    # file_path = ttl_file
    # try:
    #     graph_store.parse(file_path, format="ttl")
    #     return "Success", 200
    # except Exception as e:
    #     print(e)
    #     return "Failed to upload to Neo4j", 500

    try:
        neo4j_aura = Graph(store=Neo4jStore(config=config))
        # Calling the parse method will implictly open the store
        neo4j_aura.parse(ttl_file, format="ttl")
        neo4j_aura.close(True)
        return "Success", 200
    except Exception as e:
        print(e)
        return "Failed to upload to Neo4j", 500

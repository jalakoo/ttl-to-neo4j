from rdflib_neo4j import Neo4jStoreConfig, Neo4jStore, HANDLE_VOCAB_URI_STRATEGY
from rdflib import Graph
import os

# set the configuration to connect to your Aura DB
AURA_DB_URI = os.environ.get("NEO4J_URI")
AURA_DB_USERNAME = "neo4j"
AURA_DB_PWD = os.environ.get("NEO4J_PASSWORD")

if not AURA_DB_URI or not AURA_DB_USERNAME or not AURA_DB_PWD:
    raise ValueError("Aura DB credentials not configured")

prefixes = {
    "skos": "http://www.w3.org/2004/02/skos/core#",
}

auth_data = {
    "uri": AURA_DB_URI,
    "database": "neo4j",
    "user": AURA_DB_USERNAME,
    "pwd": AURA_DB_PWD,
}

# Define your custom mappings & store config
config = Neo4jStoreConfig(
    auth_data=auth_data,
    custom_prefixes=prefixes,
    handle_vocab_uri_strategy=HANDLE_VOCAB_URI_STRATEGY.IGNORE,
    batching=True,
)

file_path = (
    "https://github.com/jbarrasa/gc-2022/raw/main/search/onto/concept-scheme-skos.ttl"
)

# Create the RDF Graph, parse & ingest the data to Neo4j, and close the store(If the field batching is set to True in the Neo4jStoreConfig, remember to close the store to prevent the loss of any uncommitted records.)
neo4j_aura = Graph(store=Neo4jStore(config=config))
# Calling the parse method will implictly open the store
neo4j_aura.parse(file_path, format="ttl")
neo4j_aura.close(True)

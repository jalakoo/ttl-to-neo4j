from rdflib import Graph
from rdflib.namespace import Namespace
import re
import requests


# Function to extract prefixes from a Turtle file
def extract_prefixes_from_ttl(url):
    # Fetch the Turtle file from the URL
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(
            f"Failed to fetch the file, status code: {response.status_code}"
        )

    ttl_data = response.text

    # Use regex to find all @prefix declarations in the Turtle file
    prefix_pattern = re.compile(r"@prefix\s+(\w+):\s+<([^>]+)>")
    matches = prefix_pattern.findall(ttl_data)

    # Create a dictionary to hold the prefixes
    prefixes = {}
    for prefix, namespace in matches:
        prefixes[prefix] = Namespace(namespace)

    # Parse the RDF triples using rdflib (ignore the prefixes for now)
    graph = Graph()
    graph.parse(data=ttl_data, format="turtle")

    # Return the extracted prefixes
    return prefixes


# Function to extract prefixes from a Turtle file - including referenced prefixes from prefixes
def extract_all_prefixes_from_ttl(url):
    # Fetch the Turtle file from the URL
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(
            f"Failed to fetch the file, status code: {response.status_code}"
        )

    # Create an empty graph
    graph = Graph()

    # Parse the Turtle file from the URL response content
    graph.parse(data=response.text, format="turtle")

    # Extract the prefixes from the graph's namespace bindings
    prefixes = {}
    for prefix, namespace in graph.namespaces():
        prefixes[prefix] = Namespace(namespace)

    return prefixes

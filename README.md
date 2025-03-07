# TTL to Neo4j GCR Function

Google Cloud Run Function for uploading a .ttl file to a Neo4j Graph Database using the [RDFLib-Neo4j package](https://neo4j.com/labs/rdflib-neo4j/1.0/)

## Updating requirements.txt file

Using poetry:

```bash
poetry export -f requirements.txt --output requirements.txt --without-hashes
```

## Running tests

```bash
poetry run pytest
```

## Running locally

TERMINAL 1:

```bash
AUTH_USERNAME=neo4j AUTH_PASSWORD=password \
poetry run functions-framework --target=upload --port=8080
```

TERMINAL 2:

```bash
curl -X POST "http://localhost:8080" -u "neo4j:password" -H "Content-Type: application/json" -d '{"uri": "...", "username": "...", "password": "...", "ttl_url": "..."}'
```

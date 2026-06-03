# NLP-LegalQA

Vietnamese legal document retrieval and QA chatbot built for a coursework team project. The system parses legal documents into a Neo4j graph, retrieves relevant legal provisions with hybrid search, reranks results, and generates grounded answers with legal citations.

## Project Note

This repository is a sanitized public version of a coursework team project. The original development repository is kept private because it contained credentials, local configuration files, large experiment artifacts, and internal development outputs.

This public version focuses on the core implementation:

- Vietnamese legal document scraping and parsing
- Neo4j content graph import
- Dense vector retrieval and Neo4j fulltext search
- Hybrid retrieval with multi-query aggregation
- Cross-encoder reranking integration
- Retrieval context assembly with amendment-aware metadata
- Domain-specific answer generation
- FastAPI and Streamlit prototypes

## Team And Credit

This was a team project. Please update this section before publishing with the final contributor list approved by the team.

- Thai Hoang Phuc - query routing, query rewriting/decomposition, hybrid retrieval integration, reranking/evaluation pipeline, answer generation, API/Streamlit prototype
- Teammate A - data collection / preprocessing
- Teammate B - evaluation dataset / experiments
- Teammate C - report / testing / supporting implementation

## Security Notice

No production credentials are included in this public version. Configure services through environment variables only. Do not commit `.env`, local tool settings, model checkpoints, offline payloads, database dumps, or generated evaluation outputs.

## Setup

```bash
uv sync
```

Copy the environment template and fill in your own local values:

```bash
cp .env.example .env
```

## Core Commands

Search for legal documents:

```bash
uv run legal-scraper search "Luật" -n 10
```

Parse downloaded documents:

```bash
uv run legal-scraper parse -i data/ -o data/parsed/
```

Import parsed documents into Neo4j:

```bash
uv run legal-scraper import-neo4j \
  -i data/parsed \
  -a data/amends \
  --uri "$NEO4J_URI" \
  --user "$NEO4J_USER" \
  --password "$NEO4J_PASSWORD" \
  --database "$NEO4J_DATABASE"
```

Run the full retrieval pipeline:

```bash
uv run legal-scraper query \
  -q "không đội mũ bảo hiểm phạt bao nhiêu" \
  --uri "$NEO4J_URI" \
  --user "$NEO4J_USER" \
  --password "$NEO4J_PASSWORD" \
  --database "$NEO4J_DATABASE"
```

Start the API:

```bash
uv run legal-api
```

Start the Streamlit prototype:

```bash
uv run streamlit run streamlit_ui/app.py
```

## Public Release Scope

The following were intentionally excluded from this sanitized version:

- Real credentials and local `.env` files
- `.claude/`, `.agents/`, editor and local tool settings
- Large scraped datasets and generated experiment outputs
- Fine-tuning artifacts, local model checkpoints, offline payloads
- Notebook outputs that may contain local paths or run-specific data
- Original Git history from the private repository

## License

No license is provided yet. This repository is published for academic portfolio and demonstration purposes. Choose a license only after the team agrees on reuse permissions.

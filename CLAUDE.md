# CLAUDE.md

## Project Overview

Vietnamese legal document scraper and Graph RAG QA toolkit. This public repository is a sanitized public version of a coursework team project. The original private repository is retained for full development history and internal artifacts.

## Public Scope

Included:

- Core `legal_scraper` package
- Neo4j import, embedding, retrieval, reranking, answer generation, API, and CLI code
- Streamlit prototype
- Offline unit tests
- Evaluation scripts that can be run with user-provided data and credentials


## Team Project Note

This was a team project.
My main contributions:

- Query routing and intent classification
- Query rewriting and decomposition
- Hybrid retrieval integration
- Multi-query aggregation and reranking/evaluation pipeline integration
- Amendment-aware context assembly
- Domain-specific answer generation prompts
- FastAPI and Streamlit chatbot prototype wiring

## Setup

```bash
uv sync
```

## Tests

```bash
uv run pytest
```

The default public tests are offline and should not require credentials or running services.

## Demo Mode

The real RAG pipeline requires Neo4j, embeddings, a reranker model, and an LLM endpoint. Use demo mode for public portfolio review:

```powershell
$env:LEGALQA_DEMO="1"
uv run legal-api
```

In another terminal:

```powershell
uv run --extra ui streamlit run streamlit_ui/app.py
```

Demo mode returns deterministic sample responses with mock source cards and timings. It is only for showing the API/UI flow; it is not legal advice and does not exercise the full graph RAG stack.

Integration checks require your own Neo4j database and LLM configuration:

```bash
uv run legal-scraper query \
  -q "không đội mũ bảo hiểm phạt bao nhiêu" \
  --uri "$NEO4J_URI" \
  --user "$NEO4J_USER" \
  --password "$NEO4J_PASSWORD" \
  --database "$NEO4J_DATABASE"
```

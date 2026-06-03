# CLAUDE.md

## Project Overview

Vietnamese legal document scraper and Graph RAG QA toolkit. This public repository is a sanitized portfolio version of a coursework team project. The original private repository is retained for full development history and internal artifacts.

## Public Scope

Included:

- Core `legal_scraper` package
- Neo4j import, embedding, retrieval, reranking, answer generation, API, and CLI code
- Streamlit prototype
- Offline unit tests
- Evaluation scripts that can be run with user-provided data and credentials

Excluded:

- Real credentials and local `.env` files
- `.claude/`, `.agents/`, editor settings, and local tool state
- Large scraped datasets, generated experiment outputs, fine-tuning artifacts, model checkpoints, and notebook outputs
- Original private Git history

## Team Project Note

This was a team project. In public descriptions, do not present the entire system as solo work.

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

Copy `.env.example` to `.env` and fill in your own local credentials.

## Tests

```bash
uv run pytest
```

The default public tests are offline and should not require credentials or running services.

Integration checks require your own Neo4j database and LLM configuration:

```bash
uv run legal-scraper query \
  -q "không đội mũ bảo hiểm phạt bao nhiêu" \
  --uri "$NEO4J_URI" \
  --user "$NEO4J_USER" \
  --password "$NEO4J_PASSWORD" \
  --database "$NEO4J_DATABASE"
```

## Security Rules

- Never commit `.env`.
- Never commit real database URIs, passwords, API keys, model checkpoints, offline payloads, or generated evaluation dumps.
- Use placeholders in documentation and environment templates.
- Rotate any credential that was ever committed to the private development history before making a public repository.

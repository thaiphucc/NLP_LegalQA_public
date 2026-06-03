# CLAUDE.md

## Project Overview

Vietnamese legal document scraper and Graph RAG QA toolkit. This public repository is a sanitized portfolio version of a coursework team project. The original private repository is retained for full development history and internal artifacts.

Do not present this project as solo work. Public descriptions should say it was a team project and identify only the parts the repository owner was mainly responsible for.

## Repository Structure

```text
src/legal_scraper/       Core package: scraper, parser, Neo4j import, retrieval, reranking, API
streamlit_ui/            Streamlit chat prototype
scripts/                 Evaluation scripts and local Neo4j sample setup
data_sample/             Small non-sensitive parsed sample document
tests/unit/              Offline tests run by default
tests/integration/       Optional tests requiring Neo4j or external services
docker-compose.yml       Local Neo4j for sample-data demo
```

## Setup

```bash
uv sync
```

Copy `.env.example` to `.env` and fill in local credentials only on your machine. Never commit `.env`.

## Default Tests

```bash
uv run --extra dev pytest
```

Default tests must stay offline. They should not require:

- Neo4j credentials
- Running Neo4j
- API keys
- Local LLM endpoints
- Downloaded embedding/reranker models
- Private data files

## Integration Tests

Integration tests are marked with `pytest.mark.integration` and excluded by default.

Run them only after configuring Neo4j:

```bash
uv run --extra dev pytest -m integration
```

Integration tests should skip gracefully if required environment variables are missing.

## Demo Mode

Use demo mode for public portfolio review without private infrastructure:

```powershell
$env:LEGALQA_DEMO="1"
uv run legal-api
```

Then in another terminal:

```powershell
uv run --extra ui streamlit run streamlit_ui/app.py
```

Demo mode returns deterministic sample responses with mock source cards and timings. It is not legal advice and does not exercise the full graph RAG stack.

## Local Neo4j Sample Data

The original coursework database is not included. To test the sample graph:

```bash
docker compose up -d
uv run python scripts/init_neo4j.py
uv run python scripts/import_sample_data.py
uv run --extra dev pytest -m integration
```

## Coding Conventions

- Keep public defaults safe and local-only.
- Prefer environment variables for credentials and service URLs.
- Keep unit tests deterministic and offline.
- Put DB/model/API-dependent tests under `tests/integration/`.
- Do not add large generated data, model checkpoints, notebook outputs, or local runtime artifacts.

## Security Rules

- Never commit `.env`.
- Never commit real database URIs, passwords, API keys, local hostnames, local paths, model checkpoints, offline payloads, generated evaluation dumps, or private datasets.
- Use placeholders in docs and `.env.example`.
- If any real credential appears in development history, rotate it before public release.
- Keep `.gitignore` updated for local settings, caches, data dumps, eval outputs, notebooks checkpoints, and model files.

## Teamwork Credit

This is a team project. In README/CV text, list only the repository owner's main responsibilities:

- Query routing and query rewriting/decomposition
- Hybrid retrieval integration with dense search and Neo4j full-text search
- Reranking/evaluation pipeline integration
- Legal answer generation prompts and context construction
- FastAPI and Streamlit prototype wiring

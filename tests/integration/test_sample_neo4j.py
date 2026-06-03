import os

import pytest


pytestmark = pytest.mark.integration


def _missing_neo4j_env() -> list[str]:
    return [
        name
        for name in ("NEO4J_URI", "NEO4J_USER", "NEO4J_PASSWORD")
        if not os.getenv(name)
    ]


def test_sample_data_can_be_imported_into_configured_neo4j():
    missing = _missing_neo4j_env()
    if missing:
        pytest.skip(f"Missing Neo4j env vars: {', '.join(missing)}")

    from pathlib import Path

    from legal_scraper.neo4j_importer import Neo4jImporter

    repo_root = Path(__file__).resolve().parents[2]
    sample_path = repo_root / "data_sample" / "parsed" / "sample_traffic_law.json"

    importer = Neo4jImporter(
        os.environ["NEO4J_URI"],
        os.environ["NEO4J_USER"],
        os.environ["NEO4J_PASSWORD"],
        os.getenv("NEO4J_DATABASE", "neo4j"),
    )
    try:
        importer.ensure_constraints()
        result = importer.import_parsed_file(sample_path)
    finally:
        importer.close()

    assert result["nodes"] >= 1

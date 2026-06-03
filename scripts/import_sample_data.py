"""Import the small public sample dataset into a local Neo4j database."""

from __future__ import annotations

import argparse
import os
from pathlib import Path

from dotenv import load_dotenv

from legal_scraper.neo4j_importer import Neo4jImporter


def parse_args() -> argparse.Namespace:
    load_dotenv()
    repo_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description="Import NLP-LegalQA sample data")
    parser.add_argument("--uri", default=os.getenv("NEO4J_URI", "neo4j://localhost:7687"))
    parser.add_argument("--user", default=os.getenv("NEO4J_USER", "neo4j"))
    parser.add_argument("--password", default=os.getenv("NEO4J_PASSWORD", "change_me_for_local_demo"))
    parser.add_argument("--database", default=os.getenv("NEO4J_DATABASE", "neo4j"))
    parser.add_argument(
        "--input",
        type=Path,
        default=repo_root / "data_sample" / "parsed" / "sample_traffic_law.json",
        help="Parsed JSON file to import",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not args.input.exists():
        raise FileNotFoundError(f"Sample file not found: {args.input}")

    importer = Neo4jImporter(args.uri, args.user, args.password, args.database)
    try:
        importer.ensure_constraints()
        result = importer.import_parsed_file(args.input)
    finally:
        importer.close()

    print(f"Imported {args.input.name}: {result}")


if __name__ == "__main__":
    main()

"""Initialize local Neo4j constraints and fulltext indexes for the demo."""

from __future__ import annotations

import argparse
import os

from dotenv import load_dotenv

from legal_scraper.embedder import Neo4jEmbedder
from legal_scraper.neo4j_importer import Neo4jImporter


def parse_args() -> argparse.Namespace:
    load_dotenv()
    parser = argparse.ArgumentParser(description="Initialize Neo4j schema for NLP-LegalQA")
    parser.add_argument("--uri", default=os.getenv("NEO4J_URI", "neo4j://localhost:7687"))
    parser.add_argument("--user", default=os.getenv("NEO4J_USER", "neo4j"))
    parser.add_argument("--password", default=os.getenv("NEO4J_PASSWORD", "change_me_for_local_demo"))
    parser.add_argument("--database", default=os.getenv("NEO4J_DATABASE", "neo4j"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    importer = Neo4jImporter(args.uri, args.user, args.password, args.database)
    try:
        importer.ensure_constraints()
        print("Created/verified uniqueness constraints.")
    finally:
        importer.close()

    embedder = Neo4jEmbedder(args.uri, args.user, args.password, args.database)
    try:
        embedder.create_fulltext_indexes()
    finally:
        embedder.close()

    print("Neo4j schema initialization complete.")


if __name__ == "__main__":
    main()

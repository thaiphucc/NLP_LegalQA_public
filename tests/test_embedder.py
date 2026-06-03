import pytest
from legal_scraper.embedder import Neo4jEmbedder


class FakeDriver:
    def __init__(self):
        self.closed = False

    def close(self):
        self.closed = True


class TestNeo4jEmbedderInit:
    def test_embedder_stores_uri_and_credentials(self):
        embedder = Neo4jEmbedder(
            uri="neo4j+ssc://host:7687",
            user="neo4j",
            password="secret",
            database="neo4j",
        )
        assert embedder.uri == "neo4j+ssc://host:7687"
        assert embedder.user == "neo4j"
        assert embedder.password == "secret"
        assert embedder.database == "neo4j"
        assert embedder._driver is None  # lazy connection

    def test_close_without_driver_is_safe(self):
        embedder = Neo4jEmbedder(uri="bolt://x", user="x", password="x")
        embedder.close()  # should not raise

    def test_close_after_driver_open(self, monkeypatch):
        fake_driver = FakeDriver()
        monkeypatch.setattr(
            "legal_scraper.embedder.GraphDatabase.driver",
            lambda *args, **kwargs: fake_driver,
        )

        embedder = Neo4jEmbedder(
            uri="neo4j+ssc://example.invalid:7687",
            user="neo4j",
            password="example-password",
        )
        driver = embedder._get_driver()
        assert driver is fake_driver
        embedder.close()
        assert fake_driver.closed is True
        assert embedder._driver is None  # driver was closed

    def test_get_driver_is_lazy(self, monkeypatch):
        fake_driver = FakeDriver()
        monkeypatch.setattr(
            "legal_scraper.embedder.GraphDatabase.driver",
            lambda *args, **kwargs: fake_driver,
        )

        embedder = Neo4jEmbedder(
            uri="neo4j+ssc://example.invalid:7687",
            user="neo4j",
            password="example-password",
        )
        assert embedder._driver is None
        driver = embedder._get_driver()
        assert driver is fake_driver
        assert embedder._driver is driver  # same instance
        embedder.close()

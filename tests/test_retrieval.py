import pytest

from legal_scraper import retrieval
from legal_scraper.embedder import SearchResult


class FakeEmbedder:
    def fetch_node_hierarchy(self, uids):
        return {uid: f"Hierarchy for {uid}" for uid in uids}

    def fetch_nodes(self, uids, labels):
        return {
            (uid, label): {"title": f"{label} title", "content": f"Content for {uid}"}
            for uid in uids
            for label in labels
            if label in uid or uid.startswith("doc")
        }


def test_aggregate_search_results_rrf_deduplicates_and_sorts():
    raw = {
        0: [
            SearchResult(uid="doc1::Article", label="Article", score=0.9),
            SearchResult(uid="doc2::Article", label="Article", score=0.8),
        ],
        1: [
            SearchResult(uid="doc1::Article", label="Article", score=0.85),
            SearchResult(uid="doc3::Clause", label="Clause", score=0.7),
        ],
    }

    agg = retrieval.aggregate_search_results(raw, strategy="rrf")

    assert [r.uid for r in agg] == [
        "doc1::Article",
        "doc2::Article",
        "doc3::Clause",
    ]
    assert agg[0].score > agg[1].score


def test_aggregate_search_results_max_uses_highest_score():
    raw = {
        0: [SearchResult(uid="doc1", label="Article", score=0.5)],
        1: [SearchResult(uid="doc1", label="Article", score=0.9)],
    }

    agg = retrieval.aggregate_search_results(raw, strategy="max")

    assert len(agg) == 1
    assert agg[0].score == 0.9


def test_aggregate_search_results_borda_averages_scores():
    raw = {
        0: [SearchResult(uid="doc1", label="Article", score=0.5)],
        1: [SearchResult(uid="doc1", label="Article", score=0.9)],
    }

    agg = retrieval.aggregate_search_results(raw, strategy="borda")

    assert len(agg) == 1
    assert agg[0].score == pytest.approx(0.7)


def test_aggregate_search_results_rejects_unknown_strategy():
    raw = {0: [SearchResult(uid="doc1", label="Article", score=0.5)]}

    with pytest.raises(ValueError):
        retrieval.aggregate_search_results(raw, strategy="unknown")


def test_fetch_context_for_results_uses_hierarchy_when_requested():
    results = [SearchResult(uid="doc1::Article", label="Article", score=0.9)]

    ctx = retrieval.fetch_context_for_results(FakeEmbedder(), results, include_hierarchy=True)

    assert ctx[("doc1::Article", "Article")] == "Hierarchy for doc1::Article"


def test_fetch_context_for_results_can_fetch_node_content_only():
    results = [SearchResult(uid="doc1::Article", label="Article", score=0.9)]

    ctx = retrieval.fetch_context_for_results(FakeEmbedder(), results, include_hierarchy=False)

    assert "Article title" in ctx[("doc1::Article", "Article")]
    assert "Content for doc1::Article" in ctx[("doc1::Article", "Article")]


def test_build_context_str_adds_amendment_sibling_and_child_context():
    result = SearchResult(uid="doc1::article::1::clause::1::point::a", label="Point", score=0.9)
    context_map = {(result.uid, result.label): "Original provision"}
    amends_map = {
        result.uid: [
            {
                "amending_uid": "doc2::article::3::clause::2",
                "amending_content": "Updated penalty range",
            }
        ]
    }
    siblings_map = {result.uid: "Sibling point b"}
    children_map = {result.uid: "Child detail"}

    context = retrieval.build_context_str(
        [result],
        context_map,
        amends_map=amends_map,
        siblings_map=siblings_map,
        children_map=children_map,
    )

    assert "Original provision" in context
    assert "Updated penalty range" in context
    assert "Sibling point b" in context
    assert "Child detail" in context

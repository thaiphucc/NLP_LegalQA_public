from fastapi.testclient import TestClient


def test_demo_api_health_and_chat(monkeypatch):
    monkeypatch.setenv("LEGALQA_DEMO", "1")

    from legal_scraper.api import app

    with TestClient(app) as client:
        health = client.get("/health")
        assert health.status_code == 200
        assert health.json()["demo_mode"] is True

        response = client.post(
            "/chat",
            json={
                "query": "không đội mũ bảo hiểm phạt bao nhiêu",
                "chat_history": [],
            },
        )

    assert response.status_code == 200
    body = response.json()
    assert body["intent"] == "retrieve"
    assert "Demo mode" in body["answer"]
    assert body["sources"]
    assert body["timings"]["rerank"] > 0

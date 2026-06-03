"""Small offline demo responses for the public portfolio release.

The real system needs Neo4j, embeddings, a reranker, and an LLM.  Public
reviewers should still be able to launch the API and Streamlit UI without
private infrastructure, so this module returns a deterministic sample response
that mirrors the production response shape.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DemoSource:
    uid: str
    label: str
    score: float
    uid_formatted: str
    context_snippet: str


def build_demo_response(query: str) -> dict:
    """Return a deterministic demo response shaped like the real API output."""
    normalized = query.lower()

    if "mũ" in normalized or "mu bao hiem" in normalized or "bảo hiểm" in normalized:
        answer = (
            "Demo mode: Với tình huống không đội mũ bảo hiểm khi đi xe máy, hệ thống "
            "sẽ truy xuất các điểm/khoản liên quan trong nhóm quy định xử phạt người "
            "điều khiển xe mô tô, xe gắn máy, sau đó rerank và sinh câu trả lời có "
            "trích dẫn. Bản demo này dùng dữ liệu mẫu, không phải tư vấn pháp lý thật."
        )
        sources = [
            DemoSource(
                uid="168/2024/NĐ-CP::article::7::clause::2::point::a",
                label="Point",
                score=8.72,
                uid_formatted="Điểm a Khoản 2 Điều 7 Nghị định 168/2024/NĐ-CP",
                context_snippet=(
                    "Nội dung mẫu: quy định xử phạt hành vi không đội mũ bảo hiểm "
                    "hoặc đội mũ bảo hiểm không cài quai đúng quy cách khi tham gia giao thông."
                ),
            ),
            DemoSource(
                uid="168/2024/NĐ-CP::article::7::clause::2",
                label="Clause",
                score=7.94,
                uid_formatted="Khoản 2 Điều 7 Nghị định 168/2024/NĐ-CP",
                context_snippet="Nội dung mẫu: nhóm chế tài áp dụng cho người điều khiển xe mô tô, xe gắn máy.",
            ),
        ]
    else:
        answer = (
            "Demo mode: Hệ thống sẽ phân loại intent, viết lại câu hỏi nếu cần, "
            "tách truy vấn phức tạp thành các sub-query, kết hợp vector search với "
            "Neo4j fulltext search, rerank, rồi sinh câu trả lời dựa trên ngữ cảnh. "
            "Bản demo này dùng dữ liệu mẫu, không phải tư vấn pháp lý thật."
        )
        sources = [
            DemoSource(
                uid="168/2024/NĐ-CP::article::6::clause::4",
                label="Clause",
                score=8.31,
                uid_formatted="Khoản 4 Điều 6 Nghị định 168/2024/NĐ-CP",
                context_snippet="Nội dung mẫu: điều khoản được truy xuất từ graph pháp luật.",
            )
        ]

    sub_queries = [
        "xác định hành vi vi phạm giao thông trong câu hỏi",
        "tìm mức phạt và căn cứ pháp lý tương ứng",
    ]

    return {
        "answer": answer,
        "intent": "retrieve",
        "sources": [source.__dict__ for source in sources],
        "timings": {
            "route": 0.01,
            "rewrite": 0.02,
            "decompose": 0.03,
            "search": 0.04,
            "rerank": 0.05,
            "generation": 0.03,
        },
        "rewritten_query": query,
        "sub_queries": sub_queries,
        "cypher_query": None,
    }

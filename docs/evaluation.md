# Evaluation Summary

This page summarizes a sanitized snapshot of the internal evaluation results from the original coursework repository. Raw QA datasets, row-level model outputs, private credentials, generated databases, and large experiment artifacts are intentionally omitted from this public portfolio release.

## What Was Evaluated

- Basic RAG retrieval over the legal corpus.
- Hybrid retrieval using graph/full-text search plus dense retrieval.
- Reranking and result aggregation variants.
- LLM answer generation with zero-shot, few-shot, and fine-tuned model settings.

## Retrieval Baseline

The basic RAG baseline was evaluated on 200 QA examples:

| Metric | Score |
| --- | ---: |
| Recall@1 | 0.344 |
| Recall@3 | 0.445 |
| Recall@5 | 0.489 |
| Recall@10 | 0.574 |
| Precision@1 | 0.370 |
| Precision@3 | 0.175 |
| MRR | 0.463 |

## Retrieval Ablations

The full pipeline was compared against ablations that remove hybrid retrieval, heuristic filtering, or change aggregation. Scores below are averaged summaries from 200 examples.

### Gemma Judge Configuration

| Config | Recall@1 | Recall@5 | Recall@10 | Precision@1 | MRR |
| --- | ---: | ---: | ---: | ---: | ---: |
| agg_borda | 0.493 | 0.668 | 0.710 | 0.600 | 0.694 |
| agg_max | 0.465 | 0.674 | 0.731 | 0.575 | 0.696 |
| full_pipeline | 0.474 | 0.645 | 0.699 | 0.575 | 0.679 |
| no_heuristic | 0.413 | 0.640 | 0.701 | 0.465 | 0.603 |
| no_hybrid | 0.476 | 0.649 | 0.702 | 0.590 | 0.678 |

### Gemini Flash Judge Configuration

| Config | Recall@1 | Recall@5 | Recall@10 | Precision@1 | MRR |
| --- | ---: | ---: | ---: | ---: | ---: |
| agg_borda | 0.488 | 0.669 | 0.695 | 0.595 | 0.692 |
| agg_max | 0.495 | 0.677 | 0.719 | 0.610 | 0.713 |
| full_pipeline | 0.499 | 0.671 | 0.711 | 0.610 | 0.703 |
| no_heuristic | 0.457 | 0.628 | 0.692 | 0.515 | 0.635 |
| no_hybrid | 0.493 | 0.644 | 0.687 | 0.595 | 0.678 |

## LLM Answer Quality

LLM answer quality was evaluated with automatic text overlap metrics and an LLM judge rubric for legal accuracy, citation correctness, completeness, hallucinated citation handling, structure, and overall score.

| Model config | BLEU | ROUGE-L | METEOR | Judge overall |
| --- | ---: | ---: | ---: | ---: |
| Gemini Flash zero-shot | 0.290 | 0.476 | 0.527 | 8.590 |
| Gemini Flash few-shot | 0.311 | 0.493 | 0.522 | 8.185 |
| Gemma 4 zero-shot | 0.293 | 0.481 | 0.558 | 8.488 |
| Gemma 4 few-shot | 0.348 | 0.516 | 0.592 | 8.363 |
| Fine-tuned local model | 0.281 | 0.483 | 0.495 | 4.948 |

## Takeaways

- Hybrid retrieval, reranking, and aggregation helped the system retrieve more legally relevant context than the basic RAG baseline.
- Removing heuristic filtering reduced retrieval quality most clearly in the ablation tables.
- The hosted zero-shot and few-shot LLM settings produced stronger judged answer quality than the small fine-tuned local model.
- The fine-tuned model remains useful as a reproducible local experiment, but the best public-facing QA path is the graph/vector RAG pipeline with a stronger external LLM endpoint.

# Evaluation report - 20261030-223626_rerank-nemotron-all96

Questions: 96 | judge: `none` | generator: `nvidia/nemotron-3.5-lightning-30b-a3b` | reranker: `nvidia/nemotron-3.5-rerank-8b` | top_k: 4

## Retriever (deterministic, by document)

| hit@k | recall@k | precision@k | MRR |
|---|---|---|---|
| 1.000 | 0.942 | 0.685 | 0.897 |

## Retriever (DeepEval)

| Metric | Mean | Pass rate (>= 0.5) | n |
|---|---|---|---|
| contextual_recall | - | - | 0 |
| contextual_precision | - | - | 0 |

## Generator in isolation (golden evidence as context)

| Metric | Mean | Pass rate (>= 0.5) | n |
|---|---|---|---|
| faithfulness | - | - | 0 |
| answer_relevancy | - | - | 0 |

## Whole pipeline (real retrieval)

| Metric | Mean | Pass rate (>= 0.5) | n |
|---|---|---|---|
| contextual_relevancy | - | - | 0 |
| faithfulness | - | - | 0 |
| answer_relevancy | - | - | 0 |

## Application

### Latency (ms)

| Stage | p50 | p95 | mean | max |
|---|---|---|---|---|
| search | 123 | 193 | 126 | 397 |
| rerank | 827 | 1,736 | 1,035 | 9,352 |
| retrieval | 952 | 1,973 | 1,161 | 9,445 |
| generation | 1,424 | 3,559 | 1,812 | 12,117 |
| total | 2,467 | 4,706 | 2,943 | 13,007 |
| generation_isolated | - | - | - | - |

### Quality

- GEval correctness: mean -, pass rate -
- Behaviour pass rate (cites an expected doc / abstains when it should): 0.927

| Category | Pass rate |
|---|---|
| ambiguous | 0.000 |
| direct_factual | 1.000 |
| exception_eligibility | 1.000 |
| instruction_override | 1.000 |
| insufficient_evidence | 1.000 |
| multi_document | 1.000 |
| nonexistent_entity | 0.750 |
| procedure_policy | 0.957 |

### Safety

- GEval safety: mean -, pass rate -
- Abstention rate on unsupported questions: 0.684
- False abstention rate on supported questions: 0.000
- Prompt injections declined by the guard: 4/5

### Operations

- Pipeline errors: 0 | metric errors: 0 
- Generator provider errors: 0 | fallbacks to Ollama: 0 | reranker errors (fell back to vector order): 0
- Judge calls: 0 | retries: 0 | 429s: 0 | timeouts: 0 | 5xx: 0 | failed: 0
- Judge latency p50/p95: -s / -s
- Judge tokens in/out: 0 / 0
- Wall time: pipeline 273.7s, judge 0.0s | pipeline throughput 21.040 questions/min

### Cost (USD)

- Generator: 0.0 | judge: 0.0 | per question: 0.0
- Generator, reranker and judge run on NVIDIA's free hosted trial API (or local Ollama), so cost is $0. Judge cost uses JUDGE_PRICE_INPUT/OUTPUT (USD per 1M tokens).

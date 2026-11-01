# Evaluation report - 20261030-231632_clarify-sample16

Questions: 16 | judge: `openai/gpt-oss-20b` | generator: `nvidia/nemotron-3.5-lightning-30b-a3b` | reranker: `nvidia/nemotron-3.5-rerank-8b` | top_k: 4

## Retriever (deterministic, by document)

| hit@k | recall@k | precision@k | MRR |
|---|---|---|---|
| 1.000 | 0.938 | 0.719 | 0.917 |

## Retriever (DeepEval)

| Metric | Mean | Pass rate (>= 0.5) | n |
|---|---|---|---|
| contextual_recall | 0.875 | 0.875 | 8 |
| contextual_precision | 0.969 | 1.000 | 8 |

## Generator in isolation (golden evidence as context)

| Metric | Mean | Pass rate (>= 0.5) | n |
|---|---|---|---|
| faithfulness | 1.000 | 1.000 | 8 |
| answer_relevancy | 0.938 | 1.000 | 8 |

## Whole pipeline (real retrieval)

| Metric | Mean | Pass rate (>= 0.5) | n |
|---|---|---|---|
| contextual_relevancy | 0.383 | 0.125 | 8 |
| faithfulness | 1.000 | 1.000 | 8 |
| answer_relevancy | 0.969 | 1.000 | 8 |

## Application

### Latency (ms)

| Stage | p50 | p95 | mean | max |
|---|---|---|---|---|
| search | 91 | 132 | 99 | 133 |
| rerank | 977 | 1,053 | 1,020 | 1,782 |
| retrieval | 1,090 | 1,133 | 1,119 | 1,873 |
| generation | 1,240 | 1,692 | 1,366 | 2,490 |
| total | 2,497 | 3,448 | 2,515 | 3,605 |
| generation_isolated | 1,108 | 1,861 | 1,152 | 1,861 |

### Quality

- GEval correctness: mean 0.863, pass rate 0.875
- Behaviour pass rate (cites an expected doc / abstains when it should): 0.938

| Category | Pass rate |
|---|---|
| ambiguous | 1.000 |
| direct_factual | 1.000 |
| exception_eligibility | 1.000 |
| instruction_override | 1.000 |
| insufficient_evidence | 1.000 |
| multi_document | 1.000 |
| nonexistent_entity | 0.500 |
| procedure_policy | 1.000 |

### Safety

- GEval safety: mean 0.975, pass rate 1.000
- Abstention rate on unsupported questions: 0.875
- False abstention rate on supported questions: 0.000
- Prompt injections declined by the guard: 2/2

### Operations

- Pipeline errors: 0 | metric errors: 0 
- Generator provider errors: 0 | fallbacks to Ollama: 0 | reranker errors (fell back to vector order): 0
- Clarifying questions asked: 3 | clarity-check errors: 0
- Judge calls: 152 | retries: 0 | 429s: 0 | timeouts: 0 | 5xx: 0 | failed: 0
- Judge latency p50/p95: 7.900s / 38.900s
- Judge tokens in/out: 98,356 / 41,375
- Wall time: pipeline 44.4s, judge 536.6s | pipeline throughput 21.620 questions/min

### Cost (USD)

- Generator: 0.0 | judge: 0.0 | per question: 0.0
- Generator, reranker and judge run on NVIDIA's free hosted trial API (or local Ollama), so cost is $0. Judge cost uses JUDGE_PRICE_INPUT/OUTPUT (USD per 1M tokens).

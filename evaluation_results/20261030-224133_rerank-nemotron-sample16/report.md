# Evaluation report - 20261030-224133_rerank-nemotron-sample16

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
| answer_relevancy | 1.000 | 1.000 | 8 |

## Whole pipeline (real retrieval)

| Metric | Mean | Pass rate (>= 0.5) | n |
|---|---|---|---|
| contextual_relevancy | 0.368 | 0.125 | 8 |
| faithfulness | 1.000 | 1.000 | 8 |
| answer_relevancy | 0.885 | 0.875 | 8 |

## Application

### Latency (ms)

| Stage | p50 | p95 | mean | max |
|---|---|---|---|---|
| search | 93 | 169 | 116 | 312 |
| rerank | 822 | 1,069 | 895 | 1,685 |
| retrieval | 933 | 1,381 | 1,011 | 1,839 |
| generation | 1,396 | 3,012 | 1,682 | 3,369 |
| total | 2,393 | 3,792 | 2,693 | 4,302 |
| generation_isolated | 957 | 1,699 | 1,081 | 1,699 |

### Quality

- GEval correctness: mean 0.900, pass rate 1.000
- Behaviour pass rate (cites an expected doc / abstains when it should): 0.750

| Category | Pass rate |
|---|---|
| ambiguous | 0.000 |
| direct_factual | 1.000 |
| exception_eligibility | 1.000 |
| instruction_override | 1.000 |
| insufficient_evidence | 0.500 |
| multi_document | 1.000 |
| nonexistent_entity | 0.500 |
| procedure_policy | 1.000 |

### Safety

- GEval safety: mean 0.906, pass rate 0.875
- Abstention rate on unsupported questions: 0.500
- False abstention rate on supported questions: 0.000
- Prompt injections declined by the guard: 2/2

### Operations

- Pipeline errors: 0 | metric errors: 0 
- Generator provider errors: 0 | fallbacks to Ollama: 0 | reranker errors (fell back to vector order): 0
- Judge calls: 152 | retries: 1 | 429s: 0 | timeouts: 0 | 5xx: 1 | failed: 0
- Judge latency p50/p95: 13.800s / 57.500s
- Judge tokens in/out: 97,768 / 42,553
- Wall time: pipeline 46.4s, judge 744.4s | pipeline throughput 20.690 questions/min

### Cost (USD)

- Generator: 0.0 | judge: 0.0 | per question: 0.0
- Generator, reranker and judge run on NVIDIA's free hosted trial API (or local Ollama), so cost is $0. Judge cost uses JUDGE_PRICE_INPUT/OUTPUT (USD per 1M tokens).

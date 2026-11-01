# Evaluation report - 20261030-192337_sample16

Questions: 16 | judge: `openai/gpt-oss-20b` | generator: `gemma2:2b` | top_k: 6

## Retriever (deterministic, by document)

| hit@k | recall@k | precision@k | MRR |
|---|---|---|---|
| 1.000 | 0.875 | 0.583 | 0.833 |

## Retriever (DeepEval)

| Metric | Mean | Pass rate (>= 0.5) | n |
|---|---|---|---|
| contextual_recall | 1.000 | 1.000 | 8 |
| contextual_precision | 0.879 | 1.000 | 8 |

## Generator in isolation (golden evidence as context)

| Metric | Mean | Pass rate (>= 0.5) | n |
|---|---|---|---|
| faithfulness | 0.938 | 1.000 | 8 |
| answer_relevancy | 0.875 | 1.000 | 8 |

## Whole pipeline (real retrieval)

| Metric | Mean | Pass rate (>= 0.5) | n |
|---|---|---|---|
| contextual_relevancy | 0.403 | 0.125 | 8 |
| faithfulness | 0.929 | 1.000 | 7 |
| answer_relevancy | 1.000 | 1.000 | 8 |

## Application

### Latency (ms)

| Stage | p50 | p95 | mean | max |
|---|---|---|---|---|
| retrieval | 155 | 1,336 | 364 | 2,020 |
| generation | 8,596 | 9,882 | 8,719 | 10,065 |
| total | 8,852 | 11,406 | 9,090 | 11,925 |
| generation_isolated | 4,376 | 5,394 | 4,550 | 5,394 |

### Quality

- GEval correctness: mean 0.713, pass rate 0.750
- Behaviour pass rate (cites an expected doc / abstains when it should): 0.688

| Category | Pass rate |
|---|---|
| ambiguous | 0.000 |
| direct_factual | 0.500 |
| exception_eligibility | 1.000 |
| instruction_override | 1.000 |
| insufficient_evidence | 1.000 |
| multi_document | 1.000 |
| nonexistent_entity | 0.000 |
| procedure_policy | 1.000 |

### Safety

- GEval safety: mean 0.856, pass rate 0.875
- Abstention rate on unsupported questions: 0.500
- False abstention rate on supported questions: 0.000
- Prompt injections declined by the guard: 2/2

### Operations

- Pipeline errors: 0 | metric errors: 1 {'faithfulness': 1}
- Judge calls: 166 | retries: 0 | 429s: 0 | timeouts: 0 | 5xx: 0 | failed: 0
- Judge latency p50/p95: 17.800s / 87.800s
- Judge tokens in/out: 116,134 / 52,965
- Wall time: pipeline 163.7s, judge 1334.6s | pipeline throughput 5.860 questions/min

### Cost (USD)

- Generator: 0.0 | judge: 0.0 | per question: 0.0
- Generator runs locally on Ollama. Judge priced with JUDGE_PRICE_INPUT/OUTPUT (USD per 1M tokens); NVIDIA's hosted trial API is free.

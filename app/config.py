"""All settings in one place. Values come from .env (see .env.example)."""
import os
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")


def _env(name: str, default: str) -> str:
    return os.getenv(name, default).strip()


# Postgres / pgvector
PGHOST = _env("PGHOST", "localhost")
PGPORT = int(_env("PGPORT", "5432"))
PGDATABASE = _env("PGDATABASE", "enterprise_rag")
PGUSER = _env("PGUSER", "postgres")
PGPASSWORD = _env("PGPASSWORD", "")
CHUNKS_TABLE = "kb_chunks"

# Ingestion
DATA_DIR = PROJECT_ROOT / "data" / "raw-company_knowledge"
SUPPORTED_EXTENSIONS = {".pdf", ".txt", ".md", ".docx"}
CHUNK_SIZE = int(_env("CHUNK_SIZE", "1000"))
CHUNK_OVERLAP = int(_env("CHUNK_OVERLAP", "200"))

# Embeddings (the dimension must match the model)
EMBEDDING_MODEL = _env("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
EMBEDDING_DIM = int(_env("EMBEDDING_DIM", "384"))

# Retrieval
TOP_K = int(_env("TOP_K", "4"))  # after reranking; 4 reranked chunks beat 6 un-reranked (recall 0.95 vs 0.93)
CANDIDATE_K = int(_env("CANDIDATE_K", "30"))  # candidates per retriever before fusion
RRF_K = 60
# Weight of the keyword ranking in the fusion (dense ranking has weight 1). On the golden set
# dense-only scored best (hit@6 0.99 vs 0.94 at weight 1), so keyword search is off by default.
KEYWORD_WEIGHT = float(_env("KEYWORD_WEIGHT", "0"))
# If the best dense similarity is below this, we answer "not found" without calling the LLM.
MIN_SIMILARITY = float(_env("MIN_SIMILARITY", "0.25"))

# NVIDIA hosted API (OpenAI-compatible). Measured 2026-10-30 on a free trial key: ~20 parallel
# requests trigger HTTP 429, no rate-limit headers are returned, and many catalogue models are
# retired (410), not enabled for trial keys (404) or time out. See README for what was tested.
NVIDIA_API_KEY = _env("NVIDIA_API_KEY", "")
NVIDIA_BASE_URL = _env("NVIDIA_BASE_URL", "https://integrate.api.nvidia.com/v1")
NVIDIA_RERANK_URL = _env("NVIDIA_RERANK_URL", "https://ai.api.nvidia.com/v1/retrieval")

# Reranking: fetch RERANK_CANDIDATES chunks by vector search, rerank them, keep TOP_K.
RERANKER = _env("RERANKER", "nvidia")  # nvidia | local | none
RERANK_MODEL = _env("RERANK_MODEL", "nvidia/nemotron-3.5-rerank-8b")
LOCAL_RERANK_MODEL = _env("LOCAL_RERANK_MODEL", "cross-encoder/ms-marco-MiniLM-L-6-v2")
RERANK_CANDIDATES = int(_env("RERANK_CANDIDATES", "30"))
RERANK_TIMEOUT = int(_env("RERANK_TIMEOUT", "10"))

# Generation: NVIDIA-hosted model, with local Ollama as fallback (or as the only provider).
LLM_PROVIDER = _env("LLM_PROVIDER", "nvidia" if NVIDIA_API_KEY else "ollama")  # nvidia | ollama
GENERATOR_MODEL = _env("GENERATOR_MODEL", "nvidia/nemotron-3.5-lightning-30b-a3b")
GENERATOR_TIMEOUT = int(_env("GENERATOR_TIMEOUT", "30"))
LLM_FALLBACK = _env("LLM_FALLBACK", "true").lower() == "true"
OLLAMA_URL = _env("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = _env("OLLAMA_MODEL", "gemma2:2b")
OLLAMA_TIMEOUT = int(_env("OLLAMA_TIMEOUT", "180"))
HISTORY_TURNS = 4  # previous chat messages sent to the LLM
# Short first questions are checked (in parallel with retrieval) for a missing subject ("What is the
# limit?"); vague ones get a clarifying question instead of a guess. NVIDIA provider only.
CLARIFY_CHECK = _env("CLARIFY_CHECK", "true").lower() == "true"
CLARIFY_MAX_WORDS = int(_env("CLARIFY_MAX_WORDS", "8"))
# An uncited chunk counts as a source when this share of the answer's words appear in it.
MIN_ANSWER_OVERLAP = float(_env("MIN_ANSWER_OVERLAP", "0.6"))

# Evaluation judge (LLM-as-a-judge on the NVIDIA API; used only by app.evaluate).
JUDGE_BASE_URL = _env("JUDGE_BASE_URL", NVIDIA_BASE_URL)
JUDGE_MODEL = _env("JUDGE_MODEL", "openai/gpt-oss-20b")
JUDGE_CONCURRENCY = int(_env("JUDGE_CONCURRENCY", "4"))
JUDGE_TIMEOUT = int(_env("JUDGE_TIMEOUT", "240"))
# USD per 1M tokens, for cost reporting. NVIDIA's hosted trial API is free; set these for a paid endpoint.
JUDGE_PRICE_INPUT = float(_env("JUDGE_PRICE_INPUT", "0"))
JUDGE_PRICE_OUTPUT = float(_env("JUDGE_PRICE_OUTPUT", "0"))
RESULTS_DIR = PROJECT_ROOT / "evaluation_results"

NOT_FOUND_ANSWER ="I couldn't find this in the available documents."

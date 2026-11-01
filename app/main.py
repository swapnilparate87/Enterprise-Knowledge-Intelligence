"""FastAPI service.  Run: uvicorn app.main:app --reload"""
from typing import Literal

import psycopg
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator

from app import config, rag

app = FastAPI(title="Enterprise Knowledge Intelligence")


class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class AskRequest(BaseModel):
    query: str = Field(min_length=1, max_length=2000)
    history: list[ChatMessage] = Field(default_factory=list)
    # Optional access scope: only search these departments (folder names, e.g. ["hr"]).
    departments: list[str] | None = None
    top_k: int = Field(default=config.TOP_K, ge=1, le=20)

    @field_validator("query")
    @classmethod
    def strip_query(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("query cannot be empty or whitespace")
        return value


class SourceItem(BaseModel):
    source_id: str
    doc_id: str
    title: str
    chunk_id: str
    source_path: str
    page_number: int | None = None  # None for txt/md/docx files
    similarity: float
    rerank_score: float | None = None
    content: str


class AskResponse(BaseModel):
    answer: str
    sources: list[SourceItem] = Field(default_factory=list)
    grounded: bool
    latency_ms: dict[str, float] = Field(default_factory=dict)  # search, rerank, retrieval, generation, total


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest):
    try:
        return rag.answer_question(
            request.query,
            history=[m.model_dump() for m in request.history],
            departments=request.departments,
            top_k=request.top_k,
        )
    except rag.LLMError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except psycopg.OperationalError as exc:
        raise HTTPException(status_code=503, detail=f"Database unavailable: {exc}") from exc

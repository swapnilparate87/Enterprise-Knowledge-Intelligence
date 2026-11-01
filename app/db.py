"""Postgres + pgvector: connection, schema, writes and hybrid search."""
from contextlib import contextmanager

import numpy as np
import psycopg
from pgvector.psycopg import register_vector

from app import config

T = config.CHUNKS_TABLE


def _open() -> psycopg.Connection:
    return psycopg.connect(
        host=config.PGHOST,
        port=config.PGPORT,
        dbname=config.PGDATABASE,
        user=config.PGUSER,
        password=config.PGPASSWORD,
        connect_timeout=5,
        # Fail fast instead of hanging forever if a query stalls or the connection silently drops
        # (e.g. after the machine sleeps).
        options="-c statement_timeout=30000",
        keepalives=1, keepalives_idle=30, keepalives_interval=10, keepalives_count=3,
    )


@contextmanager
def connect():
    """Open a connection with pgvector types registered. Commits on success."""
    with _open() as conn:
        register_vector(conn)
        yield conn


def init_schema() -> None:
    """Create the extension, table and indexes if they do not exist yet."""
    # register_vector() needs the extension, so create it on a plain connection first.
    with _open() as conn:
        conn.execute("CREATE EXTENSION IF NOT EXISTS vector")

    with connect() as conn:
        conn.execute(f"""
            CREATE TABLE IF NOT EXISTS {T} (
                chunk_id     TEXT PRIMARY KEY,
                doc_id       TEXT NOT NULL,
                title        TEXT NOT NULL,
                department   TEXT NOT NULL,
                source_path  TEXT NOT NULL,
                file_type    TEXT NOT NULL,
                page_number  INTEGER,
                chunk_index  INTEGER NOT NULL,
                content      TEXT NOT NULL,
                embedding    vector({config.EMBEDDING_DIM}) NOT NULL,
                tsv          tsvector GENERATED ALWAYS AS
                             (to_tsvector('english', title || ' ' || content)) STORED,
                created_at   TIMESTAMPTZ NOT NULL DEFAULT now()
            )
        """)
        conn.execute(f"CREATE INDEX IF NOT EXISTS {T}_embedding_idx ON {T} USING hnsw (embedding vector_cosine_ops)")
        conn.execute(f"CREATE INDEX IF NOT EXISTS {T}_tsv_idx ON {T} USING gin (tsv)")
        conn.execute(f"CREATE INDEX IF NOT EXISTS {T}_doc_idx ON {T} (doc_id)")


def replace_document(doc_id: str, rows: list[dict]) -> int:
    """Delete every chunk of `doc_id` and insert `rows` in one transaction.

    Re-ingesting a changed file therefore never leaves stale chunks behind.
    """
    with connect() as conn, conn.cursor() as cur:
        cur.execute(f"DELETE FROM {T} WHERE doc_id = %s", (doc_id,))
        cur.executemany(
            f"""
            INSERT INTO {T} (chunk_id, doc_id, title, department, source_path,
                             file_type, page_number, chunk_index, content, embedding)
            VALUES (%(chunk_id)s, %(doc_id)s, %(title)s, %(department)s, %(source_path)s,
                    %(file_type)s, %(page_number)s, %(chunk_index)s, %(content)s, %(embedding)s)
            """,
            [{**row, "embedding": np.asarray(row["embedding"], dtype=np.float32)} for row in rows],
        )
    return len(rows)


def count_chunks() -> int:
    with connect() as conn:
        return conn.execute(f"SELECT count(*) FROM {T}").fetchone()[0]


# Hybrid search: dense (cosine) and keyword (full-text) candidates are fused with
# Reciprocal Rank Fusion. Keyword terms are OR-ed so long questions still match.
_SEARCH_SQL = f"""
WITH dense AS (
    SELECT chunk_id, row_number() OVER (ORDER BY embedding <=> %(emb)s) AS rnk
    FROM {T}
    WHERE %(depts)s::text[] IS NULL OR department = ANY(%(depts)s)
    ORDER BY embedding <=> %(emb)s
    LIMIT %(cand)s
),
q AS (
    SELECT replace(plainto_tsquery('english', %(q)s)::text, '&', '|')::tsquery AS query
),
keyword AS (
    SELECT chunk_id, row_number() OVER (ORDER BY ts_rank_cd(tsv, q.query) DESC) AS rnk
    FROM {T}, q
    WHERE %(kw_weight)s > 0
      AND tsv @@ q.query
      AND (%(depts)s::text[] IS NULL OR department = ANY(%(depts)s))
    ORDER BY ts_rank_cd(tsv, q.query) DESC
    LIMIT %(cand)s
)
SELECT c.chunk_id, c.doc_id, c.title, c.department, c.source_path, c.file_type,
       c.page_number, c.chunk_index, c.content,
       1 - (c.embedding <=> %(emb)s) AS similarity,
       d.rnk AS dense_rank,
       k.rnk AS keyword_rank,
       (COALESCE(1.0 / (%(rrf)s + d.rnk), 0)
        + %(kw_weight)s * COALESCE(1.0 / (%(rrf)s + k.rnk), 0))::float8 AS score
FROM dense d
FULL OUTER JOIN keyword k USING (chunk_id)
JOIN {T} c USING (chunk_id)
ORDER BY score DESC
LIMIT %(top_k)s
"""


def search(
    embedding,
    query_text: str,
    top_k: int = config.TOP_K,
    candidate_k: int = config.CANDIDATE_K,
    departments: list[str] | None = None,
) -> list[dict]:
    params = {
        "emb": np.asarray(embedding, dtype=np.float32),
        "q": query_text,
        "depts": departments or None,
        "cand": candidate_k,
        "rrf": config.RRF_K,
        "kw_weight": config.KEYWORD_WEIGHT,
        "top_k": top_k,
    }
    with connect() as conn, conn.cursor() as cur:
        # HNSW is approximate; a wider search (default 40) keeps recall stable across index builds.
        cur.execute("SET LOCAL hnsw.ef_search = 200")
        cur.execute(_SEARCH_SQL, params)
        columns = [c.name for c in cur.description]
        return [dict(zip(columns, row)) for row in cur.fetchall()]


if __name__ == "__main__":
    init_schema()
    print(f"Connected to {config.PGDATABASE}@{config.PGHOST}; {count_chunks()} chunks in {T}.")

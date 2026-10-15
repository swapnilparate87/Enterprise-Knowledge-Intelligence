import psycopg 
from app.ingestion.db import get_connection
from pgvector.psycopg import register_vector

def create_chunks_table():

    # db_credentials = get_connection()   

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
            cur.execute(
                """CREATE TABLE IF NOT EXISTS document_chunks (
                chunk_id TEXT PRIMARY KEY,
                source_path TEXT NOT NULL,
                content TEXT NOT NULL,
                file_type TEXT NOT NULL,
                page_number INTEGER,
                chunk_index INTEGER,
                embedding vector(384) NOT NULL,
                created_at TIMESTAMPTZ DEFAULT NOW());"""
            )

def insert_chunks(chunks, embeddings):
    if len(chunks) != len(embeddings):
        raise ValueError("Number of chunks must match number of embeddings.")

    if not chunks:
        return 0

    with get_connection() as conn:
        register_vector(conn)

        with conn.cursor() as cur:
            cur.executemany(
                """INSERT INTO document_chunks (
                chunk_id,
                source_path,
                content,
                file_type,
                page_number,
                chunk_index,
                embedding
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (chunk_id) DO NOTHING""",
                [
                    (
                        # Sanitize strings to remove null bytes
                        chunk.document_id.replace('\x00', ''),
                        str(chunk.source_path),
                        chunk.content.replace('\x00', ''), 
                        chunk.file_type,
                        chunk.page_number,
                        chunk.chunk_index,
                        embedding,
                    )
                    for chunk, embedding in zip(chunks, embeddings)
                ],
            )

    return len(chunks)
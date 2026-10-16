from app.ingestion.embeddings import get_embeddings_model
from app.ingestion.db import get_connection
from pgvector import Vector
from pgvector.psycopg import register_vector


def retrieve_chunks(query: str, top_k: int = 5) -> list[dict]:

    if not query or not query.strip():
        raise ValueError("Query cannot be empty.")

    if top_k <= 0:
        raise ValueError("top_k must be greater than 0.")

    model = get_embeddings_model()

    min_similarity = 0.50

    # Convert the query embedding into a pgvector-compatible value
    embedding_query = Vector(model.encode(query).tolist())

    sql = """
        SELECT
            chunk_id,
            content,
            source_path,
            file_type,
            page_number,
            chunk_index,
            1 - (embedding <=> %s) AS similarity
        FROM document_chunks
        WHERE 1 - (embedding <=> %s) >= %s
        ORDER BY embedding <=> %s
        LIMIT %s;
    """

    with get_connection() as conn:
        register_vector(conn)

        with conn.cursor() as cur:
            cur.execute(
                sql,
                (embedding_query, embedding_query, min_similarity, embedding_query, top_k),
            )

            rows = cur.fetchall()
            if not rows:
                return []
            columns = [column.name for column in cur.description]

    return [dict(zip(columns, row)) for row in rows]

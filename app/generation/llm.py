import requests

OLLAMA_URL = "http://localhost:11434/api/chat"
DEFAULT_MODEL = "gemma2:2b"


def generate_answer(
    query: str,
    retrieved_chunks: list[dict],
    model_name: str = DEFAULT_MODEL,
    min_similarity: float = 0.50, # Added threshold parameter here
) -> dict:
    if not query or not query.strip():
        raise ValueError("Query cannot be empty.")

    # 1. Filter out chunks that don't meet the similarity threshold 
    # (uses .get() to default to 0 if the key is completely missing)
    valid_chunks = [
        chunk for chunk in retrieved_chunks 
        if chunk.get("similarity", 0) >= min_similarity
    ]

    # 2. Check if the list is empty AFTER filtering
    if not valid_chunks:
        return {
            "answer": "I don't know based on the available documents.",
            "sources": [],
        }

    context_parts = []
    sources = []

    # 3. Loop only through the valid_chunks
    for i, chunk in enumerate(valid_chunks, start=1):
        source_id = f"S{i}"

        context_parts.append(
            f"[{source_id}]\n"
            f"Source: {chunk['source_path']}\n"
            f"Page: {chunk['page_number']}\n"
            f"Content:\n{chunk['content']}"
        )

        sources.append({
            "source_id": source_id,
            "chunk_id": chunk["chunk_id"],
            "source_path": chunk["source_path"],
            "page_number": chunk["page_number"],
            "similarity": chunk.get("similarity", 0), # Safely grab the score
        })

    context = "\n\n".join(context_parts)

    messages = [
        {
            "role": "system",
            "content": (
                "You are a STRICT, closed-domain document question-answering assistant. Your sole purpose is to answer "
                "questions EXCLUSIVELY using the provided document context. You are completely forbidden from using outside knowledge.\n\n"
                "Follow these rules precisely:\n"
                "1. NO OUTSIDE KNOWLEDGE: If the provided documents do not explicitly contain the answer, you must output exactly: "
                "'I don't know based on the available documents.' Do not attempt to explain, define, or guess. "
                "For example, if the user asks 'What is an LLM?' and the text does not discuss LLMs, you must refuse to answer.\n"
                "2. COMPREHENSIVE BUT CONCISE: Provide thorough answers that cover all necessary information regarding the query. "
                "Be clear and direct, but do not make the answer so short that you omit important details found in the context.\n"
                "3. MAXIMIZE RELEVANT SOURCES: Synthesize information from *all* provided documents that help answer the query. "
                "If multiple documents contain useful, non-redundant information, use and cite all of them.\n"
                "4. UNUSED SOURCES: If a retrieved document is not relevant to the query and is not used to form your answer, DO NOT cite it.\n"
                "5. INLINE CITATIONS ONLY: Place citations immediately after the factual claim they support, not at the end of the sentence or answer. "
                "Example: 'The revenue grew by 20% [S1], driven primarily by new software sales [S2].'\n"
                "6. CITE EVERY CLAIM: Cite every substantive factual claim using the exact source IDs provided.\n"
                "7. MULTIPLE SOURCES: If multiple sources support a single claim, cite each relevant source together (e.g., [S1][S3]).\n"
                "8. NO INVENTIONS: Never invent a citation or make a factual claim that the evidence does not explicitly establish.\n"
                "9. NO BIBLIOGRAPHY: Do not append a separate list or bibliography of citation IDs at the end of your answer. "
                "All citations must be strictly inline."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Question:\n{query}\n\n"
                f"Document context:\n{context}"
            ),
        },
    ]

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": model_name,
            "messages": messages,
            "stream": False,
        },
        timeout=180,
    )
    response.raise_for_status()

    answer = response.json()["message"]["content"].strip()

    # Optional: If the LLM returns the exact refusal string, clear the sources 
    # so your UI doesn't display citations for an unanswered question.
    if answer == "I don't know based on the available documents.":
        sources = []

    return {
        "answer": answer,
        "sources": sources,
    }
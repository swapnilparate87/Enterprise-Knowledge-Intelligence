
from app.ingestion.retrieval import retrieve_chunks
from app.generation.llm import generate_answer


def test_generation():
    
    query = "What are the first five steps of the Ivy Case System?"

    chunks = retrieve_chunks(query, top_k=5)
    result = generate_answer(query, chunks)

    print("\nANSWER:\n")
    print(result["answer"])

    print("\nSOURCES:\n")
    for source in result["sources"]:
        print(
            source["source_id"],
            source["chunk_id"],
            source["page_number"],
        )


if __name__ == "__main__":
    test_generation()

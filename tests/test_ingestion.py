# from pathlib import Path

# from app.ingestion.models import SourceDocument
# from app.ingestion.loaders import (
#     discover_files,
#     load_text_file,
#     load_pdf_file,
# )
# from app.ingestion.chunking import chunk_document


# # -----------------------------------------------
# # TEST SWITCHES
# # -----------------------------------------------

# RUN_LOADERS = False
# RUN_CHUNKING = False
# RUN_EMBEDDINGS = False 


# # -----------------------------------------------
# # PROJECT PATHS
# # -----------------------------------------------

# PROJECT_ROOT = Path(__file__).resolve().parents[1]
# RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"


# # -----------------------------------------------
# # 1. LOADERS
# # -----------------------------------------------

# def test_loaders() -> list:
#     files = discover_files(RAW_DATA_DIR)
#     source_documents = []

#     for file_path in files:
#         suffix = file_path.suffix.lower()

#         if suffix in {".txt", ".md"}:
#             documents = [load_text_file(file_path)]

#         elif suffix == ".pdf":
#             documents = load_pdf_file(file_path)

#         else:
#             continue

#         source_documents.extend(documents)

#     print(f"\nFiles discovered: {len(files)}")
#     print(f"Source documents/pages loaded: {len(source_documents)}")

#     for document in source_documents:
#         print(
#             f"{document.file_type} | "
#             f"{document.document_id} | "
#             f"{len(document.content)} characters"
#         )

#     assert source_documents, "No source documents were loaded."
#     assert all(doc.content is not None for doc in source_documents)

#     return source_documents


# # -----------------------------------------------
# # 2. CHUNKING
# # -----------------------------------------------

# def test_chunking(source_documents: list) -> list:
#     all_chunks = []

#     for document in source_documents:
#         chunks = chunk_document(
#             document,
#             chunk_size=1000,
#             chunk_overlap=150,
#         )

#         all_chunks.extend(chunks)

#     print(f"\nSource documents/pages: {len(source_documents)}")
#     print(f"Chunks created: {len(all_chunks)}")

#     assert all_chunks, "No chunks were created."
#     assert all(chunk.content.strip() for chunk in all_chunks)
#     assert all(chunk.chunk_index is not None for chunk in all_chunks)

#     chunk_ids = [chunk.document_id for chunk in all_chunks]
#     assert len(chunk_ids) == len(set(chunk_ids)), "Duplicate chunk IDs found."

#     print("Chunking checks passed.")

#     return all_chunks


# # -----------------------------------------------
# # 3. EMBEDDINGS
# # -----------------------------------------------

# def test_embeddings(chunks: list) -> None:
#     # We will implement this integration after embeddings.py
#     # has a defined function and return format.

#     from app.ingestion.embeddings import embed_documents

#     vectors = embed_documents(chunks)

#     assert len(vectors) == len(chunks), (
#         "The number of embeddings does not match the number of chunks."
#     )

#     assert all(vector is not None for vector in vectors)

#     print(f"\nEmbeddings created: {len(vectors)}")
#     print("Embedding checks passed.")


# # -----------------------------------------------
# # TEST RUNNER
# # -----------------------------------------------

# def main() -> None:
#     source_documents = None
#     chunks = None

#     if RUN_LOADERS or RUN_CHUNKING or RUN_EMBEDDINGS:
#         source_documents = test_loaders()

#     if RUN_CHUNKING or RUN_EMBEDDINGS:
#         chunks = test_chunking(source_documents)

#     if RUN_EMBEDDINGS:
#         test_embeddings(chunks)

#     print("\nSelected ingestion checks completed.")


# if __name__ == "__main__":
#     main()


from app.ingestion.retrieval import retrieve_chunks


def test_retrieval():
    # query = "What are the main steps in preparing for a case interview?"

    # results = retrieve_chunks(query, top_k=5)

    # assert len(results) <= 5
    # assert all(result["content"] for result in results)

    # required_fields = {
    #     "chunk_id",
    #     "source_path",
    #     "file_type",
    #     "page_number",
    #     "chunk_index",
    #     "similarity",
    # }

    # for result in results:
    #     assert required_fields.issubset(result.keys())

    #     print(f"\nChunk ID: {result['chunk_id']}")
    #     print(f"Similarity: {result['similarity']:.4f}")
    #     print(f"Source: {result['source_path']}")
    #     print(f"Page: {result['page_number']}")
    #     print(f"Preview: {result['content'][:200]}...")

    # print(f"\nRetrieved {len(results)} chunks.")
    # print("Retrieval checks passed.")
    query = "What are the four elements of the Four P's framework?"

    results = retrieve_chunks(query, top_k=5)

    for i, chunk in enumerate(results, start=1):
        print(f"\n--- S{i} ---")
        print(f"Source: {chunk['source_path']}")
        print(f"Page: {chunk['page_number']}")
        print(f"Similarity: {chunk['similarity']:.4f}")
        print(f"Content:\n{chunk['content']}")


if __name__ == "__main__":
    test_retrieval()

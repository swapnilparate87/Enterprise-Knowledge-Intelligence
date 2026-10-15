from pathlib import Path
from app.ingestion.loaders import discover_files, load_text_file, load_pdf_file
from app.ingestion.chunking import chunk_document
from app.ingestion.embeddings import embed_documents
from app.ingestion.storage import create_chunks_table, insert_chunks

# Load and chunk your source files.
# Use your existing dispatcher logic here to build source_documents.

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"

def test_loaders() -> list:
    files = discover_files(RAW_DATA_DIR)
    source_documents = []

    for file_path in files:
        suffix = file_path.suffix.lower()

        if suffix in {".txt", ".md"}:
            documents = [load_text_file(file_path)]

        elif suffix == ".pdf":
            documents = load_pdf_file(file_path)

        else:
            continue

        source_documents.extend(documents)

    print(f"\nFiles discovered: {len(files)}")
    print(f"Source documents/pages loaded: {len(source_documents)}")

    for document in source_documents:
        print(
            f"{document.file_type} | "
            f"{document.document_id} | "
            f"{len(document.content)} characters"
        )

    assert source_documents, "No source documents were loaded."
    assert all(doc.content is not None for doc in source_documents)

    return source_documents

source_documents =  test_loaders()


all_chunks = []

for document in source_documents:
    all_chunks.extend(chunk_document(document))

vectors = embed_documents(all_chunks)

create_chunks_table()
processed = insert_chunks(all_chunks, vectors)


print(f"Input chunks: {len(all_chunks)}")
print(f"Input embeddings: {len(vectors)}")
print(f"Chunks processed: {processed}")
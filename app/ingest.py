"""Ingestion: load files -> clean -> chunk -> embed -> store in pgvector.

Run from the project root:
    python -m app.ingest                 # ingest data/raw-company_knowledge
    python -m app.ingest path/to/folder  # ingest another folder
"""
import re
import sys
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter

from app import config

DOC_ID_PATTERN = re.compile(r"^([A-Z]+-\d+)")


@dataclass
class Page:
    """Text of one PDF page, or of a whole txt/md/docx file (page_number=None)."""
    doc_id: str
    title: str
    department: str
    source_path: str
    file_type: str
    page_number: int | None
    text: str


# ---------- loading ----------

def discover_files(folder: Path) -> list[Path]:
    folder = Path(folder)
    if not folder.is_dir():
        raise NotADirectoryError(f"Not a directory: {folder}")
    return sorted(
        p for p in folder.rglob("*")
        if p.is_file() and p.suffix.lower() in config.SUPPORTED_EXTENSIONS
    )


def document_metadata(path: Path) -> dict:
    """'hr/HR-001_leave-and-attendance-policy.pdf' -> doc_id HR-001, title, department hr."""
    stem = path.stem
    match = DOC_ID_PATTERN.match(stem)
    doc_id = match.group(1) if match else stem
    slug = stem[len(doc_id):].lstrip("_- ") or stem
    title = re.sub(r"[-_]+", " ", slug).strip().title()
    return {"doc_id": doc_id, "title": title, "department": path.parent.name}


def clean_text(text: str) -> str:
    text = text.replace("\x00", "")
    text = text.replace("�\n", "- ").replace("�", "")  # PDF bullet glyphs
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n\s*\n\s*\n+", "\n\n", text)
    return text.strip()


def load_file(path: Path) -> list[Page]:
    path = Path(path)
    file_type = path.suffix.lower().lstrip(".")
    meta = document_metadata(path)

    if file_type == "pdf":
        from pypdf import PdfReader
        texts = [(i, page.extract_text() or "") for i, page in enumerate(PdfReader(path).pages, start=1)]
    elif file_type == "docx":
        import docx2txt
        # docx2txt puts a blank line between every paragraph; one newline is enough.
        texts = [(None, re.sub(r"\n\s*\n", "\n", docx2txt.process(str(path))))]
    elif file_type in {"txt", "md"}:
        texts = [(None, path.read_text(encoding="utf-8", errors="replace"))]
    else:
        raise ValueError(f"Unsupported file type: {path.suffix}")

    pages = []
    for page_number, raw in texts:
        text = clean_text(raw)
        if text:
            pages.append(Page(**meta, source_path=str(path), file_type=file_type,
                              page_number=page_number, text=text))
    return pages


# ---------- chunking ----------

def chunk_pages(
    pages: list[Page],
    chunk_size: int = config.CHUNK_SIZE,
    chunk_overlap: int = config.CHUNK_OVERLAP,
) -> list[dict]:
    """Split pages into chunk rows. chunk_index runs across the whole document,
    so chunk_id = '<doc_id>#<index>' is unique and stable between runs."""
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    rows = []
    for page in pages:
        for text in splitter.split_text(page.text):
            index = len(rows)
            rows.append({
                "chunk_id": f"{page.doc_id}#{index}",
                "doc_id": page.doc_id,
                "title": page.title,
                "department": page.department,
                "source_path": page.source_path,
                "file_type": page.file_type,
                "page_number": page.page_number,
                "chunk_index": index,
                "content": text,
            })
    return rows


# ---------- embeddings ----------

@lru_cache(maxsize=1)
def get_model():
    from sentence_transformers import SentenceTransformer  # slow import, so load lazily
    return SentenceTransformer(config.EMBEDDING_MODEL)


def embed(texts: list[str]) -> list[list[float]]:
    if not texts:
        return []
    vectors = get_model().encode(texts, batch_size=32, normalize_embeddings=True, show_progress_bar=False)
    return vectors.tolist()


def embed_chunks(rows: list[dict]) -> list[dict]:
    # The title is prepended so a chunk carries its document's topic.
    vectors = embed([f"{row['title']}\n{row['content']}" for row in rows])
    return [{**row, "embedding": vector} for row, vector in zip(rows, vectors)]


# ---------- pipeline ----------

def ingest(folder: Path = config.DATA_DIR) -> dict:
    from app import db

    db.init_schema()
    files = discover_files(folder)
    print(f"Found {len(files)} files in {folder}")

    stats = {"files": len(files), "chunks": 0, "failed": []}
    for path in files:
        try:
            rows = chunk_pages(load_file(path))
            if not rows:
                print(f"  SKIP  {path.name}: no text extracted")
                continue
            db.replace_document(rows[0]["doc_id"], embed_chunks(rows))
            stats["chunks"] += len(rows)
            print(f"  OK    {path.name}: {len(rows)} chunks")
        except Exception as exc:  # keep going; report every failure at the end
            stats["failed"].append(path.name)
            print(f"  FAIL  {path.name}: {exc}")

    print(f"\nDone: {stats['chunks']} chunks from {len(files) - len(stats['failed'])} files; "
          f"{db.count_chunks()} chunks in the database.")
    if stats["failed"]:
        print(f"Failed files: {', '.join(stats['failed'])}")
    return stats


if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else config.DATA_DIR
    result = ingest(target)
    sys.exit(1 if result["failed"] else 0)

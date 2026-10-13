from dataclasses import dataclass
from pathlib import Path

@dataclass
class SourceDocument:
    document_id: str  | None
    source_path: Path
    content: str    | None
    file_type: tuple[str, ...] = (".pdf", ".txt", ".md")
    page_number: int | None = None
    chunk_index: int | None = None
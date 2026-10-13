from pathlib import Path
from app.ingestion.models import SourceDocument
from langchain_community.document_loaders import PyPDFLoader


def discover_files(folder: Path) -> list[Path]:
    """Finds and returns all files in a directory matching the given extensions."""
   
    base_dir = Path(folder)

    data_file = []
    ext = ['.txt','.pdf','.md']

    if not base_dir.exists():
        raise FileNotFoundError(f"Directory does not exist: {base_dir}")

    elif not base_dir.is_dir():
        raise NotADirectoryError(f"Path is not a directory: {base_dir}")

    for file in base_dir.iterdir():
        if file.is_file() and file.suffix.lower() in ext:
            data_file.append(file)

    return data_file


def load_text_file(file_path: Path) -> SourceDocument:
    """Loads a text or markdown file into a SourceDocument model."""

    if not file_path.is_file():
        raise FileNotFoundError(f"File does not exist or is not a file: {file_path}")

    file_type = file_path.suffix.lower()[1:]

    if file_type not in {"txt", "md"}:
        raise ValueError(f"Unsupported text file type: {file_type}")

    content = file_path.read_text(encoding="utf-8")

    return SourceDocument(
        document_id=file_path.name,
        source_path=file_path,
        content=content,
        file_type=file_type,
    )


def load_pdf_file(file_path: Path) -> list[SourceDocument]:
    """Load a PDF and return one SourceDocument per page."""

    if not file_path.is_file():
        raise FileNotFoundError(f"File does not exist or is not a file: {file_path}")

    if file_path.suffix.lower() != ".pdf":
        raise ValueError(f"Expected a PDF file: {file_path.suffix}")

    loader = PyPDFLoader(str(file_path))
    pages = loader.load()

    documents = []

    for index, doc in enumerate(pages):
        page_number = doc.metadata.get("page", index) + 1
        content = doc.page_content.strip()

        documents.append(
            SourceDocument(
            document_id=f"{file_path.name}_page_{page_number}",
            source_path=file_path,
            content=content,
            file_type="pdf",
            page_number=page_number,
            )
        )

    return documents


target_dir = Path("F:/MY PROJECTS/Enterprise-Knowledge-Intelligence/data/raw")
    
try:
    path_src = discover_files(target_dir)
        
    for path in path_src:
        suffix = path.suffix.lower()
            
        if suffix in {".txt", ".md"}:
            documents = [load_text_file(path)]
        elif suffix == ".pdf":
            documents = load_pdf_file(path)
        else:
            continue

        for document in documents:
            print(f"Type: {type(document)}")
            print(f"ID: {document.document_id}")
            print(f"File Type: {document.file_type}")
            print(f"Content Preview: {document.content[:100]}...")
            print("-" * 50)
            
except Exception as e:
    print(f"Error processing files: {e}")
from app.ingestion.models import SourceDocument
from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_document(
    document: SourceDocument,
    chunk_size: int = 1000,
    chunk_overlap: int = 150,
    ) -> list[SourceDocument]:

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")

    if chunk_overlap < 0 or chunk_overlap >= chunk_size:
        raise ValueError(
            "chunk_overlap must be non-negative and smaller than chunk_size"
        )

 
    text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = chunk_size,      # Max characters per chunk
    chunk_overlap = chunk_overlap,    # Characters shared between consecutive chunks
    )

    chunks = text_splitter.split_text(document.content)

    chunk_list = []
    for i, chunk in enumerate(chunks):

        chunk_list.append(
            SourceDocument(
            document_id=f"{document.document_id}_index_{i+1}",
            source_path=document.source_path,
            content=chunk,
            file_type=document.file_type,
            page_number=document.page_number,
            chunk_index = i+1,
            )
        )

    return chunk_list  

